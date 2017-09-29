#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file EventPort_pyfsm.py
# @brief EventInPort template class
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import OpenRTM_aist.StaticFSM_pyfsm
import pyfsm


class EventBinder0(OpenRTM_aist.ConnectorDataListener):
  def __init__(self, fsm, event_name, handler, ptask=False):
    self._fsm = fsm
    self._eventName = event_name
    self._handler = handler
    self._ptask = ptask
  def __del__(self):
    pass
  def __call__(self, info, data):
    if info.properties.getProperty("fsm_event_name") == self._eventName or info.name == self._eventName:
      if not self._ptask:
        self._fsm.dispatch(pyfsm.Event(self._handler))
      else:
        task = OpenRTM_aist.Async_tInvoker(self._fsm, pyfsm.Machine.dispatch, pyfsm.Event(self._handler))
        task.invoke()
      return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE
    return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE

    

class EventBinder1(OpenRTM_aist.ConnectorDataListenerT):
  def __init__(self, fsm, event_name, handler, data_type, ptask=False):
    self._fsm = fsm
    self._eventName = event_name
    self._handler = handler
    self._data_type = data_type
    self._ptask = ptask
  def __del__(self):
    pass
  def __call__(self, info, data):
    data_ = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, data, self._data_type)
    
    if info.properties.getProperty("fsm_event_name") == self._eventName or info.name == self._eventName:
      if not self._ptask:
        self._fsm.dispatch(pyfsm.Event(self._handler, data_))
      else:
        task = OpenRTM_aist.Async_tInvoker(self._fsm, pyfsm.Machine.dispatch, pyfsm.Event(self._handler, data_))
        task.invoke()
      return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE
    return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE






##
# @if jp
#
# @class EventInPort
#
# @brief EventInPort �ƥ�ץ졼�ȥ��饹
# 
# EventInPort �μ����Ǥ��� EventInPort<T> �Υƥ�ץ졼�ȥ��饹��
# <T> ��BasicDataType.idl �ˤ��������Ƥ��뷿�ǡ����ФȤ���
# Time ���� tm , ����� T���� data ����Ĺ�¤�ΤǤʤ��ƤϤʤ�ʤ���
# EventInPort �������˥�󥰥Хåե�����������������������줿�ǡ�����缡
# ���Υ�󥰥Хåե��˳�Ǽ���롣��󥰥Хåե��Υ������ϥǥե���Ȥ�64��
# �ʤäƤ��뤬�����󥹥ȥ饯�������ˤ�ꥵ��������ꤹ�뤳�Ȥ��Ǥ��롣
# �ǡ����ϥե饰�ˤ�ä�̤�ɡ����ɾ��֤��������졢isNew(), write(), read(),
# isFull(), isEmpty() ���Υ᥽�åɤˤ��ϥ�ɥ�󥰤��뤳�Ȥ��Ǥ��롣
#   
# OnRead�ϥ�����Хå� (�ɤ߽Ф��˵������륤�٥�Ȥˤ�ꥳ���뤵���)
#
# - void OnRead::operator(): 
#     EventInPort::read() ��ƤӽФ��ɤ߽Ф���Ԥ��ݤ˥����뤵��롣
#
# - DataType OnReadConvert::operator(DataType): 
#     EventInPort::read() ��ƤӽФ����ǡ�����Хåե������ɤߤ����ݤ˸ƤФ�
#     �ǡ������Ѵ���Ԥ��������ˤϥХåե������ɤ߽Ф��줿�ͤ�Ϳ����졢
#     �Ѵ���Υǡ���������ͤȤ����֤��������ͤ�read()���֤��ͤȤʤ롣
#
# @since 0.2.0
#
# @else
#
# @class EventInPort
#
# @brief EventInPort template class
#
# This is a template class that implements EventInPort.  <T> is the type
# defined in BasicDataType.idl and must be the structure which has
# both Time type tm and type-T data as a member. EventInPort has a ring
# buffer internally, and stores the received data externally in
# this buffer one by one. The size of ring buffer can be specified
# according to the argument of constructor, though the default size
# is 64. Unread data and data which is already read are managed
# with the flag, and the data can be handled by the isNew(),
# write(), read(), isFull() and isEmpty() method etc.
#
# @since 0.2.0
#
# @endif
#
class EventInPort(OpenRTM_aist.InPortBase):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  # �ѥ�᡼���Ȥ���Ϳ������ T �����ѿ��˥Х���ɤ���롣
  #
  # @param name EventInPort ̾��EventInPortBase:name() �ˤ�껲�Ȥ���롣
  # @param value ���� EventInPort �˥Х���ɤ���� T �����ѿ�
  # @param bufsize EventInPort �����Υ�󥰥Хåե��ΥХåե�Ĺ(�ǥե������:64)
  # @param read_block �ɹ��֥�å��ե饰��
  #        �ǡ����ɹ�����̤�ɥǡ������ʤ���硢���Υǡ��������ޤǥ֥�å�����
  #        ���ɤ���������(�ǥե������:false)
  # @param write_block ����֥�å��ե饰��
  #        �ǡ���������˥Хåե����ե�Ǥ��ä���硢�Хåե��˶������Ǥ���
  #        �ޤǥ֥�å����뤫�ɤ���������(�ǥե������:false)
  # @param read_timeout �ɹ��֥�å�����ꤷ�Ƥ��ʤ����Ρ��ǡ����ɼ西����
  #        �����Ȼ���(�ߥ���)(�ǥե������:0)
  # @param write_timeout ����֥�å�����ꤷ�Ƥ��ʤ����Ρ��ǡ������������
  #        �����Ȼ���(�ߥ���)(�ǥե������:0)
  #
  # @else
  #
  # @brief A constructor.
  #
  # constructor.
  # This is bound to type-T variable given as a parameter.
  #
  # @param name A name of the EventInPort. This name is referred by
  #             EventInPortBase::name().
  # @param value type-T variable that is bound to this EventInPort.
  # @param bufsize Buffer length of internal ring buffer of EventInPort
  #                (The default value:64)
  # @param read_block Flag of reading block.
  #                   When there are not unread data at reading data,
  #                   set whether to block data until receiving the next 
  #                   data. (The default value:false)
  # @param write_block Flag of writing block.
  #                    If the buffer was full at writing data, set whether 
  #                    to block data until the buffer has space. 
  #                    (The default value:false)
  # @param read_timeout Data reading timeout time (millisecond) 
  #                     when not specifying read blocking.
  #                     (The default value:0)
  # @param write_timeout Data writing timeout time (millisecond)
  #                      when not specifying writing block.
  #                      (The default value:0)
  #
  # @endif
  #
  def __init__(self, name, fsm, bufsize=64, read_block=False, write_block=False, read_timeout=0, write_timeout=0):
    super(EventInPort, self).__init__(name, "any")
    self._name = name
    self._fsm = fsm
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯����
  #
  # @else
  #
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    pass
  ##
  # @if jp
  #
  # @brief �ݡ���̾�Τ�������롣
  #
  # �ݡ���̾�Τ�������롣
  #
  # @return �ݡ���̾��
  #
  # @else
  #
  # @brief Get port name
  #
  # Get port name.
  #
  # @return The port name
  #
  # @endif
  #
  def name(self):
    return self._name

  def bindEvent0(self, name, handler, ptask=False):
    self.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                  EventBinder0(self._fsm, name, handler, ptask))
    
  def bindEvent1(self, name, handler, data_type, ptask=False):
    self.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                  EventBinder1(self._fsm, name, handler, data_type, ptask))
  




