#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file OpenSpliceSerializer.py
# @brief OpenSplice Serializer class
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
import omniORB

import struct
import OpenSpliceMessageInfo
import RTC
import ddsutil
import os
import site
import sys


##
# @if jp
# @brief omniORB�Υǡ�������OpenSplice�Υǡ������Ѵ�
# omniORB�Υǡ������ξ����_NP_RepositoryId�����������
# ������줿����̾���ͤ��Ǽ���Ƥ���
#
# @param self
# @param data �Ѵ����Υǡ���(omniORB)
# @param gen_info OpenSplice�Υǡ�����Info���֥�������
# @return �Ѵ���Υǡ���(OpenSplice)
# 
#
# @else
# @brief 
#
# @param self
# @param data 
# @param gen_info 
# @return 
#
# @endif
def OmniDataToDDSData(data, gen_info):
  desc=omniORB.findType(data._NP_RepositoryId)
  if desc[0] == omniORB.tcInternal.tv_struct:
    arg = {}
    for i in  range(4, len(desc), 2):
      attr = desc[i]
      attr_type = desc[i+1]
      if isinstance(attr_type, int):
        arg[attr] = data.__dict__[attr]
      else:
        cdata = data.__dict__[attr]
        data_name = cdata._NP_RepositoryId
        data_name = data_name.split(":")[1]
        data_name = data_name.replace("/","::")
        datatype = gen_info.get_class(data_name)
        cv = OmniDataToDDSData(cdata, gen_info)
        arg[attr] = datatype(**cv)
    return arg

if sys.version_info[0] == 3:
    long = int


##
# @if jp
# @brief OpenSplice�Υǡ�������omniORB�Υǡ������Ѵ�
# OpenSplice�Υǡ�����xml.etree.ElementTree���������Ƥ��ꡢ
# ElementTree��������̾����������ͤ��Ǽ����
#
# @param self
# @param ddsdata �Ѵ����Υǡ���(OpenSplice)
# @param omnidata �ѹ��оݤΥǡ���(omniORB)
# 
#
# @else
# @brief 
#
# @param self
# @param ddsdata 
# @param omnidata 
#
# @endif
def DDSDataToOmniData(ddsdata, omnidata):
  for k in ddsdata._members.keys():
    v = ddsdata.__dict__[k]
    if isinstance(v, int):
      omnidata.__dict__[k] = v
    elif isinstance(v, long):
      omnidata.__dict__[k] = v
    elif isinstance(v, float):
      omnidata.__dict__[k] = v
    elif isinstance(v, str):
      omnidata.__dict__[k] = v
    else:
      DDSDataToOmniData(v, omnidata.__dict__[k])



##
# @if jp
# @class OpenSpliceSerializer
# @brief OpenSplice�ѥ��ꥢ�饤��
#
# @else
# @class OpenSpliceSerializer
# @brief 
#
#
# @endif
class OpenSpliceSerializer(OpenRTM_aist.ByteDataStreamBase):
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
    pass

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
  # @brief �ǡ������Ѵ�(omniORB->OpenSplice)
  #
  # 
  # @param data omniORB����Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value��OpenSplice����Υǡ���
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
  def serialize(self, data):
    factory = OpenSpliceMessageInfo.OpenSpliceMessageInfoFactory.instance()
    info = factory.createObject(data._NP_RepositoryId)
    if info:
      datatype = info.datatype()
      idlFile = info.idlFile()
      factory.deleteObject(info)
      try:
        gen_info = ddsutil.get_dds_classes_from_idl(idlFile, datatype)
        osdata = gen_info.topic_data_class(**OmniDataToDDSData(data, gen_info))
        if osdata:
          return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, osdata
        else:
          return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_ERROR, osdata
      except:
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_ERROR, None
    else:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOTFOUND, None

  ##
  # @if jp
  # @brief �ǡ������Ѵ�(OpenSplice->omniORB)
  #
  # @param bdata OpenSplice����Υǡ���
  # @param data_type omniORB����Υǡ�����
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value��omniORB����Υǡ���
  #
  # @else
  #
  # @brief 
  #
  # @param bdata
  # @param data_type 
  # @return 
  #
  # @endif
  def deserialize(self, bdata, data_type):
    try:
      DDSDataToOmniData(bdata, data_type)
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data_type
    except:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_ERROR, data_type

##
# @if jp
# @brief OpenSplice�ǻ��Ѥ���ǡ��������ɲä���
# OpenSplice��omniORB��Ʊ���IDL�ե��������������ǡ���������Ѥ��뤬��
# omniORB�Υǡ���������ɤ�IDL�ե��������������ǡ������ʤΤ���������뤳�ȤϤǤ��ʤ����ᡢ
# omniORB�Υǡ�����̾��OpenSplice�Υǡ�����̾��IDL�ե�����̾���Ϣ�դ���������Ͽ����
#
# @param datatype omniORB����Υǡ�����̾
# @param idlfile IDL�ե�����Υѥ�
#
# @else
#
# @brief 
#
# @param datatype 
# @param idlfile 
#
# @endif
def addDataType(datatype, idlfile):
  name = datatype._NP_RepositoryId
  data_name = name.split(":")[1]
  data_name = data_name.replace("/","::")
  OpenSpliceMessageInfo.OpenSpliceMessageInfoFactory.instance().addFactory(name,
                                                      OpenSpliceMessageInfo.opensplice_message_info(data_name, idlfile),
                                                      OpenRTM_aist.Delete)




