#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ROSInPort.py
# @brief ROS OutPort class
# @date $Date$
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2019
#     Noriaki Ando
#     Robot Innovation Research Center,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import OpenRTM_aist
import rosgraph.xmlrpc
import socket
import threading
import select
import xmlrpclib
from rosgraph.network import read_ros_handshake_header, write_ros_handshake_header
from ROSTopicManager import ROSTopicManager
import ROSMessageInfo
import struct

try:
  from cStringIO import StringIO
except ImportError:
  from io import StringIO


##
# @if jp
# @class ROSInPort
# @brief ROS Subscriber���б����륯�饹
# InPortProvider���֥������ȤȤ��ƻ��Ѥ���
#
# @else
# @class ROSInPort
# @brief 
#
#
# @endif
class ROSInPort(OpenRTM_aist.InPortProvider):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # �ݡ��ȥץ�ѥƥ��˰ʲ��ι��ܤ����ꤹ�롣
  #  - ���󥿡��ե����������� : ros
  #  - �ǡ����ե������� : Push
  #
  # @param self 
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  # Set the following items to port properties
  #  - Interface type : CORBA_Any
  #  - Data flow type : Push, Pull
  #
  # @param self 
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.InPortProvider.__init__(self)

    # PortProfile setting
    self.setInterfaceType("ros")


    self._profile = None
    self._listeners = None

    self._client = None

    self._topic = "chatter"
    self._callerid = ""
    self._messageType = "ROSFloat32"
    self._roscorehost = "localhost"
    self._roscoreport = "11311"

    self._tcp_connecters = {}

    self._mutex = threading.RLock()

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self 
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @param self 
  #
  # @endif
  #
  def __del__(self):
    return


  ##
  # @if jp
  # @brief ��λ����
  #
  # @param self 
  #
  # @else
  # @brief 
  #
  # @param self 
  #
  # @endif
  #
  def exit(self):
    self._rtcout.RTC_PARANOID("exit()")
    if self._client is not None:
      self._rtcout.RTC_PARANOID("unregister Subscriber()")
      try:
        ret, _, __ = self._client.unregisterSubscriber(self._callerid, self._topic, self._topicmgr.getURI())
        if ret != 1:
          self._rtcout.RTC_ERROR("unregister subscriber error")
      except xmlrpclib.Fault as err:
        self._rtcout.RTC_ERROR("XML-RPC Error:%s", err.faultString)

    if self._topicmgr is not None:
      self._rtcout.RTC_VERBOSE("remove subscriber")
      self._topicmgr.removeSubscriber(self)

    for k, connector in self._tcp_connecters.items():
      try:
        self._rtcout.RTC_VERBOSE("connection close")
        #connector["socket"].shutdown(socket.SHUT_RDWR)
        connector["socket"].close()
        connector["listener"].shutdown()
        connector["thread"].join()
      except:
        self._rtcout.RTC_ERROR("socket shutdown error")

  ##
  # @if jp
  # @brief ��³�ѤߤΥ����åȤ�λ������
  #
  # @param self 
  # @param uri �����åȤ���³���URI
  #
  # @else
  # @brief 
  #
  # @param self 
  # @param uri
  #
  # @endif
  #
  def deleteSocket(self, uri):
    if uri in self._tcp_connecters:
      try:
        self._rtcout.RTC_VERBOSE("close socket")
        #self._tcp_connecters[uri].shutdown(socket.SHUT_RDWR)
        self._tcp_connecters[uri]["socket"].close()
        self._tcp_connecters[uri]["listener"].shutdown()
        self._tcp_connecters[uri]["thread"].join()
        del self._tcp_connecters[uri]
      except:
        self._rtcout.RTC_ERROR("close socket error")

  ##
  # @if jp
  # @brief �����
  #
  # @param self 
  # @param prop ��³����
  # marshaling_type ���ꥢ�饤���μ��� �ǥե���ȡ�ROSFloat32
  # topic �ȥԥå�̾ �ǥե���� chatter
  # roscore_host roscore�Υۥ���̾ �ǥե���ȡ�localhost
  # roscore_port roscore�Υݡ����ֹ� �ǥե���ȡ�11311
  #
  # @else
  # @brief 
  #
  # @param self 
  # @param prop
  #
  # @endif
  #
  ## virtual void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_PARANOID("init()")
    if len(prop.propertyNames()) == 0:
      self._rtcout.RTC_DEBUG("Property is empty.")
      return
    
    self._topicmgr = ROSTopicManager.instance()
    if self._topicmgr.existSubscriber(self):
      self._rtcout.RTC_VERBOSE("Subscriber already exists.")
      return

    self._messageType = prop.getProperty("marshaling_type", "ROSFloat32")
    self._topic = prop.getProperty("topic", "chatter")
    self._topic = "/"+self._topic
    self._roscorehost = prop.getProperty("roscore_host", "localhost")
    self._roscoreport = prop.getProperty("roscore_port", "11311")

    
    self._rtcout.RTC_VERBOSE("topic name: %s", self._topic)
    self._rtcout.RTC_VERBOSE("roscore address: %s:%s", (self._roscorehost, self._roscoreport))

    if not self._callerid:
      self._callerid = str(OpenRTM_aist.uuid1())

    factory = ROSMessageInfo.ROSMessageInfoFactory.instance()
    info = factory.createObject(self._messageType)

    info_type = info.datatype()

    factory.deleteObject(info)



    self._rtcout.RTC_VERBOSE("caller id: %s", self._callerid)

    self._topicmgr.addSubscriber(self)

    self._client = xmlrpclib.ServerProxy('http://'+self._roscorehost+":"+self._roscoreport)
    
    try:
      _, __, val = self._client.registerSubscriber(self._callerid, self._topic, info_type, self._topicmgr.getURI())
    except xmlrpclib.Fault as err:
      self._rtcout.RTC_ERROR("XML-RPC ERROR: %s", err.faultString)
      return
    
    self.connect(self._callerid, self._topic, val)

  ##
  # @if jp
  # @brief publisher����³
  #
  # @param self 
  # @param caller_id �ƤӽФ�ID
  # @param topic �ȥԥå�̾
  # @param publishers publisher��URI�Υꥹ��
  #
  # @else
  # @brief 
  #
  # @param self 
  # @param caller_id 
  # @param topic 
  # @param publishers 
  #
  # @endif
  #
  def connect(self, caller_id, topic, publishers):
    self._rtcout.RTC_VERBOSE("connect()")
    if topic != self._topic:
      self._rtcout.RTC_WARN("Topic name is not match(%s:%s)",(topic, self._topic))
      return
    
    
    for uri in publishers:
      if uri in self._tcp_connecters:
        continue
      self._rtcout.RTC_PARANOID("connectTCP(%s, %s, %s)", (caller_id, topic, uri))
      pub = xmlrpclib.ServerProxy(uri)
      ret, message, result = pub.requestTopic(caller_id, topic, [['TCPROS']])
      
      if ret == -1:
        self._rtcout.RTC_WARN("requestTopic error: %s",message)
        continue
      elif ret == 0:
        self._rtcout.RTC_WARN("requestTopic error: %s",message)
        continue
      else:
        _, dest_addr, dest_port = result
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 9)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 10)
        sock.settimeout(1)
        sock.connect((dest_addr, dest_port))
        
        
        fileno = sock.fileno()
        poller = select.poll()
        poller.register(fileno, select.POLLOUT)
        ready = False
        
        while not ready:
          events = poller.poll()
          for _, flag in events:
            if flag & select.POLLOUT:
              ready = True
        


        factory = ROSMessageInfo.ROSMessageInfoFactory.instance()
        info = factory.createObject(self._messageType)

        info_type = info.datatype()
        info_md5sum = info.md5sum()
        info_message_definition = info.message_definition()

        factory.deleteObject(info)

        sock.setblocking(1)
        fields = {'topic': topic,
                  'message_definition': info_message_definition,
                  'tcp_nodelay': '0',
                  'md5sum': info_md5sum,
                  'type': info_type,
                  'callerid': caller_id}

        try:
          write_ros_handshake_header(sock, fields)
        except rosgraph.network.ROSHandshakeException:
          self._rtcout.RTC_ERROR("write ROS handshake header")
          continue
        read_buff = StringIO()
        sock.setblocking(1)

        try:
          read_ros_handshake_header(sock, read_buff, 65536)
        except rosgraph.network.ROSHandshakeException:
          self._rtcout.RTC_ERROR("read ROS handshake header")
          continue

        
        
        listener = SubListener(self, sock, uri)
        
        self._rtcout.RTC_VERBOSE("Subscriber Listener thread start")
        task = threading.Thread(target=listener.recieve, args=())
        task.start()
        
        self._tcp_connecters[uri] = {"socket":sock, "listener": listener, "thread": task}
        
      
      

  ## virtual void setBuffer(BufferBase<cdrMemoryStream>* buffer);
  def setBuffer(self, buffer):
    return

  ##
  # @if jp
  # @brief ���ͥ����ꥹ�ʤ�����
  #
  # @param info ��³����
  # @param listeners �ꥹ��
  #
  # @else
  # @brief 
  #
  # @param info 
  # @param listeners 
  #
  # @endif
  #
  # void setListener(ConnectorInfo& info,
  #                  ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._profile = info
    self._listeners = listeners
    return


  ##
  # @if jp
  # @brief �Хåե��˥ǡ�����񤭹���
  #
  # ���ꤵ�줿�Хåե��˥ǡ�����񤭹��ࡣ
  #
  # @param data ����оݥǡ���
  #
  # @else
  # @brief Write data into the buffer
  #
  # Write data into the specified buffer.
  #
  # @param data The target data for writing
  #
  # @endif
  #
  def put(self, data):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    try:
      self._rtcout.RTC_PARANOID("ROSInPort.put()")
      if not self._connector:
        self.onReceiverError(data)
        return OpenRTM.PORT_ERROR

      self._rtcout.RTC_PARANOID("received data size: %d", len(data))

      self.onReceived(data)

      ret = self._connector.write(data)

      self.convertReturn(ret, data)

    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      



  def convertReturn(self, status, data):
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      self.onBufferWrite(data)
      return
            
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      self.onReceiverError(data)
      return

    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      self.onBufferFull(data)
      self.onReceiverFull(data)
      return

    elif status == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      return OpenRTM.BUFFER_EMPTY

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      self.onReceiverError(data)
      return

    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferWriteTimeout(data)
      self.onReceiverTimeout(data)
      return

    else:
      self.onReceiverError(data)
      return
        

  ##
  # @brief Connector data listener functions
  #
  # inline void onBufferWrite(const cdrMemoryStream& data)
  def onBufferWrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE].notify(self._profile, data)
    return


  ## inline void onBufferFull(const cdrMemoryStream& data)
  def onBufferFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL].notify(self._profile, data)
    return


  ## inline void onBufferWriteTimeout(const cdrMemoryStream& data)
  def onBufferWriteTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT].notify(self._profile, data)
    return

  ## inline void onBufferWriteOverwrite(const cdrMemoryStream& data)
  def onBufferWriteOverwrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE].notify(self._profile, data)
    return


  ## inline void onReceived(const cdrMemoryStream& data)
  def onReceived(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)
    return


  ## inline void onReceiverFull(const cdrMemoryStream& data)
  def onReceiverFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL].notify(self._profile, data)
    return


  ## inline void onReceiverTimeout(const cdrMemoryStream& data)
  def onReceiverTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT].notify(self._profile, data)
    return


  ## inline void onReceiverError(const cdrMemoryStream& data)
  def onReceiverError(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR].notify(self._profile, data)
    return

