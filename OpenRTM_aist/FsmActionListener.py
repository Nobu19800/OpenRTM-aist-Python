#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file FsmActionListener.py
# @brief FSM Action listener class
# @date $Date$
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Nobuhiko Miyamoto
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import OpenRTM_aist
import threading
import OpenRTM_aist.Guard

##
# @if jp
# @brief
#
# FSM����ݡ��ͥ�Ȥ˴ؤ����ο����񤤤�եå����뤿��Υꥹ����
# �����ꥹ�ʤˤ��礭��ʬ����ȡ�
#
# - FSM���Τ�Τ�ư���եå����뤿��Υꥹ��
# - FSM�˴ؤ���᥿�ǡ����ѹ�����ư���եå����뤿��Υꥹ��
#
# ��2�����ʬ�����롣��������Ԥϡ�FSM�ξ����������Υ�����������
# �夽�줾���եå����뤿��� PreFsmActionListener ��
# PostFsmActionListener ����Ĥ����ꡢ��Ԥϡ�FSM��Profile���ѹ���ե�
# ������ FsmProfileListener �� FSM�ι�¤ (Structure) ���ѹ���եå�
# ���� FsmStructureListener ����Ĥ�ʬ�����롣�ʾ塢�ʲ���FSM�˴�
# ����ʲ���4����Υꥹ�ʡ����饹�����󶡤���Ƥ��롣
#
# - PreFsmActionListener
# - PostFsmActionListener
# - FsmProfileListner
# - FsmStructureListener
#
#
# @else
#
#
# @endif
#

##
# @if jp
# @brief PreFsmActionListener �Υ�����
#
# PreFsmActionListener �ˤϰʲ��Υեå��ݥ���Ȥ��������Ƥ��롣��
# ��餬�ƤӽФ���뤫�ɤ����ϡ�FSM�μ����˰�¸���롣
#
# - PRE_ON_INIT:          init ľ��
# - PRE_ON_ENTRY:         entry ľ��
# - PRE_ON_DO:            do ľ��
# - PRE_ON_EXIT:          exit ľ��
# - PRE_ON_STATE_CHANGE:  ��������ľ��
#
# @else
# @brief The types of ConnectorDataListener
#
# PreFsmActionListener has the following hook points. If these
# listeners are actually called or not called are depends on FSM
# implementations.
#
# - PRE_ON_INIT:          just before "init" action
# - PRE_ON_ENTRY:         just before "entry" action
# - PRE_ON_DO:            just before "do" action
# - PRE_ON_EXIT:          just before "exit" action
# - PRE_ON_STATE_CHANGE:  just before state transition action
#
# @endif
#
class PreFsmActionListenerType:
  """
  """

  def __init__(self):
    pass
  PRE_ON_INIT = 0
  PRE_ON_ENTRY = 1
  PRE_ON_DO = 2
  PRE_ON_EXIT = 3
  PRE_ON_STATE_CHANGE = 4
  PRE_FSM_ACTION_LISTENER_NUM = 5


