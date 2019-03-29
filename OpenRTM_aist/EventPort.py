#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file EventPort.py
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
import OpenRTM_aist.Macho
import copy


##
# @if jp
#
# @class Event0
#
# @brief �����ʤ��Υ��٥�Ȥ��Ǽ���륯�饹
# ���٥�ȼ������˥ꥹ�ʤ��Ǽ����Event0���֥������Ȥ�Хåե��˳�Ǽ����
# �¹Ի���__call__�᥽�åɤˤ�ꥤ�٥�Ȥ�¹ԤǤ���
#
# @since 2.0.0
#
# @else
#
# @class Event0
#
# @brief 
#
# @since 2.0.0
#
#
# @endif
#
class Event0:
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param eb ���٥�ȼ������Υꥹ��
  #
  # @else
  #
  # @brief A constructor.
  #
  # @param self
  # @param eb
  #
  # @endif
  #
  def __init__(self, eb):
    self._eb = eb
  ##
  # @if jp
  #
  # @brief ���٥�ȼ¹�
  #
  # @param self
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  def __call__(self):
    self._eb.run()

##
# @if jp
#
# @class Event1
#
# @brief ����1�ĤΥ��٥�Ȥ��Ǽ���륯�饹
# ���٥�ȼ������˥ꥹ�ʡ��������Ǽ����Event1���֥������Ȥ�Хåե��˳�Ǽ����
# �¹Ի���__call__�᥽�åɤˤ�ꥤ�٥�Ȥ�¹ԤǤ���
#
# @since 2.0.0
#
# @else
#
# @class Event1
#
# @brief 
#
# @since 2.0.0
#
#
# @endif
#
class Event1(Event0):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param eb ���٥�ȼ������Υꥹ��
  # @param data ���٥�ȼ¹Ի��˻��ꤹ�����
  #
  # @else
  #
  # @brief A constructor.
  #
  # @param self
  # @param eb 
  # @param data 
  #
  # @endif
  #
  def __init__(self, eb, data):
    Event0.__init__(self, eb)
    self._data = data
  ##
  # @if jp
  #
  # @brief ���٥�ȼ¹�
  #
  # @param self
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  def __call__(self):
    self._eb.run(self._data)

##
# @if jp
#
# @class EventBinder0
#
# @brief �����ʤ��Υ��٥�ȼ������Υꥹ��
# InPort��ON_RECEIVED������Хå��˻��ꤹ�뤳�Ȥǡ�
# ���٥�ȼ������˥Хåե��˥��٥�Ȥ��Ǽ����
# 
#
# @since 2.0.0
#
# @else
#
# @class EventBinder0
#
# @brief 
#
# @since 2.0.0
#
#
# @endif
#
class EventBinder0(OpenRTM_aist.ConnectorDataListener):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param fsm ͭ�¾��֥ޥ���
  # @param event_name ���٥��̾
  # @param handler ���٥�ȥϥ�ɥ�
  # @param buffer ���٥�Ȥ��Ǽ����Хåե�
  #
  # @else
  #
  # @brief A constructor.
  #
  # @param self
  # @param fsm 
  # @param event_name 
  # @param handler 
  # @param buffer 
  #
  # @endif
  #
  def __init__(self, fsm, event_name, handler, buffer):
    self._fsm = fsm
    self._eventName = event_name
    self._handler = handler
    self._buffer = buffer
    
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @brief A destructor.
  #
  # @param self
  #
  # @endif
  #
  def __del__(self):
    pass
  ##
  # @if jp
  #
  # @brief ���٥�ȼ������Υ�����Хå��ؿ�
  # ���ͥ����ץ�ե������fsm_event_name���ͤ����٥��̾�Ȱ��פ��Ƥ����硢�Хåե��˥��٥�Ȥ��Ǽ����
  #
  # @param self
  # @param info ���ͥ����ץ�ե�����
  # @param data �����ǡ���
  # @return �꥿���󥳡���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param info 
  # @param data 
  # @return 
  #
  # @endif
  #
  def __call__(self, info, data):
    if info.properties.getProperty("fsm_event_name") == self._eventName or info.name == self._eventName:
      self._buffer.write(Event0(self))
      
      return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE
    return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE
  
  ##
  # @if jp
  #
  # @brief ���٥�ȼ¹Դؿ�
  # ���٥�ȥϥ�ɥ�˻��ꤷ��������¹Ԥ���
  #
  # @param self
  #
  # @else
  #
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  def run(self):
    self._fsm.dispatch(OpenRTM_aist.Macho.Event(self._handler))
    

    
