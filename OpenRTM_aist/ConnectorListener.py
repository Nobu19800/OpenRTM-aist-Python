#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  ConnectorListener.py
# @brief connector listener class
# @date  $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import cdrUnmarshal
from omniORB import any

import OpenRTM_aist
import OpenRTM_aist.Guard
import threading


##
# @if jp
# @class ConnectorListenerStatus mixin class
# @brief ConnectorListenerStatus mixin ���饹
#
# ���Υ��饹�ϡ�enum������줿�꥿���󥳡��ɤ�ConnectorListener��
# Ϣ�Υ��֥��饹�Ƕ������Ѥ��뤿��� mixin ���饹�Ǥ��롣���Υ꥿��
# �󥳡��ɤ���Ѥ��륯�饹�Ǥϡ�ConnectorListenerStatus ���饹��
# public �Ѿ���������define ���Ƥ��� CONNLISTENER_STATUS_ENUM �򥯥�
# ����˵��Ҥ��뤳�Ȥ����Ѳ�ǽ�Ȥʤ롣����ˤ�ꡢenum ��
# ReturnCode ���Ȥ��� typedef �����ʸ� ReturnCode �����ѤǤ���褦��
# ����ȤȤ�ˡ�̾�����֤� enum ������줿�Ƽ��̻Ҥ��������饹̾����
# �����Ƴ�����롣
#
# @else
# @class DataPortStatus mixin class
# @brief DataPortStatus mixin class
#
# This is a mixin class to provide enumed return codes that are
# commonly utilised in connector listener related sub-classes. To
# use this class, sub-class should inherit this class as a public
# super class, and declare CONNLISTENERSTATUS_ENUM defined
# below. Consequently, ReturnCode type that is typedefed by this
# macro can be used in the sub-class, and enumed identifiers are
# imported to the class's namespace.
#
# @endif
#
class ConnectorListenerStatus:
  NO_CHANGE = 0
  INFO_CHANGED = 1 << 0
  DATA_CHANGED = 1 << 1
  BOTH_CHANGED = INFO_CHANGED | DATA_CHANGED


##
# @if jp
# @brief ConnectorDataListener �Υ�����
#
# - ON_BUFFER_WRITE:          �Хåե��񤭹��߻�
# - ON_BUFFER_FULL:           �Хåե��ե��
# - ON_BUFFER_WRITE_TIMEOUT:  �Хåե��񤭹��ߥ����ॢ���Ȼ�
# - ON_BUFFER_OVERWRITE:      �Хåե���񤭻�
# - ON_BUFFER_READ:           �Хåե��ɤ߽Ф���
# - ON_SEND:                  InProt�ؤ�������
# - ON_RECEIVED:              InProt�ؤ�������λ��
# - ON_RECEIVER_FULL:         InProt¦�Хåե��ե��
# - ON_RECEIVER_TIMEOUT:      InProt¦�Хåե������ॢ���Ȼ�
# - ON_RECEIVER_ERROR:        InProt¦���顼��
#
# @else
# @brief The types of ConnectorDataListener
# 
# - ON_BUFFER_WRITE:          At the time of buffer write
# - ON_BUFFER_FULL:           At the time of buffer full
# - ON_BUFFER_WRITE_TIMEOUT:  At the time of buffer write timeout
# - ON_BUFFER_OVERWRITE:      At the time of buffer overwrite
# - ON_BUFFER_READ:           At the time of buffer read
# - ON_SEND:                  At the time of sending to InPort
# - ON_RECEIVED:              At the time of finishing sending to InPort
# - ON_RECEIVER_FULL:         At the time of bufferfull of InPort
# - ON_RECEIVER_TIMEOUT:      At the time of timeout of InPort
# - ON_RECEIVER_ERROR:        At the time of error of InPort
#
# @endif
#
class ConnectorDataListenerType:
  def __init__(self):
    pass

  ON_BUFFER_WRITE              = 0
  ON_BUFFER_FULL               = 1
  ON_BUFFER_WRITE_TIMEOUT      = 2
  ON_BUFFER_OVERWRITE          = 3
  ON_BUFFER_READ               = 4
  ON_SEND                      = 5
  ON_RECEIVED                  = 6
  ON_RECEIVER_FULL             = 7
  ON_RECEIVER_TIMEOUT          = 8
  ON_RECEIVER_ERROR            = 9
  CONNECTOR_DATA_LISTENER_NUM  = 10



