#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file OpenSpliceMessageInfo.py
# @brief OpenSplice Message Info class
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
# @class OpenSpliceMessageInfoBase
# @brief OpenSplice��å����������Ǽ���֥������Ȥδ��쥯�饹
# OpenSplice�ǡ�����̾��IDL�ե�����ѥ�����Ͽ����
#
# @else
# @class OpenSpliceOutPort
# @brief 
#
#
# @endif
class OpenSpliceMessageInfoBase(object):
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
    return ""

  ##
  # @if jp
  # @brief IDL�ե�����Υѥ������
  #
  # @param self
  # @return IDL�ե�����Υѥ�
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
  def idlFile(self):
    return ""

  

##
# @if jp
# @brief ��å������ξ����Ǽ���֥������������ؿ�
#
# @param data_class OpenSplice�ǡ�����
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
def opensplice_message_info(datatype, idlfile):
  ##
  # @if jp
  # @class OpenSpliceMessageInfo
  # @brief ��å������ξ����Ǽ���饹
  #
  #
  # @else
  # @class OpenSpliceMessageInfo
  # @brief 
  #
  #
  # @endif
  class OpenSpliceMessageInfo(OpenSpliceMessageInfoBase):
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
      super(OpenSpliceMessageInfo, self).__init__()
      

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

    ##
    # @if jp
    # @brief IDL�ե�����Υѥ������
    #
    # @param self
    # @return IDL�ե�����Υѥ�
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
    def idlFile(self):
      return idlfile

  return OpenSpliceMessageInfo



opensplicemessageinfofactory = None


##
# @if jp
# @class OpenSpliceMessageInfoFactory
# @brief OpenSplice��å����������Ǽ���֥������������ե����ȥ�
#
# @else
# @class OpenSpliceMessageInfoFactory
# @brief 
#
#
# @endif
class OpenSpliceMessageInfoFactory(OpenRTM_aist.Factory,OpenSpliceMessageInfoBase):
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
    global opensplicemessageinfofactory

    if opensplicemessageinfofactory is None:
      opensplicemessageinfofactory = OpenSpliceMessageInfoFactory()

    return opensplicemessageinfofactory

  instance = staticmethod(instance)

