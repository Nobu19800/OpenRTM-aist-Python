#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file ComponentObserverProvider.py
# @brief test for ComponentObserverConsumer
# @date $Date$
# @author Shinji Kurihara
#
# Copyright (C) 2011
#     Noriaki Ando
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys

from omniORB import CORBA, PortableServer
import RTC, RTC__POA
import OpenRTM, OpenRTM__POA
import SDOPackage
import OpenRTM_aist
import OpenRTM_aist.NVUtil

class ExtendedFsmServiceProvider(RTC__POA.ExtendedFsmService, OpenRTM_aist.SdoServiceProviderBase):
  def __init__(self):
    self._rtobj = None
    self._profile = None
    self._fsmState = ""
    structure = """
<scxml xmlns=\"http://www.w3.org/2005/07/scxml\
           version=\"1.0\"
           initial=\"airline-ticket\">
  <state id=\"state0\">
    <datamodel>
      <data id=\"data0\">
      </data>
    </datamodel>
    <transition event=\"toggle\" target=\"state1\" />
  </state>
  <state id=\"state1\">
    <datamodel>"
      <data id=\"data1\">
      </data>
    </datamodel>
    <transition event=\"toggle\" target=\"state0\" />
  </state>
</scxml>
    """
    event_profile = RTC.FsmEventProfile("toggle","TimedShort")
    nv = OpenRTM_aist.NVUtil.newNV("fsm_structure.format","scxml")
    self._fsmStructure = RTC.FsmStructure("dummy_name","",[event_profile],[nv])

  ##
  # @if jp
  # @brief �����
  # @else
  # @brief Initialization
  # @endif
  #
  def init(self, rtobj, profile):
    self._rtobj = rtobj
    self._profile = profile
    return True

  ##
  # @if jp
  # @brief �ƽ����
  # @else
  # @brief Re-initialization
  # @endif
  #
  def reinit(self, profile):
    self._profile = profile
    return True

  ##
  # @if jp
  # @brief ServiceProfile ���������
  # @else
  # @brief getting ServiceProfile
  # @endif
  #
  def getProfile(self):
    return self._profile

  ##
  # @if jp
  # @brief ��λ����
  # @else
  # @brief Finalization
  # @endif
  #
  def finalize(self):
    pass

  ##
  # @if jp
  # @brief FSM�θ��ߤξ��֤����
  #
  # ���Υ��ڥ졼������FSM����ݡ��ͥ�Ȥ�FSM�θ��ߤξ��֤��֤���
  # (FSM4RTC spec. p.20)
  #
  # @return ���ߤξ��֤�ɽ��ʸ����
  #
  # @else
  # @brief Get Current FSM State
  #
  # This operation returns the current state of an FSM in the
  # target FSM component. (FSM4RTC spec. p.20)
  #
  # @return A string which represent the current status
  #
  # @endif
  #
  def get_current_state(self):
    return self._fsmState

  ##
  # @if jp
  # @brief FSM�ι�¤�����ꤹ��
  #
  # ���Υ��ڥ졼�������оݤΥ���ݡ��ͥ�Ȥ��Ф��ơ�FSM�ι�¤����
  # ������ FsmStruccture �����ꤹ�롣�оݥ���ݡ��ͥ�Ȥ�
  # fsm_structure ��Ϳ����줿�ͤ��˾������ܥ롼������FSM��¤���
  # ���ꤹ�롣���Υ��ڥ졼�����̤�����ξ��ϡ�UNSUPPORTED ���֤���
  #
  # @param fsm_structure FSM�ι�¤��ɽ��FsmStructure��¤�Ρ�
  # @return RTC_OK ���ｪλ
  #         RTC_ERROR ����¾�Υ��顼
  #         BAD_PARAMETER �����ʥѥ�᡼��
  #         UNSUPPORTED ̤���ݡ���
  #
  # @else
  # @brief Set FSM Structure
  #
  # This operation sets an FsmStructure to the target
  # component. Then the target component reconfigures its FSM
  # structure such as transition rules according to the values of
  # the given fsm_structure. RTCs may return UNSUPPORTED if this
  # operation is not implemented.
  #
  # @param fsm_structure FsmStructure structure which represents
  #        FSM structure
  # @return RTC_OK normal return
  #         RTC_ERROR other error
  #         BAD_PARAMETER invalid parameter
  #         UNSUPPORTED unsupported or not implemented
  #
  # @endif
  #
  def set_fsm_structure(self, fsm_structure):
    self._fsmStructure = fsm_structure
    return RTC.RTC_OK
    

  ##
  # @if jp
  # @brief FSM�ι�¤���������
  #
  # ���Υ��ڥ졼�������оݤΥ���ݡ��ͥ�Ȥ��Ф��ơ������ݻ����Ƥ�
  # ��FSM�ι�¤��������롣ExtendedFsmService ��¤�Τϥե������
  # name (FSM��̾��), structure (FSM�ι�¤) ��EventProfile �ʤɤ���
  # ����structure �Υե����ޥåȤϡ��ե������ properties ��˳�Ǽ��
  # �줿���� "fsm_structure.format" �˻��ꤵ��롣���Υ��ڥ졼�����
  # ��̤�����ξ��ϡ�UNSUPPORTED ���֤���
  #
  # ref: SCXML https://www.w3.org/TR/scxml/
  #
  # @param fsm_structure FSM�ι�¤��ɽ��FsmStructure��¤�Ρ�
  # @return RTC_OK ���ｪλ
  #         RTC_ERROR ����¾�Υ��顼
  #         BAD_PARAMETER �����ʥѥ�᡼��
  #         UNSUPPORTED ̤���ݡ���
  #
  # @else
  # @brief Set FSM Structure
  #
  # This operation returns the structure of an FSM in the target
  # FSM component. ExtendedFsmService returns the name, structure
  # with format specified by fsm_structure.format and
  # EventProfiles. RTCs may return UNSUPPORTED if this operation is
  # not implemented.
  #
  # @param fsm_structure FsmStructure structure which represents
  #        FSM structure
  # @return RTC_OK normal return
  #         RTC_ERROR other error
  #         BAD_PARAMETER invalid parameter
  #         UNSUPPORTED unsupported or not implemented
  #
  # @endif
  #
  def get_fsm_structure(self):
    return (RTC.RTC_OK,self._fsmStructure)


  ##
  # @if jp
  # @brief RTObject�ؤΥꥹ����³����
  # @else
  # @brief Connectiong listeners to RTObject
  # @endif
  #
  def setListeners(self, prop):
    pass

  ##
  # @if jp
  # @brief FSM��������
  # @else
  # @brief FSM status change
  # @endif
  #
  def changeStatus(self, state):
    self._fsmState = state

  ##
  # @if jp
  # @brief �ϡ��ȥӡ��Ȥ�������
  # @else
  # @brief Unsetting heartbeat
  # @endif
  #
  def changeStructure(self, fsm_structure):
    self._fsmStructure.structure = fsm_structure

  ##
  # @if jp
  # @brief FSM�����Ѳ��ꥹ�ʤ��������
  # @else
  # @brief Setting FSM status listeners
  # @endif
  #
  def setFSMStatusListeners(self):
    pass

  ##
  # @if jp
  # @brief FSM�����Ѳ��ꥹ�ʤβ������
  # @else
  # @brief Unsetting FSM status listeners
  # @endif
  #
  def unsetFSMStatusListeners(self):
    pass

  ##
  # @if jp
  # @brief FsmProfile�����Ѳ��ꥹ�ʤ�����
  # @else
  # @brief Setting FsmProfile listener
  # @endif
  #
  def setFSMProfileListeners(self):
    pass

  ##
  # @if jp
  # @brief FsmProfile�����Ѳ��ꥹ�ʤβ��
  # @else
  # @brief Unsetting FsmProfile listener
  # @endif
  #
  def unsetFSMProfileListeners(self):
    pass

  ##
  # @if jp
  # @brief FsmStructure�����Ѳ��ꥹ�ʤ�����
  # @else
  # @brief Setting FsmStructure listener
  # @endif
  #
  def setFSMStructureListeners(self):
    pass

  ##
  # @if jp
  # @brief FsmStructure�����Ѳ��ꥹ�ʤβ��
  # @else
  # @brief Unsetting FsmStructure listener
  # @endif
  #
  def unsetFSMStructureListeners(self):
    pass
    
    
    

def ExtendedFsmServiceProviderInit(mgr=None):
  factory = OpenRTM_aist.SdoServiceProviderFactory.instance()
  factory.addFactory(RTC.ExtendedFsmService._NP_RepositoryId,
                     ExtendedFsmServiceProvider,
                     OpenRTM_aist.Delete)
  return
