#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ROSTransport.py
# @brief ROS Transport class
# @date $Date$
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2019
#     Noriaki Ando
#     Robot Innovation Research Center,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import OpenRTM_aist
import ROSInPort
import ROSOutPort
import ROSSerializer
from ROSTopicManager import ROSTopicManager



##
# @if jp
# @class ManagerActionListener
# @brief OpenSpliceTopicManager�˴ؤ���ޥ͡����㥢�������ꥹ��
#
#
# @else
# @class ManagerActionListener
# @brief 
#
#
# @endif
class ManagerActionListener:
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  #
  # @param self
  #
  # @else
  #
  # @brief self
  #
  # @endif
  def __init__(self):
    pass

  def preShutdown(self):
    pass
  ##
  # @if jp
  # @brief RTM�ޥ͡����㽪λ���ROSTopicManager�ν�λ������¹�
  #
  #
  # @param self
  #
  # @else
  #
  # @brief self
  #
  # @endif
  def postShutdown(self):
    ROSTopicManager.shutdown_global()

  def preReinit(self):
    pass

  def postReinit(self):
    pass


##
# @if jp
# @brief �⥸�塼����Ͽ�ؿ�
#
#
# @else
# @brief 
#
#
# @endif
#
def ROSTransportInit(mgr):
  ROSInPort.ROSInPortInit()
  ROSOutPort.ROSOutPortInit()
  ROSSerializer.ROSSerializerInit()

  mgr.addManagerActionListener(ManagerActionListener())

