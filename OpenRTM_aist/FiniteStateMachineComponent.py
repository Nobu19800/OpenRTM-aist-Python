#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file FiniteStateMachineComponentBase.py
# @brief Finite StateMachine Component Base class
# @date  $Date: 2017-06-09 07:49:59 $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Nobuhiko Miyamoto
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.




import OpenRTM_aist
import OpenRTM, OpenRTM__POA





##
# @if jp
# @brief 
# FiniteStateMachine�Υ١������饹��
# �桼����������RT����ݡ��ͥ�Ȥ����������ϡ����Υ��饹���ĥ���롣
# ��RT����ݡ��ͥ�ȤΥ١����Ȥʤ륯�饹��}
#
#
# @else
# @brief 
# This is a class to be a base of each RT-Component.
# This is a implementation class of lightweightRTComponent in Robotic
# Technology Component specification
#
# @endif
class FiniteStateMachineComponent_impl(OpenRTM_aist.RTObject_impl, OpenRTM__POA.FiniteStateMachineComponent):
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @brief Consructor
  #
  #
  # @endif
  def __init__(self, manager=None, orb=None, poa=None):
    OpenRTM_aist.RTObject_impl.__init__(self, manager, orb, poa)



  ##
  # @if jp
  #
  # @brief 
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief 
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_action(self, ec_id):
    self._rtcout.RTC_TRACE("on_action(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      #self.preOnAction(ec_id)
      ret = self.onAction(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    #self.postOnAction(ec_id, ret)
    return ret
