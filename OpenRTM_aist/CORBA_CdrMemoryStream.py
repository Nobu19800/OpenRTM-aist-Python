#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file CORBA_CdrMemoryStream.py
# @brief CORBA Cdr Memory Stream class
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

import sys
import OpenRTM_aist
from omniORB import cdrMarshal
from omniORB import cdrUnmarshal
from omniORB import any

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
class CORBA_CdrMemoryStream(OpenRTM_aist.ByteDataStreamBase):
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
    self._endian = None

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
    self._endian = little_endian


  ##
  # @if jp
  # @brief �ǡ�������沽
  #
  # 
  # @param data ��沽���Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # cdr���Х�����
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
    if self._endian is not None:
      try:
        cdr = cdrMarshal(any.to_any(data).typecode(), data, self._endian)
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, cdr
      except:
        if sys.version_info[0] == 3:
          return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_ERROR, b""
        else:
          return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_ERROR, ""
    else:
      if sys.version_info[0] == 3:
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, b""
      else:
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, ""


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
    if self._endian is not None:
      try:
        data = cdrUnmarshal(any.to_any(data_type).typecode(), cdr ,self._endian)
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data
      except:
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_ERROR, data_type
    else:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, data_type



def CORBA_CdrMemoryStreamInit():
  OpenRTM_aist.SerializerFactory.instance().addFactory("corba",
                                                      OpenRTM_aist.CORBA_CdrMemoryStream,
                                                      OpenRTM_aist.Delete)

