#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file CSPOutPort.py
# @brief CSPOutPort template class
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
# @class EventInPort
#
# @brief EventInPort �ƥ�ץ졼�ȥ��饹
# 
#
# @since 2.0.0
#
# @else
#
# @class EventInPort
#
# @brief EventInPort template class
#
#
# @since 2.0.0
#
# @endif
#
class CSPOutPort(OpenRTM_aist.OutPortBase):
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
  #
  # @endif
  #
  def __init__(self, name, value, manager=None):
    super(CSPOutPort, self).__init__(name, OpenRTM_aist.toTypename(value))
    self._value = value
    self._ctrl = OpenRTM_aist.CSPOutPort.WorkerThreadCtrl()
    self._name = name
    self._OnWrite = None
    self._OnWriteConvert = None
    self._buffdata = [None]

    self._channeltimeout = 10
    self._writableConnector = None
    self._manager = manager
    if manager:
      manager.addOutPort(self)
    
    
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
    super(CSPOutPort, self).__del__()

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
  def init(self, prop):
    super(CSPOutPort, self).init(prop)
    num = [10]
    if OpenRTM_aist.stringTo(num, self._properties.getProperty("channel_timeout","10")):
      self._channeltimeout = num[0]

    self._readable_listener = OpenRTM_aist.CSPOutPort.IsReadableListener(self._buffdata, self._ctrl, self._channeltimeout, self, self._manager)
    self._read_listener = OpenRTM_aist.CSPOutPort.ReadListener(self._buffdata, self._ctrl, self._channeltimeout)


  ##
  # @if jp
  #
  # @brief ���ͥ�����³�ؿ�
  # OutPortBase����³�����Τۤ��ˡ����ͥ������ɤ߹��߳�ǧ�����ɤ߹��߻��Υ�����Хå��ؿ������ꤹ��
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
    ret, prof = super(CSPOutPort, self).notify_connect(connector_profile)
    guard_con = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
        con.setIsReadableListener(self._readable_listener)
        con.setReadListener(self._read_listener)
    return (ret, prof)

  ##
  # @if jp
  #
  # @brief �ǡ������񤭹��߲�ǽ�����ǧ
  #
  # @param self
  # @return ret, con
  # ret��True(�񤭹��߲�ǽ)��False(�񤭹����Բ�)
  # con���񤭹��߲�ǽ�ʥ��ͥ������񤭹����ԲĤξ���None
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
  def dataWritable(self):
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      if con.isWritable():
        return True, con
    return False, None
  ##
  # @if jp
  #
  # @brief �񤭹��߲�ǽ�ʥ��ͥ��������򤷤�self._writableConnector�˳�Ǽ����
  #
  # @param self
  # @return True���񤭹��߲�ǽ��False���񤭹����Բ�
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
    guard_con = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    if self._ctrl._waiting:
      return True
    if self._ctrl._reading:
      self._ctrl._cond.wait(self._channeltimeout)
    del guard_con
    ret, self._writableConnector = self.dataWritable()
    return ret

  ##
  # @if jp
  #
  # @brief self._writableConnector�˳�Ǽ�������ͥ����˥ǡ�����񤭹���
  # ���Τ��ᡢ������select�ؿ���¹Ԥ���ɬ�פ�����
  #
  # @param self
  # @param value �ǡ���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param value
  #
  # @endif
  #
  def writeData(self, value=None):
    self._rtcout.RTC_TRACE("writeData()")
    if not value:
      value=self._value
    if self._OnWrite:
      self._OnWrite(value)

    if self._OnWriteConvert:
      value = self._OnWriteConvert(value)

    guard_con = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    if self._ctrl._waiting:
      ret, cdr_data = self._connectors[0].serializeData(value)
      if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
        self.setData(cdr_data)
        self._ctrl._waiting = False
        self._ctrl._cond.notify()
        return True

    if self._writableConnector:
      del guard_con
      self._writableConnector.write(value)

  ##
  # @if jp
  #
  # @brief �Ե����ֻ��˰ܹԤ������˥ǡ�������Ū���ѿ��˳�Ǽ����
  #
  # @param self
  # @param data �ǡ���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param data
  #
  # @endif
  #
  def setData(self, data):
    self._buffdata[0] = data

  ##
  # @if jp
  #
  # @brief �ǡ�����񤭹���
  # �񤭹��߲�ǽ�ʥ��ͥ�����¸�ߤ�����ϡ��ǡ�����񤭹���ǽ�����λ����
  # �񤭹��߲�ǽ�ʥ��ͥ�����¸�ߤ��ʤ����ϡ�InPort¦����ǡ������ɤ߹���ޤ��Ե�����
  #
  # @param self
  # @param value �ǡ���
  # @return True�����ﴰλ��False�����顼
  # �ǡ����Υޡ������󥰡��񤭹��ߤΥ����ॢ���Ȥǥ��顼��ȯ������
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param value
  # @return
  #
  # @endif
  #
  def write(self, value=None):
    if not value:
      value=self._value
    if self._OnWrite:
      self._OnWrite(value)

    if not self._connectors:
      return False

    if self._OnWriteConvert:
      value = self._OnWriteConvert(value)

    guard_con = OpenRTM_aist.ScopedLock(self._ctrl._cond)
    if not self._ctrl._waiting:
      del guard_con
      ret, con = self.dataWritable()
      if ret:
        retcon = con.write(value)
        if retcon == OpenRTM_aist.DataPortStatus.PORT_OK:
          return True
        else:
          self._rtcout.RTC_ERROR("write error %d", (retcon))
          return False

    ret, cdr_data = self._connectors[0].serializeData(value)
    if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
      self.setData(cdr_data)
      if self._ctrl._waiting:
        self._ctrl._waiting = False
        self._ctrl._cond.notify()
        return True
      self._ctrl._readable = True
      self._ctrl._cond.wait(self._channeltimeout)
      if self._ctrl._readable:
        self._rtcout.RTC_ERROR("write timeout")
        self._ctrl._readable = False
        return False
      return True
    else:
      self._rtcout.RTC_ERROR("serialize error")
      return False
    

  def setOnWrite(self, on_write):
    self._OnWrite = on_write

  def setOnWriteConvert(self, on_wconvert):
    self._OnWriteConvert = on_wconvert

  ##
  # @if jp
  #
  # @class IsReadableListener
  #
  # @brief �ǡ����ɤ߹��߳�ǧ�ꥹ�ʴ��쥯�饹
  # 
  #
  # @since 2.0.0
  #
  # @else
  #
  # @class IsReadableListener
  #
  # @brief 
  #
  #
  # @since 2.0.0
  #
  # @endif
  #
  class IsReadableListener(OpenRTM_aist.IsReadableListenerBase):
    ##
    # @if jp
    #
    # @brief ���󥹥ȥ饯��
    # 
    #
    # @param self
    # @param control WorkerThreadCtrl���֥�������
    # @param timeout �ɤ߹����Ե��Υ����ॢ���Ȼ���
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
    # @param control 
    # @param timeout 
    # @param manager 
    #
    # @endif
    #
    def __init__(self, data, control, timeout, port, manager=None):
      self._ctrl = control
      self._data = data
      self._channeltimeout = timeout
      self._port = port
      self._manager = manager
    ##
    # @if jp
    #
    # @brief �ɤ߹��߳�ǧ���Υ�����Хå��ؿ�
    # ¾�Υ��ͥ������ǡ����ɤ߹�����ξ��ϴ�λ�ޤ��Ե�����
    # �ǡ����񤭹��ߤ��Ե����Ƥ���ξ����ɤ߹��߾��֤˰ܹԤ���
    # ���Τ��ᡢ�ɤ߹��߲�ǽ�ʾ���ɬ���ǡ������ɤ߹���ɬ�פ�����
    # 
    #
    # @param self
    # @param con OutPortConnector
    # @return True���ɤ߹��߲�ǽ��False���ɤ߹����Բ�
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
        if self._manager.notify(outport=self._port):
          guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
          self._ctrl._reading = True
          return True
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if self._ctrl._reading:
        self._ctrl._cond.wait(self._channeltimeout)
      if not self._ctrl._readable:
        self._ctrl._reading = False
        return False
      else:
        self._ctrl._reading = True
        return True

  ##
  # @if jp
  #
  # @class ReadListener
  #
  # @brief �ǡ����ɤ߹��߻��Υꥹ�ʴ��쥯�饹
  # 
  #
  # @since 2.0.0
  #
  # @else
  #
  # @class ReadListener
  #
  # @brief 
  #
  #
  # @since 2.0.0
  #
  # @endif
  #
  class ReadListener(OpenRTM_aist.ReadListenerBase):
    ##
    # @if jp
    #
    # @brief ���󥹥ȥ饯��
    # 
    #
    # @param self
    # @param data �ǡ������Ǽ�����ѿ�
    # @param control WorkerThreadCtrl���֥�������
    # 
    #
    #
    # @else
    #
    # @brief 
    #
    # @param self
    # @param data 
    # @param control 
    #
    # @endif
    #
    def __init__(self, data, control, timeout):
      self._ctrl = control
      self._data = data
      self._channeltimeout = timeout
    ##
    # @if jp
    #
    # @brief �ɤ߹��߻��Υ�����Хå��ؿ�
    # �ǡ������ѿ�������Ф����ɤ߹��߾��֤�������
    # 
    #
    # @param self
    # @return ret, data
    # ret���꥿���󥳡���
    # BUFFER_OK�����ﴰλ
    # BUFFER_ERROR���ǡ�������Ǽ����Ƥ��ʤ�
    # data���ǡ���
    # 
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
    def __call__(self):
      guard = OpenRTM_aist.ScopedLock(self._ctrl._cond)
      if self._data[0] is None:
        self._ctrl._waiting = True
        self._ctrl._cond.wait(self._channeltimeout)

      self._ctrl._reading = False
      data = self._data[0]
      self._data[0] = None
      self._ctrl._readable = False
      self._ctrl._cond.notify()
      if data is None:
        return OpenRTM_aist.BufferStatus.BUFFER_ERROR, data
      else:
        return OpenRTM_aist.BufferStatus.BUFFER_OK, data
    
  class WorkerThreadCtrl:
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._reading = False
      self._readable = False
      self._waiting = False

    
    
  




