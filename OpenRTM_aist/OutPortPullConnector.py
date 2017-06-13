#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPortPullConnector.py
# @brief OutPortPull type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

from omniORB import cdrMarshal
from omniORB import any

import OpenRTM_aist
import threading


##
# @if jp
# @class OutPortPullConnector
# @brief OutPortPullConnector ���饹
#
# OutPort �� pull ���ǡ����ե��Τ���� Connector ���饹�����Υ���
# �������Ȥϡ���³���� dataflow_type �� pull �����ꤵ�줿��硢
# OutPort �ˤ�ä���������ͭ���졢InPortPullConnector ���Фˤʤäơ�
# �ǡ����ݡ��Ȥ� pull ���Υǡ����ե���¸����롣��Ĥ���³���Ф��ơ�
# ��ĤΥǡ������ȥ꡼����󶡤���ͣ��� Connector ���б����롣
# Connector �� ��³������������� UUID ������ ID �ˤ����̤���롣
#
# OutPortPullConnector �ϰʲ��λ��ĤΥ��֥������Ȥ��ͭ���������롣
#
# - InPortConsumer
# - Buffer
#
# OutPort �˽񤭹��ޤ줿�ǡ����� OutPortPullConnector::write() ����
# ���� Buffer �˽񤭹��ޤ�롣InPortPullConnector ��
# OutPortPullConnector ����ǡ������ɤ߽Ф����Ȥ� InPort �˥ǡ�����
# ž������롣
#
# @since 1.0.0
#
# @else
# @class OutPortPullConnector
# @brief OutPortPullConnector class
#
# Connector class of OutPort for pull type dataflow. When "pull" is
# specified as dataflow_type at the time of establishing
# connection, this object is generated and owned by the OutPort.
# This connector and InPortPullConnector make a pair and realize
# pull type dataflow of data ports. One connector corresponds to
# one connection which provides a data stream. Connector is
# distinguished by ID of the UUID that is generated at establishing
# connection.
#
# OutPortPullConnector owns and manages the following objects.
#
# - InPortConsumer
# - Buffer
#
# Data written into the OutPort is passed to
# OutPortPullConnector::write(), and it is written into the buffer.
# By reading data from OutPortPullConnector to InPortPullConnector,
# data transfer is realized.
#
# @since 1.0.0
#
# @endif
#
class OutPortPullConnector(OpenRTM_aist.OutPortConnector):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # OutPortPullConnector �Υ��󥹥ȥ饯���ϥ��֥��������������˲���
  # ������ˤȤ롣ConnectorInfo ����³�����ޤߡ����ξ���˽����Х�
  # �ե������������롣OutPort ���󥿡��ե������Υץ�Х������֥�����
  # �ȤؤΥݥ��󥿤��ꡢ��ͭ������ĤΤǡ�OutPortPullConnector ��
  # OutPortProvider �β�����Ǥ����ġ��Ƽ磻�٥�Ȥ��Ф��륳����Х�
  # ���������󶡤��� ConnectorListeners �������Ŭ�ڤʥ����ߥ󥰤ǥ���
  # ��Хå���ƤӽФ����ǡ����Хåե����⤷ OutPortBase �����󶡤�
  # �����Ϥ��Υݥ��󥿤��롣
  #
  # @param info ConnectorInfo
  # @param provider OutPortProvider
  # @param listeners ConnectorListeners ���Υꥹ�ʥ��֥������ȥꥹ��
  # @param buffer CdrBufferBase ���ΥХåե�
  #
  # @else
  # @brief Constructor
  #
  # OutPortPullConnector's constructor is given the following
  # arguments.  According to ConnectorInfo which includes
  # connection information, a buffer is created.  It is also given
  # a pointer to the provider object for the OutPort interface.
  # The owner-ship of the pointer is owned by this
  # OutPortPullConnector, it has responsibility to destruct the
  # OutPortProvider.  OutPortPullConnector also has
  # ConnectorListeners to provide event callback mechanisms, and
  # they would be called at the proper timing.  If data buffer is
  # given by OutPortBase, the pointer to the buffer is also given
  # as arguments.
  #
  # @param info ConnectorInfo
  # @param provider OutPortProvider
  # @param listeners ConnectorListeners type lsitener object list
  # @param buffer CdrBufferBase type buffer
  #
  # @endif
  #
  # OutPortPullConnector(ConnectorInfo info,
  #                      OutPortProvider* provider,
  #                      ConnectorListeners& listeners,
  #                      CdrBufferBase* buffer = 0);
  def __init__(self, info, provider, listeners, buffer = 0):
    OpenRTM_aist.OutPortConnector.__init__(self, info)
    self._provider = provider
    self._listeners = listeners
    self._buffer = buffer

    self._directInPort = None
    self._inPortListeners = None
    
    self._directNewData = False
    self._valueMutex = threading.RLock()
    self._value = None

    if not self._buffer:
      self._buffer = self.createBuffer(info)

    if not self._provider or not self._buffer:
      self._rtcout.RTC_ERROR("Exeption: in OutPortPullConnector.__init__().")
      raise

    self._buffer.init(info.properties.getNode("buffer"))
    self._provider.init(info.properties)
    self._provider.setBuffer(self._buffer)
    self._provider.setConnector(self)
    self._provider.setListener(info, self._listeners)
    self.onConnect()
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # disconnect() ���ƤФ졢provider, buffer �����Ρ��������롣
  #
  # @else
  #
  # @brief Destructor
  #
  # This operation calls disconnect(), which destructs and deletes
  # the consumer, the publisher and the buffer.
  #
  # @endif
  #
  def __del__(self):
    return


  ##
  # @if jp
  # @brief �ǡ����ν񤭹���
  #
  # Publisher���Ф��ƥǡ�����񤭹��ߡ�����ˤ���б�����InPort��
  # �ǡ�����ž������롣
  #
  # @else
  #
  # @brief Writing data
  #
  # This operation writes data into publisher and then the data
  # will be transferred to correspondent InPort.
  #
  # @endif
  #
  # virtual ReturnCode write(const cdrMemoryStream& data);
  def write(self, data):
    if self._directInPort is not None:
      
      guard = OpenRTM_aist.ScopedLock(self._valueMutex)
      self._value = data
      self._directNewData = True
      
      del guard
      
      return self.PORT_OK
    # data -> (conversion) -> CDR stream
    cdr_data = None
    if self._endian is not None:
      cdr_data = cdrMarshal(any.to_any(data).typecode(), data, self._endian)
    else:
      self._rtcout.RTC_ERROR("write(): endian %s is not support.",self._endian)
      return self.UNKNOWN_ERROR
    if self._buffer:
      self._buffer.write(cdr_data)
    else:
      return self.UNKNOWN_ERROR
    return self.PORT_OK


  ##
  # @if jp
  # @brief ��³���
  #
  # consumer, publisher, buffer �����Ρ��������롣
  #
  # @else
  #
  # @brief disconnect
  #
  # This operation destruct and delete the consumer, the publisher
  # and the buffer.
  #
  # @endif
  #
  # virtual ReturnCode disconnect();
  def disconnect(self):
    self._rtcout.RTC_TRACE("disconnect()")
    self.onDisconnect()
    # delete provider
    if self._provider:
      OpenRTM_aist.OutPortProviderFactory.instance().deleteObject(self._provider)
      self._provider.exit()
    self._provider = 0

    # delete buffer
    if self._buffer:
      OpenRTM_aist.CdrBufferFactory.instance().deleteObject(self._buffer)
    self._buffer = 0

    if self._directInPort:
      self._directInPort.removeOutPortConnector(self)
      self._directInPort = None

    return self.PORT_OK


  ##
  # @if jp
  # @brief Buffer ���������
  #
  # Connector ���ݻ����Ƥ��� Buffer ���֤�
  #
  # @else
  # @brief Getting Buffer
  #
  # This operation returns this connector's buffer
  #
  # @endif
  #
  # virtual CdrBufferBase* getBuffer();
  def getBuffer(self):
    return self._buffer


  ##
  # @if jp
  # @brief �����ƥ��ֲ�
  #
  # ���Υ��ͥ����򥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector activation
  #
  # This operation activates this connector
  #
  # @endif
  #
  # virtual void activate(){}; // do nothing
  def activate(self):  # do nothing
    pass


  ##
  # @if jp
  # @brief �󥢥��ƥ��ֲ�
  #
  # ���Υ��ͥ������󥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector deactivation
  #
  # This operation deactivates this connector
  #
  # @endif
  #
  # virtual void deactivate(){}; // do nothing
  def deactivate(self): # do nothing
    pass

    
  ##
  # @if jp
  # @brief Buffer������
  # @else
  # @brief create buffer
  # @endif
  #
  # CdrBufferBase* createBuffer(ConnectorInfo& info);
  def createBuffer(self, info):
    buf_type = info.properties.getProperty("buffer_type","ring_buffer")
    return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)


  ##
  # @if jp
  # @brief ��³��Ω���˥�����Хå���Ƥ�
  # @else
  # @brief Invoke callback when connection is established
  # @endif
  # void onConnect()
  def onConnect(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_CONNECT].notify(self._profile)
    return


  ##
  # @if jp
  # @brief ��³���ǻ��˥�����Хå���Ƥ�
  # @else
  # @brief Invoke callback when connection is destroied
  # @endif
  # void onDisconnect()
  def onDisconnect(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT].notify(self._profile)
    return


  ##
  # @if jp
  # @brief �ǡ���������쥯�Ȥ˽񤭹��ि���InPort�Υ����Х�Ȥ����ꤹ��
  #
  # @param self
  # @param directInPort InPort�Υ����Х��
  # @return True: ��������� False: ��������ѤߤΤ��Ἲ��
  # @else
  # @brief 
  #
  # @param self
  # @param directInPort 
  # @return 
  # @endif
  #
  # bool setPorts(InPortBase* directInPort, OutPortBase* outPort);
  def setInPort(self, directInPort):
    if self._directInPort is not None:
      return False
    self._directInPort = directInPort
    self._inPortListeners = self._directInPort._listeners
    
    self._directInPort.addOutPortConnector(self)
    return True

  ##
  # @if jp
  #
  # @brief �ǡ���������쥯�Ȥ��ɤ߹���
  #
  # @param self
  # @return Ƚ��(�ǡ������񤭹��ޤ�Ƥ��ʤ����True)���ɤ߹���ǡ���
  #
  # @else
  # @brief 
  #
  # @param self
  # @param data 
  # @endif
  # DataType* read()
  def read(self):
    guard = OpenRTM_aist.ScopedLock(self._valueMutex)
    if not self.isNew():
        self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY].notify(self._profile)
        self._inPortListeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY].notify(self._profile)
        self._rtcout.RTC_TRACE("ON_BUFFER_EMPTY(OutPort), ")
        self._rtcout.RTC_TRACE("ON_SENDER_EMPTY(InPort) ")
        self._rtcout.RTC_TRACE("callback called in direct mode.")
        return False, ""
    
    data = self._value
    ret = self._directNewData
    self._directNewData = False
    del guard
    
    
    self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ].notify(self._profile, data)
    self._rtcout.RTC_TRACE("ON_BUFFER_READ(OutPort), ")
    self._rtcout.RTC_TRACE("callback called in direct mode.")
    self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    self._rtcout.RTC_TRACE("ON_SEND(OutPort), ")
    self._rtcout.RTC_TRACE("callback called in direct mode.")
    self._inPortListeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)
    self._rtcout.RTC_TRACE("ON_RECEIVED(InPort), ")
    self._rtcout.RTC_TRACE("callback called in direct mode.")
    self._inPortListeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE].notify(self._profile, data)
    self._rtcout.RTC_TRACE("ON_BUFFER_WRITE(InPort), ")
    self._rtcout.RTC_TRACE("callback called in direct mode.")
    
    return ret, data

  def isNew(self):
    return self._directNewData