#!/usr/bin/env python
# -*- coding: euc-jp -*-

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
import RTC


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
class FiniteStateMachineComponentBase(OpenRTM_aist.RTObject_impl):
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
  def __init__(self, manager):
    OpenRTM_aist.RTObject_impl.__init__(self, manager)
    self._rtcout = self._manager.getLogbuf("FiniteStateMachineComponentBase")
    self._ref = None

  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC����������
  #
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��ơ�ComponentAction::on_initialize
  # ������Хå��ؿ����ƤФ�롣
  # 
  # ����
  # - RTC �� Created���֤ξ��߽�������Ԥ��롣¾�ξ��֤ˤ�����ˤ�
  #   ReturnCode_t::PRECONDITION_NOT_MET ���֤���ƤӽФ��ϼ��Ԥ��롣
  # - ���Υ��ڥ졼������ RTC �Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
  #   ���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
  #   ����Ƥ��ʤ���
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Initialize the RTC that realizes this interface.
  #
  # The invocation of this operation shall result in the invocation of the
  # callback ComponentAction::on_initialize.
  #
  # Constraints
  # - An RTC may be initialized only while it is in the Created state. Any
  #   attempt to invoke this operation while in another state shall fail
  #   with ReturnCode_t::PRECONDITION_NOT_MET.
  # - Application developers are not expected to call this operation
  #   directly; it exists for use by the RTC infrastructure.
  #
  # @return
  # 
  # @endif
  def initialize(self):
    return OpenRTM_aist.RTObject_impl.initialize(self)



  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC ��λ����
  #
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� ComponentAction::on_finalize()
  # ��ƤӽФ���
  #
  # ����
  # - RTC �� ExecutionContext �˽�°���Ƥ���֤Ͻ�λ����ʤ������ξ��ϡ�
  #   �ޤ��ǽ�� ExecutionContextOperations::remove_component �ˤ�äƻ��ä�
  #   ������ʤ���Фʤ�ʤ�������ʳ��ξ��ϡ����Υ��ڥ졼�����ƤӽФ���
  #   �����ʤ���� ReturnCode_t::PRECONDITION_NOT_ME �Ǽ��Ԥ��롣
  # - RTC �� Created ���֤Ǥ����硢��λ�����ϹԤ��ʤ���
  #   ���ξ�硢���Υ��ڥ졼�����ƤӽФ��Ϥ����ʤ����
  #   ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
  # - ���Υ��ڥ졼������RTC�Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
  #   ���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
  #   ����Ƥ��ʤ���
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Finalize the RTC for preparing it for destruction
  # 
  # This invocation of this operation shall result in the invocation of the
  # callback ComponentAction::on_finalize.
  #
  # Constraints
  # - An RTC may not be finalized while it is participating in any execution
  #   context. It must first be removed with 
  #   ExecutionContextOperations::remove_component. Otherwise, this operation
  #   shall fail with ReturnCode_t::PRECONDITION_NOT_MET. 
  # - An RTC may not be finalized while it is in the Created state. Any 
  #   attempt to invoke this operation while in that state shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  # - Application developers are not expected to call this operation directly;
  #  it exists for use by the RTC infrastructure.
  #
  # @return
  # 
  # @endif
  def finalize(self):
    return OpenRTM_aist.RTObject_impl.finalize(self)



  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC �������ʡ��Ǥ��� ExecutionContext ��
  #        ��ߤ��������Υ���ƥ�Ĥȶ��˽�λ������
  #
  # ���� RTC �������ʡ��Ǥ��뤹�٤Ƥμ¹ԥ���ƥ����Ȥ���ߤ��롣
  # ���� RTC ��¾�μ¹ԥ���ƥ����Ȥ��ͭ���� RTC ��°����¹ԥ���ƥ�����
  # (i.e. �¹ԥ���ƥ����Ȥ��ͭ���� RTC �Ϥ��ʤ�����μ¹ԥ���ƥ����Ȥ�
  # �����ʡ��Ǥ��롣)�˻��ä��Ƥ����硢���� RTC �Ϥ����Υ���ƥ����Ⱦ�
  # �������������ʤ���Фʤ�ʤ���
  # RTC ���¹���Τɤ� ExecutionContext �Ǥ� Active ���֤ǤϤʤ��ʤä��塢
  # ���� RTC �Ȥ���˴ޤޤ�� RTC ����λ���롣
  # 
  # ����
  # - RTC �����������Ƥ��ʤ���С���λ�����뤳�ȤϤǤ��ʤ���
  #   Created ���֤ˤ��� RTC �� exit() ��ƤӽФ�����硢
  #   ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Stop the RTC's execution context(s) and finalize it along with its
  #        contents.
  # 
  # Any execution contexts for which the RTC is the owner shall be stopped. 
  # If the RTC participates in any execution contexts belonging to another
  # RTC that contains it, directly or indirectly (i.e. the containing RTC
  # is the owner of the ExecutionContext), it shall be deactivated in those
  # contexts.
  # After the RTC is no longer Active in any Running execution context, it
  # and any RTCs contained transitively within it shall be finalized.
  #
  # Constraints
  # - An RTC cannot be exited if it has not yet been initialized. Any
  #   attempt to exit an RTC that is in the Created state shall fail with
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  #
  # @return
  # 
  # @endif
  def exit(self):
    return OpenRTM_aist.RTObject_impl.exit(self)



  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC �� Alive ���֤Ǥ��뤫�ɤ�����ǧ���롣
  #
  # RTC �����ꤷ�� ExecutionContext ���Ф��� Alive���֤Ǥ��뤫�ɤ�����ǧ���롣
  # RTC �ξ��֤� Active �Ǥ��뤫��Inactive �Ǥ��뤫��Error �Ǥ��뤫�ϼ¹����
  # ExecutionContext �˰�¸���롣���ʤ�������� ExecutionContext ���Ф��Ƥ�
  # Active  ���֤Ǥ��äƤ⡢¾�� ExecutionContext ���Ф��Ƥ� Inactive ���֤�
  # �ʤ���⤢�ꤨ�롣���äơ����Υ��ڥ졼�����ϻ��ꤵ�줿
  # ExecutionContext ���䤤��碌�ơ����� RTC �ξ��֤� Active��Inactive��
  # Error �ξ��ˤ� Alive ���֤Ȥ����֤���
  #
  # @param self
  #
  # @param exec_context �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return Alive ���ֳ�ǧ���
  #
  # @else
  #
  # @brief Confirm whether RTC is an Alive state or NOT.
  #
  # A component is alive or not regardless of the execution context from
  # which it is observed. However, whether or not it is Active, Inactive,
  # or in Error is dependent on the execution context(s) in which it is
  # running. That is, it may be Active in one context but Inactive in
  # another. Therefore, this operation shall report whether this RTC is
  # either Active, Inactive or in Error; which of those states a component
  # is in with respect to a particular context may be queried from the
  # context itself.
  #
  # @return Result of Alive state confirmation
  #
  # @endif
  # virtual CORBA::Boolean is_alive(ExecutionContext_ptr exec_context)
  def is_alive(self, exec_context):
    return OpenRTM_aist.RTObject_impl.is_alive(self, exec_context)




  ##
  # @if jp
  # @brief [CORBA interface] ��ͭ���� ExecutionContextList�� ��������
  #
  # ���� RTC ����ͭ���� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContextList.
  #
  # This operation returns a list of all execution contexts owned by this
  # RTC.
  #
  # @return ExecutionContext List
  #
  # @endif
  # virtual ExecutionContextList* get_owned_contexts()
  def get_owned_contexts(self):
    return OpenRTM_aist.RTObject_impl.get_owned_contexts(self)


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext���������
  #
  # ���ꤷ���ϥ�ɥ�� ExecutionContext ��������롣
  # �ϥ�ɥ뤫�� ExecutionContext �ؤΥޥåԥ󥰤ϡ������ RTC ���󥹥��󥹤�
  # ��ͭ�Ǥ��롣�ϥ�ɥ�Ϥ��� RTC �� attach_context �����ݤ˼����Ǥ��롣
  #
  # @param self
  # @param ec_id �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return ExecutionContext
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContext.
  #
  # Obtain a reference to the execution context represented by the given 
  # handle.
  # The mapping from handle to context is specific to a particular RTC 
  # instance. The given handle must have been obtained by a previous call to 
  # attach_context on this RTC.
  #
  # @param ec_id ExecutionContext handle
  #
  # @return ExecutionContext
  #
  # @endif
  # virtual ExecutionContext_ptr get_context(UniqueId exec_handle)
  def get_owned_contexts(self):
    return OpenRTM_aist.RTObject_impl.get_owned_contexts(self)



  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext���������
  #
  # ���ꤷ���ϥ�ɥ�� ExecutionContext ��������롣
  # �ϥ�ɥ뤫�� ExecutionContext �ؤΥޥåԥ󥰤ϡ������ RTC ���󥹥��󥹤�
  # ��ͭ�Ǥ��롣�ϥ�ɥ�Ϥ��� RTC �� attach_context �����ݤ˼����Ǥ��롣
  #
  # @param self
  # @param ec_id �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return ExecutionContext
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContext.
  #
  # Obtain a reference to the execution context represented by the given 
  # handle.
  # The mapping from handle to context is specific to a particular RTC 
  # instance. The given handle must have been obtained by a previous call to 
  # attach_context on this RTC.
  #
  # @param ec_id ExecutionContext handle
  #
  # @return ExecutionContext
  #
  # @endif
  # virtual ExecutionContext_ptr get_context(UniqueId exec_handle)
  def get_context(self, ec_id):
    return OpenRTM_aist.RTObject_impl.get_context(self, ec_id)




  ##
  # @if jp
  # @brief [CORBA interface] ���ä��Ƥ��� ExecutionContextList ���������
  #
  # ���� RTC �����ä��Ƥ��� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get participating ExecutionContextList.
  #
  # This operation returns a list of all execution contexts in
  # which this RTC participates.
  #
  # @return ExecutionContext List
  #
  # @endif
  # virtual ExecutionContextList* get_participating_contexts()
  def get_participating_contexts(self):
    return OpenRTM_aist.RTObject_impl.get_participating_contexts(self)



  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext �Υϥ�ɥ���֤�
  #
  # @param ExecutionContext �¹ԥ���ƥ�����
  #
  # @return ExecutionContextHandle
  #
  # Ϳ����줿�¹ԥ���ƥ����Ȥ˴�Ϣ�դ���줿�ϥ�ɥ���֤���
  #
  # @else
  # @brief [CORBA interface] Return a handle of a ExecutionContext
  #
  # @param ExecutionContext
  #
  # @return ExecutionContextHandle
  #
  # This operation returns a handle that is associated with the given
  # execution context.
  #
  # @endif
  #
  # virtual ExecutionContextHandle_t
  #   get_context_handle(ExecutionContext_ptr cxt)
  def get_context_handle(self, cxt):
    return OpenRTM_aist.RTObject_impl.get_context_handle(self, cxt)



  ##
  # @if jp
  #
  # @brief [RTObject CORBA interface] ����ݡ��ͥ�ȥץ�ե�������������
  #
  # ��������ݡ��ͥ�ȤΥץ�ե����������֤��� 
  #
  # @param self
  #
  # @return ����ݡ��ͥ�ȥץ�ե�����
  #
  # @else
  #
  # @brief [RTObject CORBA interface] Get RTC's profile
  #
  # This operation returns the ComponentProfile of the RTC
  #
  # @return ComponentProfile
  #
  # @endif
  # virtual ComponentProfile* get_component_profile()
  def get_component_profile(self):
    return OpenRTM_aist.RTObject_impl.get_component_profile(self)




  ##
  # @if jp
  #
  # @brief [RTObject CORBA interface] �ݡ��Ȥ��������
  #
  # ��������ݡ��ͥ�Ȥ���ͭ����ݡ��Ȥλ��Ȥ��֤���
  #
  # @param self
  #
  # @return �ݡ��ȥꥹ��
  #
  # @else
  #
  # @brief [RTObject CORBA interface] Get Ports
  #
  # This operation returns a list of the RTCs ports.
  #
  # @return PortList
  #
  # @endif
  # virtual PortServiceList* get_ports()
  def get_ports(self):
    return OpenRTM_aist.RTObject_impl.get_ports(self)



  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext��attach����
  #
  # ���ꤷ�� ExecutionContext �ˤ��� RTC ���°�����롣���� RTC �ȴ�Ϣ���� 
  # ExecutionContext �Υϥ�ɥ���֤���
  # ���Υ��ڥ졼�����ϡ�ExecutionContextOperations::add_component ���ƤФ줿
  # �ݤ˸ƤӽФ���롣�֤��줿�ϥ�ɥ��¾�Υ��饤����Ȥǻ��Ѥ��뤳�Ȥ�����
  # ���Ƥ��ʤ���
  #
  # @param self
  # @param exec_context ��°�� ExecutionContext
  #
  # @return ExecutionContext �ϥ�ɥ�
  #
  # @else
  # @brief [CORBA interface] Attach ExecutionContext.
  #
  # Inform this RTC that it is participating in the given execution context. 
  # Return a handle that represents the association of this RTC with the 
  # context.
  # This operation is intended to be invoked by 
  # ExecutionContextOperations::add_component. It is not intended for use by 
  # other clients.
  #
  # @param exec_context Prticipating ExecutionContext
  #
  # @return ExecutionContext Handle
  #
  # @endif
  # UniqueId attach_context(ExecutionContext_ptr exec_context)
  def attach_context(self, exec_context):
    return OpenRTM_aist.RTObject_impl.attach_context(self, exec_context)




  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext��detach����
  #
  # ���ꤷ�� ExecutionContext ���餳�� RTC �ν�°�������롣
  # ���Υ��ڥ졼�����ϡ�ExecutionContextOperations::remove_component ���Ƥ�
  # �줿�ݤ˸ƤӽФ���롣�֤��줿�ϥ�ɥ��¾�Υ��饤����Ȥǻ��Ѥ��뤳�Ȥ�
  # ���ꤷ�Ƥ��ʤ���
  # 
  # ����
  # - ���ꤵ�줿 ExecutionContext �� RTC �����Ǥ˽�°���Ƥ��ʤ����ˤϡ�
  #   ReturnCode_t::PRECONDITION_NOT_MET ���֤���롣
  # - ���ꤵ�줿 ExecutionContext �ˤ��������Ф��� RTC ��Active ���֤Ǥ����
  #   ��ˤϡ� ReturnCode_t::PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param ec_id ����о� ExecutionContext�ϥ�ɥ�
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  # @brief [CORBA interface] Attach ExecutionContext.
  #
  # Inform this RTC that it is no longer participating in the given execution 
  # context.
  # This operation is intended to be invoked by 
  # ExecutionContextOperations::remove_component. It is not intended for use 
  # by other clients.
  # Constraints
  # - This operation may not be invoked if this RTC is not already 
  #   participating in the execution context. Such a call shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  # - This operation may not be invoked if this RTC is Active in the indicated
  #   execution context. Otherwise, it shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  #
  # @param ec_id Dettaching ExecutionContext Handle
  #
  # @return
  #
  # @endif
  # ReturnCode_t detach_context(UniqueId exec_handle)
  def detach_context(self, ec_id):
    return OpenRTM_aist.RTObject_impl.detach_context(self, ec_id)




  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �ν����
  #
  # RTC ����������졢Alive ���֤����ܤ��롣
  # RTC ��ͭ�ν���������Ϥ����Ǽ¹Ԥ��롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onInitialize() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Initialize RTC
  #
  # The RTC has been initialized and entered the Alive state.
  # Any RTC-specific initialization logic should be performed here.
  #
  # @return
  #
  # @endif
  def on_initialize(self):
    return OpenRTM_aist.RTObject_impl.on_initialize(self)




  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �ν�λ
  #
  # RTC ���˴�����롣
  # RTC ��ͭ�ν�λ�����Ϥ����Ǽ¹Ԥ��롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onFinalize() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Finalize RTC
  #
  # The RTC is being destroyed.
  # Any final RTC-specific tear-down logic should be performed here.
  #
  # @return
  #
  # @endif
  def on_finalize(self):
    return OpenRTM_aist.RTObject_impl.on_finalize(self)





  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �γ���
  #
  # RTC ����°���� ExecutionContext �� Stopped ���֤��� Running ���֤�����
  # �������˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onStartup() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] StartUp RTC
  #
  # The given execution context, in which the RTC is participating, has 
  # transitioned from Stopped to Running.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_startup(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_startup(self, ec_id)



  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �����
  #
  # RTC ����°���� ExecutionContext �� Running ���֤��� Stopped ���֤�����
  # �������˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onShutdown() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] ShutDown RTC
  #
  # The given execution context, in which the RTC is participating, has 
  # transitioned from Running to Stopped.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_shutdown(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_shutdown(self, ec_id)




  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �γ�����
  #
  # ��°���� ExecutionContext ���� RTC �����������줿�ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onActivated() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id ������ ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Activate RTC
  #
  # The RTC has been activated in the given execution context.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_activated(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_activated(self, ec_id)





  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC ���������
  #
  # ��°���� ExecutionContext ���� RTC ������������줿�ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onDeactivated() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id ������� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Deactivate RTC
  #
  # The RTC has been deactivated in the given execution context.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_deactivated(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_deactivated(self, ec_id)




  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υ��顼����
  #
  # RTC �����顼���֤ˤ���ݤ˸ƤӽФ���롣
  # RTC �����顼���֤ξ��ˡ��оݤȤʤ� ExecutionContext ��ExecutionKind ��
  # �����������ߥ󥰤ǸƤӽФ���롣�㤨�С�
  # - ExecutionKind �� PERIODIC �ξ�硢�ܥ��ڥ졼������
  #   DataFlowComponentAction::on_execute �� on_state_update ���ؤ��ˡ�
  #   ���ꤵ�줿���֡����ꤵ�줿�����ǸƤӽФ���롣
  # - ExecutionKind �� EVENT_DRIVEN �ξ�硢�ܥ��ڥ졼������
  #   FsmParticipantAction::on_action ���ƤФ줿�ݤˡ��ؤ��˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onError() ������Хå��ؿ����Ƥӽ�
  # ����롣
  #
  # @param self
  # @param ec_id �о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Error Processing of RTC
  #
  # The RTC remains in the Error state.
  # If the RTC is in the Error state relative to some execution context when
  # it would otherwise be invoked from that context (according to the 
  # context��s ExecutionKind), this callback shall be invoked instead. 
  # For example,
  # - If the ExecutionKind is PERIODIC, this operation shall be invoked in 
  #   sorted order at the rate of the context instead of 
  #   DataFlowComponentAction::on_execute and on_state_update.
  # - If the ExecutionKind is EVENT_DRIVEN, this operation shall be invoked 
  #   whenever FsmParticipantAction::on_action would otherwise have been 
  #   invoked.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_error(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_error(self, ec_id)




  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υ��顼���֤ؤ�����
  #
  # RTC ����°���� ExecutionContext �� Active ���֤��� Error ���֤����ܤ���
  # ���˸ƤӽФ���롣
  # ���Υ��ڥ졼������ RTC �� Error ���֤����ܤ����ݤ˰��٤����ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onAborting() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Transition Error State
  #
  # The RTC is transitioning from the Active state to the Error state in some
  # execution context.
  # This callback is invoked only a single time for time that the RTC 
  # transitions into the Error state from another state. This behavior is in 
  # contrast to that of on_error.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_aborting(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_aborting(self, ec_id)





  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υꥻ�å�
  #
  # Error ���֤ˤ��� RTC �Υꥫ�Х������¹Ԥ���Inactive ���֤�����������
  # ���˸ƤӽФ���롣
  # RTC �Υꥫ�Х������������������ Inactive ���֤��������뤬������ʳ���
  # ���ˤ� Error ���֤�α�ޤ롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onReset() ������Хå��ؿ����Ƥ�
  # �Ф���롣
  #
  # @param self
  # @param ec_id �ꥻ�å��о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Resetting RTC
  #
  # The RTC is in the Error state. An attempt is being made to recover it such
  # that it can return to the Inactive state.
  # If the RTC was successfully recovered and can safely return to the
  # Inactive state, this method shall complete with ReturnCode_t::OK. Any
  # other result shall indicate that the RTC should remain in the Error state.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_reset(self, ec_id):
    return OpenRTM_aist.RTObject_impl.on_reset(self, ec_id)




  ##
  # @if jp
  # @brief 
  #
  # 
  #
  # @param self
  #
  # @else
  #
  # @brief Consructor
  #
  #
  # @endif
  def on_action(self, ec_id):
    return RTC.RTC_OK