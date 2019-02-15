#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ByteDataStreamBase.py
# @brief ByteData Stream Base class
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
# @class 
#
#
# @else
# @brief 
#
#
# @endif
class ByteDataStreamBase:
  """
  """
  SERIALIZE_OK = 0
  SERIALIZE_ERROR = 1
  SERIALIZE_NOTFOUND = 2
  SERIALIZE_NOT_SUPPORT_ENDIAN = 3


  ##
  # @if jp
  # @brief ��������
  #
  # 
  # @param prop �������
  #
  # @else
  #
  # @brief Initializing configuration
  #
  #
  # @param prop Configuration information
  #
  # @endif
  ## virtual ReturnCode init(coil::Properties& prop) = 0;
  def init(self, prop):
    pass



  ##
  # @if jp
  # @brief ����ǥ����������
  #
  # 
  # @param little_endian ��ȥ륨��ǥ�����(True)���ӥå�����ǥ�����(False)
  #
  # @else
  #
  # @brief 
  #
  #
  # @param little_endian 
  #
  # @endif
  ## virtual void isLittleEndian(bool little_endian) = 0;
  def isLittleEndian(self, little_endian):
    pass


  ##
  # @if jp
  # @brief �ǡ�������沽
  #
  # 
  # @param data ��沽���Υǡ���
  # @return SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  #
  # @else
  #
  # @brief 
  #
  #
  # @param data 
  # @return
  #
  # @endif
  ## virtual bool serialize(const DataType& data) = 0;
  def serialize(self, data):
    return ByteDataStreamBase.SERIALIZE_NOTFOUND, ""


  ##
  # @if jp
  # @brief �ǡ��������沽
  #
  # @param cdr �Х�����
  # @param data_type �ǡ�����
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value�����沽��Υǡ���
  #
  # @else
  #
  # @brief 
  #
  # @param cdr
  # @param data_type 
  # @return 
  #
  # @endif
  ## virtual bool deserialize(DataType& data) = 0;
  def deserialize(self, cdr, data_type):
    return ByteDataStreamBase.SERIALIZE_NOTFOUND, data_type




serializerfactory = None

class SerializerFactory(OpenRTM_aist.Factory,ByteDataStreamBase):
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    pass


  def __del__(self):
    pass


  def instance():
    global serializerfactory

    if serializerfactory is None:
      serializerfactory = SerializerFactory()

    return serializerfactory

  instance = staticmethod(instance)