##
# @if jp
# @class PreFsmActionListener ���饹
# @brief PreFsmActionListener ���饹
#
# PreFsmActionListener ���饹�ϡ�Fsm�Υ��������˴ؤ��륳����Хå�
# ��¸�����ꥹ�ʡ����֥������Ȥδ��쥯�饹�Ǥ��롣FSM�Υ��������
# ��ľ����ư���եå���������硢�ʲ�����Τ褦�ˡ����Υ��饹��Ѿ�
# ����������Хå����֥������Ȥ��������Ŭ�ڤʥ�����Хå�����ؿ���
# ��RTObject���Ф��ƥ�����Хå����֥������Ȥ򥻥åȤ���ɬ�פ����롣
#
# <pre>
# class MyListener
#   : public PreFsmActionListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#
#   virtual void operator()(const char* state_name)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#     std::cout << "Current state: " state_name << std::endl;
#   };
# };
# </pre>
#
# ���Τ褦�ˤ���������줿�ꥹ�ʥ��饹�ϡ��ʲ��Τ褦��RTObject���Ф�
# �ơ����åȤ���롣
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addPreFsmActionListener(PRE_ON_STATE_CHANGE,
#                             new MyListener("init listener"),
#                             true);
#    :
# </pre>
#
# ��1������ "PRE_ON_STATE_CHANGE" �ϡ�������Хå���եå�����ݥ���
# �ȤǤ��ꡢ�ʲ����ͤ��뤳�Ȥ���ǽ�Ǥ��롣�ʤ������٤ƤΥ�����Х�
# ���ݥ���Ȥ���������Ƥ���Ȥϸ¤餺������餬�ƤӽФ���뤫�ɤ���
# �ϡ�FSM�μ����˰�¸���롣
#
# - PRE_ON_INIT:          init ľ��
# - PRE_ON_ENTRY:         entry ľ��
# - PRE_ON_DO:            do ľ��
# - PRE_ON_EXIT:          exit ľ��
# - PRE_ON_STATE_CHANGE:  ��������ľ��
#
# ��2�����ϥꥹ�ʥ��֥������ȤΥݥ��󥿤Ǥ��롣��3�����ϥ��֥�������
# ��ư����ե饰�Ǥ��ꡢtrue �ξ��ϡ�RTObject������˼�ưŪ�˥ꥹ
# �ʥ��֥������Ȥ��������롣false�ξ��ϡ����֥������Ȥν�ͭ����
# �ƤӽФ�¦�˻Ĥꡢ����ϸƤӽФ�¦����Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
# RTObject �Υ饤�ե���������˥�����Хå���ɬ�פʤ�о嵭�Τ褦��
# �ƤӽФ�������3������ true �Ȥ��Ƥ����Ȥ褤���դˡ�������Хå���
# �������˱����ƥ��åȤ����ꥢ�󥻥åȤ����ꤹ��ɬ�פ��������
# false�Ȥ����֤����ꥹ�ʥ��֥������ȤΥݥ��󥿤�����ѿ��ʤɤ���
# �����Ƥ�����
# RTObject_impl::addPreFsmActionListener()/removePreFsmActionListener()
# �ˤ�ꡢ���åȤȥ��󥻥åȤ��������Ȥ��ä��Ȥ������ǽ�Ǥ��롣
#
# @else
# @class PreFsmActionListener class
# @brief PreFsmActionListener class
#
# PreFsmActionListener class is a base class for the listener
# objects which realize callback to hook FSM related pre-actions.
# To hook execution just before a FSM action, the callback object
# should be defined as follows, and set to RTObject through
# appropriate callback set function.
#
# <pre>
# class MyListener
#   : public PreFsmActionListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#
#   virtual void operator()(const char* state_name)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#     std::cout << "Current state: " state_name << std::endl;
#   };
# };
# </pre>
#
# The listener class defined above is set to RTObject as follows.
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addPreFsmActionListener(PRE_ON_STATE_CHANGE,
#                             new MyListener("init listener"),
#                             true);
#    :
# </pre>
#
# The first argument "PRE_ON_STATE_CHANGE" specifies callback hook
# point, and the following values are available. Not all the
# callback points are implemented. It depends on the FSM
# implementations.
#
# - PRE_ON_INIT:          just before "init" action
# - PRE_ON_ENTRY:         just before "entry" action
# - PRE_ON_DO:            just before "do" action
# - PRE_ON_EXIT:          just before "exit" action
# - PRE_ON_STATE_CHANGE:  just before state transition action
#
# The second argument is a pointers to the listener object. The
# third argument is a flag for automatic object destruction. When
# "true" is given to the third argument, the given object in second
# argument is automatically destructed with RTObject. In the "false
# " case, the ownership of the object is left in the caller side,
# and then destruction of the object must be done by users'
# responsibility.
#
# It is good for setting "true" as third argument, if the listener
# object life span is equals to the RTObject's life cycle.  On the
# otehr hand, if callbacks are required to set/unset depending on
# its situation, the third argument could be "false".  In that
# case, listener objects pointers must be stored to member
# variables, and set/unset of the listener objects shoud be
# paerformed throguh
# RTObject_impl::addPreFsmActionListener()/removePreFsmActionListener()
# functions.
#
# @endif
#
class PreFsmActionListener:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    pass


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    pass


  ##
  # @if jp
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # PreFsmActionListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PreFsmActionListener.
  #
  # @endif
  # virtual void operator()(const char*) = 0;
  def __call__(self, state):
    pass

  ##
  # @if jp
  #
  # @brief PreFsmActionListenerType ��ʸ������Ѵ�
  #
  # PreFsmActionListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PreFsmActionListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PreFsmActionListenerType into the string.
  #
  # Convert PreFsmActionListenerType into the string.
  #
  # @param type The target PreFsmActionListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #
  def toString(type):
    typeString = ["PRE_ON_INIT",
                  "PRE_ON_ENTRY",
                  "PRE_ON_DO",
                  "PRE_ON_EXIT",
                  "PRE_ON_STATE_CHANGE",
                  "PRE_FSM_ACTION_LISTENER_NUM"]
    if type < PreFsmActionListenerType.PRE_FSM_ACTION_LISTENER_NUM:
      return typeString[type]

    return ""
  toString = staticmethod(toString)
    


##
# @if jp
# @brief PreFsmActionListener �Υ�����
#
# PreFsmActionListener �ˤϰʲ��Υեå��ݥ���Ȥ��������Ƥ��롣��
# ��餬�ƤӽФ���뤫�ɤ����ϡ�FSM�μ����˰�¸���롣
#
# - POST_ON_INIT:          init ľ��
# - POST_ON_ENTRY:         entry ľ��
# - POST_ON_DO:            do ľ��
# - POST_ON_EXIT:          exit ľ��
# - POST_ON_STATE_CHANGE:  ��������ľ��
#
# @else
# @brief The types of ConnectorDataListener
#
# PreFsmActionListener has the following hook points. If these
# listeners are actually called or not called are depends on FSM
# implementations.
#
# - POST_ON_INIT:          just after "init" action
# - POST_ON_ENTRY:         just after "entry" action
# - POST_ON_DO:            just after "do" action
# - POST_ON_EXIT:          just after "exit" action
# - POST_ON_STATE_CHANGE:  just after state transition action
#
# @endif
#
class PostFsmActionListenerType:
  """
  """

  def __init__(self):
    pass
  POST_ON_INIT = 0
  POST_ON_ENTRY = 1
  POST_ON_DO = 2
  POST_ON_EXIT = 3
  POST_ON_STATE_CHANGE = 4
  POST_FSM_ACTION_LISTENER_NUM = 5




##
# @if jp
# @class PostFsmActionListener ���饹
# @brief PostFsmActionListener ���饹
#
# PostFsmActionListener ���饹�ϡ�Fsm�Υ��������˴ؤ��륳����Хå�
# ��¸�����ꥹ�ʡ����֥������Ȥδ��쥯�饹�Ǥ��롣FSM�Υ��������
# ��ľ���ư���եå���������硢�ʲ�����Τ褦�ˡ����Υ��饹��Ѿ�
# ����������Хå����֥������Ȥ��������Ŭ�ڤʥ�����Хå�����ؿ���
# ��RTObject���Ф��ƥ�����Хå����֥������Ȥ򥻥åȤ���ɬ�פ����롣
#
# <pre>
# class MyListener
#   : public PostFsmActionListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#
#   virtual void operator()(const char* state_name, ReturnCode_t ret)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#     std::cout << "Current state: " state_name << std::endl;
#   };
# };
# </pre>
#
# ���Τ褦�ˤ���������줿�ꥹ�ʥ��饹�ϡ��ʲ��Τ褦��RTObject���Ф�
# �ơ����åȤ���롣
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addPostFsmActionListener(POST_ON_STATE_CHANGE,
#                             new MyListener("init listener"),
#                             true);
#    :
# </pre>
#
# ��1������ "POST_ON_STATE_CHANGE" �ϡ�������Хå���եå�����ݥ���
# �ȤǤ��ꡢ�ʲ����ͤ��뤳�Ȥ���ǽ�Ǥ��롣�ʤ������٤ƤΥ�����Х�
# ���ݥ���Ȥ���������Ƥ���Ȥϸ¤餺������餬�ƤӽФ���뤫�ɤ���
# �ϡ�FSM�μ����˰�¸���롣
#
# - POST_ON_INIT:          init ľ��
# - POST_ON_ENTRY:         entry ľ��
# - POST_ON_DO:            do ľ��
# - POST_ON_EXIT:          exit ľ��
# - POST_ON_STATE_CHANGE:  ��������ľ��
#
# ��2�����ϥꥹ�ʥ��֥������ȤΥݥ��󥿤Ǥ��롣��3�����ϥ��֥�������
# ��ư����ե饰�Ǥ��ꡢtrue �ξ��ϡ�RTObject������˼�ưŪ�˥ꥹ
# �ʥ��֥������Ȥ��������롣false�ξ��ϡ����֥������Ȥν�ͭ����
# �ƤӽФ�¦�˻Ĥꡢ����ϸƤӽФ�¦����Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
# RTObject �Υ饤�ե���������˥�����Хå���ɬ�פʤ�о嵭�Τ褦��
# �ƤӽФ�������3������ true �Ȥ��Ƥ����Ȥ褤���դˡ�������Хå���
# �������˱����ƥ��åȤ����ꥢ�󥻥åȤ����ꤹ��ɬ�פ��������
# false�Ȥ����֤����ꥹ�ʥ��֥������ȤΥݥ��󥿤�����ѿ��ʤɤ���
# �����Ƥ�����
# RTObject_impl::addPostFsmActionListener()/removePostFsmActionListener()
# �ˤ�ꡢ���åȤȥ��󥻥åȤ��������Ȥ��ä��Ȥ������ǽ�Ǥ��롣
#
# @else
# @class PostFsmActionListener class
# @brief PostFsmActionListener class
#
# PostFsmActionListener class is a base class for the listener
# objects which realize callback to hook FSM related post-actions.
# To hook execution just before a FSM action, the callback object
# should be defined as follows, and set to RTObject through
# appropriate callback set function.
#
# <pre>
# class MyListener
#   : public PostFsmActionListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#
#   virtual void operator()(const char* state_name, ReturnCode\t ret)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#     std::cout << "Current state: " state_name << std::endl;
#   };
# };
# </pre>
#
# The listener class defined above is set to RTObject as follows.
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addPostFsmActionListener(POST_ON_STATE_CHANGE,
#                             new MyListener("init listener"),
#                             true);
#    :
# </pre>
#
# The first argument "POST_ON_STATE_CHANGE" specifies callback hook
# point, and the following values are available. Not all the
# callback points are implemented. It depends on the FSM
# implementations.
#
# - POST_ON_INIT:          just after "init" action
# - POST_ON_ENTRY:         just after "entry" action
# - POST_ON_DO:            just after "do" action
# - POST_ON_EXIT:          just after "exit" action
# - POST_ON_STATE_CHANGE:  just after state transition action
#
# The second argument is a pointers to the listener object. The
# third argument is a flag for automatic object destruction. When
# "true" is given to the third argument, the given object in second
# argument is automatically destructed with RTObject. In the "false
# " case, the ownership of the object is left in the caller side,
# and then destruction of the object must be done by users'
# responsibility.
#
# It is good for setting "true" as third argument, if the listener
# object life span is equals to the RTObject's life cycle.  On the
# otehr hand, if callbacks are required to set/unset depending on
# its situation, the third argument could be "false".  In that
# case, listener objects pointers must be stored to member
# variables, and set/unset of the listener objects shoud be
# paerformed throguh
# RTObject_impl::addPostFsmActionListener()/removePostFsmActionListener()
# functions.
#
# @endif
#
class PostFsmActionListener:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    pass


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    pass


  ##
  # @if jp
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # PostFsmActionListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PostFsmActionListener.
  #
  # @endif
  # virtual void operator()(const char* state, ReturnCode_t ret) = 0;
  def __call__(self, state, ret):
    pass

  ##
  # @if jp
  #
  # @brief PostFsmActionListenerType ��ʸ������Ѵ�
  #
  # PostFsmActionListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PostFsmActionListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PostFsmActionListenerType into the string.
  #
  # Convert PostFsmActionListenerType into the string.
  #
  # @param type The target PostFsmActionListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #
  def toString(type):
    typeString = ["POST_ON_INIT",
                  "POST_ON_ENTRY",
                  "POST_ON_DO",
                  "POST_ON_EXIT",
                  "POST_ON_STATE_CHANGE",
                  "POST_FSM_ACTION_LISTENER_NUM"]
    if type < PostFsmActionListenerType.POST_FSM_ACTION_LISTENER_NUM:
      return typeString[type]

    return ""
  toString = staticmethod(toString)



##
# @if jp
# @brief FsmProfileListener �Υ�����
#
# - SET_FSM_PROFILE       : FSM Profile�����
# - GET_FSM_PROFILE       : FSM Profile������
# - ADD_FSM_STATE         : FSM��State���ɲä��줿
# - REMOVE_FSM_STATE      : FSM����State��������줿
# - ADD_FSM_TRANSITION    : FSM�����ܤ��ɲä��줿
# - REMOVE_FSM_TRANSITION : FSM�������ܤ�������줿
# - BIND_FSM_EVENT        : FSM�˥��٥�Ȥ��Х���ɤ��줿
# - UNBIND_FSM_EVENT      : FSM�˥��٥�Ȥ�����Х���ɤ��줿
#
# @else
# @brief The types of FsmProfileListener
#
# - SET_FSM_PROFILE       : Setting FSM Profile
# - GET_FSM_PROFILE       : Getting FSM Profile
# - ADD_FSM_STATE         : A State added to the FSM
# - REMOVE_FSM_STATE      : A State removed from FSM
# - ADD_FSM_TRANSITION    : A transition added to the FSM
# - REMOVE_FSM_TRANSITION : A transition removed from FSM
# - BIND_FSM_EVENT        : An event bounded to the FSM
# - UNBIND_FSM_EVENT      : An event unbounded to the FSM
#
# @endif
#
class FsmProfileListenerType:
  """
  """

  def __init__(self):
    pass
  SET_FSM_PROFILE = 0
  GET_FSM_PROFILE = 1
  ADD_FSM_STATE = 2
  REMOVE_FSM_STATE = 3
  ADD_FSM_TRANSITION = 4
  REMOVE_FSM_TRANSITION = 5
  BIND_FSM_EVENT = 6
  UNBIND_FSM_EVENT = 7
  FSM_PROFILE_LISTENER_NUM = 8



##
# @if jp
# @class FsmProfileListener ���饹
# @brief FsmProfileListener ���饹
#
# FsmProfileListener ���饹�ϡ�FSM��Profile�˴�Ϣ�������������Υ���
# ��Хå���¸�����ꥹ�ʡ����֥������Ȥδ��쥯�饹�Ǥ��롣FSM
# Profile�Υ���������ư���եå���������硢�ʲ�����Τ褦�ˡ���
# �Υ��饹��Ѿ�����������Хå����֥������Ȥ��������Ŭ�ڤʥ�����Х�
# ������ؿ�����RTObject���Ф��ƥ�����Хå����֥������Ȥ򥻥åȤ���
# ɬ�פ����롣
#
# <pre>
# class MyListener
#   : public FsmProfileListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#
#   virtual void operator()(const ::RTC::FsmProfile& fsmprof)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#   };
# };
# </pre>
#
# ���Τ褦�ˤ���������줿�ꥹ�ʥ��饹�ϡ��ʲ��Τ褦��RTObject���Ф�
# �ơ����åȤ���롣
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addFsmProfileListener(SET_FSM_PROFILE,
#                           new MyListener("prof listener"),
#                           true);
#    :
# </pre>
#
# ��1������ "SET_FSM_PROFILE" �ϡ�������Хå���եå�����ݥ���
# �ȤǤ��ꡢ�ʲ����ͤ��뤳�Ȥ���ǽ�Ǥ��롣�ʤ������٤ƤΥ�����Х�
# ���ݥ���Ȥ���������Ƥ���Ȥϸ¤餺������餬�ƤӽФ���뤫�ɤ���
# �ϡ�FSM�����ӥ��μ����˰�¸���롣
#
# - SET_FSM_PROFILE       : FSM Profile�����
# - GET_FSM_PROFILE       : FSM Profile������
# - ADD_FSM_STATE         : FSM��State���ɲä��줿
# - REMOVE_FSM_STATE      : FSM����State��������줿
# - ADD_FSM_TRANSITION    : FSM�����ܤ��ɲä��줿
# - REMOVE_FSM_TRANSITION : FSM�������ܤ�������줿
# - BIND_FSM_EVENT        : FSM�˥��٥�Ȥ��Х���ɤ��줿
# - UNBIND_FSM_EVENT      : FSM�˥��٥�Ȥ�����Х���ɤ��줿
#
# ��2�����ϥꥹ�ʥ��֥������ȤΥݥ��󥿤Ǥ��롣��3�����ϥ��֥�������
# ��ư����ե饰�Ǥ��ꡢtrue �ξ��ϡ�RTObject������˼�ưŪ�˥ꥹ
# �ʥ��֥������Ȥ��������롣false�ξ��ϡ����֥������Ȥν�ͭ����
# �ƤӽФ�¦�˻Ĥꡢ����ϸƤӽФ�¦����Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
# RTObject �Υ饤�ե���������˥�����Хå���ɬ�פʤ�о嵭�Τ褦��
# �ƤӽФ�������3������ true �Ȥ��Ƥ����Ȥ褤���դˡ�������Хå���
# �������˱����ƥ��åȤ����ꥢ�󥻥åȤ����ꤹ��ɬ�פ��������
# false�Ȥ����֤����ꥹ�ʥ��֥������ȤΥݥ��󥿤�����ѿ��ʤɤ���
# �����Ƥ�����addFsmProfileListener()/removeFsmProfileListener() ��
# ��ꡢ���åȤȥ��󥻥åȤ��������Ȥ��ä��Ȥ������ǽ�Ǥ��롣
#
# @else
# @class FsmProfileListener class
# @brief FsmProfileListener class
#
# FsmProfileListener class is a base class for the listener
# objects which realize callback to hook FSM Profile related actions.
# To hook execution just before a FSM profile action, the callback object
# should be defined as follows, and set to RTObject through
# appropriate callback set function.
#
# <pre>
# class MyListener
#   : public FsmProfileListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#
#   virtual void operator()(const ::RTC::FsmProfile& fsmprof)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#   };
# };
# </pre>
#
# The listener class defined above is set to RTObject as follows.
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addFsmProfileListener(SET_FSM_PROFILE,
#                           new MyListener("prof listener"),
#                           true);
#    :
# </pre>
#
# The first argument "SET_FSM_PROFILE" specifies callback hook
# point, and the following values are available. Not all the
# callback points are implemented. It depends on the FSM service
# implementations.
#
# - SET_FSM_PROFILE       : Setting FSM Profile
# - GET_FSM_PROFILE       : Getting FSM Profile
# - ADD_FSM_STATE         : A State added to the FSM
# - REMOVE_FSM_STATE      : A State removed from FSM
# - ADD_FSM_TRANSITION    : A transition added to the FSM
# - REMOVE_FSM_TRANSITION : A transition removed from FSM
# - BIND_FSM_EVENT        : An event bounded to the FSM
# - UNBIND_FSM_EVENT      : An event unbounded to the FSM
#
# The second argument is a pointers to the listener object. The
# third argument is a flag for automatic object destruction. When
# "true" is given to the third argument, the given object in second
# argument is automatically destructed with RTObject. In the "false
# " case, the ownership of the object is left in the caller side,
# and then destruction of the object must be done by users'
# responsibility.
#
# It is good for setting "true" as third argument, if the listener
# object life span is equals to the RTObject's life cycle.  On the
# otehr hand, if callbacks are required to set/unset depending on
# its situation, the third argument could be "false".  In that
# case, listener objects pointers must be stored to member
# variables, and set/unset of the listener objects shoud be
# paerformed throguh
# addFsmProfileListener()/removeFsmProfileListener() functions.
#
# @endif
#
class FsmProfileListener:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    pass

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    pass


  ##
  # @if jp
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # FsmProfileListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for FsmProfileListener.
  #
  # @endif
  # virtual void operator()(const ::RTC::FsmProfile& fsmprof) = 0;
  def __call__(self, fsmprof):
    pass

  ##
  # @if jp
  #
  # @brief FsmProfileListenerType ��ʸ������Ѵ�
  #
  # FsmProfileListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� FsmProfileListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert FsmProfileListenerType into the string.
  #
  # Convert FsmProfileListenerType into the string.
  #
  # @param type The target FsmProfileListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #
  def toString(type):
    typeString = ["SET_FSM_PROFILE",
                  "GET_FSM_PROFILE",
                  "ADD_FSM_STATE",
                  "REMOVE_FSM_STATE",
                  "ADD_FSM_TRANSITION",
                  "REMOVE_FSM_TRANSITION",
                  "BIND_FSM_EVENT",
                  "UNBIND_FSM_EVENT",
                  "PRE_FSM_ACTION_LISTENER_NUM"]
    if type < FsmProfileListenerType.FSM_PROFILE_LISTENER_NUM:
      return typeString[type]

    return ""
  toString = staticmethod(toString)



##
# @if jp
# @brief FsmStructureListener �Υ�����
#
# - SET_FSM_STRUCTURE: FSM��¤������
# - GET_FSM_STRUCTURE: FSM��¤�μ���
#
# @else
# @brief The types of FsmStructureListener
#
# - SET_FSM_STRUCTURE: Setting FSM structure
# - GET_FSM_STRUCTURE: Getting FSM structure
#
# @endif
#
class FsmStructureListenerType:
  """
  """
  
  def __init__(self):
    pass
  SET_FSM_STRUCTURE = 0
  GET_FSM_STRUCTURE = 1
  FSM_STRUCTURE_LISTENER_NUM = 2


##
# @if jp
# @class FsmStructureListener ���饹
# @brief FsmStructureListener ���饹
#
# FsmStructureListener ���饹�ϡ�FSM Structure�Υ��������˴ؤ��륳��
# ��Хå���¸�����ꥹ�ʡ����֥������Ȥδ��쥯�饹�Ǥ��롣FSM
# Structure �Υ���������ľ���ư���եå���������硢�ʲ�����Τ�
# ���ˡ����Υ��饹��Ѿ�����������Хå����֥������Ȥ��������Ŭ�ڤ�
# ������Хå�����ؿ�����RTObject���Ф��ƥ�����Хå����֥������Ȥ�
# ���åȤ���ɬ�פ����롣
#
# <pre>
# class MyListener
#   : public FsmStructureListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#   virtual void operator()(::RTC::FsmStructure& pprof)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#   };
# };
# </pre>
#
# ���Τ褦�ˤ���������줿�ꥹ�ʥ��饹�ϡ��ʲ��Τ褦��RTObject���Ф�
# �ơ����åȤ���롣
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addFsmStructureListener(SET_FSM_STRUCTURE,
#                             new MyListener("set structure listener"),
#                             true);
#    :
# </pre>
#
# ��1������ "SET_FSM_STRUCTURE" �ϡ�������Хå���եå�����ݥ���
# �ȤǤ��ꡢ�ʲ����ͤ��뤳�Ȥ���ǽ�Ǥ��롣�ʤ������٤ƤΥ�����Х�
# ���ݥ���Ȥ���������Ƥ���Ȥϸ¤餺������餬�ƤӽФ���뤫�ɤ���
# �ϡ�FSM�μ����˰�¸���롣
#
# - SET_FSM_STRUCTURE: FSM��¤������
# - GET_FSM_STRUCTURE: FSM��¤�μ���
#
# ��2�����ϥꥹ�ʥ��֥������ȤΥݥ��󥿤Ǥ��롣��3�����ϥ��֥�������
# ��ư����ե饰�Ǥ��ꡢtrue �ξ��ϡ�RTObject������˼�ưŪ�˥ꥹ
# �ʥ��֥������Ȥ��������롣false�ξ��ϡ����֥������Ȥν�ͭ����
# �ƤӽФ�¦�˻Ĥꡢ����ϸƤӽФ�¦����Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
# RTObject �Υ饤�ե���������˥�����Хå���ɬ�פʤ�о嵭�Τ褦��
# �ƤӽФ�������3������ true �Ȥ��Ƥ����Ȥ褤���դˡ�������Хå���
# �������˱����ƥ��åȤ����ꥢ�󥻥åȤ����ꤹ��ɬ�פ��������
# false�Ȥ����֤����ꥹ�ʥ��֥������ȤΥݥ��󥿤�����ѿ��ʤɤ���
# �����Ƥ�����
# RTObject_impl::addPostFsmActionListener()/removePostFsmActionListener()
# �ˤ�ꡢ���åȤȥ��󥻥åȤ��������Ȥ��ä��Ȥ������ǽ�Ǥ��롣
#
# @else
# @class FsmStructureListener class
# @brief FsmStructureListener class
#
# PostFsmActionListener class is a base class for the listener
# objects which realize callback to hook FSM structure profile
# related actions. To hook execution just before a FSM action, the
# callback object should be defined as follows, and set to RTObject
# through appropriate callback set function.
#
# <pre>
# class MyListener
#   : public FsmStructureListener
# {
#   std::string m_name;
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#   virtual void operator()(::RTC::FsmStructure& pprof)
#   {
#     std::cout << "Listner name:  " m_name << std::endl;
#   };
# };
# </pre>
#
# The listener class defined above is set to RTObject as follows.
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     addFsmStructureListener(SET_FSM_STRUCTURE,
#                             new MyListener("set structure listener"),
#                             true);
#    :
# </pre>
#
# The first argument "SET_FSM_STRUCTURE" specifies callback hook
# point, and the following values are available. Not all the
# callback points are implemented. It depends on the FSM
# implementations.
#
# - SET_FSM_STRUCTURE: Setting FSM structure
# - GET_FSM_STRUCTURE: Getting FSM structure
#
# The second argument is a pointers to the listener object. The
# third argument is a flag for automatic object destruction. When
# "true" is given to the third argument, the given object in second
# argument is automatically destructed with RTObject. In the "false
# " case, the ownership of the object is left in the caller side,
# and then destruction of the object must be done by users'
# responsibility.
#
# It is good for setting "true" as third argument, if the listener
# object life span is equals to the RTObject's life cycle.  On the
# otehr hand, if callbacks are required to set/unset depending on
# its situation, the third argument could be "false".  In that
# case, listener objects pointers must be stored to member
# variables, and set/unset of the listener objects shoud be
# paerformed throguh
# RTObject_impl::addPostFsmActionListener()/removePostFsmActionListener()
# functions.
#
# @endif
#
class FsmStructureListener:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    pass


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    pass


  ##
  # @if jp
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # FsmStructureListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for FsmStructureListener.
  #
  # @endif
  # virtual void operator()(const ::RTC::FsmStructure& fsmprof) = 0;
  def __call__(self, pprof):
    pass

  ##
  # @if jp
  #
  # @brief FsmStructureListenerType ��ʸ������Ѵ�
  #
  # FsmStructureListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� FsmStructureListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert FsmStructureListenerType into the string.
  #
  # Convert FsmStructureListenerType into the string.
  #
  # @param type The target FsmStructureListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #
  def toString(type):
    typeString = ["SET_FSM_STRUCTURE",
                  "GET_FSM_STRUCTURE",
                  "FSM_STRUCTURE_LISTENER_NUM"]
    if type < FsmStructureListenerType.FSM_STRUCTURE_LISTENER_NUM:
      return typeString[type]

    return ""
  toString = staticmethod(toString)


class Entry:
  def __init__(self,listener, autoclean):
    self.listener  = listener
    self.autoclean = autoclean
    return
  

##
# @if jp
# @class PreFsmActionListenerHolder
# @brief PreFsmActionListener �ۥ�����饹
#
# ʣ���� PreFsmActionListener ���ݻ����������륯�饹��
#
# @else
# @class PreFsmActionListenerHolder
# @brief PreFsmActionListener holder class
#
# This class manages one ore more instances of
# PreFsmActionListener class.
#
# @endif
#
class PreFsmActionListenerHolder:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    self._listeners = []
    self._mutex = threading.RLock()
  
  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None



  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  #
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    self._listeners.append(Entry(listener, autoclean))

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  #
  def removeListener(self, listener):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @endif
  #
  def notify(self, state):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for listener in self._listeners:
      listener.listener(state)
    return





##
# @if jp
# @class PostFsmActionListenerHolder
# @brief PostFsmActionListener �ۥ�����饹
#
# ʣ���� PostFsmActionListener ���ݻ����������륯�饹��
#
# @else
# @class PostFsmActionListenerHolder
# @brief PostFsmActionListener holder class
#
# This class manages one ore more instances of
# PostFsmActionListener class.
#
# @endif
#
class PostFsmActionListenerHolder:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    self._listeners = []
    self._mutex = threading.RLock()
  
  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None



  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  #
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    self._listeners.append(Entry(listener, autoclean))

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  #
  def removeListener(self, listener):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @endif
  #
  def notify(self, state, ret):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for listener in self._listeners:
      listener.listener(state, ret)
    return


##
# @if jp
# @class FsmProfileListenerHolder
# @brief FsmProfileListener �ۥ�����饹
#
# ʣ���� FsmProfileListener ���ݻ����������륯�饹��
#
# @else
# @class FsmProfileListenerHolder
# @brief FsmProfileListener holder class
#
# This class manages one ore more instances of
# FsmProfileListener class.
#
# @endif
#
class FsmProfileListenerHolder:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    self._listeners = []
    self._mutex = threading.RLock()
  
  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None



  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  #
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    self._listeners.append(Entry(listener, autoclean))

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  #
  def removeListener(self, listener):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @endif
  #
  def notify(self, state):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for listener in self._listeners:
      listener.listener(state)
    return

##
# @if jp
# @class FsmStructureListenerHolder
# @brief FsmStructureListener �ۥ�����饹
#
# ʣ���� FsmStructureListener ���ݻ����������륯�饹��
#
# @else
# @class FsmStructureListenerHolder
# @brief FsmStructureListener holder class
#
# This class manages one ore more instances of
# FsmStructureListener class.
#
# @endif
#
class FsmStructureListenerHolder:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #
  def __init__(self):
    self._listeners = []
    self._mutex = threading.RLock()
  
  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None



  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  #
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    self._listeners.append(Entry(listener, autoclean))

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  #
  def removeListener(self, listener):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @endif
  #
  def notify(self, state):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for listener in self._listeners:
      listener.listener(state)
    return




##
# @if jp
# @class FsmActionListeners
# @brief FsmActionListeners ���饹
#
#
# @else
# @class FsmActionListeners
# @brief FsmActionListeners class
#
#
# @endif
class FsmActionListeners:
  def __init__(self):

    ##
    # @if jp
    # @brief PreFsmActionListenerType
    # PreFsmActionListenerType�ꥹ�ʤ��Ǽ
    # @else
    # @brief PreFsmActionListenerType listener array
    # The PreFsmActionListenerType listener is stored. 
    # @endif
    self.preaction_num = PreFsmActionListenerType.PRE_FSM_ACTION_LISTENER_NUM
    self.preaction_ = [PreFsmActionListenerHolder() 
                for i in range(self.preaction_num)]

    ##
    # @if jp
    # @brief PostFsmActionType�ꥹ������
    # PostFsmActionType�ꥹ�ʤ��Ǽ
    # @else
    # @brief PostFsmActionType listener array
    # The PostFsmActionType listener is stored.
    # @endif
    self.postaction_num = PostFsmActionListenerType.POST_FSM_ACTION_LISTENER_NUM
    self.postaction_ = [PostFsmActionListenerHolder()
                 for i in range(self.postaction_num)]

    ##
    # @if jp
    # @brief FsmProfileType
    # FsmProfileType�ꥹ�ʤ��Ǽ
    # @else
    # @brief FsmProfileType listener array
    # The FsmProfileType listener is stored.
    # @endif
    self.profile_num = FsmProfileListenerType.FSM_PROFILE_LISTENER_NUM
    self.profile_ = [FsmProfileListenerHolder()
                 for i in range(self.profile_num)]
  
    ##
    # @if jp
    # @brief FsmStructureType�ꥹ������
    # FsmStructureType�ꥹ�ʤ��Ǽ
    # @else
    # @brief FsmStructureTypelistener array
    # The FsmStructureType listener is stored.
    # @endif
    self.structure_num = FsmStructureListenerType.FSM_STRUCTURE_LISTENER_NUM
    self.structure_ = [FsmStructureListenerHolder()
               for i in range(self.structure_num)]

