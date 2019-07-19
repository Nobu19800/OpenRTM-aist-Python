#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file SdoServiceConsumerBase.py
# @brief SDO service consumer base class and its factory
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM_aist


##
# @if jp
#
# SdoServiceConsumerFactory&
#                     factory(SdoServiceConsumerFactory.instance());
#
# factory.addFactory(toRepositoryId<IDL Type>(),
#                   Creator< SdoServiceConsumerBase,
#                            your_sdo_service_consumer_subclass>,
#                   Destructor< SdoServiceConsumerBase,
#                            your_sdo_service_consumer_subclass>);
#
# @else
#
#
#
# @endif
class SdoServiceConsumerBase:
  """
  """

  def __init__(self):
    pass

  def __del__(self):
    pass

  ##
  # @if jp
  # @brief ���󥷥塼�ޥ��饹�ν�����ؿ�
  #
  # ������ؿ���Ϳ����줿 RTObject ����� ServiceProfile ���顢����
  # ���֥������Ȥ��������ޤ������Υ����ӥ���
  # ''sdo.service.provider.enabled_services'' ��ͭ��������Ƥ���С�
  # ���δؿ����б�����RTC�����󥹥��󥹲����줿ľ��˸ƤӽФ���ޤ���
  #
  # ServiceProfile �ˤϰʲ��ξ������ä����֤ǸƤӽФ���ޤ���
  #
  # - ServiceProfile.id: ���������ӥ���IFR��
  # - ServiceProfile.interface_type: ���������ӥ���IFR��
  # - ServiceProfile.service: ���������ӥ��Υ��֥������Ȼ���
  # - ServiceProfile.properties: rtc.conf �� <component>.conf ����Ϳ
  #                   ����줿SDO�����ӥ���ͭ�Υ��ץ�����Ϥ���롣
  #                   conf�ե��������
  #                   �ϡ�''<pragma>.<module_name>.<interface_name>''
  #                   �Ȥ����ץ�ե��å�����Ĥ������ץ����Ȥ���Ϳ
  #                   ���뤳�Ȥ��Ǥ���properties ��ˤϡ����Υץ�
  #                   �ե��å�������������ץ����key:value������
  #                   �ޤޤ�Ƥ��롣
  #
  # �ؿ���Ǥϡ���� properties �����������Ƥ��ɤ߹��ߥ����ӥ���ͭ��
  # ��������Ԥ��ޤ���Ϳ����줿 ServiceProfile�����Ƥ����������뤤
  # �Ϥ���¾����ͳ�����������ӥ��򥤥󥹥��󥹲����ʤ����� false
  # ���֤��ޤ������ξ�硢finalize() ���ƤӽФ��줽�θ奪�֥�������
  # �Ϻ������ޤ�������ʳ��ξ��� true ���֤��ȡ������ӥ����֥���
  # ���Ȥ� RTC ����ݻ�����ޤ���
  #
  # @param rtobj ���Υ��֥������Ȥ����󥹥��󥹲����줿 RTC
  # @param profile ��������Ϳ����줿 SDO ServiceProfile
  # @return Ϳ����줿 SDO Service �� ServiceProfile �������ξ�� false
  #
  # @else
  # @brief Initialization function of the consumer class
  #
  # @endif
  #
  # virtual bool init(RTObject_impl& rtobj,
  #                   const SDOPackage::ServiceProfile& profile) = 0;
  def init(self, rtobj, profile):
    pass

  ##
  # @if jp
  # @brief ���󥷥塼�ޥ��饹�κƽ�����ؿ�
  #
  # ���Υ��֥������Ȥκƽ������Ԥ���ServiceProfile �ˤ� id �ե���
  # ��ɤ˥��å�����ͭ�� UUID �����åȤ���Ƥ��뤬��Ʊ��� id �ξ�
  # �硢properties �����ꤵ�줿���������ѹ��䡢service �ե������
  # �Υ����ӥ��λ��Ȥ��ѹ����Ԥ��롣���κݤ˸ƤФ��Τ�����
  # reinit() �ؿ��Ǥ��롣�����Ǥϡ�service �ե�����ɤΥ��֥�������
  # ��ե���󥹤�Ʊ�������ǧ�����ۤʤäƤ������ݻ����Ƥ����ե�
  # ��󥹤򹹿�����ɬ�פ����롣�ޤ� properties �ˤϿ��������꤬Ϳ��
  # ���Ƥ����ǽ��������Τǡ����Ƥ��ɤ߹�������򹹿����롣
  #
  # @param profile ������Ϳ����줿 SDO ServiceProfile
  # @return ������ ServiceProfile ��Ϳ����줿���� false
  #
  # @else
  # @brief Reinitialization function of the consumer class
  #
  # @endif
  #
  # virtual bool reinit(const SDOPackage::ServiceProfile& profile) = 0;
  def reinit(self, profile):
    pass

  ##
  # @if jp
  # @brief ServiceProfile ���֤�
  #
  # init()/reinit()��Ϳ����줿 ServiceProfile ���̾索�֥���������
  # ���ݻ�����롣SDO Service �����ե졼�����ϴ����夳�Υ��֥���
  # ���Ȥ��б����� ServiceProfile ��ɬ�פȤ���Τǡ����δؿ��Ǥ��ݻ�
  # ����Ƥ��� ServiceProfile ���֤���
  # 
  # @return ���Υ��֥������Ȥ��ݻ����Ƥ��� ServiceProfile
  #
  # @else
  # @brief Getting ServiceProfile
  # @endif
  #
  # virtual const SDOPackage::ServiceProfile& getProfile() const = 0;
  def getProfile(self):
    pass
  
  ##
  # @if jp
  # @brief ��λ����
  #
  # SDO�����ӥ����ǥ��å������ݤ˸ƤӽФ���뽪λ�����Ѵؿ�������
  # �ӥ��Τǥ��å��˺ݤ��ơ��������֥������Ȥ��ݻ�����꥽���������
  # ����ʤɤν�����Ԥ���
  #
  # @else
  # @brief Finalization
  #
  # @endif
  #
  # virtual void finalize() = 0;
  def finalize(self):
    pass

sdoserviceconsumerfactory = None

class SdoServiceConsumerFactory(OpenRTM_aist.Factory,SdoServiceConsumerBase):
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    return

  def __del__(self):
    pass

  def instance():
    global sdoserviceconsumerfactory

    if sdoserviceconsumerfactory is None:
      sdoserviceconsumerfactory = SdoServiceConsumerFactory()

    return sdoserviceconsumerfactory

  instance = staticmethod(instance)
