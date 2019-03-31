#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ROSTopicManager.py
# @brief ROS Topic Manager class
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
import threading
import rosgraph.xmlrpc
import time
import socket

try:
  from cStringIO import StringIO
except ImportError:
  from io import StringIO



manager = None
mutex = threading.RLock()

##
# @if jp
# @class ROSTopicManager
# @brief ROS�ȥԥå���������륯�饹
#
#
# @else
# @class ROSTopicManager
# @brief 
#
#
# @endif
class ROSTopicManager(rosgraph.xmlrpc.XmlRpcHandler):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Constructor
  #
  # @param self
  #
  # @endif
  def __init__(self):
    self._node = None
    self._server_sock = None
    self._publishers = []
    self._subscribers = []
    self._addr = ""
    self._port = 0
    self._shutdown = False
    self._thread = None
    self._old_uris = []

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  #
  # @param self
  #
  # @else
  #
  # @brief self
  #
  # @endif
  def __del__(self):
    pass

  ##
  # @if jp
  # @brief �ȥԥå��ޥ͡����㳫��
  #
  # @param self
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  def start(self):
    self._node = rosgraph.xmlrpc.XmlRpcNode(9000, self)
    self._node.start()
    self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._server_sock.bind((rosgraph.network.get_bind_address(), self._port))
    (self._addr, self._port) = self._server_sock.getsockname()[0:2]
    self._server_sock.listen(5)
    self._thread = threading.Thread(target=self.run, args=())
    self._thread.daemon = True
    self._thread.start()

  ##
  # @if jp
  # @brief ROSOutPort��Ͽ
  #
  # @param self
  # @param publisher ��Ͽ�оݤ�ROSOutPort
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param publisher 
  #
  # @endif
  def addPublisher(self, publisher):
    if not self.existPublisher(publisher):
      self._publishers.append(publisher)

  ##
  # @if jp
  # @brief ROSInPort��Ͽ
  #
  # @param self
  # @param subscriber ��Ͽ�оݤ�ROSInPort
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param subscriber 
  #
  # @endif
  def addSubscriber(self, subscriber):
    if not self.existSubscriber(subscriber):
      self._subscribers.append(subscriber)


  ##
  # @if jp
  # @brief ROSOutPort���
  #
  # @param self
  # @param publisher ����оݤ�ROSOutPort
  # @return True�����������False������оݤ�¸�ߤ��ʤ�
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param publisher 
  # @return 
  #
  # @endif
  def removePublisher(self, publisher):
    try:
      self._publishers.remove(publisher)
      return True
    except ValueError:
      return False

  ##
  # @if jp
  # @brief ROSInPort���
  #
  # @param self
  # @param subscriber ����оݤ�ROSInPort
  # @return True�����������False������оݤ�¸�ߤ��ʤ�
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param subscriber 
  # @return 
  #
  # @endif
  def removeSubscriber(self, subscriber):
    try:
      self._subscribers.remove(subscriber)
      return True
    except ValueError:
      return False

  ##
  # @if jp
  # @brief ROSOutPort����Ͽ�Ѥߤ��γ�ǧ
  #
  # @param self
  # @param publisher ROSOutPort
  # @return True����Ͽ�Ѥߡ�False��̤��Ͽ
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param publisher 
  # @return 
  #
  # @endif
  def existPublisher(self, publisher):
    if self._publishers.count(publisher) > 0:
      return True
    else:
      return False

  ##
  # @if jp
  # @brief ROSInPort����Ͽ�Ѥߤ��γ�ǧ
  #
  # @param self
  # @param subscriber ROSInPort
  # @return True����Ͽ�Ѥߡ�False��̤��Ͽ
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param subscriber 
  # @return 
  #
  # @endif
  def existSubscriber(self, subscriber):
    if self._subscribers.count(subscriber) > 0:
      return True
    else:
      return False

  ##
  # @if jp
  # @brief publisherUpdate������Хå��ؿ�
  #
  # @param self
  # @param caller_id �ƤӽФ�ID
  # @param topic �ȥԥå�̾
  # @param publishers publisher����
  # @return ret, msg, value
  # ret���꥿���󥳡���(1������ʤ�)
  # msg����å�����
  # value����
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param caller_id 
  # @param topic 
  # @param publishers 
  # @return 
  #
  # @endif
  def publisherUpdate(self, caller_id, topic, publishers):
    lost_uris = []
    for uri in self._old_uris:
      if not (uri in publishers):
        lost_uris.append(uri)
    


    for subscriber in self._subscribers:
      subscriber.connect(caller_id, topic, publishers)
      for lost_uri in lost_uris:
        subscriber.deleteSocket(lost_uri)
    self._old_uris = publishers[:]
    
    

    
    return 1, "", 0

  ##
  # @if jp
  # @brief TCP�����åȼ������ν����ؿ�
  #
  # @param self
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  def run(self):
    while not self._shutdown:
      try:
        (client_sock, client_addr) = self._server_sock.accept()
        addr = client_addr[0] + ":" + str(client_addr[1])
        for publisher in self._publishers:
          publisher.connect(client_sock, addr)
      except:
        pass
    
  ##
  # @if jp
  # @brief �����åȡ�����åɽ�λ����
  #
  # @param self
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  def shutdown(self):
    self._shutdown = True
    self._server_sock.shutdown(socket.SHUT_RDWR)
    self._server_sock.close()
    self._thread.join()
    
    #self._node.shutdown("")


  ##
  # @if jp
  # @brief requestTopic������Хå��ؿ�
  #
  # @param self
  # @param caller_id �ƤӽФ�ID
  # @param topic �ȥԥå�̾
  # @param protocols �ץ�ȥ������
  # @return ret, msg, value
  # ret���꥿���󥳡���(1������ʤ���-1���ȥԥå����б�����Publisher��¸�ߤ��ʤ���0������ʳ��Υ��顼)
  # msg����å�����
  # value���ץ�ȥ��롢���ɥ쥹���ݡ����ֹ�
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param caller_id
  # @param topic
  # @param protocols
  # @return
  #
  # @endif
  def requestTopic(self, caller_id, topic, protocols):
    if not self.hasPublisher(topic):
      return -1, "Not a publisher of [%s]"%topic, []
    for protocol in protocols:
      protocol_id = protocol[0]
      if protocol_id == "TCPROS":
        addr = rosgraph.network.get_host_name()
        port = self._port
        return 1, "ready on %s:%s"%(addr, port), ["TCPROS", addr, port]
    return 0, "no supported protocol implementations", []

  ##
  # @if jp
  # @brief ����ȥԥå�̾��Publisher����Ͽ����Ƥ��뤫���ǧ
  #
  # @param self
  # @param topic �ȥԥå�̾
  # @return True��¸�ߤ��롢False��¸�ߤ��ʤ�
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param topic
  # @return
  #
  # @endif
  def hasPublisher(self, topic):
    for publisher in self._publishers:
      if publisher.getTopic() == topic:
        return True
    return False

  ##
  # @if jp
  # @brief TCP�����åȤ�URI�����
  #
  # @param self
  # @return URI
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @return
  #
  # @endif
  def getURI(self):
    for i in range(0,10):
      if self._node.uri:
        return self._node.uri
      time.sleep(1)

  ##
  # @if jp
  # @brief ���󥹥��󥹼���
  #
  # @return ���󥹥���
  #
  # @else
  #
  # @brief 
  #
  # @return ���󥹥���
  #
  # @endif
  def instance():
    global manager
    global mutex
    
    guard = OpenRTM_aist.ScopedLock(mutex)
    if manager is None:
      manager = ROSTopicManager()
      manager.start()

    return manager
  
  instance = staticmethod(instance)
