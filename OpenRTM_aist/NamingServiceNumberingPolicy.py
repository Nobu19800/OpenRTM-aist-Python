#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file NamingServiceNumberingPolicy.py
# @brief Object numbering policy class
# @date $Date: 2016/02/25$
# @author Nobuhiko Miyamoto
#

import string
import OpenRTM_aist
import CosNaming






##
# @if jp
#
# @class NamingServiceNumberingPolicy
# @brief ���֥��������������͡��ߥ󥰡��ݥꥷ��(̿̾��§)�����ѥ��饹
#���͡��ߥ󥰥����ӥ�����RTC�򸡺����ƥʥ�Х�󥰤�Ԥ�
#
#
# @else
#
# @endif
class NamingServiceNumberingPolicy(OpenRTM_aist.NumberingPolicy):
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
    self._num = 0
    self._objects = []
    self._mgr = OpenRTM_aist.Manager.instance()


  ##
  # @if jp
  #
  # @brief ���֥���������������̾�κ���
  #
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
  # @brief RTC�θ���
  #
  # �͡��ߥ󥰥����ӥ�����RTC�򥤥󥹥���̾���鸡������
  # ���פ���RTC���������True���֤�
  # 
  # @param self
  # @param context ���߸�����Υ���ƥ�����
  # @param name RTC�Υ��󥹥���̾
  #
  # @return Ƚ��
  #
  # @else
  #
  # @endif
  def find_RTC_by_Name(self, context, name):
    length = 500
    bl,bi = context.list(length)
    for i in bl:
      if i.binding_type == CosNaming.ncontext:
        next_context = context.resolve(i.binding_name)
        if self.find_RTC_by_Name(next_context, name):
          return True
      elif i.binding_type == CosNaming.nobject:
        if i.binding_name[0].id == name and i.binding_name[0].kind == "rtc":
          return True
    return False
        
    

  ##
  # @if jp
  #
  # @brief ���֥������Ȥθ���
  #
  # ����̾�Υ��󥹥���̾��RTC�򸡺�����
  # ���פ���RTC��¸�ߤ������True���֤�
  # 
  # @param self
  # @param name RTC�Υ��󥹥���̾
  #
  # @return Ƚ��
  #
  # @else
  #
  # @endif
  def find(self, name):
    ns = self._mgr._namingManager._names
    for n in ns:
      noc = n.ns
      if noc is None:
        continue
      cns = noc._cosnaming
      if cns is None:
        continue
      root_cxt = cns.getRootContext()
      return self.find_RTC_by_Name(root_cxt, name)



def NamingServiceNumberingPolicyInit():
  OpenRTM_aist.NumberingPolicyFactory.instance().addFactory("ns_unique",
                                                      OpenRTM_aist.NamingServiceNumberingPolicy,
                                                      OpenRTM_aist.Delete)
