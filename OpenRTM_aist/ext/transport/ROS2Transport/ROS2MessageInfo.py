#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file ROS2MessageInfo.py
# @brief ROS2 Message Info class
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

##
# @if jp
# @class ROS2MessageInfoBase
# @brief ROS2��å����������Ǽ���֥������Ȥδ��쥯�饹
# ROS2�ǡ�����̾��IDL�ե�����ѥ�����Ͽ����
#
# @else
# @class ROS2OutPort
# @brief 
#
#
# @endif
class ROS2MessageInfoBase(object):
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Constructor
  #
  # @param self
  #
  # @endif
  def __init__(self):
    pass
  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
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
  def __del__(self):
    pass

  ##
  # @if jp
  # @brief �ǡ����η�̾�����
  #
  # @param self
  # @return ��̾
  #
  # @else
  # @brief 
  #
  #
  # @param self
  # @return
  #
  # @endif
  #
  def datatype(self):
    return None



  

##
# @if jp
# @brief ��å������ξ����Ǽ���֥������������ؿ�
#
# @param data_class ROS2�ǡ�����
# @return ��å������ξ����Ǽ���֥�������
#
# @else
# @brief 
#
# @param data_class 
# @return 
#
# @endif
#
def ros2_message_info(datatype):
  ##
  # @if jp
  # @class ROS2MessageInfo
  # @brief ��å������ξ����Ǽ���饹
  #
  #
  # @else
  # @class ROS2MessageInfo
  # @brief 
  #
  #
  # @endif
  class ROS2MessageInfo(ROS2MessageInfoBase):
    """
    """

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    #
    # @else
    # @brief Constructor
    #
    # @param self
    #
    # @endif
    def __init__(self):
      super(ROS2MessageInfo, self).__init__()
      

    ##
    # @if jp
    # @brief �ǥ��ȥ饯��
    #
    #
    # @param self
    #
    # @else
    #
    # @brief self
    #
    # @endif
    def __del__(self):
      pass

    ##
    # @if jp
    # @brief ��å������η�̾�����
    #
    # @param self
    # @return ��̾
    #
    # @else
    # @brief 
    #
    #
    # @param self
    # @return
    #
    # @endif
    #
    def datatype(self):
      return datatype


  return ROS2MessageInfo



ros2messageinfofactory = None


##
# @if jp
# @class ROS2MessageInfoFactory
# @brief ROS2��å����������Ǽ���֥������������ե����ȥ�
#
# @else
# @class ROS2MessageInfoFactory
# @brief 
#
#
# @endif
class ROS2MessageInfoFactory(OpenRTM_aist.Factory,ROS2MessageInfoBase):
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Constructor
  #
  # @param self
  #
  # @endif
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
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
  def __del__(self):
    pass

  ##
  # @if jp
  # @brief ���󥹥��󥹼���
  #
  #
  # @return ���󥹥���
  #
  # @else
  # @brief 
  #
  #
  # @return
  #
  # @endif
  #
  def instance():
    global ros2messageinfofactory

    if ros2messageinfofactory is None:
      ros2messageinfofactory = ROS2MessageInfoFactory()

    return ros2messageinfofactory

  instance = staticmethod(instance)

