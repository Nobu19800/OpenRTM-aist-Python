#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file NodeNumberingPolicy.py
# @brief Object numbering policy class
# @date $Date: 2016/02/25$
# @author Nobuhiko Miyamoto
#

import string
import OpenRTM_aist





##
# @if jp
#
# @class NodeNumberingPolicy
# @brief ���֥��������������͡��ߥ󥰡��ݥꥷ��(̿̾��§)�����ѥ��饹
# �ޥ������ޥ͡����㡢���졼�֥ޥ͡����㤫��RTC�򸡺����ƥʥ�Х�󥰤�Ԥ�
#
# 
#
# @since 0.4.0
#
# @else
#
# @endif
class NodeNumberingPolicy(OpenRTM_aist.NumberingPolicy):
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self
  # 
  # @else
  #
  # @brief virtual destractor
  #
  # @endif
  def __init__(self):
    self._mgr = OpenRTM_aist.Manager.instance()


  ##
  # @if jp
  #
  # @brief ���֥���������������̾�κ���
  #
  # 
  # @param self
  # @param obj ̾�������оݥ��֥�������
  #
  # @return �����������֥�������̾��
  #
  # @else
  #
  # @endif
  def onCreate(self, obj):
    num = 0
    while True:
      num_str = OpenRTM_aist.otos(num)
      
      name = obj.getTypeName() + num_str
      if not self.find(name):
        return num_str
      else:
        num += 1
        

  ##
  # @if jp
  #
  # @brief ���֥������Ⱥ������̾�β���
  #
  # 
  # @param self
  # @param obj ̾�β����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def onDelete(self, obj):
    pass

  
    
    

  ##
  # @if jp
  #
  # @brief ���֥������Ȥθ���
  #
  # �ޥ������ޥ͡����㡢����ӥ��졼�֥ޥ͡��������Ͽ���줿RTC�򸡺�����
  # ��������̾�������פ���RTC��¸�ߤ������True���֤�
  # ���Υץ����ǵ�ư�����ޥ͡����㤬�ޥ������ޥ͡�����ǤϤʤ���
  #   ����˥ޥ������ޥ͡����㤬1�Ĥ���Ͽ����Ƥ��ʤ����Ϥ��Υץ����Υޥ͡����㤫�鸡��
  # 
  # @param self
  # @param name �����оݥ��֥������Ȥ�̾��
  #
  # @return Ƚ��
  #
  # @else
  #
  # @endif
  def find(self, name):
    rtcs = []
    mgr_servant = self._mgr._mgrservant
    master_mgr = None
    if mgr_servant.is_master():
      master_mgr = mgr_servant.getObjRef()
    else:
      masters = mgr_servant.get_master_managers()
      if len(masters) > 0:
        master_mgr = masters[0]
      else:
        master_mgr = mgr_servant.getObjRef()
    
    rtcs = master_mgr.get_components_by_name(name)
    if len(rtcs) > 0:
      return True
    slaves = master_mgr.get_slave_managers()
    for ms in slaves:
      rtcs = ms.get_components_by_name(name)
      if len(rtcs) > 0:
        return True
    
    
    
    return False




def NodeNumberingPolicyInit():
  OpenRTM_aist.NumberingPolicyFactory.instance().addFactory("node_unique",
                                                      OpenRTM_aist.NodeNumberingPolicy,
                                                      OpenRTM_aist.Delete)
