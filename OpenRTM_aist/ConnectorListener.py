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
# @brief ConnectorListenerStatus mixin クラス
#
# このクラスは、enum定義されたリターンコードを、ConnectorListener関
# 連のサブクラスで共通利用するための mixin クラスである。このリター
# ンコードを使用するクラスでは、ConnectorListenerStatus クラスを
# public 継承し、下にdefine してある CONNLISTENER_STATUS_ENUM をクラ
# ス内に記述することで利用可能となる。これにより、enum を
# ReturnCode 型として typedef し、以後 ReturnCode を利用できるように
# するとともに、名前空間に enum 定義された各識別子を当該クラス名前空
# 間内に導入する。
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
# @brief ConnectorDataListener のタイプ
#
# - ON_BUFFER_WRITE:          バッファ書き込み時
# - ON_BUFFER_FULL:           バッファフル時
# - ON_BUFFER_WRITE_TIMEOUT:  バッファ書き込みタイムアウト時
# - ON_BUFFER_OVERWRITE:      バッファ上書き時
# - ON_BUFFER_READ:           バッファ読み出し時
# - ON_SEND:                  InProtへの送信時
# - ON_RECEIVED:              InProtへの送信完了時
# - ON_RECEIVER_FULL:         InProt側バッファフル時
# - ON_RECEIVER_TIMEOUT:      InProt側バッファタイムアウト時
# - ON_RECEIVER_ERROR:        InProt側エラー時
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
# @class ConnectorDataListener クラス
#
# データポートの Connector において発生する各種イベントに対するコー
# ルバックを実現するリスナクラスの基底クラス。
#
# コアロジックがOutPortに対してデータ書き込み、InPort側でデータが取
# 得されるまでの間で発生する各種イベントをフックするコールバックを設
# 定することができる。なお、リスナークラスは2種類存在し、バッファフ
# ルや送信時のコールバックで、その時点で有効なデータをファンクタの引
# 数として受け取る ConnectorDataListener であり、もう一方はデータエ
# ンプティやバッファ読み込み時のタイムアウトなどデータが取得できない
# 場合などにコールされるファンクタの引数に何もとらならい
# ConnecotorListener がある。
# 
# データポートには、接続時にデータの送受信方法についてデータフロー型、
# サブスクリプション型等を設定することができる。
# ConnectorDaataListener/ConnectorListener はともに、様々なイベント
# に対するコールバックを設定することができるが、これらデータフロー型
# およびサブスクリプション型の設定に応じて、利用可能なもの利用不可能
# なものや、呼び出されるタイミングが異なる。
# 以下に、インターフェースがCORBA CDR型の場合のコールバック一覧を示す。
# 
# OutPort:
#  -  Push型: Subscription Typeによりさらにイベントの種類が分かれる。
#    - Flush: Flush型にはバッファがないため ON_BUFFER 系のイベントは発生しない
#      - ON_SEND
#      - ON_RECEIVED
#      - ON_RECEIVER_FULL
#      - ON_RECEIVER_TIMEOUT
#      - ON_RECEIVER_ERROR
#      - ON_CONNECT
#      - ON_DISCONNECT
#      .
#    - New型
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
#    - Periodic型
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
#  - Pull型
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
#  - Push型:
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
#  - Pull型
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
  # @brief ConnectorDataListenerType を文字列に変換
  #
  # ConnectorDataListenerType を文字列に変換する
  #
  # @param type 変換対象 ConnectorDataListenerType
  #
  # @return 文字列変換結果
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
# @class ConnectorDataListenerT クラス
#
# データポートの Connector において発生する各種イベントに対するコー
# ルバックを実現するリスナクラスの基底クラス。
# 
# このクラスは、operator()() の第2引数に cdrMemoryStream 型ではなく、
# 実際にデータポートで使用される変数型をテンプレート引数として
# 渡すことができる。
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
  # @brief コールバックメソッド
  #
  # データをデータポートで使用される変数型に変換して ConnectorDataListenerT
  # のコールバックメソッドを呼び出す。
  #
  # @param info ConnectorInfo 
  # @param cdrdata cdrMemoryStream型のデータ
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
# @brief ConnectorListener のタイプ
#  
# - ON_BUFFER_EMPTY:       バッファが空の場合
# - ON_BUFFER_READTIMEOUT: バッファが空でタイムアウトした場合
# - ON_SENDER_EMPTY:       OutPort側バッファが空
# - ON_SENDER_TIMEOUT:     OutPort側タイムアウト時
# - ON_SENDER_ERROR:       OutPort側エラー時
# - ON_CONNECT:            接続確立時
# - ON_DISCONNECT:         接続切断時
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
# @class ConnectorListener クラス
# @brief ConnectorListener クラス
#
# データポートの Connector において発生する各種イベントに対するコー
# ルバックを実現するリスナクラスの基底クラス。
#
# コアロジックがOutPortに対してデータ書き込み、InPort側でデータが取
# 得されるまでの間で発生する各種イベントをフックするコールバックを設
# 定することができる。なお、リスナークラスは2種類存在し、バッファフ
# ルや送信時のコールバックで、その時点で有効なデータをファンクタの引
# 数として受け取る ConnectorDataListener であり、もう一方はデータエ
# ンプティやバッファ読み込み時のタイムアウトなどデータが取得できない
# 場合などにコールされるファンクタの引数に何もとらならい
# ConnecotorListener がある。
#
# ConnectorListener クラスによって関連する動作をフックしたい場合、以
# 下の例のように、このクラスを継承し、コネクタの情報を引数に取る以下
# のようなコールバックオブジェクトを定義し、データポートの適切なコー
# ルバック設定関数からコールバックオブジェクトをセットする必要がある。
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
# このようにして定義されたリスナクラスは、以下のようにデータポートに
# 対して、以下のようにセットされる。
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
# 第1引数の "ON_BUFFER_EMPTY" は、コールバックをフックするポイントで
# あり、以下に列挙する値を取ることが可能である。データポートには、接
# 続時にデータの送受信方法について、インターフェース型、データフロー
# 型、サブスクリプション型等を設定することができるが、これらの設定に
# よりフックされるポイントは異なる。以下に、インターフェースがCORBA
# CDR型の場合のコールバック一覧を示す。
#
# OutPort:
# -  Push型: Subscription Typeによりさらにイベントの種類が分かれる。
#   - Flush: Flush型にはバッファがないため ON_BUFFER 系のイベントは発生しない
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   - New型
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   - Periodic型
#     - ON_BUFFER_EMPTY
#     - ON_BUFFER_READ_TIMEOUT
#     - ON_SENDER_EMPTY
#     - ON_SENDER_ERROR
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
#   .
# - Pull型
#   - ON_BUFFER_EMPTY
#   - ON_BUFFER_READ_TIMEOUT
#   - ON_SENDER_EMPTY
#   - ON_SENDER_TIMEOUT
#   - ON_SENDER_ERROR
#   - ON_CONNECT
#   - ON_DISCONNECT
#   .
# InPort:
# - Push型:
#     - ON_BUFFER_EMPTY
#     - ON_BUFFER_READ_TIMEOUT
#     - ON_CONNECT
#     - ON_DISCONNECT
#     .
# - Pull型
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
  # @brief ConnectorListenerType を文字列に変換
  #
  # ConnectorListenerType を文字列に変換する
  #
  # @param type 変換対象 ConnectorListenerType
  #
  # @return 文字列変換結果
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
# @class ConnectorDataListener ホルダクラス
#
# 複数の ConnectorDataListener を保持し管理するクラス。
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
  # @brief コンストラクタ
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
  # @brief デストラクタ
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for listener in self._listeners:
      for (k,v) in listener.items():
        if v:
          del k
    return

    
  ##
  # @if jp
  #
  # @brief リスナーの追加
  #
  # リスナーを追加する。
  #
  # @param self
  # @param listener 追加するリスナ
  # @param autoclean true:デストラクタで削除する,
  #                  false:デストラクタで削除しない
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
  # @brief リスナーの削除
  #
  # リスナを削除する。
  #
  # @param self
  # @param listener 削除するリスナ
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
  # @brief リスナーへ通知する
  #
  # 登録されているリスナのコールバックメソッドを呼び出す。
  #
  # @param self
  # @param info ConnectorInfo
  # @param cdrdata データ
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
# @class ConnectorListener ホルダクラス
#
# 複数の ConnectorListener を保持し管理するクラス。
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
  # @brief コンストラクタ
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
  # @brief デストラクタ
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    guard = OpenRTM_aist.Guard.ScopedLock(self._mutex)
    for listener in self._listeners:
      for (k,v) in listener.items():
        if v:
          del k
    return
        
    
  ##
  # @if jp
  #
  # @brief リスナーの追加
  #
  # リスナーを追加する。
  #
  # @param self
  # @param listener 追加するリスナ
  # @param autoclean true:デストラクタで削除する,
  #                  false:デストラクタで削除しない
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
  # @brief リスナーの削除
  #
  # リスナを削除する。
  #
  # @param self
  # @param listener 削除するリスナ
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
  # @brief リスナーへ通知する
  #
  # 登録されているリスナのコールバックメソッドを呼び出す。
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