##
# @if jp
# @class ConnectorDataListener ���饹
#
# �ǡ����ݡ��Ȥ� Connector �ˤ�����ȯ������Ƽ磻�٥�Ȥ��Ф��륳��
# ��Хå���¸�����ꥹ�ʥ��饹�δ��쥯�饹��
#
# �������å���OutPort���Ф��ƥǡ����񤭹��ߡ�InPort¦�ǥǡ�������
# �������ޤǤδ֤�ȯ������Ƽ磻�٥�Ȥ�եå����륳����Хå�����
# �ꤹ�뤳�Ȥ��Ǥ��롣�ʤ����ꥹ�ʡ����饹��2����¸�ߤ����Хåե���
# ����������Υ�����Хå��ǡ����λ�����ͭ���ʥǡ�����ե��󥯥��ΰ�
# ���Ȥ��Ƽ������ ConnectorDataListener �Ǥ��ꡢ�⤦�����ϥǡ�����
# ��ץƥ���Хåե��ɤ߹��߻��Υ����ॢ���Ȥʤɥǡ����������Ǥ��ʤ�
# ���ʤɤ˥����뤵���ե��󥯥��ΰ����˲���Ȥ�ʤ餤
# ConnecotorListener �����롣
# 
# �ǡ����ݡ��Ȥˤϡ���³���˥ǡ�������������ˡ�ˤĤ��ƥǡ����ե�����
# ���֥�����ץ�����������ꤹ�뤳�Ȥ��Ǥ��롣
# ConnectorDaataListener/ConnectorListener �ϤȤ�ˡ��͡��ʥ��٥��
# ���Ф��륳����Хå������ꤹ�뤳�Ȥ��Ǥ��뤬�������ǡ����ե���
# ����ӥ��֥�����ץ���󷿤�����˱����ơ����Ѳ�ǽ�ʤ�������Բ�ǽ
# �ʤ�Τ䡢�ƤӽФ���륿���ߥ󥰤��ۤʤ롣
# �ʲ��ˡ����󥿡��ե�������CORBA CDR���ξ��Υ�����Хå������򼨤���
# 
# OutPort:
#  -  Push��: Subscription Type�ˤ�ꤵ��˥��٥�Ȥμ��बʬ����롣
#    - Flush: Flush���ˤϥХåե����ʤ����� ON_BUFFER �ϤΥ��٥�Ȥ�ȯ�����ʤ�
#      - ON_SEND
#      - ON_RECEIVED
#      - ON_RECEIVER_FULL
#      - ON_RECEIVER_TIMEOUT
#      - ON_RECEIVER_ERROR
#      - ON_CONNECT
#      - ON_DISCONNECT
#      .
#    - New��
#      - ON_BUFFER_WRITE
#      - ON_BUFFER_FULL
#      - ON_BUFFER_WRITE_TIMEOUT
#      - ON_BUFFER_OVERWRITE
#      - ON_BUFFER_READ
#      - ON_SEND
#      - ON_RECEIVED
#      - ON_RECEIVER_FULL
#      - ON_RECEIVER_TIMEOUT
#      - ON_RECEIVER_ERROR
#      - ON_SENDER_ERROR
#      - ON_CONNECT
#      - ON_DISCONNECT
#      .
#    - Periodic��
#      - ON_BUFFER_WRITE
#      - ON_BUFFER_FULL
#      - ON_BUFFER_WRITE_TIMEOUT
#      - ON_BUFFER_READ
#      - ON_SEND
#      - ON_RECEIVED
#      - ON_RECEIVER_FULL
#      - ON_RECEIVER_TIMEOUT
#      - ON_RECEIVER_ERROR
#      - ON_BUFFER_EMPTY
#      - ON_SENDER_EMPTY
#      - ON_SENDER_ERROR
#      - ON_CONNECT
#      - ON_DISCONNECT
#      .
#    .
#  - Pull��
#    - ON_BUFFER_READ
#    - ON_SEND
#    - ON_BUFFER_EMPTY
#    - ON_BUFFER_READ_TIMEOUT
#    - ON_SENDER_EMPTY
#    - ON_SENDER_TIMEOUT
#    - ON_SENDER_ERROR
#    - ON_CONNECT
#    - ON_DISCONNECT
# 
#  InPort:
#  - Push��:
#      - ON_BUFFER_WRITE
#      - ON_BUFFER_FULL
#      - ON_BUFFER_WRITE_TIMEOUT
#      - ON_BUFFER_WRITE_OVERWRITE
#      - ON_RECEIVED
#      - ON_RECEIVER_FULL
#      - ON_RECEIVER_TIMEOUT
#      - ON_RECEIVER_ERROR
#      - ON_CONNECT
#      - ON_DISCONNECT
#      .
#  - Pull��
#      - ON_CONNECT
#      - ON_DISCONNECT
# @else
# @class ConnectorDataListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in the data port's
# connectors.
#
# @endif
#
class ConnectorDataListener:
  """
  """

  def __del__(self):
    pass

  # virtual ReturnCode operator()(const ConnectorInfo& info,
  #                         const cdrMemoryStream& data) = 0;
  def __call__(self, info, data):
    pass

  ##
  # @if jp
  #
  # @brief ConnectorDataListenerType ��ʸ������Ѵ�
  #
  # ConnectorDataListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� ConnectorDataListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert ConnectorDataListenerType into the string.
  #
  # Convert ConnectorDataListenerType into the string.
  #
  # @param type The target ConnectorDataListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #
  def toString(type):
    typeString = ["ON_BUFFER_WRITE",
                  "ON_BUFFER_FULL",
                  "ON_BUFFER_WRITE_TIMEOUT",
                  "ON_BUFFER_OVERWRITE",
                  "ON_BUFFER_READ", 
                  "ON_SEND", 
                  "ON_RECEIVED",
                  "ON_RECEIVER_FULL", 
                  "ON_RECEIVER_TIMEOUT", 
                  "ON_RECEIVER_ERROR",
                  "CONNECTOR_DATA_LISTENER_NUM"]

    if type < ConnectorDataListenerType.CONNECTOR_DATA_LISTENER_NUM:
      return typeString[type]

    return ""

  toString = staticmethod(toString)


