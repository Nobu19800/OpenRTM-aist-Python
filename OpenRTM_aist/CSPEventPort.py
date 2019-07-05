#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file CSPEventPort.py
# @brief CSPEventPort template class
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2019
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import OpenRTM_aist.EventPort
import copy
import threading



##
# @if jp
#
# @class CSPEventPort
#
# @brief CSPEventPort �ƥ�ץ졼�ȥ��饹
# 
#
# @since 2.0.0
#
# @else
#
# @class CSPEventPort
#
# @brief CSPEventPort template class
#
#
# @since 2.0.0
#
# @endif
#
class CSPEventPort(OpenRTM_aist.InPortBase):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  # �ѥ�᡼���Ȥ���Ϳ������ T �����ѿ��˥Х���ɤ���롣
  #
  # @param self
  # @param name EventInPort ̾��EventInPortBase:name() �ˤ�껲�Ȥ���롣
  # @param fsm FSM
  #
  # @else
  #
  # @brief A constructor.
  #
  # constructor.
  # This is bound to type-T variable given as a parameter.
  #
  # @param self
  # @param name A name of the EventInPort. This name is referred by
  #             EventInPortBase::name().
  # @param value type-T variable that is bound to this EventInPort.
  # @param fsm 
  #
  # @endif
  #
  def __init__(self, name, fsm=None, manager=None):
    super(CSPEventPort, self).__init__(name, "any")
    self._ctrl = CSPEventPort.WorkerThreadCtrl()
    self._name = name
    self._value = None

    self._OnRead = None

    self._singlebuffer  = True
    self._eventbuffer = None

    self._channeltimeout = 10
    self._bufferzeromode = False
    self._fsm = fsm
    
    self._manager = manager
    if manager:
      self._manager.addInPort(self)
    self._writingConnector = None


    
    
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯����
  #
  # @param self
  #
  # @else
  #
  # @brief Destructor
  #
  # Destructor
  #
  # @param self
  #
  # @endif
  #
  def __del__(self):
    super(CSPEventPort, self).__del__()
    if self._eventbuffer is not None:
      OpenRTM_aist.CdrBufferFactory.instance().deleteObject(self._eventbuffer)


  ##
  # @if jp
  #
  # @brief �ݡ���̾�Τ�������롣
  #
  # �ݡ���̾�Τ�������롣
  #
  # @param self
  # @return �ݡ���̾��
  #
  # @else
  #
  # @brief Get port name
  #
  # Get port name.
  #
  # @param self
  # @return The port name
  #
  # @endif
  #
  def name(self):
    return self._name



  ##
  # @if jp
  #
  # @brief �����ʤ��Υ��٥�ȥϥ�ɥ����Ͽ����
  #
  # @param self
  # @param name ���٥��̾
  # @param handler ���٥�ȥϥ�ɥ�
  # ���ͥ�����³����fsm_event_name�Ȥ������Ǥ����ꤹ�롣
  # fsm_event_name�ȥ��٥��̾�����פ���ȥ��٥�Ȥ��¹Ԥ���롣
  # ���٥�ȥϥ�ɥ�ˤ�Macho��������������٥�Ȥ����Ϥ���
  # 
  #
  # @else
  #
  # @param self
  # @param name 
  # @param handler 
  #
  # @endif
  #
  def bindEvent0(self, name, handler):
    self.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                  OpenRTM_aist.EventPort.EventBinder0(self._fsm, name, handler, self._eventbuffer))
    
  ##
  # @if jp
  #
  # @brief ��������Υ��٥�ȥϥ�ɥ����Ͽ����
  #
  # @param self
  # @param name ���٥��̾
  # @param handler ���٥�ȥϥ�ɥ�
  # @param data_type ���ϥǡ���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param name 
  # @param handler 
  # @param data_type 
  #
  # @endif
  #
  def bindEvent1(self, name, handler, data_type):
    self.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                  OpenRTM_aist.EventPort.EventBinder1(self._fsm, name, handler, data_type, self._eventbuffer))

  ##
  # @if jp
  #
  # @brief ������ؿ�
  #
  # @param self
  # @param prop ���ͥ����Υץ�ѥƥ�
  # buffer(dataport.buffer)���ǤǥХåե�Ĺ����������
  # channel_timeout(dataport.channel_timeout)���Ǥǡ�
  # ������ǽ�ʥ����ȥݡ��Ȥ�¸�ߤ��ʤ����Υ֥�å��Υ����ॢ���Ȥ�����
  # 
  # @return �ݡ���̾��
  #
  # @else
  #
  # @brief Get port name
  #
  # @param self
  # @param prop 
  #
  # @endif
  #
  def init(self,prop):
    super(CSPEventPort, self).init(prop)

    num = [10]
    if OpenRTM_aist.stringTo(num, self._properties.getProperty("channel_timeout","10")):
      self._channeltimeout = num[0]

    buff_prop = prop.getNode("buffer")
    length = [8]
    OpenRTM_aist.stringTo(length, buff_prop.getProperty("length","8"))

    if length[0] == 0:
      buff_prop.setProperty("length","1")
      self._bufferzeromode = True

    self._eventbuffer = OpenRTM_aist.CdrBufferFactory.instance().createObject("ring_buffer")
    if self._eventbuffer is None:
        self._rtcout.RTC_ERROR("default buffer creation failed")
    self._eventbuffer.init(buff_prop)


    if not self._bufferzeromode:
      self._writable_listener = CSPEventPort.IsWritableListener(self._eventbuffer, self._ctrl, self._channeltimeout, self, self._manager)
      self._write_listener = CSPEventPort.WriteListener(self._ctrl)
    else:
      self._writable_listener = CSPEventPort.IsWritableZeroModeListener(self._ctrl, self._channeltimeout, self, self._manager)
      self._write_listener = CSPEventPort.WriteZeroModeListener(self._ctrl)

  def setManager(self, manager):
    self._writable_listener.setManager(manager)
    self._manager = manager
    if manager:
      self._manager.addInPort(self)

  ##  
  # @if jp
  #
  # @brief �񤭹��߽����򳫻Ϥ������ͥ�������Ͽ
  #
  # @param self
  # @param con InPortConnector
  # 
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param con
  #
  # @endif
  #
  def setWritingConnector(self, con):
    self._writingConnector = con

  ##
  # @if jp
  #
  # @brief ��³���OutPort�����ϲ�ǽ�Ǥ��뤳�Ȥ�����
  # �Хåե����ե�ˤʤ롢�⤷�����Ե����OutPort���ʤ��ʤ�ޤǡ���³��Υ��ͥ����Υǡ������ɤ߹���
  # �Хåե�����ǡ������ɤ߹�������ϡ����δؿ���ƤӽФ�ɬ�פ�����
  #
  # @param self
  # 
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  def notify(self):
    for con in self._connectors:
      guard_ctrl = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if self._ctrl._writing:
        self._ctrl._cond.wait(self._channeltimeout)
      if not self._eventbuffer.full():
        if con.isReadable():
          ret, _ = con.readBuff()
          if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
            pass
          else:
            self._rtcout.RTC_ERROR("read error:%s",(OpenRTM_aist.DataPortStatus.toString(ret)))
          
  ##
  # @if jp
  #
  # @brief ���ͥ�����³�ؿ�
  # InPortBase����³�����Τۤ��ˡ����ͥ����˽񤭹��߳�ǧ�����񤭹��߻��Υ�����Хå��ؿ������ꤹ��
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  # @return ret, prof
  # ret���꥿���󥳡���
  # prof�����ͥ����ץ�ե�����
  # 
  # @return �ݡ���̾��
  #
  # @else
  #
  # @brief Get port name
  #
  # @param self
  # @param connector_profile 
  # @return ret, prof
  #
  # @endif
  #
  def notify_connect(self, connector_profile):
    ret, prof = super(CSPEventPort, self).notify_connect(connector_profile)
    guard_con = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      con.setIsWritableListener(self._writable_listener)
      con.setWriteListener(self._write_listener)
    return (ret, prof)

  ##
  # @if jp
  #
  # @brief ��󥰥Хåե����ѥ⡼�ɻ��Υǡ����ɤ߹��߽���
  # �Хåե���empty�ǤϤʤ����ϥХåե������ɤ߹���
  # ���ͥ���������ɤ߹��߲�ǽ�ʤ�Τ�������ϡ����Υ��ͥ��������ɤ߹���
  # ���������񤭹�����ξ��Ͻ񤭹��߽�λ�ޤǥ֥�å�����
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  # @return ret, prof
  # ret��True���ɤ߹���������False���Хåե���empty�Ǥ����ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ�
  # data���ǡ���
  # 
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return ret, data
  #
  # @endif
  #
  def dataPullBufferMode(self):
    guard_con = OpenRTM_aist.ScopedLock(self._connector_mutex)
    if not self._connectors:
      self._rtcout.RTC_DEBUG("no connectors")
      return False, None

    if self._eventbuffer.empty():
      for con in self._connectors:
        guard_ctrl = OpenRTM_aist.ScopedLock(self._ctrl._cond)
        if not self._eventbuffer.empty():
          value = [None]
          self._eventbuffer.read(value)
          del guard_ctrl
          self.notify()
          return True, value[0]
        elif self._ctrl._writing:
          self._ctrl._cond.wait(self._channeltimeout)
          value = [None]
          if not self._eventbuffer.empty():
            self._eventbuffer.read(value)
            del guard_ctrl
            self.notify()
            return True, value[0]
          else:
            self._rtcout.RTC_ERROR("read timeout")
            return False, None
        else:
          readable = con.isReadable()
          if readable:
            ret, _ = con.readBuff()
            value = [None]
            self._eventbuffer.read(value)
            if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
              return True, value[0]
            else:
              self._rtcout.RTC_ERROR("read error:%s",(OpenRTM_aist.DataPortStatus.toString(ret)))
              return False, None
    else:
      value = [None]
      guard_ctrl = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if not self._eventbuffer.empty():
        self._eventbuffer.read(value)
        del guard_ctrl
        self.notify()
        return True, value[0]
      else:
        self._rtcout.RTC_ERROR("read error:%s",(OpenRTM_aist.BufferStatus.toString(ret)))
        del guard_ctrl
        self.notify()
        return False, None
    return False, None

  ##
  # @if jp
  #
  # @brief ���󥰥Хåե����ѥ⡼�ɻ��Υǡ����ɤ߹��߽���
  # �ǡ����ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ�����ϡ����Υ��ͥ�������ǡ������ɤ߹���
  # 
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  # @return ret, data
  # ret��True���ɤ߹���������False���ǡ����ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ�
  # data���ǡ���(�ɤ߹��߼��Ԥξ���None)
  # 
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return ret, data
  #
  # @endif
  #
  def dataPullZeroMode(self):
    guard_con = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      if con.isReadable():
        guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
        ret, _ = con.readBuff()
        value = [None]
        self._eventbuffer.read(value)
        if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
          return True, value[0]
        else:
          self._rtcout.RTC_ERROR("read error:%s",(OpenRTM_aist.DataPortStatus.toString(ret)))
          return False, None
    return False, None

  ##
  # @if jp
  #
  # @brief �ǡ����ɤ߹��߲�ǽ�ʥ��ͥ��������򤷡�
  # self._value���ɤ߹�����ǡ������Ǽ����
  # 
  #
  # @param self
  # @return True���ɤ߹���������False���ɤ߹����Բ�
  #
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def select(self):
    self._rtcout.RTC_TRACE("select()")
    if not self._bufferzeromode:
      ret, value = self.dataPullBufferMode()
    else:
      ret, value = self.dataPullZeroMode()
    guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    if ret:
      self._value = value
    return ret
    
  ##
  # @if jp
  #
  # @brief select�ؿ��ǳ�Ǽ�����ǡ����μ���
  # 
  #
  # @param self
  # @return �ǡ���
  #
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def readData(self):
    guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    self._rtcout.RTC_TRACE("readData()")
    if self._OnRead is not None:
      self._OnRead()
      self._rtcout.RTC_TRACE("OnRead called")

    if self._ctrl._writing:
      self._ctrl._cond.wait(self._channeltimeout)
      
    if not self._eventbuffer.empty():
      value = [None]
      self._eventbuffer.read(value)
      return value[0]

    return self._value

  ##
  # @if jp
  #
  # @brief �ǡ������ɤ߹��߲�ǽ�ʥ��ͥ��������򤷥ǡ������������
  # �ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ������Ե�����
  # 
  #
  # @param self
  # @return �ǡ���(�����ॢ���Ȥ�������None)
  #
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def read(self):
    self._rtcout.RTC_TRACE("DataType read()")
    if self._OnRead is not None:
      self._OnRead()
      self._rtcout.RTC_TRACE("OnRead called")

    if not self._connectors:
      self._rtcout.RTC_DEBUG("no connectors")
      return None

    if not self._bufferzeromode:
      return self.readBufferMode()
    else:
      return self.readZeroMode()


  ##
  # @if jp
  #
  # @brief ��󥰥Хåե����ѥ⡼�ɻ��Υǡ����ɤ߹��߽���
  # �ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ������Ե�����
  # 
  #
  # @param self
  # @return �ǡ���(�����ॢ���Ȥ�������None)
  #
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def readBufferMode(self):
    ret, data = self.dataPullBufferMode()
    if ret:
      return data
    else:
      value = [None]
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if self._ctrl._writing or self._eventbuffer.empty():
        self._ctrl._cond.wait(self._channeltimeout)
      if not self._eventbuffer.empty():
        self._eventbuffer.read(value)

        return value[0]
      else:
        self._rtcout.RTC_ERROR("read timeout")
        return None

  ##
  # @if jp
  #
  # @brief ���󥰥Хåե����ѥ⡼�ɻ��Υǡ����ɤ߹��߽���
  # �ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ������Ե�����
  # 
  #
  # @param self
  # @return �ǡ���(�����ॢ���Ȥ�������None)
  #
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return 
  #
  # @endif
  #
  def readZeroMode(self):
    ret, data = self.dataPullZeroMode()
    if ret:
      return data
    else:
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      self._ctrl._waiting = True
      self._ctrl._cond.wait(self._channeltimeout)
      self._ctrl._waiting = False
      value = [None]
      if not self._eventbuffer.empty():
        self._eventbuffer.read(value)
        return value[0]
      else:
        self._rtcout.RTC_ERROR("read timeout")
        return None

  def setOnRead(self, on_read):
    self._OnRead = on_read
    

  ##
  # @if jp
  #
  # @class IsWritableListener
  #
  # @brief �ǡ����񤭹��߻��γ�ǧ�ꥹ�ʴ��쥯�饹(��󥰥Хåե����ѥ⡼��)
  # 
  #
  # @since 2.0.0
  #
  # @else
  #
  # @class IsWritableListener
  #
  # @brief 
  #
  #
  # @since 2.0.0
  #
  # @endif
  #
  class IsWritableListener(OpenRTM_aist.IsWritableListenerBase):
    ##
    # @if jp
    #
    # @brief ���󥹥ȥ饯��
    # 
    #
    # @param self
    # @param buff ��󥰥Хåե�
    # @param control WorkerThreadCtrl���֥�������
    # @param timeout �񤭹����Ե��Υ����ॢ����
    # @param manager CSP����ͥ�����ޥ͡�����
    # manager����ꤷ�����ϡ�manager���Ե���ξ��˥�å���������Τ�Ԥ�
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param buff 
    # @param control 
    # @param timeout 
    # @param manager 
    #
    # @endif
    #
    def __init__(self, buff, control, timeout, port, manager=None):
      self._ctrl = control
      self._buffer = buff
      self._channeltimeout = timeout
      self._manager = manager
      self._port = port
    ##
    # @if jp
    #
    # @brief �񤭹��߳�ǧ���Υ�����Хå��ؿ�
    # ¾�Υ��ͥ������ǡ����񤭹�����ξ��ϴ�λ�ޤ��Ե�����
    # �Хåե����ե�ǤϤʤ����Ͻ񤭹��߾��֤˰ܹԤ���
    # ���Τ��ᡢ�񤭹��߲�ǽ�ʾ���ɬ���ǡ�����񤭹���ɬ�פ�����
    # 
    #
    # @param self
    # @param con InPortConnector
    # @return True���񤭹��߲�ǽ��False���񤭹����Բ�
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param con 
    # @return
    #
    # @endif
    #
    def __call__(self, con):
      if self._manager:
        if self._manager.notify(inport=self._port):
          return True
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if self._ctrl._writing:
        self._ctrl._cond.wait(self._channeltimeout)
      if not self._buffer.full():
        self._ctrl._writing = True
        return True
      else:
        self._ctrl._writing = False
        return False

    def setManager(self, manager):
      self._manager = manager

  ##
  # @if jp
  #
  # @class WriteListener
  #
  # @brief �ǡ����񤭹��߻��Υꥹ�ʴ��쥯�饹(��󥰥Хåե����ѥ⡼��)
  # 
  #
  # @since 2.0.0
  #
  # @else
  #
  # @class WriteListener
  #
  # @brief 
  #
  #
  # @since 2.0.0
  #
  # @endif
  #
  class WriteListener(OpenRTM_aist.WriteListenerBase):
    ##
    # @if jp
    #
    # @brief ���󥹥ȥ饯��
    # 
    #
    # @param self
    # @param control WorkerThreadCtrl���֥�������
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param control 
    #
    # @endif
    #
    def __init__(self, control):
      self._ctrl = control
    ##
    # @if jp
    #
    # @brief �񤭹��߻��Υ�����Хå��ؿ�
    # CSPEventPort�ǤϥХåե��ؤν񤭹��ߤ�ON_RECEIVED������Хå��Ǽ¹Ԥ��뤿�ᡢ
    # �񤭹��߾��֤β���Τߤ�Ԥ���
    # 
    #
    # @param self
    # @param data �ǡ���
    # @return �꥿���󥳡���
    # BUFFER_OK�����ﴰλ
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param data 
    # @return
    #
    # @endif
    #
    def __call__(self, data):
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      self._ctrl._writing = False
      self._ctrl._cond.notify()
      return OpenRTM_aist.BufferStatus.BUFFER_OK

  ##
  # @if jp
  #
  # @class IsWritableZeroModeListener
  #
  # @brief �ǡ����񤭹��߳�ǧ�ꥹ�ʴ��쥯�饹(���󥰥Хåե����ѥ⡼��)
  # 
  #
  # @since 2.0.0
  #
  # @else
  #
  # @class IsWritableZeroModeListener
  #
  # @brief 
  #
  #
  # @since 2.0.0
  #
  # @endif
  #
  class IsWritableZeroModeListener(OpenRTM_aist.IsWritableListenerBase):
    ##
    # @if jp
    #
    # @brief ���󥹥ȥ饯��
    # 
    #
    # @param self
    # @param buff ��󥰥Хåե�
    # @param control WorkerThreadCtrl���֥�������
    # @param timeout �񤭹����Ե��Υ����ॢ����
    # @param manager CSP����ͥ�����ޥ͡�����
    # manager����ꤷ�����ϡ�manager���Ե���ξ��˥�å���������Τ�Ԥ�
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param buff 
    # @param control 
    # @param timeout 
    # @param manager 
    #
    # @endif
    #
    def __init__(self, control, timeout, port, manager=None):
      self._ctrl = control
      self._channeltimeout = timeout
      self._manager = manager
      self._port = port
    ##
    # @if jp
    #
    # @brief �񤭹��߳�ǧ���Υ�����Хå��ؿ�
    # ¾�Υ��ͥ������ǡ����񤭹�����ξ��ϴ�λ�ޤ��Ե�����
    # �Хåե����ե�ǤϤʤ����Ͻ񤭹��߾��֤˰ܹԤ���
    # ���Τ��ᡢ�񤭹��߲�ǽ�ʾ���ɬ���ǡ�����񤭹���ɬ�פ�����
    # 
    #
    # @param self
    # @param con InPortConnector
    # @return True���񤭹��߲�ǽ��False���񤭹����Բ�
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param con 
    # @return
    #
    # @endif
    #
    def __call__(self, con):
      if self._manager:
        if self._manager.notify(inport=self._port):
          return True
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if self._ctrl._waiting and self._ctrl._writing:
        self._ctrl._cond.wait(self._channeltimeout)
      if self._ctrl._waiting:
        self._ctrl._writing = True
        return True
      else:
        self._ctrl._writing = False
        return False

    def setManager(self, manager):
      self._manager = manager
        
  ##
  # @if jp
  #
  # @class WriteZeroModeListener
  #
  # @brief �ǡ����񤭹��߻��Υꥹ�ʴ��쥯�饹(���󥰥Хåե����ѥ⡼��)
  # 
  #
  # @since 2.0.0
  #
  # @else
  #
  # @class WriteZeroModeListener
  #
  # @brief 
  #
  #
  # @since 2.0.0
  #
  # @endif
  #
  class WriteZeroModeListener(OpenRTM_aist.WriteListenerBase):
    ##
    # @if jp
    #
    # @brief ���󥹥ȥ饯��
    # 
    #
    # @param self
    # @param control WorkerThreadCtrl���֥�������
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param control 
    #
    # @endif
    #
    def __init__(self, control):
      self._ctrl = control
    ##
    # @if jp
    #
    # @brief �񤭹��߻��Υ�����Хå��ؿ�
    # CSPEventPort�ǤϥХåե��ؤν񤭹��ߤ�ON_RECEIVED������Хå��Ǽ¹Ԥ��뤿�ᡢ
    # �񤭹��߾��֤β���Τߤ�Ԥ���
    # 
    #
    # @param self
    # @param data �ǡ���
    # @return �꥿���󥳡���
    # BUFFER_OK�����ﴰλ
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param data
    # @return
    #
    # @endif
    #
    def __call__(self, data):
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      self._ctrl._writing = False
      self._ctrl._cond.notify()
      return OpenRTM_aist.BufferStatus.BUFFER_OK
        

  class WorkerThreadCtrl:
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._writing = False
      self._waiting = False

