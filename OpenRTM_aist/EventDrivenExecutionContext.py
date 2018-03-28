#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file EventDrivenExecutionContext.py
# @brief EventDrivenExecutionContext class
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
# @class PeriodicExecutionContext
# @brief PeriodicExecutionContext ���饹
#
# Periodic EventDrivenExecutionContext���饹��
#
# @since 2.0.0
#
# @else
# @class EventDrivenExecutionContext
# @brief EventDrivenExecutionContext class
# @endif
class EventDrivenExecutionContext(OpenRTM_aist.PeriodicExecutionContext):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # ���ꤵ�줿�ͤ�ץ�ե���������ꤹ�롣
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    OpenRTM_aist.PeriodicExecutionContext.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.eventdriven_ec")
    self.setKind(RTC.EVENT_DRIVEN)

    return



##
# @if jp
# @brief ExecutionContext ����������
#
# ExecutionContext ��ư�ѥե����ȥ����Ͽ���롣
#
# @param manager �ޥ͡����㥪�֥�������
#
# @else
#
# @endif
def EventDrivenExecutionContextInit(manager):
  OpenRTM_aist.ExecutionContextFactory.instance().addFactory("EventDrivenExecutionContext",
                                                             OpenRTM_aist.EventDrivenExecutionContext,
                                                             OpenRTM_aist.ECDelete)
  return