##
# @if jp
# @class ConnectorDataListenerT ���饹
#
# �ǡ����ݡ��Ȥ� Connector �ˤ�����ȯ������Ƽ磻�٥�Ȥ��Ф��륳��
# ��Хå���¸�����ꥹ�ʥ��饹�δ��쥯�饹��
# 
# ���Υ��饹�ϡ�operator()() ����2������ cdrMemoryStream ���ǤϤʤ���
# �ºݤ˥ǡ����ݡ��Ȥǻ��Ѥ�����ѿ�����ƥ�ץ졼�Ȱ����Ȥ���
# �Ϥ����Ȥ��Ǥ��롣
#
# @else
# @class ConnectorDataListenerT class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in the data port's
# connectors.
#
# This class template can have practical data types that are used
# as typed variable for DataPort as an argument of template instead
# of cdrMemoryStream.
#
# @endif
#
class ConnectorDataListenerT(ConnectorDataListener):
  """
  """

  def __del__(self):
    pass


  ##
  # @if jp
  #
  # @brief ������Хå��᥽�å�
  #
  # �ǡ�����ǡ����ݡ��Ȥǻ��Ѥ�����ѿ������Ѵ����� ConnectorDataListenerT
  # �Υ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo 
  # @param cdrdata cdrMemoryStream���Υǡ���
  #
  # @else
  #
  # @brief Callback method
  #
  # This method invokes the callback method of ConnectorDataListenerT. 
  # Data is converted into the variable type used in DataPort.
  #
  # @param info ConnectorInfo 
  # @param cdrdata Data of cdrMemoryStream type
  #
  # @endif
  #
  # virtual ReturnCode operator()(const ConnectorInfo& info,
  #                         const cdrMemoryStream& cdrdata)
  def __call__(self, info, cdrdata, data):
    endian = info.properties.getProperty("serializer.cdr.endian","little")
    if endian is not "little" and endian is not None:
      endian = OpenRTM_aist.split(endian, ",") # Maybe endian is ["little","big"]
      endian = OpenRTM_aist.normalize(endian) # Maybe self._endian is "little" or "big"

    if endian == "little":
      endian = True
    elif endian == "big":
      endian = False
    else:
      endian = True

    _data = cdrUnmarshal(any.to_any(data).typecode(), cdrdata, endian)
    return _data



