#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# \file DataFlowComponentBase.py
# \brief DataFlowParticipant RT-Component base class
# \date $Date: 2007/09/04$
# \author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import OpenRTM__POA
import RTC


##
# @if jp
# @class DataFlowComponentBase
# @brief DataFlowComponentBase ���饹
#
# �ǡ����ե���RTComponent�δ��쥯�饹��
# �Ƽ�ǡ����ե���RTComponent�����������ϡ��ܥ��饹��Ѿ�������Ǽ���
# ���롣
#
# @since 0.4.0
#
# @else
# @class DataFlowComponentBase
# @brief DataFlowComponentBase class
# @endif
class DataFlowComponentBase(OpenRTM_aist.RTObject_impl, OpenRTM__POA.DataFlowComponent):
  """
  """


  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param manager �ޥ͡����㥪�֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, manager=None, orb=None, poa=None):
    OpenRTM_aist.RTObject_impl.__init__(self, manager, orb, poa)
    self._objref = self._this()


  ##
  # @if jp
  # @brief �����(���֥��饹������)
  #
  # �ǡ����ե��� RTComponent �ν������¹Ԥ��롣
  # �ºݤν���������ϡ��ƶ�ݥ��饹��˵��Ҥ��롣
  #
  # @param self
  #
  # @else
  # @brief Initialization
  # @endif
  def init(self):
    pass


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] RTC ��������(������)
  #
  # �ʲ��ξ��֤��ݻ�����Ƥ�����ˡ����ꤵ�줿���������Ū�˸ƤӽФ���롣
  # - RTC �� Alive ���֤Ǥ��롣
  # - ���ꤵ�줿 ExecutionContext �� Running ���֤Ǥ��롣
  # �ܥ��ڥ졼�����ϡ�Two-Pass Execution ���������Ǽ¹Ԥ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onExecute() ������Хå��ؿ����Ƥ�
  # �Ф���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Primary Periodic 
  #        Operation of RTC
  #
  # This operation will be invoked periodically at the rate of the given
  # execution context as long as the following conditions hold:
  # - The RTC is Active.
  # - The given execution context is Running
  # This callback occurs during the first execution pass.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_execute(self, ec_id):
    self._rtcout.RTC_TRACE("on_execute(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnExecute(ec_id)
      if self._readAll:
        self.readAll()
      
      ret = self.onExecute(ec_id)

      if self._writeAll:
        self.writeAll()
      
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnExecute(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] RTC ��������(�������)
  #
  # �ʲ��ξ��֤��ݻ�����Ƥ�����ˡ����ꤵ�줿���������Ū�˸ƤӽФ���롣
  # - RTC �� Alive ���֤Ǥ��롣
  # - ���ꤵ�줿 ExecutionContext �� Running ���֤Ǥ��롣
  # �ܥ��ڥ졼�����ϡ�Two-Pass Execution ����������Ǽ¹Ԥ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onStateUpdate() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Secondary Periodic 
  #        Operation of RTC
  #
  # This operation will be invoked periodically at the rate of the given
  # execution context as long as the following conditions hold:
  # - The RTC is Active.
  # - The given execution context is Running
  # This callback occurs during the second execution pass.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_state_update(self, ec_id):
    self._rtcout.RTC_TRACE("on_state_update(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnStateUpdate(ec_id)
      ret = self.onStateUpdate(ec_id)
      self._configsets.update()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnStateUpdate(ec_id, ret)
    return ret




  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] �¹Լ����ѹ�����
  #
  # �ܥ��ڥ졼�����ϡ�ExecutionContext �μ¹Լ������ѹ����줿���Ȥ����Τ���
  # �ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onRateChanged() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Notify rate chenged
  #
  # This operation is a notification that the rate of the indicated execution 
  # context has changed.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_rate_changed(self, ec_id):
    self._rtcout.RTC_TRACE("on_rate_changed(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnRateChanged(ec_id)
      ret = self.onRateChanged(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnRateChanged(ec_id, ret)
    return ret

