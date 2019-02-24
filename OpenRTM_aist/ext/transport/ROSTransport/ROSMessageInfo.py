#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ROSMessageInfo.py
# @brief ROS Message Info class
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
# @class ROSMessageInfoBase
# @brief ROS��å����������Ǽ���֥������Ȥδ��쥯�饹
#
# @else
# @class ROSOutPort
# @brief 
#
#
# @endif
class ROSMessageInfoBase(object):
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
    return ""

  ##
  # @if jp
  # @brief ��å�������MD5�����å���������
  #
  # @param self
  # @return MD5�����å�����
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
  def md5sum(self):
    return ""

  ##
  # @if jp
  # @brief ��å������ξܺ����������
  #
  # @param self
  # @return �ܺ�����
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
  def message_definition(self):
    return ""
  

##
# @if jp
# @brief ��å������ξ����Ǽ���֥������������ؿ�
#
# @param data_class ROS��å�������
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
def ros_message_info(data_class):
  ##
  # @if jp
  # @class ROSMessageInfo
  # @brief ��å������ξ����Ǽ���饹
  #
  #
  # @else
  # @class ROSMessageInfo
  # @brief 
  #
  #
  # @endif
  class ROSMessageInfo(ROSMessageInfoBase):
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
      super(ROSMessageInfo, self).__init__()
      

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
      return data_class._type

    ##
    # @if jp
    # @brief ��å�������MD5�����å���������
    #
    # @param self
    # @return MD5�����å�����
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
    def md5sum(self):
      return data_class._md5sum

    ##
    # @if jp
    # @brief ��å�������MD5�����å���������
    #
    # @param self
    # @return MD5�����å�����
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
    def message_definition(self):
      return data_class._full_text
  return ROSMessageInfo



rosmessageinfofactory = None


##
# @if jp
# @class ROSMessageInfoFactory
# @brief ROS��å����������Ǽ���֥������������ե����ȥ�
#
# @else
# @class ROSMessageInfoFactory
# @brief 
#
#
# @endif
class ROSMessageInfoFactory(OpenRTM_aist.Factory,ROSMessageInfoBase):
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
    global rosmessageinfofactory

    if rosmessageinfofactory is None:
      rosmessageinfofactory = ROSMessageInfoFactory()

    return rosmessageinfofactory

  instance = staticmethod(instance)