##
# @if jp
# @brief ConnectorListener �Υ�����
#  
# - ON_BUFFER_EMPTY:       �Хåե������ξ��
# - ON_BUFFER_READTIMEOUT: �Хåե������ǥ����ॢ���Ȥ������
# - ON_SENDER_EMPTY:       OutPort¦�Хåե�����
# - ON_SENDER_TIMEOUT:     OutPort¦�����ॢ���Ȼ�
# - ON_SENDER_ERROR:       OutPort¦���顼��
# - ON_CONNECT:            ��³��Ω��
# - ON_DISCONNECT:         ��³���ǻ�
#
# @else
# @brief The types of ConnectorListener
# 
# - ON_BUFFER_EMPTY:       At the time of buffer empty
# - ON_BUFFER_READTIMEOUT: At the time of buffer read timeout
# - ON_BUFFER_EMPTY:       At the time of empty of OutPort
# - ON_SENDER_TIMEOUT:     At the time of timeout of OutPort
# - ON_SENDER_ERROR:       At the time of error of OutPort
# - ON_CONNECT:            At the time of connection
# - ON_DISCONNECT:         At the time of disconnection
#
# @endif
#
# enum ConnectorListenerType
class ConnectorListenerType:

  def __init__(self):
    pass
  
  ON_BUFFER_EMPTY        = 0
  ON_BUFFER_READ_TIMEOUT = 1
  ON_SENDER_EMPTY        = 2
  ON_SENDER_TIMEOUT      = 3
  ON_SENDER_ERROR        = 4
  ON_CONNECT             = 5
  ON_DISCONNECT          = 6
  CONNECTOR_LISTENER_NUM = 7



