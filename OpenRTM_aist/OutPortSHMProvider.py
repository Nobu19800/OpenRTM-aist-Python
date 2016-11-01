#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortSHMProvider.py
# @brief OutPortSHMProvider class
# @date  $Date: 2016-01-12 $
# @author Nobuhiko Miyamoto
#
#

import sys
from omniORB import *
from omniORB import any

import OpenRTM_aist
import OpenRTM__POA,OpenRTM


##
# @if jp
# @class OutPortSHMProvider
# @brief OutPortSHMProvider クラス
#
# OutPortProvider 
#
# 通信手段に 共有メモリ を利用した出力ポートプロバイダの実装クラス。
#
#
# @else
# @class OutPortSHMProvider
# @brief OutPortSHMProvider class
#
#
#
# @endif
#
class OutPortSHMProvider(OpenRTM_aist.OutPortProvider,OpenRTM_aist.SharedMemory):
  ##
  # @if jp
  # @brief コンストラクタ
  # 共有メモリの空間名はUUIDで作成し、コネクタプロファイルのdataport.shared_memory.addressに保存する
  #
  # コンストラクタ
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.OutPortProvider.__init__(self)
    OpenRTM_aist.SharedMemory.__init__(self)
    self.setInterfaceType("shared_memory")
    
    self._objref = self._this()
    self._buffer = None
    orb = OpenRTM_aist.Manager.instance().getORB()
    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.outport_ior",
                                                      orb.object_to_string(self._objref)))
    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.outport_ref",
                                                      self._objref))
    self._listeners = None
    self._connector = None
    self._profile   = None
    

    self._shm_address = str(OpenRTM_aist.uuid1())
    
    self._endian = True

    

    
    
    

    return


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    return

  ##
  # @if jp
  # @brief 終了処理
  #
  # @else
  # @brief 
  #
  # 
  #
  # @endif
  #
  def exit(self):
    oid = self._default_POA().servant_to_id(self)
    self._default_POA().deactivate_object(oid)
  
  # virtual void init(coil::Properties& prop);
  def init(self, prop):

    ds = prop.getProperty("shem_default_size")
    self._memory_size = self.string_to_MemorySize(ds)


    if prop.hasKey("serializer"):
      endian = prop.getProperty("serializer.cdr.endian")
      if not endian:
        self._rtcout.RTC_ERROR("init(): endian is not set.")
        
      endian = OpenRTM_aist.split(endian, ",")
      endian = OpenRTM_aist.normalize(endian)
      if endian == "little":
        self._endian = True
      elif endian == "big":
        self._endian = False

    else:
      self._endian = True
    
    return
    
  def setBuffer(self, buffer):
    self._buffer = buffer
    return
  
  def setListener(self, info, listeners):
    self._profile = info
    self._listeners = listeners
    return
  
  def setConnector(self, connector):
    self._connector = connector
    return

  
    
  
  ##
  # @if jp
  # @brief バッファからデータを取得する
  #
  # @return (リターンコード、取得データ)
  #
  # @else
  # @brief Get data from the buffer
  #
  #
  # @return 
  #
  # @endif
  #
  # virtual ::OpenRTM::PortStatus get(::OpenRTM::CdrData_out data);
  def get(self):
    self._rtcout.RTC_PARANOID("OutPortSHMProvider.get()")
    
    if not self._buffer:
      self.onSenderError()
      return OpenRTM.UNKNOWN_ERROR

    try:
      if self._buffer.empty():
        self._rtcout.RTC_ERROR("buffer is empty.")
        return OpenRTM.BUFFER_EMPTY

      cdr = [None]
      ret = self._buffer.read(cdr)
      
      if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
        if not cdr[0]:
          self._rtcout.RTC_ERROR("buffer is empty.")
          return OpenRTM.BUFFER_EMPTY
      
    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      return OpenRTM.UNKNOWN_ERROR


    self.setEndian(self._endian)
    self.create_memory(self._memory_size, self._shm_address)
    self.write(cdr[0])
    
    return self.convertReturn(ret, cdr[0])

    
  def onBufferRead(self, data):
    if self._listeners and self._profile:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ].notify(self._profile, data)
    return

  def onSend(self, data):
    if self._listeners and self._profile:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    return    
    
    

  def onBufferEmpty(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY].notify(self._profile)
    return
  
  def onBufferReadTimeout(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_READ_TIMEOUT].notify(self._profile)
    return

  def onSenderEmpty(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY].notify(self._profile)
    return

  def onSenderTimeout(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT].notify(self._profile)
    return

  def onSenderError(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)
    return

  def convertReturn(self, status, data):
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      self.onBufferRead(data)
      self.onSend(data)
      return OpenRTM.PORT_OK
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      self.onSenderError()
      return OpenRTM.PORT_ERROR
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      # never come here
      return OpenRTM.BUFFER_FULL

    elif status == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      self.onBufferEmpty()
      self.onSenderEmpty()
      return OpenRTM.BUFFER_EMPTY

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      self.onSenderError()
      return OpenRTM.PORT_ERROR
    
    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferReadTimeout()
      self.onSenderTimeout()
      return OpenRTM.BUFFER_TIMEOUT
    
    else:
      return OpenRTM.UNKNOWN_ERROR
    
    self.onSenderError()
    return OpenRTM.UNKNOWN_ERROR




def OutPortSHMProviderInit():
  factory = OpenRTM_aist.OutPortProviderFactory.instance()
  factory.addFactory("shared_memory",
                     OpenRTM_aist.OutPortSHMProvider,
                     OpenRTM_aist.Delete)
