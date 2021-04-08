#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file  InPortCSPConsumer.py
# @brief InPortCSPConsumer class
# @date  $Date: 2016/01/08 $
# @author Nobuhiko Miyamoto


import OpenRTM_aist
import OpenRTM
import CSP


##
# @if jp
# @class InPortCSPConsumer
# @brief InPortCSPConsumer クラス
#
# CSPモデルのチャネルを模擬した入力ポートプロバイダーの実装クラス。
#
#
# @else
# @class InPortCSPConsumer
# @brief InPortCSPConsumer class
#
#
#
# @endif
#
class InPortCSPConsumer(OpenRTM_aist.InPortCorbaConsumerBase):

    """
    """

    ##
    # @if jp
    # @brief コンストラクタ
    #
    # コンストラクタ
    # Interface Typeにはshared_memoryを指定する
    # 共有メモリの空間名はUUIDで作成し、コネクタプロファイルのdataport.shared_memory.addressに保存する
    #
    # self
    #
    # @else
    # @brief Constructor
    #
    # Constructor
    #
    # self
    # @endif
    #
    def __init__(self):
        OpenRTM_aist.InPortCorbaConsumerBase.__init__(
            self, CSP.InPortCsp, "csp_channel")
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("InPortCSPConsumer")
        return

    ##
    # @if jp
    # @brief デストラクタ
    #
    # デストラクタ
    #
    # @param self
    #
    # @else
    # @brief Destructor
    #
    # Destructor
    #
    # @param self
    #
    # @endif
    #
    def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
        self._rtcout.RTC_PARANOID("~InPortCSPConsumer()")
        OpenRTM_aist.InPortCorbaConsumerBase.__del__(self)

    ##
    # @if jp
    # @brief バッファにデータを書き込む
    #
    #
    # @param self
    # @param data 書込対象データ
    # @return リターンコード
    # PORT_OK：正常完了
    # PORT_ERROR：バッファ書き込みエラー、通常は発生しない
    # SEND_FULL：バッファがフル
    # SEND_TIMEOUT：書き込みタイムアウト
    # UNKNOWN_ERROR：その他のエラー
    # CONNECTION_LOST：通信エラー
    #
    # @else
    # @brief
    #
    #
    # @param self
    # @param data
    # @return
    #
    # @endif
    #

    def put(self, data):
        self._rtcout.RTC_PARANOID("put()")

        try:
            outportcsp = self._ptr()
            if outportcsp:
                ret = outportcsp.put(data)
                return self.convertReturnCode(ret)
            return self.CONNECTION_LOST
        except BaseException:
            self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
            return self.CONNECTION_LOST

    ##
    # @if jp
    # @brief 書き込み可能かを接続先のProviderに確認
    #
    #
    # @param self
    # @param retry True：再検索、False：通常の書き込み確認
    # @return True：書き込み可能、False：書き込み不可
    #
    # @else
    # @brief
    #
    #
    # @param self
    # @param retry
    # @return
    #
    # @endif
    #

    def isWritable(self, retry=False):
        self._rtcout.RTC_PARANOID("isWritable()")
        try:
            outportcsp = self._ptr()
            if outportcsp:
                return outportcsp.is_writable(retry)
            return False
        except BaseException:
            self._rtcout.RTC_WARN("Exception caught from InPort.isWritable().")
            self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
            return False

    ##
    # @if jp
    # @brief リターンコード変換
    # @else
    # @brief Return codes conversion
    # @endif
    #
    # ReturnCode convertReturnCode(OpenRTM::PortStatus ret)

    def convertReturnCode(self, ret):
        if ret == OpenRTM.PORT_OK:
            return self.PORT_OK

        elif ret == OpenRTM.PORT_ERROR:
            return self.PORT_ERROR

        elif ret == OpenRTM.BUFFER_FULL:
            return self.SEND_FULL

        elif ret == OpenRTM.BUFFER_TIMEOUT:
            return self.SEND_TIMEOUT

        elif ret == OpenRTM.UNKNOWN_ERROR:
            return self.UNKNOWN_ERROR

        else:
            return self.UNKNOWN_ERROR


def InPortCSPConsumerInit():
    factory = OpenRTM_aist.InPortConsumerFactory.instance()
    factory.addFactory("csp_channel",
                       OpenRTM_aist.InPortCSPConsumer)