##
# @if jp
# @class ConnectorListener ���饹
# @brief ConnectorListener ���饹
#
# �ǡ����ݡ��Ȥ� Connector �ˤ�����ȯ������Ƽ磻�٥�Ȥ��Ф��륳��
# ��Хå���¸�����ꥹ�ʥ��饹�δ��쥯�饹��
#
# �������å���OutPort���Ф��ƥǡ����񤭹��ߡ�InPort¦�ǥǡ�������
# �������ޤǤδ֤�ȯ������Ƽ磻�٥�Ȥ�եå����륳����Хå�����
# �ꤹ�뤳�Ȥ��Ǥ��롣�ʤ����ꥹ�ʡ����饹��2����¸�ߤ����Хåե���
# ����������Υ�����Хå��ǡ����λ�����ͭ���ʥǡ�����ե��󥯥��ΰ�
# ���Ȥ��Ƽ������ ConnectorDataListener �Ǥ��ꡢ�⤦�����ϥǡ�����
# ��ץƥ���Хåե��ɤ߹��߻��Υ����ॢ���Ȥʤɥǡ����������Ǥ��ʤ�
# ���ʤɤ˥����뤵���ե��󥯥��ΰ����˲���Ȥ�ʤ餤
# ConnecotorListener �����롣
#
# ConnectorListener ���饹�ˤ�äƴ�Ϣ����ư���եå���������硢��
# ������Τ褦�ˡ����Υ��饹��Ѿ��������ͥ����ξ��������˼��ʲ�
# �Τ褦�ʥ�����Хå����֥������Ȥ���������ǡ����ݡ��Ȥ�Ŭ�ڤʥ���
# ��Хå�����ؿ����饳����Хå����֥������Ȥ򥻥åȤ���ɬ�פ����롣
#
# <pre>
# class MyListener
#   : public ConnectorListener
# {
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#   virtual ReturnCode operator()(ConnectorInfo& info)
#   {
#     std::cout << "Data Listener: " << m_name       << std::endl;
#     std::cout << "Profile::name: " << info.name    << std::endl;
#     std::cout << "Profile::id:   " << info.id      << std::endl;
#     std::cout << "Profile::properties: "           << std::endl;
#     std::cout << info.properties;
#   };
#   std::string m_name;
# };
# </pre>
#
# ���Τ褦�ˤ���������줿�ꥹ�ʥ��饹�ϡ��ʲ��Τ褦�˥ǡ����ݡ��Ȥ�
# �Ф��ơ��ʲ��Τ褦�˥��åȤ���롣
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     m_outOut.
#         addConnectorListener(ON_BUFFER_EMPTY,
#                              new MyListener("ON_BUFFER_EMPTY"));
#    :
# </pre>
#
# ��1������ "ON_BUFFER_EMPTY" �ϡ�������Хå���եå�����ݥ���Ȥ�
# ���ꡢ�ʲ�����󤹤��ͤ��뤳�Ȥ���ǽ�Ǥ��롣�ǡ����ݡ��Ȥˤϡ���
# ³���˥ǡ�������������ˡ�ˤĤ��ơ����󥿡��ե����������ǡ����ե�
# �������֥�����ץ�����������ꤹ�뤳�Ȥ��Ǥ��뤬�������������
# ���եå������ݥ���Ȥϰۤʤ롣�ʲ��ˡ����󥿡��ե�������CORBA
# CDR���ξ��Υ�����Хå������򼨤���
#
# OutPort:
# -  Push��: Subscription Type�ˤ�ꤵ��˥��٥�Ȥμ��बʬ����롣
#   - Flush: Flush���ˤϥХåե����ʤ����� ON_BUFFER �ϤΥ��٥�Ȥ�ȯ�����ʤ�
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   - New��
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   - Periodic��
#     - ON_BUFFER_EMPTY
#     - ON_BUFFER_READ_TIMEOUT
#     - ON_SENDER_EMPTY
#     - ON_SENDER_ERROR
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   .
# - Pull��
#   - ON_BUFFER_EMPTY
#   - ON_BUFFER_READ_TIMEOUT
#   - ON_SENDER_EMPTY
#   - ON_SENDER_TIMEOUT
#   - ON_SENDER_ERROR
#   - ON_CONNECT
#   - ON_DISCONNECT
#   .
# InPort:
# - Push��:
#     - ON_BUFFER_EMPTY
#     - ON_BUFFER_READ_TIMEOUT
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
# - Pull��
#     - ON_CONNECT
#     - ON_DISCONNECT
#
# @else
# @class ConnectorListener class
# @brief ConnectorListener class
#
# This class is abstract base class for listener classes that
# realize callbacks for various events in the data port's
# connectors.
#
# Callbacks can be hooked to the various kind of events which occur
# throgh OutPort side data write action to InPort side data-read
# action. Two types listener classes exist. One is
# ConnectorDataListener which receives valid data-port's data value
# at that time such as buffer-full event, data-send event, and so
# on. Other is ConnectorListener which does not receive any data
# such as buffer-empty event, buffer-read-timeout event and so on.
#
# If you want to hook related actions by
# ConnectorListener, a class which inherits this class should
# be defined, and the functor should receive a connector
# information as an argument. And then, the defined
# class must be set to data-port object through its member
# function, as follows.
#
# <pre>
# class MyListener
#   : public ConnectorListener
# {
# public:
#   MyListener(const char* name) : m_name(name) {}
#   virtual ~MyListener() {}
#   virtual ReturnCode operator()(ConnectorInfo& info)
#   {
#     std::cout << "Data Listener: " << m_name       << std::endl;
#     std::cout << "Profile::name: " << info.name    << std::endl;
#     std::cout << "Profile::id:   " << info.id      << std::endl;
#     std::cout << "Profile::properties: "           << std::endl;
#     std::cout << info.properties;
#   };
#   std::string m_name;
# };
# </pre>
#
# The listener class defained as above can be attached to a
# data-port as follows.
#
# <pre>
# RTC::ReturnCode_t ConsoleIn::onInitialize()
# {
#     m_outOut.
#         addConnectorListener(ON_BUFFER_EMPTY,
#                              new MyDataListener("ON_BUFFER_EMPTY"));
#    :
# </pre>
#
# The first argument "ON_BUFFER_EMPTY" specifies hook point of
# callback, and the following values are available. Data-port can
# be specified some properties such as interface-type,
# dataflow-type, subscription type and so on. Available hook points
# vary by the those settings. The following hook points are
# available when interface type is CORBA CDR type.
#
# OutPort:
# -  Push type: Available hook event varies by subscription type.
#   - Flush: No ON_BUFFER* events since flush-type has no buffer.
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   - New type:
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   - Periodic type:
#     - ON_BUFFER_EMPTY
#     - ON_BUFFER_READ_TIMEOUT
#     - ON_SENDER_EMPTY
#     - ON_SENDER_ERROR
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   .
# - Pull type:
#   - ON_BUFFER_EMPTY
#   - ON_BUFFER_READ_TIMEOUT
#   - ON_SENDER_EMPTY
#   - ON_SENDER_TIMEOUT
#   - ON_SENDER_ERROR
#   - ON_CONNECT
#   - ON_DISCONNECT
#   .
# InPort:
# - Push type:
#     - ON_BUFFER_EMPTY
#     - ON_BUFFER_READ_TIMEOUT
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
# - Pull type:
#     - ON_CONNECT
#     - ON_DISCONNECT
#
# @endif
#
class ConnectorListener:
  """
  """

  def __del__(self):
    pass

  # virtual void operator()(const ConnectorInfo& info) = 0;
  def __call__(self,  info):
    pass

  ##
  # @if jp
  #
  # @brief ConnectorListenerType ��ʸ������Ѵ�
  #
  # ConnectorListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� ConnectorListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert ConnectorListenerType into the string.
  #
  # Convert ConnectorListenerType into the string.
  #
  # @param type The target ConnectorListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #
  def toString(type):
    typeString = ["ON_BUFFER_EMPTY",
                  "ON_BUFFER_READ_TIMEOUT",
                  "ON_SENDER_EMPTY", 
                  "ON_SENDER_TIMEOUT", 
                  "ON_SENDER_ERROR", 
                  "ON_CONNECT",
                  "ON_DISCONNECT",
                  "CONNECTOR_LISTENER_NUM"]

    if type < ConnectorListenerType.CONNECTOR_LISTENER_NUM:
      return typeString[type]

    return ""

  toString = staticmethod(toString)