##
# @if jp
# @brief ���ꥢ�饤����������ǡ�����������Ͽ
#
#
# @else
# @brief 
#
#
# @endif
#
def OpenSpliceSerializerInit():
  OpenRTM_aist.SerializerFactory.instance().addFactory("opensplice",
                                                      OpenSpliceSerializer,
                                                      OpenRTM_aist.Delete)

  OpenRTM_dir = OpenRTM_aist.__path__[0]

  idl_dir = os.path.join(OpenRTM_dir, "RTM_IDL")
  basicdatatypefile = os.path.join(idl_dir, "BasicDataType.idl")
  extendeddatatypes = os.path.join(idl_dir, "ExtendedDataTypes.idl")
  interfacedataTypes = os.path.join(idl_dir, "InterfaceDataTypes.idl")
  addDataType(RTC.TimedState, basicdatatypefile)
  addDataType(RTC.TimedShort, basicdatatypefile)
  addDataType(RTC.TimedLong, basicdatatypefile)
  addDataType(RTC.TimedUShort, basicdatatypefile)
  addDataType(RTC.TimedULong, basicdatatypefile)
  addDataType(RTC.TimedFloat, basicdatatypefile)
  addDataType(RTC.TimedDouble, basicdatatypefile)
  addDataType(RTC.TimedChar, basicdatatypefile)
  addDataType(RTC.TimedWChar, basicdatatypefile)
  addDataType(RTC.TimedBoolean, basicdatatypefile)
  addDataType(RTC.TimedOctet, basicdatatypefile)
  addDataType(RTC.TimedString, basicdatatypefile)
  addDataType(RTC.TimedWString, basicdatatypefile)
  addDataType(RTC.TimedShortSeq, basicdatatypefile)
  addDataType(RTC.TimedLongSeq, basicdatatypefile)
  addDataType(RTC.TimedUShortSeq, basicdatatypefile)
  addDataType(RTC.TimedULongSeq, basicdatatypefile)
  addDataType(RTC.TimedFloatSeq, basicdatatypefile)
  addDataType(RTC.TimedDoubleSeq, basicdatatypefile)
  addDataType(RTC.TimedCharSeq, basicdatatypefile)
  addDataType(RTC.TimedWCharSeq, basicdatatypefile)
  addDataType(RTC.TimedBooleanSeq, basicdatatypefile)
  addDataType(RTC.TimedOctetSeq, basicdatatypefile)
  addDataType(RTC.TimedStringSeq, basicdatatypefile)
  addDataType(RTC.TimedWStringSeq, basicdatatypefile)
  addDataType(RTC.TimedRGBColour, extendeddatatypes)
  addDataType(RTC.TimedPoint2D, extendeddatatypes)
  addDataType(RTC.TimedVector2D, extendeddatatypes)
  addDataType(RTC.TimedPose2D, extendeddatatypes)
  addDataType(RTC.TimedVelocity2D, extendeddatatypes)
  addDataType(RTC.TimedAcceleration2D, extendeddatatypes)
  addDataType(RTC.TimedPoseVel2D, extendeddatatypes)
  addDataType(RTC.TimedSize2D, extendeddatatypes)
  addDataType(RTC.TimedGeometry2D, extendeddatatypes)
  addDataType(RTC.TimedCovariance2D, extendeddatatypes)
  addDataType(RTC.TimedPointCovariance2D, extendeddatatypes)
  addDataType(RTC.TimedCarlike, extendeddatatypes)
  addDataType(RTC.TimedSpeedHeading2D, extendeddatatypes)
  addDataType(RTC.TimedPoint3D, extendeddatatypes)
  addDataType(RTC.TimedVector3D, extendeddatatypes)
  addDataType(RTC.TimedOrientation3D, extendeddatatypes)
  addDataType(RTC.TimedPose3D, extendeddatatypes)
  addDataType(RTC.TimedVelocity3D, extendeddatatypes)
  addDataType(RTC.TimedAngularVelocity3D, extendeddatatypes)
  addDataType(RTC.TimedAcceleration3D, extendeddatatypes)
  addDataType(RTC.TimedAngularAcceleration3D, extendeddatatypes)
  addDataType(RTC.TimedPoseVel3D, extendeddatatypes)
  addDataType(RTC.TimedSize3D, extendeddatatypes)
  addDataType(RTC.TimedGeometry3D, extendeddatatypes)
  addDataType(RTC.TimedCovariance3D, extendeddatatypes)
  addDataType(RTC.TimedSpeedHeading3D, extendeddatatypes)
  addDataType(RTC.TimedOAP, extendeddatatypes)
  addDataType(RTC.ActArrayActuatorPos, interfacedataTypes)
  addDataType(RTC.ActArrayActuatorSpeed, interfacedataTypes)
  addDataType(RTC.ActArrayActuatorCurrent, interfacedataTypes)
  addDataType(RTC.ActArrayState, interfacedataTypes)
  addDataType(RTC.CameraImage, interfacedataTypes)
  addDataType(RTC.Fiducials, interfacedataTypes)
  addDataType(RTC.GPSData, interfacedataTypes)
  addDataType(RTC.GripperState, interfacedataTypes)
  addDataType(RTC.INSData, interfacedataTypes)
  addDataType(RTC.LimbState, interfacedataTypes)
  addDataType(RTC.Hypotheses2D, interfacedataTypes)
  addDataType(RTC.Hypotheses3D, interfacedataTypes)
  addDataType(RTC.Features, interfacedataTypes)
  addDataType(RTC.MultiCameraImages, interfacedataTypes)
  addDataType(RTC.Path2D, interfacedataTypes)
  addDataType(RTC.Path3D, interfacedataTypes)
  addDataType(RTC.PointCloud, interfacedataTypes)
  addDataType(RTC.PanTiltAngles, interfacedataTypes)
  addDataType(RTC.PanTiltState, interfacedataTypes)
  addDataType(RTC.RangeData, interfacedataTypes)
  addDataType(RTC.IntensityData, interfacedataTypes)

