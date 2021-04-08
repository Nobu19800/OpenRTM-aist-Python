#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##
# @file  OutPortSHMProvider.py
# @brief OutPortSHMProvider class
# @date  $Date: 2016-01-12 $
# @author Nobuhiko Miyamoto
#
#


import OpenRTM_aist
import OpenRTM
import OpenRTM__POA
from omniORB import CORBA

import threading

##
# @if jp
# @class OutPortSHMConsumer
#
# @brief OutPortSHMConsumer クラス
#
# 通信手段に 共有メモリ を利用した出力ポートプロバイダーの実装クラス。
#
#
# @else
# @class OutPortSHMConsumer
#
# @brief OutPortSHMConsumer class
#
#
# @endif
#


class OutPortSHMConsumer(OpenRTM_aist.OutPortCorbaConsumerBase):
    """
    """

    ##
    # @if jp
    # @brief コンストラクタ
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
        OpenRTM_aist.OutPortCorbaConsumerBase.__init__(
            self, OpenRTM__POA.PortSharedMemory, "shared_memory")
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortSHMConsumer")

        self._shmem = OpenRTM_aist.SharedMemory()

        self._mutex = threading.RLock()

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
        self._rtcout.RTC_PARANOID("~OutPortSHMConsumer()")
        OpenRTM_aist.OutPortCorbaConsumerBase.__del__(self)
        try:
            if not self._ptr():
                self._ptr().close_memory(True)
        except BaseException:
            self._rtcout.RTC_WARN(
                "Exception caught from PortSharedMemory.close_memory().")
            self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

        oid = OpenRTM_aist.Manager.instance().getPOA().servant_to_id(self._shmem)
        OpenRTM_aist.Manager.instance().getPOA().deactivate_object(oid)

    def setObject(self, obj):
        if OpenRTM_aist.CorbaConsumer.setObject(self, obj):
            portshmem = self._ptr()
            if portshmem:
                portshmem.setInterface(self._shmem._this())
                return True
        return False

    def setBuffer(self, buffer):
        self._rtcout.RTC_TRACE("setBuffer()")
        self._buffer = buffer
        return

    def setListener(self, info, listeners):
        self._rtcout.RTC_TRACE("setListener()")
        self._listeners = listeners
        self._profile = info
        return

    ##
    # @if jp
    # @brief データを読み出す
    #
    # 設定されたデータを読み出す。
    #
    # データのサイズは共有メモリも先頭8byteから取得する
    # データは共有メモリから読み込む
    #
    # @param data 読み出したデータを受け取るオブジェクト
    #
    # @return リターンコード
    #
    # @else
    # @brief Read data
    #
    # Read set data
    #
    # @param data Object to receive the read data
    #
    # @return Return Code
    #
    # @endif
    #
    # virtual ReturnCode get(cdrMemoryStream& data);

    def get(self):
        self._rtcout.RTC_PARANOID("get()")

        try:
            portshmem = self._ptr()

            guard = OpenRTM_aist.ScopedLock(self._mutex)
            ret = portshmem.get()

            data = None

            if ret == OpenRTM.PORT_OK:
                self._rtcout.RTC_DEBUG("get() successful")

                shm_data = self._shmem.read()

                data = shm_data
                self.onReceived(data)
                self.onBufferWrite(data)

                if self._buffer.full():
                    self._rtcout.RTC_INFO("InPort buffer is full.")
                    self.onBufferFull(data)
                    self.onReceiverFull(data)

                self._buffer.put(data)
                self._buffer.advanceWptr()
                self._buffer.advanceRptr()

                return self.PORT_OK, data
            return self.convertReturn(ret, data)

        except BaseException:
            self._rtcout.RTC_WARN("Exception caught from OutPort.get().")
            self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
            return self.CONNECTION_LOST, None

    ##
    # @if jp
    # @brief リターンコード変換 (DataPortStatus -> BufferStatus)
    # @else
    # @brief Return codes conversion
    # @endif
    #
    # ReturnCode convertReturn(::OpenRTM::PortStatus status,
    #                          const cdrMemoryStream& data)

    def convertReturn(self, status, data):
        if status == OpenRTM.PORT_OK:
            # never comes here
            return self.PORT_OK, data

        elif status == OpenRTM.PORT_ERROR:
            self.onSenderError()
            return self.PORT_ERROR, data

        elif status == OpenRTM.BUFFER_FULL:
            # never comes here
            return self.BUFFER_FULL, data

        elif status == OpenRTM.BUFFER_EMPTY:
            self.onSenderEmpty()
            return self.BUFFER_EMPTY, data

        elif status == OpenRTM.BUFFER_TIMEOUT:
            self.onSenderTimeout()
            return self.BUFFER_TIMEOUT, data

        elif status == OpenRTM.UNKNOWN_ERROR:
            self.onSenderError()
            return self.UNKNOWN_ERROR, data

        else:
            self.onSenderError()
            return self.UNKNOWN_ERROR, data

    ##
    # @brief Connector data listener functions
    #
    # inline void onBufferWrite(const cdrMemoryStream& data)

    def onBufferWrite(self, data):
        if self._listeners is not None and self._profile is not None:
            _, data = self._listeners.notifyData(
                OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE, self._profile, data)

        return data

    # inline void onBufferFull(const cdrMemoryStream& data)

    def onBufferFull(self, data):
        if self._listeners is not None and self._profile is not None:
            _, data = self._listeners.notifyData(
                OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL, self._profile, data)

        return data

    # inline void onReceived(const cdrMemoryStream& data)

    def onReceived(self, data):
        if self._listeners is not None and self._profile is not None:
            _, data = self._listeners.notifyData(
                OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED, self._profile, data)

        return data

    # inline void onReceiverFull(const cdrMemoryStream& data)

    def onReceiverFull(self, data):
        if self._listeners is not None and self._profile is not None:
            _, data = self._listeners.notifyData(
                OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL, self._profile, data)

        return data

    ##
    # @brief Connector listener functions
    #
    # inline void onSenderEmpty()

    def onSenderEmpty(self):
        if self._listeners is not None and self._profile is not None:
            self._listeners.notify(
                OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY, self._profile)

        return

    # inline void onSenderTimeout()

    def onSenderTimeout(self):
        if self._listeners is not None and self._profile is not None:
            self._listeners.notify(
                OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT, self._profile)

        return

    # inline void onSenderError()

    def onSenderError(self):
        if self._listeners is not None and self._profile is not None:
            self._listeners.notify(
                OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR, self._profile)

        return


def OutPortSHMConsumerInit():
    factory = OpenRTM_aist.OutPortConsumerFactory.instance()
    factory.addFactory("shared_memory",
                       OpenRTM_aist.OutPortSHMConsumer)
    return