##
# @if jp
# @class ConnectorDataListener �ۥ�����饹
#
# ʣ���� ConnectorDataListener ���ݻ����������륯�饹��
#
# @else
# @class ConnectorDataListener holder class
#
# This class manages one ore more instances of ConnectorDataListener class.
#
# @endif
#
class ConnectorDataListenerHolder:
  """
  """

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
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    #guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    #for listener in self._listeners:
    #  for (k,v) in listener.items():
    #    if v:
    #      del k
    return

    
  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param self
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param self
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  #
  # void addListener(ConnectorDataListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    self._listeners.append({listener:autoclean})
    return

    
  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param self
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param self
  # @param listener Removed listener
  # @endif
  #
  # void removeListener(ConnectorDataListener* listener);
  def removeListener(self, listener):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for (i, _listener) in enumerate(self._listeners):
      if listener in _listener:
        del self._listeners[i][listener]
        return

    
  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param self
  # @param info ConnectorInfo
  # @param cdrdata �ǡ���
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param self
  # @param info ConnectorInfo
  # @param cdrdata Data
  # @endif
  #
  # ReturnCode notify(const ConnectorInfo& info,
  #             const cdrMemoryStream& cdrdata);
  def notify(self, info, cdrdata):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    ret = ConnectorListenerStatus.NO_CHANGE
    for listener in self._listeners:
      for (k,v) in listener.items():
        ret = ret | k(info, cdrdata)
    return ret


##
# @if jp
# @class ConnectorListener �ۥ�����饹
#
# ʣ���� ConnectorListener ���ݻ����������륯�饹��
#
# @else
# @class ConnectorListener holder class
#
# This class manages one ore more instances of ConnectorListener class.
#
# @endif
#
class ConnectorListenerHolder:
  """
  """

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
    return

    
  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    #guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    #for listener in self._listeners:
    #  for (k,v) in listener.items():
    #    if v:
    #      del k
    return
        
    
  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param self
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param self
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  #
  # void addListener(ConnectorListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    self._listeners.append({listener:autoclean})
    return


  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param self
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param self
  # @param listener Removed listener
  # @endif
  #
  # void removeListener(ConnectorListener* listener);
  def removeListener(self, listener):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for (i, _listener) in enumerate(self._listeners):
      if listener in _listener:
        del self._listeners[i][listener]
        return


  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param self
  # @param info ConnectorInfo
  # @return ReturnCode
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param self
  # @param info ConnectorInfo
  # @return ReturnCode
  # @endif
  #
  # void notify(const ConnectorInfo& info);
  def notify(self, info):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    ret = ConnectorListenerStatus.NO_CHANGE
    for listener in self._listeners:
      for (k,v) in listener.items():
        ret = ret | k(info)
    return ret


  
class ConnectorListeners:
  def __init__(self):
    self.connectorData_ = [ OpenRTM_aist.ConnectorDataListenerHolder() for i in range(OpenRTM_aist.ConnectorDataListenerType.CONNECTOR_DATA_LISTENER_NUM) ]
    self.connector_     = [ OpenRTM_aist.ConnectorListenerHolder() for i in range(OpenRTM_aist.ConnectorListenerType.CONNECTOR_LISTENER_NUM) ]
    return