##
# @if jp
#
# @class EventBinder1
#
# @brief ����1�ĤΥ��٥�ȼ������Υꥹ��
# InPort��ON_RECEIVED������Хå��˻��ꤹ�뤳�Ȥǡ�
# ���٥�ȼ������˥Хåե��˥��٥�Ȥ��Ǽ����
# 
#
# @since 2.0.0
#
# @else
#
# @class EventBinder1
#
# @brief 
#
# @since 2.0.0
#
#
# @endif
#
class EventBinder1(OpenRTM_aist.ConnectorDataListenerT):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param fsm ͭ�¾��֥ޥ���
  # @param event_name ���٥��̾
  # @param handler ���٥�ȥϥ�ɥ�
  # @param data_type ���ϥǡ�����
  # @param buffer ���٥�Ȥ��Ǽ����Хåե�
  #
  # @else
  #
  # @brief A constructor.
  #
  # @param self
  # @param fsm 
  # @param event_name 
  # @param handler 
  # @param data_type
  # @param buffer 
  #
  # @endif
  #
  def __init__(self, fsm, event_name, handler, data_type, buffer):
    self._fsm = fsm
    self._eventName = event_name
    self._handler = handler
    self._data_type = data_type
    self._buffer = buffer
    
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @brief A destructor.
  #
  # @param self
  #
  # @endif
  #
  def __del__(self):
    pass

  ##
  # @if jp
  #
  # @brief ���٥�ȼ������Υ�����Хå��ؿ�
  # ���ͥ����ץ�ե������fsm_event_name���ͤ����٥��̾�Ȱ��פ��Ƥ����硢�Хåե��˥��٥�Ȥ��Ǽ����
  #
  # @param self
  # @param info ���ͥ����ץ�ե�����
  # @param data �����ǡ���
  # @return �꥿���󥳡���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param info 
  # @param data 
  # @return 
  #
  # @endif
  #
  def __call__(self, info, data):
    data_ = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, data, self._data_type)
    
    if info.properties.getProperty("fsm_event_name") == self._eventName or info.name == self._eventName:
      self._buffer.write(Event1(self, data_))
      return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE
    return OpenRTM_aist.ConnectorListenerStatus.NO_CHANGE

  ##
  # @if jp
  #
  # @brief ���٥�ȼ¹Դؿ�
  # ���٥�ȥϥ�ɥ�˻��ꤷ��������¹Ԥ���
  #
  # @param self
  # @param data �����ǡ���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param data
  #
  # @endif
  #
  def run(self, data):
    self._fsm.dispatch(OpenRTM_aist.Macho.Event(self._handler, data))


