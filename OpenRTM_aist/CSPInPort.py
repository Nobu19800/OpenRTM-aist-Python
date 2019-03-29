#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file CSPInPort.py
# @brief CSPInPort template class
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2019
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import copy
import threading



##
# @if jp
#
# @class CSPInPort
#
# @brief CSPInPort �ƥ�ץ졼�ȥ��饹
# 
#
# @since 2.0.0
#
# @else
#
# @class CSPInPort
#
# @brief CSPInPort template class
#
#
# @since 2.0.0
#
# @endif
#
class CSPInPort(OpenRTM_aist.InPortBase):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  # �ѥ�᡼���Ȥ���Ϳ������ T �����ѿ��˥Х���ɤ���롣
  #
  # @param name EventInPort ̾��EventInPortBase:name() �ˤ�껲�Ȥ���롣
  # @param value ���� EventInPort �˥Х���ɤ���� T �����ѿ�
  #
  # @else
  #
  # @brief A constructor.
  #
  # constructor.
  # This is bound to type-T variable given as a parameter.
  #
  # @param name A name of the EventInPort. This name is referred by
  #             EventInPortBase::name().
  # @param value type-T variable that is bound to this EventInPort.
  # @param bufsize Buffer length of internal ring buffer of EventInPort
  #                (The default value:64)
  #
  # @endif
  #
  def __init__(self, name, value, manager=None):
    super(CSPInPort, self).__init__(name, "any")
    self._ctrl = OpenRTM_aist.CSPInPort.WorkerThreadCtrl()
    self._name = name
    self._value = value

    self._OnRead = None
    self._OnReadConvert  = None

    self._singlebuffer  = True

    self._channeltimeout = 10
    self._bufferzeromode = False
    self._manager = manager
    if manager:
      manager.addInPort(self)
    self._writingConnector = None


    
    
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯����
  #
  # @else
  #
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    super(CSPInPort, self).__del__()

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
  # @brief ������ؿ�
  #
  # @param self
  # @param prop �������
  # channel_timeout���ǡ����񤭹��ߡ��ɤ߹��߻��Υ����ॢ����
  # buffer.length��0�ξ������󥰥Хåե��⡼�ɤ�����
  # �ǡ����ɤ߹����Ե����֤˰ܹԤ��Ƥ��ʤ��ȥǡ�����񤭹��ळ�Ȥ��Ǥ��ʤ�
  # buffer.length��1�ʾ�ξ��ϥ�󥰥Хåե��⡼�ɤ�����
  # �Хåե��˶�����������ϥǡ����ν񤭹��ߤ��Ǥ���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param prop
  #
  # @endif
  #
  def init(self,prop):
    super(CSPInPort, self).init(prop)

    num = [10]
    if OpenRTM_aist.stringTo(num, self._properties.getProperty("channel_timeout","10")):
      self._channeltimeout = num[0]

    buff_prop = prop.getNode("buffer")
    length = [8]
    OpenRTM_aist.stringTo(length, buff_prop.getProperty("length","8"))

    if length[0] == 0:
      buff_prop.setProperty("length","1")
      self._bufferzeromode = True

    
    self._thebuffer.init(buff_prop)


    if not self._bufferzeromode:
      self._writable_listener = OpenRTM_aist.CSPInPort.IsWritableListener(self._thebuffer, self._ctrl, self._channeltimeout, self, self._manager)
      self._write_listener = OpenRTM_aist.CSPInPort.WriteListener(self._thebuffer,self._ctrl)
    else:
      self._writable_listener = OpenRTM_aist.CSPInPort.IsWritableZeroModeListener(self._thebuffer, self._ctrl, self._channeltimeout, self, self._manager)
      self._write_listener = OpenRTM_aist.CSPInPort.WriteZeroModeListener(self._thebuffer,self._ctrl)

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
      if not self._thebuffer.full():
        del guard_ctrl
        if con.isReadable():
          ret, cdr = con.readBuff()
          if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
            self._thebuffer.write(cdr)
          else:
            self._rtcout.RTC_ERROR("notify read error:%s",(OpenRTM_aist.DataPortStatus.toString(ret)))
          
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
  # @brief 
  #
  # @param self
  # @param connector_profile 
  # @return ret, prof
  #
  # @endif
  #
  def notify_connect(self, connector_profile):
    ret, prof = super(CSPInPort, self).notify_connect(connector_profile)
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
    
    if self._thebuffer.empty():
      for con in self._connectors:
        guard_ctrl = OpenRTM_aist.ScopedLock(self._ctrl._cond)
        if not self._thebuffer.empty():
          value = [None]
          self._thebuffer.read(value)
          del guard_ctrl
          self.notify()
          ret, data = con.deserializeData(value[0])
          if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
            return True, data
          else:
            self._rtcout.RTC_ERROR("deserialize error")
        elif self._ctrl._writing:
          self._ctrl._cond.wait(self._channeltimeout)
          value = [None]
          if not self._thebuffer.empty():
            self._thebuffer.read(value)
            del guard_ctrl
            self.notify()
            ret, data = con.deserializeData(value[0])
            if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
              return True, data
            else:
              self._rtcout.RTC_ERROR("deserialize error")
              return False, None
          else:
            self._rtcout.RTC_ERROR("read timeout")
            return False, None
        else:
          del guard_ctrl
          readable = con.isReadable()
          if readable:
            value = [None]
            ret = con.read(value)
            if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
              return True, value[0]
            else:
              self._rtcout.RTC_ERROR("empty read error:%s",(OpenRTM_aist.DataPortStatus.toString(ret)))
              return False, None
    else:
      value = [None]
      guard_ctrl = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if not self._thebuffer.empty():
        self._thebuffer.read(value)
        del guard_ctrl
        self.notify()
        ret, data = self._connectors[0].deserializeData(value[0])
        if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
          return True, data
        else:
          self._rtcout.RTC_ERROR("deserialize error")
          return False, None
      else:
        self._rtcout.RTC_ERROR("value read error:%s",(OpenRTM_aist.BufferStatus.toString(ret)))
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
  # @return ret, prof
  # ret��True���ɤ߹���������False���ǡ����ɤ߹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ�
  # data���ǡ���(�ɤ߹��߼��Ԥξ���None)
  # 
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param connector_profile 
  # @return ret, prof
  #
  # @endif
  #
  def dataPullZeroMode(self):
    guard_con = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      if con.isReadable():
        guard_ctrl = OpenRTM_aist.ScopedLock(self._ctrl._cond)
        value = [None]
        ret = con.read(value)
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

    if self._writingConnector:
      self._writingConnector = None
      if not self._thebuffer.empty():
        value = [None]
        self._thebuffer.read(value)
        ret, data = self._connectors[0].deserializeData(value[0])
        if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
          return data

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
      if self._ctrl._writing or self._thebuffer.empty():
        self._ctrl._cond.wait(self._channeltimeout)
      if not self._thebuffer.empty():
        self._thebuffer.read(value)

        ret, data = self._connectors[0].deserializeData(value[0])
        if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
          return data
        else:
          self._rtcout.RTC_ERROR("deserialize error")
          return None
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
      if not self._thebuffer.empty():
        self._thebuffer.read(value)
        ret, data = self._connectors[0].deserializeData(value[0])
        if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
          return data
        else:
          self._rtcout.RTC_ERROR("deserialize error")
          return None
      else:
        self._rtcout.RTC_ERROR("read timeout")
        return None

  def setOnRead(self, on_read):
    self._OnRead = on_read

  def setOnReadConvert(self, on_rconvert):
    self._OnReadConvert = on_rconvert
    

  ##
  # @if jp
  #
  # @class IsWritableListener
  #
  # @brief �ǡ����񤭹��߳�ǧ�ꥹ�ʴ��쥯�饹(��󥰥Хåե����ѥ⡼��)
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
    # @param timeout �񤭹����Ե��Υ����ॢ���Ȼ���
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
          guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
          self._ctrl._writing = True
          self._port.setWritingConnector(con)
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
    # @param buff ��󥰥Хåե�
    # @param control WorkerThreadCtrl���֥�������
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
    #
    # @endif
    #
    def __init__(self, buff, control):
      self._ctrl = control
      self._buffer = buff
    ##
    # @if jp
    #
    # @brief �񤭹��߻��Υ�����Хå��ؿ�
    # �ǡ�����Хåե����ɲä����񤭹��߾��֤�������
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
      self._buffer.write(data)
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
    # @param timeout �񤭹����Ե��Υ����ॢ���Ȼ���
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
      self._port = port
      self._manager = manager
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
          guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
          self._ctrl._writing = True
          self._port.setWritingConnector(con)
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
    # @param buff ��󥰥Хåե�
    # @param control WorkerThreadCtrl���֥�������
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
    #
    # @endif
    #
    def __init__(self, buff, control):
      self._ctrl = control
      self._buffer = buff
    ##
    # @if jp
    #
    # @brief �񤭹��߻��Υ�����Хå��ؿ�
    # �񤭹��߾��֤������Хåե��˥ǡ������ɲä��롣
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
      self._buffer.write(data)
      self._ctrl._cond.notify()
      return OpenRTM_aist.BufferStatus.BUFFER_OK
        

  class WorkerThreadCtrl:
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._writing = False
      self._waiting = False