##
# @if jp
# @class SubListener
# @brief ROS Subscriber�Υǡ����������Υꥹ��
# 
#
# @else
# @class SubListener
# @brief 
#
#
# @endif
class SubListener:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param sub ROSInPort
  # @param sock �����å�
  # @param uri ��³���URI
  #
  # @else
  # @brief Constructor
  #
  # @param self
  # @param sub 
  # @param sock 
  # @param uri 
  #
  # @endif
  #
  def __init__(self, sub, sock, uri):
    self._sub = sub
    self._sock = sock
    self._uri = uri
    self._shutdown = False
  ##
  # @if jp
  # @brief ��λ��������
  #
  # @param self
  #
  # @else
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  def shutdown(self):
    self._shutdown = True

  ##
  # @if jp
  # @brief ��������
  #
  # @param self
  #
  # @else
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  def recieve(self):
    while not self._shutdown:
      try:
        self._sock.setblocking(1)
        data = self._sock.recv(65536)
        if data:
          self._sub.put(data)
      except:
        self._sub.deleteSocket(self._uri)
        return


##
# @if jp
# @brief �⥸�塼����Ͽ�ؿ�
#
#
# @else
# @brief 
#
#
# @endif
#
def ROSInPortInit():
  factory = OpenRTM_aist.InPortProviderFactory.instance()
  factory.addFactory("ros",
                     ROSInPort,
                     OpenRTM_aist.Delete)