##
# @if jp
#
# @class EventConnListener
#
# @brief ���ͥ�����³���Υꥹ��
# InPort��ON_CONNECT������Хå��˻��ꤹ��
# �ݡ��Ȥ��ݻ�����Хåե���write.full_policy��read.empty_policy��do_nothing�����ꤹ�뤳�Ȥǡ�
# �ݡ��Ȥ��ݻ�����Хåե��Υǡ����ɤ߹��ߡ��񤭹��߻��˥֥�å��䥨�顼����ȯ�������ʤ��褦�ˤ���
# ͭ�¾��֥ޥ����ݻ�����Хåե��ν������Ԥ�
# ���Τ��ᡢ�����³�������ͥ���������ǥХåե������꤬��񤭤����
# 
#
# @since 2.0.0
#
# @else
#
# @class EventConnListener
#
# @brief 
#
# @since 2.0.0
#
#
# @endif
#
class EventConnListener(OpenRTM_aist.ConnectorListener):
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param buffer 
  # @param thebuffer 
  #
  # @else
  #
  # @brief A constructor.
  #
  # @param self
  # @param buffer 
  # @param thebuffer 
  #
  # @endif
  #
  def __init__(self, buffer, thebuffer):
    self._buffer = buffer
    self._thebuffer = thebuffer

  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @brief A destructor.
  #
  # @param self
  #
  # @endif
  #
  def __del__(self):
    pass

  ##
  # @if jp
  #
  # @brief ���ͥ�����³���Υ�����Хå��ؿ�
  #
  # @param self
  # @param info ���ͥ����ץ�ե�����
  # @return �꥿���󥳡���
  #
  # @else
  #
  # @brief 
  #
  # @param self
  # @param info 
  # @return 
  #
  # @endif
  #
  def __call__(self, info):
    prop = OpenRTM_aist.Properties()
    prop.setProperty("write.full_policy", "do_nothing")
    prop.setProperty("read.empty_policy", "do_nothing")
    self._thebuffer.init(prop)

    prop_ = copy.copy(info.properties.getNode("buffer"))
    
    self._buffer.init(prop_)
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
# ���Υ�󥰥Хåե��˳�Ǽ���롣��󥰥Хåե��Υ������ϥǥե���Ȥ�8��
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
# @since 2.0.0
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
# is 8. Unread data and data which is already read are managed
# with the flag, and the data can be handled by the isNew(),
# write(), read(), isFull() and isEmpty() method etc.
#
# @since 2.0.0
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
  #
  # @endif
  #
  def __init__(self, name, fsm):
    super(EventInPort, self).__init__(name, "any")
    self._name = name
    self._fsm = fsm
    self._buffer = self._fsm.getBuffer()
    
    
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
    super(EventInPort, self).__del__()
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
  ##
  # @if jp
  #
  # @brief �����
  # InPortBase�ν�����Τۤ��˥Хåե�������Τ���Υ��ͥ���������Хå��ؿ�����Ͽ��Ԥ�
  #
  # @param prop �������
  #
  #
  # @else
  #
  # @brief 
  #
  #
  # @param prop
  #
  # @endif
  #
  def init(self, prop):
    OpenRTM_aist.InPortBase.init(self, prop)
    self.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_CONNECT,
                                      EventConnListener(self._buffer, self._thebuffer))
  ##
  # @if jp
  #
  # @brief �����ʤ��Υ��٥�ȥϥ�ɥ����Ͽ����
  # ���ͥ�����ON_RECEIVED������Хå��¹Ի��˥Хåե��˼¹�ͽ��Υ��٥�ȤȤ��Ƴ�Ǽ����
  # �Хåե��˳�Ǽ�������٥�Ȥ�Machine��run_event�ؿ��Ǽ¹Ԥ���
  #
  # @param name ���٥��̾
  # @param handler ���٥�ȥϥ�ɥ�
  #
  #
  # @else
  #
  # @brief 
  #
  # @param name
  # @param handler
  #
  # @endif
  #
  def bindEvent0(self, name, handler):
    self.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                  EventBinder0(self._fsm, name, handler, self._buffer))
  ##
  # @if jp
  #
  # @brief ����1�ĤΥ��٥�ȥϥ�ɥ����Ͽ����
  # ���ͥ�����ON_RECEIVED������Хå��¹Ի��˥Хåե��˼¹�ͽ��Υ��٥�ȤȤ��Ƴ�Ǽ����
  # �Хåե��˳�Ǽ�������٥�Ȥ�Machine��run_event�ؿ��Ǽ¹Ԥ���
  #
  # @param name ���٥��̾
  # @param handler ���٥�ȥϥ�ɥ�
  # @param data_type �ǡ�����
  #
  #
  # @else
  #
  # @brief 
  #
  #
  # @param name
  # @param handler
  # @param data_type
  #
  # @endif
  #
  def bindEvent1(self, name, handler, data_type):
    self.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                  EventBinder1(self._fsm, name, handler, data_type, self._buffer))




    
      
    
    
  




