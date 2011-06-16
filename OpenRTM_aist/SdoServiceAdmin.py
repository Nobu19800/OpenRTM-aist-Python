#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SdoServiceAdmin.py
# @brief SDO service administration class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import copy
import threading
import OpenRTM_aist


##
# @if jp
#
# @class SDO service administration class
# @brief SDO service �������饹
#
# ���Υ��饹�ϡ�SDO Service ��������뤿��Υ��饹�Ǥ��롣SDO
# Service �� OMG SDO Specification �ˤ������������Ƥ��롢SDO������
# �ε�ǽ�Τ�����󶡤ޤ��׵᤹�륵���ӥ��ΰ�ĤǤ��롣�ܺ٤ϻ��ͤˤ�
# �����������Ƥ��ʤ������ܥ��饹�Ǥϰʲ��Τ褦�˿����񤦥����ӥ���
# �����ΤȤ���������������뤿��Υ��饹���ܥ��饹�Ǥ��롣
#
# SDO Service �ˤ����Ƥϡ�SDO/RTC�˽�ͭ���졢�����Υ����ӥ�����
# �����Τ� SDO Service Provider��¾��SDO/RTC�䥢�ץꥱ���������
# �����륵���ӥ����֥������Ȥλ��Ȥ������ꡢ�����ε�ǽ�����Ѥ���
# ��Τ�SDO Service Consumer �ȸƤ֡�
#
# SDO Service Provider ��¾�Υ��ץꥱ������󤫤�ƤФ졢SDO/RTC����
# �ε�ǽ�˥����������뤿����Ѥ����롣¾��SDO/RTC�ޤ��ϥ��ץꥱ��
# �����ϡ�
#
# - SDO::get_service_profiles ()
# - SDO::get_service_profile (in UniqueIdentifier id)
# - SDO::get_sdo_service (in UniqueIdentifier id) 
#
# �Τ����줫�Υ��ڥ졼�����ˤ�ꡢServiceProfile �ޤ��� SDO
# Service �λ��Ȥ����������ǽ�����Ѥ��뤿��Υ��ڥ졼������Ƥӽ�
# ����¾��SDO/RTC�ޤ��ϥ��ץꥱ��������Ǥλ��Ȥ��˴���Ǥ�դΥ���
# �ߥ󥰤ǹԤ�졢�����ӥ���¦�Ǥϡ��ɤ�����ɤ�������Ȥ���Ƥ���
# �����Τ뤳�ȤϤǤ��ʤ��������ǡ�SDO/RTC¦�⡢Ǥ�դΥ����ߥ󥰤ǥ���
# �ӥ����󶡤���ߤ��뤳�Ȥ�Ǥ��뤿�ᡢ�����ӥ�������¦�Ǥϡ����
# �����ӥ������ѤǤ���Ȥϸ¤�ʤ���ΤȤ��ƥ����ӥ����ڥ졼������
# �ƤӽФ�ɬ�פ����롣
#
# ������SDO Service Consumer ������SDO/RTC�ʳ���SDO/RTC�ޤ��ϥ��ץ�
# ��������󤬥����ӥ��μ��Τ����������SDO/RTC�˥��֥������Ȼ��Ȥ�
# �ޤ�ץ�ե������Ϳ���뤳�Ȥǡ�SDO/RTC¦���饵���ӥ����ڥ졼����
# �󤬸ƤФ쳰����SDO/RTC�ޤ��ϥ��ץꥱ��������󶡤��뵡ǽ������
# �Ǥ��롣�ޤ������֥�����Ū�ʥ��֥������Ȥ�Ϳ���뤳�Ȥǡ�SDO/RTC¦
# ����Υ�����Хå���¸����뤿��ˤ����Ѥ��뤳�Ȥ��Ǥ��롣���󥷥塼
# �ޤϡ��ץ�Х����ȤϰۤʤꡢSDO Configuration���󥿡��ե���������
# �ɲá�������Ԥ��롣��Ϣ���륪�ڥ졼�����ϰʲ��ΤȤ���Ǥ��롣
#
# - Configuration::add_service_profile (in ServiceProfile sProfile)
# - Configuration::remove_service_profile (in UniqueIdentifier id)
#
# ������SDO/RTC�ޤ��ϥ��ץꥱ�������ϡ����Ȥ�����SDO Servcie
# Provider �λ��Ȥ�ID�����interface type���ץ�ѥƥ��ȤȤ��
# ServcieProfile �˥��åȤ��������ǡ�add_service_profile() �ΰ�����
# ����Ϳ���뤳�Ȥǡ�����SDO/RTC�˥����ӥ���Ϳ���롣���κݡ�ID��UUID
# �ʤɰ�դ�ID�Ǥʤ���Фʤ�ʤ����ޤ����������ݤˤ�ID�ˤ���оݤ�
# ����ServiceProfile��õ�����뤿�ᡢ�����ӥ���¦�ǤϺ�����ޤ�ID��
# �ݻ����Ƥ����ʤ���Фʤ�ʤ���
#
# 
#
#
#
# @since 1.1.0
#
# @else
#
# @class SDO service administration class
# @brief SDO service administration class
#
#
# @since 1.1.0
#
# @endif
class SdoServiceAdmin:
  """
  """

  
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # ���󥹥ȥ饯��
  # @param 
  # 
  # @else
  # @brief Constructor
  # Constructor
  # @param 
  # @endif
  # SdoServiceAdmin(::RTC::RTObject_impl& rtobj);
  def __init__(self, rtobj):
    self._rtobj = rtobj
    self._consumerTypes = []
    self._allConsumerAllowed = True

    ##
    # @if jp
    # @brief Lock �դ� SDO ServiceProfileList
    # @else
    # @brief SDO ServiceProfileList with mutex lock
    # @endif
    self._providerProfiles = []
    self._provider_mutex = threading.RLock()
    
    ##
    # @if jp
    # @brief Lock �դ� SDO ServiceProfileList
    # @else
    # @brief SDO ServiceProfileList with mutex lock
    # @endif
    self._consumers = []
    self._consumer_mutex = threading.RLock()

    ##
    # @if jp
    # @brief logger
    # @else
    # @brief logger
    # @endif
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("SdoServiceAdmin")

    self._rtcout.RTC_TRACE("SdoServiceAdmin::SdoServiceAdmin(%s)",
                           rtobj.getProperties().getProperty("instance_name"))

    # getting consumer types from RTC's properties
    prop = copy.deepcopy(self._rtobj.getProperties())
    constypes = prop.getProperty("sdo_service.consumer_types")
    self._consumerTypes = [s.strip() for s in constypes.split(",")]
    self._rtcout.RTC_DEBUG("sdo_service.consumer_types: %s",
                           str(OpenRTM_aist.flatten(self._consumerTypes)))

    # If types include '[Aa][Ll][Ll]', all types allowed in this RTC
    for ctype in self._consumerTypes:
      tmp = ctype.lower()
      if tmp == "all":
        self._allConsumerAllowed = True
        self._rtcout.RTC_DEBUG("sdo_service.consumer_types: ALL")

    return


  ##
  # @if jp
  # @brief ���ۥǥ��ȥ饯��
  # ���ۥǥ��ȥ饯����
  # 
  # @else
  # @brief Virtual destractor
  # Virtual destractor.
  # @endif
  def __del__(self):
    return

    
  ##
  # @if jp
  # @brief Service Consumer Factory ����Ͽ����
  # 
  # @else
  # @brief Add Service Consumer Factory
  # @endif
  # bool addSdoServiceConsumerFactory();
  def addSdoServiceConsumerFactory(self):
    return False


  ##
  # @if jp
  # @brief Service Consumer Factory ��������
  # 
  # @else
  # @brief Remove Service Consumer Factory
  # @endif
  # bool removeSdoServiceConsumerFactory();
  def removeSdoServiceConsumerFactory(self):
    return False
    

  ##
  # @if jp
  # @brief Service Consumer ���ɲä���
  # 
  # @else
  # @brief Add Service Consumer
  # @endif
  # bool addSdoServiceConsumer(const SDOPackage::ServiceProfile& sProfile);
  def addSdoServiceConsumer(self, sProfile):
    self._rtcout.RTC_TRACE("addSdoServiceConsumer(IFR = %s)",
                           sProfile.interface_type)
    profile = copy.deepcopy(sProfile)

    # Not supported consumer type -> error return
    if not self.isAllowedConsumerType(sProfile):
      self._rtcout.RTC_ERROR("Not supported consumer type. %s", profile.id)
      return False

    if not self.isExistingConsumerType(sProfile):
      self._rtcout.RTC_ERROR("type %s already exists.", profile.id)
      return False
    
    if str(profile.id) ==  "":
      self._rtcout.RTC_WARN("No id specified. It should be given by clients.")
      return False

    # re-initialization
    guard = OpenRTM_aist.ScopedLock(self._consumer_mutex)
    id = str(sProfile.id)
    for i in range(len(self._consumers)):
      if id == str(self._consumers[i].getProfile().id):
        self._rtcout.RTC_INFO("Existing consumer is reinitilized.")
        self._rtcout.RTC_DEBUG("Propeteis are: %s",
                               NVUtil.toString(sProfile.properties))
        return self._consumers[i].reinit(sProfile)
    del guard

    # new pofile
    factory = OpenRTM_aist.SdoServiceConsumerFactory.instance()
    ctype = str(profile.interface_type)
    consumer = factory.createObject(ctype)
    if consumer == None:
      self._rtcout.RTC_ERROR("Hmm... consumer must be created.")
      return False

    # initialize
    if not consumer.init(self._rtobj, sProfile):
      self._rtcout.RTC_WARN("SDO service initialization was failed.")
      self._rtcout.RTC_DEBUG("id:         %s", str(sProfile.id))
      self._rtcout.RTC_DEBUG("IFR:        %s", str(sProfile.interface_type))
      self._rtcout.RTC_DEBUG("properties: %s", OpenRTM_aist.NVUtil.toString(sProfile.properties))
      factory.deleteObject(consumer)
      self._rtcout.RTC_INFO("SDO consumer was deleted by initialization failure")
      return False

    # store consumer
    guard = OpenRTM_aist.ScopedLock(self._consumer_mutex)
    self._consumers.append(consumer)
    del guard

    return True

  
  ##
  # @if jp
  # @brief Service Consumer ��������
  # 
  # @else
  # @brief Remove Service Consumer
  # @endif
  # bool removeSdoServiceConsumer(const char* id);
  def removeSdoServiceConsumer(self, id):
    if id == None or id[0] == '\0':
      self._rtcout.RTC_ERROR("removeSdoServiceConsumer(): id is invalid.")
      return False

    self._rtcout.RTC_TRACE("removeSdoServiceConsumer(id = %s)", id)

    guard = OpenRTM_aist.ScopedLock(self._consumer_mutex)
    strid = id

    for (idx,cons) in enumerate(self._consumers):
      if strid == str(cons.getProfile().id):
        cons.finalize()
        del self._consumers[idx]
        factory = OpenRTM_aist.SdoServiceConsumerFactory.instance()
        factory.deleteObject(cons)
        self._rtcout.RTC_INFO("SDO service has been deleted: %s", id)
        return True

    self._rtcout.RTC_WARN(("Specified SDO consumer not found: %s", id))
    return False
    

  ##
  # @if jp
  # @brief ���Ĥ��줿�����ӥ������ɤ���Ĵ�٤�
  # 
  # @else
  # @brief If it is allowed service type
  # @endif
  # bool isAllowedConsumerType(const SDOPackage::ServiceProfile& sProfile);
  def isAllowedConsumerType(self, sProfile):
    if self._allConsumerAllowed:
      return True

    for i in range(len(self._consumerTypes)):
      if self._consumerTypes[i] == str(sProfile.interface_type):
        self._rtcout.RTC_DEBUG("%s is supported SDO service.", str(sProfile.interface_type))
        return True
    self._rtcout.RTC_WARN("Consumer type is not supported: %s", str(sProfile.interface_type))
    return False


  ##
  # @if jp
  # @brief ¸�ߤ��륵���ӥ������ɤ���Ĵ�٤�
  # 
  # @else
  # @brief If it is existing service type
  # @endif
  # bool isExistingConsumerType(const SDOPackage::ServiceProfile& sProfile);
  def isExistingConsumerType(self, sProfile):
    factory = OpenRTM_aist.SdoServiceConsumerFactory.instance()
    consumerTypes = factory.getIdentifiers()
    for i in range(len(consumerTypes)):
      if consumerTypes[i] == str(sProfile.interface_type):
        self._rtcout.RTC_DEBUG("%s exists in the SDO service factory.", str(sProfile.interface_type))
        self._rtcout.RTC_PARANOID("Available SDO serices in the factory: %s", str(OpenRTM_aist.flatten(consumerTypes)))
        return True
    self._rtcout.RTC_WARN("No available SDO service in the factory: %s",
                          str(sProfile.interface_type))
    return False


  # const std::string getUUID() const;
  def getUUID(self):
    return str(OpenRTM_aist.uuid1())
