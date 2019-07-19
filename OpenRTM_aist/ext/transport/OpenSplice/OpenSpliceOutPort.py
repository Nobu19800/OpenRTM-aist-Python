#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file OpenSpliceOutPort.py
# @brief OpenSplice OutPort class
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
from OpenSpliceTopicManager import OpenSpliceTopicManager
import OpenSpliceMessageInfo
import RTC



##
# @if jp
# @class OpenSpliceOutPort
# @brief OpenSplice Publisher���б����륯�饹
# InPortConsumer���֥������ȤȤ��ƻ��Ѥ���
#
# @else
# @class OpenSpliceOutPort
# @brief 
#
#
# @endif
class OpenSpliceOutPort(OpenRTM_aist.InPortConsumer):
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
    OpenRTM_aist.InPortConsumer.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OpenSpliceOutPort")
    self._properties = None
    self._dataType = RTC.TimedLong._NP_RepositoryId
    self._topic = "chatter"
    self._writer = None


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
    self._rtcout.RTC_PARANOID("~OpenSpliceOutPort()")
    
  ##
  # @if jp
  # @brief ��������
  #
  # InPortConsumer�γƼ������Ԥ�
  #
  # @param self
  # @param prop ��³����
  # marshaling_type ���ꥢ�饤���μ��� �ǥե���ȡ�OpenSplice
  # topic �ȥԥå�̾ �ǥե���� chatter
  #
  # @else
  # @brief Initializing configuration
  #
  # This operation would be called to configure this consumer
  # in initialization.
  #
  # @param self
  # @param prop
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_PARANOID("init()")
    
    if len(prop.propertyNames()) == 0:
      self._rtcout.RTC_DEBUG("Property is empty.")
      return
    
    self._properties = prop

    qosxml = prop.getProperty("QOSXML")
    qosprofile = prop.getProperty("QOSPrfile")
    self._topicmgr = OpenSpliceTopicManager.instance(qosxml, qosprofile)

    self._dataType = prop.getProperty("data_type", self._dataType)

    self._topic = prop.getProperty("opensplice.topic", "chatter")

    topic = self._topicmgr.createTopic(self._dataType, self._topic)

    self._rtcout.RTC_VERBOSE("data type: %s", self._dataType)
    self._rtcout.RTC_VERBOSE("topic name: %s", self._topic)

    self._writer = self._topicmgr.createWriter(topic)

  ##
  # @if jp
  # @brief ��³��ؤΥǡ�������
  #
  # ��³��Υݡ��Ȥإǡ������������뤿��ν�貾�۴ؿ���
  # 
  # ���δؿ��ϡ��ʲ��Υ꥿���󥳡��ɤ��֤���
  #
  # - PORT_OK:       ���ｪλ��
  # - PORT_ERROR:    �ǡ��������β����ǲ��餫�Υ��顼��ȯ��������
  # - SEND_FULL:     �ǡ��������������������¦�Хåե����ե���ä���
  # - SEND_TIMEOUT:  �ǡ��������������������¦�Хåե��������ॢ���Ȥ�����
  # - UNKNOWN_ERROR: ���������Υ��顼
  #
  # @param data ��������ǡ���
  # @return �꥿���󥳡���
  #
  # @else
  # @brief Send data to the destination port
  #
  # Pure virtual function to send data to the destination port.
  #
  # This function might the following return codes
  #
  # - PORT_OK:       Normal return
  # - PORT_ERROR:    Error occurred in data transfer process
  # - SEND_FULL:     Buffer full although OutPort tried to send data
  # - SEND_TIMEOUT:  Timeout although OutPort tried to send data
  # - UNKNOWN_ERROR: Unknown error
  #
  # @endif
  #
  # virtual ReturnCode put(const cdrMemoryStream& data);
  def put(self, data):
    self._rtcout.RTC_PARANOID("put()")

    if self._writer:
      try:
        self._writer.write(data)
        return self.PORT_OK
      except:
        self._rtcout.RTC_ERROR("write error")
        return self.CONNECTION_LOST
    else:
      return self.CONNECTION_LOST
        


  ##
  # @if jp
  # @brief InterfaceProfile������������
  #
  # InterfaceProfile�����������롣
  # �����ǻ��ꤹ��ץ�ѥƥ�������� NameValue ���֥������Ȥ�
  # dataport.interface_type �ͤ�Ĵ�١������ݡ��Ȥ����ꤵ��Ƥ���
  # ���󥿡��ե����������פȰ��פ�����Τ߾����������롣
  #
  # @param properties InterfaceProfile�����������ץ�ѥƥ�
  #
  # @else
  # @brief Publish InterfaceProfile information
  #
  # Publish interfaceProfile information.
  # Check the dataport.interface_type value of the NameValue object 
  # specified by an argument in property information and get information
  # only when the interface type of the specified port is matched.
  #
  # @param properties Properties to get InterfaceProfile information
  #
  # @endif
  #
  # virtual void publishInterfaceProfile(SDOPackage::NVList& properties);
  def publishInterfaceProfile(self, properties):
    pass

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
  # @brief Subscribe to the data sending notification
  #
  # Subscribe to the data sending notification based on specified 
  # property information.
  #
  # @param properties Information for subscription
  #
  # @return Subscription result (Successful:true, Failed:false)
  #
  # @endif
  #
  # virtual bool subscribeInterface(const SDOPackage::NVList& properties);
  def subscribeInterface(self, properties):
    return True
    
  ##
  # @if jp
  # @brief �ǡ����������Τ������Ͽ���
  #
  # �ǡ����������Τμ�����꤫����Ͽ�������롣
  #
  # @param properties ��Ͽ�������
  #
  # @else
  # @brief Unsubscribe the data send notification
  #
  # Unsubscribe the data send notification.
  #
  # @param properties Information for unsubscription
  #
  # @endif
  #
  # virtual void unsubscribeInterface(const SDOPackage::NVList& properties);
  def unsubscribeInterface(self, properties):
    if self._writer:
      self._writer.close()
      self._rtcout.RTC_VERBOSE("remove writer")




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
def OpenSpliceOutPortInit():
  factory = OpenRTM_aist.InPortConsumerFactory.instance()
  factory.addFactory("opensplice",
                     OpenSpliceOutPort,
                     OpenRTM_aist.Delete)

