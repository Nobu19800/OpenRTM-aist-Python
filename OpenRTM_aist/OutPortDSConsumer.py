#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  OutPortDSConsumer.py
# @brief OutPortDSConsumer class
# @date  $Date: 2017-06-09 07:49:59 $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Nobuhiko Miyamoto
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



from omniORB import any
import OpenRTM_aist
import RTC

##
# @if jp
# @class OutPortDSConsumer
#
# @brief OutPortDSConsumer ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥ��󥷥塼�ޤμ������饹��
#
# @param DataType �ܥݡ��Ȥˤư����ǡ�����
#
# @since 1.2.0
#
# @else
# @class OutPortDSConsumer
#
# @brief OutPortDSConsumer class
#
# This is an implementation class of the output Consumer 
# that uses CORBA for means of communication.
#
# @param DataType Data type for this port
#
# @since 1.2.0
#
# @endif
#
class OutPortDSConsumer(OpenRTM_aist.OutPortConsumer,OpenRTM_aist.CorbaConsumer):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param buffer �ܥݡ��Ȥ˳�����Ƥ�Хåե�
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @param buffer Buffer that is attached to this port
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.CorbaConsumer.__init__(self, RTC.DataPullService)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortDSConsumer")
    self._buffer = None
    self._profile = None
    self._listeners = None
    return

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
    self._rtcout.RTC_PARANOID("~OutPortDSConsumer()")
    CorbaConsumer.__del__(self)
    pass


  ##
  # @if jp
  # @brief ��������
  #
  # OutPortConsumer�γƼ������Ԥ����������饹�Ǥϡ�Ϳ����줿
  # Properties����ɬ�פʾ����������ƳƼ������Ԥ������� init() ��
  # ���ϡ�OutPortProvider����ľ�太��ӡ���³���ˤ��줾��ƤФ���
  # ǽ�������롣�������äơ����δؿ���ʣ����ƤФ�뤳�Ȥ����ꤷ�Ƶ�
  # �Ҥ����٤��Ǥ��롣
  # 
  # @param prop �������
  #
  # @else
  #
  # @brief Initializing configuration
  #
  # This operation would be called to configure in initialization.
  # In the concrete class, configuration should be performed
  # getting appropriate information from the given Properties data.
  # This function might be called right after instantiation and
  # connection sequence respectivly.  Therefore, this function
  # should be implemented assuming multiple call.
  #
  # @param prop Configuration information
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    return


  ##
  # @if jp
  # @brief �Хåե��򥻥åȤ���
  #
  # OutPortConsumer���ǡ�������Ф��Хåե��򥻥åȤ��롣
  # ���Ǥ˥��åȤ��줿�Хåե��������硢�����ΥХåե��ؤ�
  # �ݥ��󥿤��Ф��ƾ�񤭤���롣
  # OutPortProvider�ϥХåե��ν�ͭ�����ꤷ�Ƥ��ʤ��Τǡ�
  # �Хåե��κ���ϥ桼������Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
  #
  # @param buffer OutPortProvider���ǡ�������Ф��Хåե��ؤΥݥ���
  #
  # @else
  # @brief Setting outside buffer's pointer
  #
  # A pointer to a buffer from which OutPortProvider retrieve data.
  # If already buffer is set, previous buffer's pointer will be
  # overwritten by the given pointer to a buffer.  Since
  # OutPortProvider does not assume ownership of the buffer
  # pointer, destructor of the buffer should be done by user.
  # 
  # @param buffer A pointer to a data buffer to be used by OutPortProvider
  #
  # @endif
  #
  # virtual void setBuffer(CdrBufferBase* buffer);
  def setBuffer(self, buffer):
    self._rtcout.RTC_TRACE("setBuffer()")
    self._buffer = buffer
    return


  # void OutPortDSConsumer::setListener(ConnectorInfo& info,
  #                                           ConnectorListeners* listeners)
  def setListener(self, info, listeners):
    self._rtcout.RTC_TRACE("setListener()")
    self._listeners = listeners
    self._profile = info
    return


  ##
  # @if jp
  # @brief �ǡ������ɤ߽Ф�
  #
  # ���ꤵ�줿�ǡ������ɤ߽Ф���
  #
  # @param data �ɤ߽Ф����ǡ����������륪�֥�������
  #
  # @return �ǡ����ɤ߽Ф��������(�ɤ߽Ф�����:true���ɤ߽Ф�����:false)
  #
  # @else
  # @brief Read data
  #
  # Read set data
  #
  # @param data Object to receive the read data
  #
  # @return Read result (Successful:true, Failed:false)
  #
  # @endif
  #
  # virtual ReturnCode get(cdrMemoryStream& data);
  def get(self, data):
    self._rtcout.RTC_PARANOID("get()")

    try:
      dataservice = self._ptr()
      ret,cdr_data = dataservice.pull()
      
      if ret == RTC.PORT_OK:
        self._rtcout.RTC_DEBUG("get() successful")
        data = cdr_data
        self.onReceived(data)
        self.onBufferWrite(data)
        
        if self._buffer.full():
          self._rtcout.RTC_INFO("InPort buffer is full.")
          self.onBufferFull(data)
          self.onReceiverFull(data)
          
        self._buffer.put(data)
        self._buffer.advanceWptr()
        self._buffer.advanceRptr()

        return self.PORT_OK, data
      return self.convertReturn(ret,data)

    except:
      self._rtcout.RTC_WARN("Exception caught from OutPort.get().")
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST, None




  ##
  # @if jp
  # @brief �ǡ����������Τؤ���Ͽ
  #
  # ���ꤵ�줿�ץ�ѥƥ��˴�Ť��ơ��ǡ����������Τμ���������Ͽ���롣
  #
  # @param properties ��Ͽ����
  #
  # @return ��Ͽ�������(��Ͽ����:true����Ͽ����:false)
  #
  # @else
  # @brief Subscribe the data receive notification
  #
  # Subscribe the data receive notification based on specified property
  # information
  #
  # @param properties Subscription information
  #
  # @return Subscription result (Successful:true, Failed:false)
  #
  # @endif
  #
  # virtual bool subscribeInterface(const SDOPackage::NVList& properties);
  def subscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("subscribeInterface()")
    index = OpenRTM_aist.NVUtil.find_index(properties,"dataport.data_service.outport_ior")
        
    if index < 0:
      self._rtcout.RTC_DEBUG("dataport.data_service.outport_ior not found.")
      return False

    if OpenRTM_aist.NVUtil.isString(properties,"dataport.data_service.outport_ior"):
      self._rtcout.RTC_DEBUG("dataport.data_service.outport_ior found.")
      ior = ""
      #try:
      ior = any.from_any(properties[index].value, keep_structs=True)
      #except:
      #  self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
            
      orb = OpenRTM_aist.Manager.instance().getORB()
      obj = orb.string_to_object(ior)
      ret = self.setObject(obj)
      if ret:
        self._rtcout.RTC_DEBUG("CorbaConsumer was set successfully.")
      else:
        self._rtcout.RTC_ERROR("Invalid object reference.")
        
      return ret

    return False


  ##
  # @if jp
  # @brief �ǡ����������Τ������Ͽ���
  #
  # �ǡ����������Τμ�����꤫����Ͽ�������롣
  #
  # @param properties ��Ͽ�������
  #
  # @else
  # @brief Unsubscribe the data receive notification
  #
  # Unsubscribe the data receive notification.
  #
  # @param properties Unsubscription information
  #
  # @endif
  #
  # virtual void unsubscribeInterface(const SDOPackage::NVList& properties);
  def unsubscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeInterface()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.data_service.outport_ior")
    if index < 0:
      self._rtcout.RTC_DEBUG("dataport.data_service.outport_ior not found.")
      return
    
    ior = ""
    
    try:
      ior = any.from_any(properties[index].value, keep_structs=True)
             
      if ior:
        self._rtcout.RTC_DEBUG("dataport.data_service.outport_ior found.")
        orb = OpenRTM_aist.Manager.instance().getORB()
        obj = orb.string_to_object(ior)
        if self._ptr(True)._is_equivalent(obj):
          self.releaseObject()
          self._rtcout.RTC_DEBUG("CorbaConsumer's reference was released.")
          return

        self._rtcout.RTC_ERROR("hmm. Inconsistent object reference.")

    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    return


  ##
  # @if jp
  # @brief �꥿���󥳡����Ѵ� (DataPortStatus -> BufferStatus)
  # @else
  # @brief Return codes conversion
  # @endif
  #
  # ReturnCode convertReturn(::OpenRTM::PortStatus status,
  #                          const cdrMemoryStream& data)
  def convertReturn(self, status, data):
    if status == RTC.PORT_OK:
      # never comes here
      return self.PORT_OK, data

    elif status == RTC.PORT_ERROR:
      self.onSenderError()
      return self.PORT_ERROR, data

    elif status == RTC.BUFFER_FULL:
      # never comes here
      return self.BUFFER_FULL, data

    elif status == RTC.BUFFER_EMPTY:
      self.onSenderEmpty()
      return self.BUFFER_EMPTY, data

    elif status == RTC.BUFFER_TIMEOUT:
      self.onSenderTimeout()
      return self.BUFFER_TIMEOUT, data

    elif status == RTC.UNKNOWN_ERROR:
      self.onSenderError()
      return self.UNKNOWN_ERROR, data

    else:
      self.onSenderError()
      return self.UNKNOWN_ERROR, data



    
  ##
  # @brief Connector data listener functions
  #
  # inline void onBufferWrite(const cdrMemoryStream& data)
  def onBufferWrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE].notify(self._profile, data)

    return


  # inline void onBufferFull(const cdrMemoryStream& data)
  def onBufferFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL].notify(self._profile, data)

    return


  # inline void onReceived(const cdrMemoryStream& data)
  def onReceived(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)

    return


  # inline void onReceiverFull(const cdrMemoryStream& data)
  def onReceiverFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL].notify(self._profile, data)

    return


  ##
  # @brief Connector listener functions
  #
  # inline void onSenderEmpty()
  def onSenderEmpty(self):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY].notify(self._profile)

    return


  # inline void onSenderTimeout()
  def onSenderTimeout(self):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT].notify(self._profile)

    return

      
  # inline void onSenderError()
  def onSenderError(self):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)

    return


def OutPortDSConsumerInit():
  factory = OpenRTM_aist.OutPortConsumerFactory.instance()
  factory.addFactory("data_service",
                     OpenRTM_aist.OutPortDSConsumer,
                     OpenRTM_aist.Delete)
  return
