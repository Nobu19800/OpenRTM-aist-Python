#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# @file ROS2Serializer.py
# @brief ROS2 Serializer class
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
import ROS2MessageInfo
import RTC
import rclpy
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from std_msgs.msg import Int8
from std_msgs.msg import Int16
from std_msgs.msg import Int32
from std_msgs.msg import Int64
from std_msgs.msg import UInt8
from std_msgs.msg import UInt16
from std_msgs.msg import UInt32
from std_msgs.msg import UInt64
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import UInt16MultiArray
from std_msgs.msg import UInt32MultiArray
from std_msgs.msg import UInt64MultiArray
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import QuaternionStamped
from geometry_msgs.msg import Vector3Stamped
from sensor_msgs.msg import Image





##
# @if jp
# @brief ñ��ǡ���������ʤɤδ��ܥ�å���������ROS2���ꥢ�饤���������ؿ�
#
# @param message_type ROS2��å�������
#
# @else
# @brief 
#
# @param message_type 
#
# @endif
#
def ros2_basic_data(message_type):
  ##
  # @if jp
  # @class ROS2BasicData
  # @brief ñ��ǡ���������ʤɤδ��ܥ�å�������
  #
  # @else
  # @class ROS2BasicData
  # @brief 
  #
  #
  # @endif
  class ROS2BasicData(OpenRTM_aist.ByteDataStreamBase):
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
    # @brief �ǡ������Ѵ�(omniORB->ROS2)
    #
    # 
    # @param data omniORB�Υǡ���
    # @return ret��value
    # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
    # value��ROS2�Υǡ���
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
      msg = message_type()
      field_type = msg.get_fields_and_field_types()["data"]
      if field_type == "int8" or field_type == "int16" or field_type == "int32" or field_type == "int64":
          msg.data = int(data.data)
      elif field_type == "uint8" or field_type == "uint16" or field_type == "uint32" or field_type == "uint64":
          msg.data = int(data.data)
      elif field_type == "float32" or field_type == "float64":
          msg.data = float(data.data)
      elif field_type == "int8[]" or field_type == "int16[]" or field_type == "int32[]" or field_type == "int64[]":
          msg.data = list(map(int, data.data))
      elif field_type == "uint8[]" or field_type == "uint16[]" or field_type == "uint32[]" or field_type == "uint64[]":
          msg.data = list(map(int, data.data))
      elif field_type == "float32[]" or field_type == "float64[]":
          msg.data = list(map(float, data.data))
      else: 
          msg.data = data.data

      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, msg

    ##
    # @if jp
    # @brief �ǡ������Ѵ�(ROS2->omniORB)
    #
    # @param self 
    # @param bdata ROS2�Υǡ���
    # @param data_type omniORB�Υǡ���
    # @return ret��value
    # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
    # value���Ѵ���Υǡ���
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
    def deserialize(self, bdata, data_type):
      try:
        if isinstance(data_type.data, bytes):
         data_type.data = bytes(bdata.data)
        elif isinstance(data_type.data, str):
          data_type.data = str(bdata.data)
        elif isinstance(data_type.data, list):
          data_type.data = list(bdata.data)
        elif isinstance(data_type.data, tuple):
          data_type.data = tuple(bdata.data)
        else:
          data_type.data = bdata.data
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data_type
      except:
        return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, data_type
  return ROS2BasicData

##
# @if jp
# @brief ñ��ǡ���������ʤɤδ��ܥ�å��������Υ��ꥢ�饤���ν����
#
# @param message_type ROS��å�������
# @param name ���ꥢ�饤����̾��
#
# @else
# @brief 
#
# @param message_type 
# @param name 
#
#
# @endif
#
def ROS2BasicDataInit(message_type, name):
  OpenRTM_aist.SerializerFactory.instance().addFactory(name,
                                                      ros2_basic_data(message_type),
                                                      OpenRTM_aist.Delete)
  ROS2MessageInfo.ROS2MessageInfoFactory.instance().addFactory(name,
                                                      ROS2MessageInfo.ros2_message_info(message_type),
                                                      OpenRTM_aist.Delete)



##
# @if jp
# @class ROS2Point3DData
# @brief PointStamped���Υ��ꥢ�饤�������
#
# @else
# @class ROS2Point3DData
# @brief 
#
#
# @endif
class ROS2Point3DData(OpenRTM_aist.ByteDataStreamBase):
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
  # @brief �ǡ������Ѵ�(omniORB->ROS2)
  #
  # 
  # @param data omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value��ROS2�Υǡ���
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
    msg = PointStamped()
    msg.header.stamp.sec = data.tm.sec
    msg.header.stamp.nanosec = data.tm.nsec
    msg.point.x = float(data.data.x)
    msg.point.y = float(data.data.y)
    msg.point.z = float(data.data.z)

    return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, msg

  ##
  # @if jp
  # @brief �ǡ������Ѵ�(ROS2->omniORB)
  #
  # @param self 
  # @param bdata ROS2�Υǡ���
  # @param data_type omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value���Ѵ���Υǡ���
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
  def deserialize(self, bdata, data_type):
    try:
      data_type.tm.sec = bdata.header.stamp.sec
      data_type.tm.nsec = bdata.header.stamp.nanosec
      data_type.data.x = bdata.point.x
      data_type.data.y = bdata.point.y
      data_type.data.z = bdata.point.z
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data_type
    except:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, data_type


##
# @if jp
# @brief PointStamped���Υ��ꥢ�饤���ν����
#
#
# @else
# @brief 
#
#
# @endif
#
def ROS2Point3DInit():
  OpenRTM_aist.SerializerFactory.instance().addFactory("ros2:geometry_msgs/PointStamped",
                                                      ROS2Point3DData,
                                                      OpenRTM_aist.Delete)
  ROS2MessageInfo.ROS2MessageInfoFactory.instance().addFactory("ros2:geometry_msgs/PointStamped",
                                                      ROS2MessageInfo.ros2_message_info(PointStamped),
                                                      OpenRTM_aist.Delete)


##
# @if jp
# @class ROS2QuaternionData
# @brief QuaternionStamped���Υ��ꥢ�饤��
#
# @else
# @class ROS2QuaternionData
# @brief 
#
#
# @endif
class ROS2QuaternionData(OpenRTM_aist.ByteDataStreamBase):
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
  # @brief �ǡ������Ѵ�(omniORB->ROS2)
  #
  # 
  # @param data omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value��ROS2�Υǡ���
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
    msg = QuaternionStamped()
    msg.header.stamp.sec = data.tm.sec
    msg.header.stamp.nanosec = data.tm.nsec
    msg.quaternion.x = float(data.data.x)
    msg.quaternion.y = float(data.data.y)
    msg.quaternion.z = float(data.data.z)
    msg.quaternion.w = float(data.data.w)

    return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, msg

  ##
  # @if jp
  # @brief �ǡ������Ѵ�(ROS2->omniORB)
  #
  # @param self 
  # @param bdata ROS2�Υǡ���
  # @param data_type omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value���Ѵ���Υǡ���
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
  def deserialize(self, bdata, data_type):
    try:
      data_type.tm.sec = bdata.header.stamp.sec
      data_type.tm.nsec = bdata.header.stamp.nanosec
      data_type.data.x = bdata.quaternion.x
      data_type.data.y = bdata.quaternion.y
      data_type.data.z = bdata.quaternion.z
      data_type.data.w = bdata.quaternion.w
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data_type
    except:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, data_type


##
# @if jp
# @brief QuaternionStamped���Υ��ꥢ�饤���ν����
#
#
# @else
# @brief 
#
#
# @endif
#
def ROS2QuaternionInit():
  OpenRTM_aist.SerializerFactory.instance().addFactory("ros2:geometry_msgs/QuaternionStamped",
                                                      ROS2QuaternionData,
                                                      OpenRTM_aist.Delete)
  ROS2MessageInfo.ROS2MessageInfoFactory.instance().addFactory("ros2:geometry_msgs/QuaternionStamped",
                                                      ROS2MessageInfo.ros2_message_info(QuaternionStamped),
                                                      OpenRTM_aist.Delete)



##
# @if jp
# @class ROS2Vector3DData
# @brief Vector3Stamped���Υ��ꥢ�饤��
#
# @else
# @class ROS2Vector3DData
# @brief 
#
#
# @endif
class ROS2Vector3DData(OpenRTM_aist.ByteDataStreamBase):
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
  # @brief �ǡ������Ѵ�(omniORB->ROS2)
  #
  # 
  # @param data omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value��ROS2�Υǡ���
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
    msg = Vector3Stamped()
    msg.header.stamp.sec = data.tm.sec
    msg.header.stamp.nanosec = data.tm.nsec
    msg.vector.x = float(data.data.x)
    msg.vector.y = float(data.data.y)
    msg.vector.z = float(data.data.z)

    return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, msg

  ##
  # @if jp
  # @brief �ǡ������Ѵ�(ROS2->omniORB)
  #
  # @param self 
  # @param bdata ROS2�Υǡ���
  # @param data_type omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value���Ѵ���Υǡ���
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
  def deserialize(self, bdata, data_type):
    try:
      data_type.tm.sec = bdata.header.stamp.sec
      data_type.tm.nsec = bdata.header.stamp.nanosec
      data_type.data.x = bdata.vector.x
      data_type.data.y = bdata.vector.y
      data_type.data.z = bdata.vector.z
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data_type
    except:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, data_type


##
# @if jp
# @brief Vector3Stamped���Υ��ꥢ�饤���ν����
#
#
# @else
# @brief 
#
#
# @endif
#
def ROS2Vector3DInit():
  OpenRTM_aist.SerializerFactory.instance().addFactory("ros2:geometry_msgs/Vector3Stamped",
                                                      ROS2Vector3DData,
                                                      OpenRTM_aist.Delete)
  ROS2MessageInfo.ROS2MessageInfoFactory.instance().addFactory("ros2:geometry_msgs/Vector3Stamped",
                                                      ROS2MessageInfo.ros2_message_info(Vector3Stamped),
                                                      OpenRTM_aist.Delete)


##
# @if jp
# @class ROS2CameraImageData
# @brief Image���Υ��ꥢ�饤��
#
# @else
# @class ROS2CameraImageData
# @brief 
#
#
# @endif
class ROS2CameraImageData(OpenRTM_aist.ByteDataStreamBase):
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
  # @brief �ǡ������Ѵ�(omniORB->ROS2)
  #
  # 
  # @param data omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value��ROS2�Υǡ���
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
    msg = Image()
    msg.header.stamp.sec = data.tm.sec
    msg.header.stamp.nanosec = data.tm.nsec
    msg.height = data.height
    msg.width = data.width
    if not data.format:
      msg.encoding = "rgb8"
    else:
      msg.encoding = data.format
    msg.step = 1920
    msg.data = data.pixels

    return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, msg

  ##
  # @if jp
  # @brief �ǡ������Ѵ�(ROS2->omniORB)
  #
  # @param self 
  # @param bdata ROS2�Υǡ���
  # @param data_type omniORB�Υǡ���
  # @return ret��value
  # ret��SERIALIZE_OK��������SERIALIZE_ERROR�����ԡ�SERIALIZE_NOTFOUND������Υ��ꥢ�饤�����ʤ�
  # value���Ѵ���Υǡ���
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
  def deserialize(self, bdata, data_type):
    try:
      data_type.tm.sec = bdata.header.stamp.sec
      data_type.tm.nsec = bdata.header.stamp.nanosec
      data_type.height = bdata.height
      data_type.width = bdata.width
      data_type.format = bdata.encoding 
      data_type.pixels = bdata.data
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_OK, data_type
    except:
      return OpenRTM_aist.ByteDataStreamBase.SERIALIZE_NOT_SUPPORT_ENDIAN, data_type


##
# @if jp
# @brief Image���Υ��ꥢ�饤���ν����
#
#
# @else
# @brief 
#
#
# @endif
#
def ROS2CameraImageInit():
  OpenRTM_aist.SerializerFactory.instance().addFactory("ros2:sensor_msgs/Image",
                                                      ROS2CameraImageData,
                                                      OpenRTM_aist.Delete)
  ROS2MessageInfo.ROS2MessageInfoFactory.instance().addFactory("ros2:sensor_msgs/Image",
                                                      ROS2MessageInfo.ros2_message_info(Image),
                                                      OpenRTM_aist.Delete)


##
# @if jp
# @brief �Ƽ亮�ꥢ�饤���ν�����ؿ�
#
#
# @else
# @brief 
#
#
# @endif
#
def ROS2SerializerInit():
  ROS2BasicDataInit(Float32, "ros2:std_msgs/Float32")
  ROS2BasicDataInit(Float64, "ros2:std_msgs/Float64")
  ROS2BasicDataInit(Int8, "ros2:std_msgs/Int8")
  ROS2BasicDataInit(Int16, "ros2:std_msgs/Int16")
  ROS2BasicDataInit(Int32, "ros2:std_msgs/Int32")
  ROS2BasicDataInit(Int64, "ros2:std_msgs/Int64")
  ROS2BasicDataInit(UInt8, "ros2:std_msgs/UInt8")
  ROS2BasicDataInit(UInt16, "ros2:std_msgs/UInt16")
  ROS2BasicDataInit(UInt32, "ros2:std_msgs/UInt32")
  ROS2BasicDataInit(UInt64, "ros2:std_msgs/UInt64")
  ROS2BasicDataInit(String, "ros2:std_msgs/String")

  ROS2BasicDataInit(Float32MultiArray, "ros2:std_msgs/Float32MultiArray")
  ROS2BasicDataInit(Float64MultiArray, "ros2:std_msgs/Float64MultiArray")
  ROS2BasicDataInit(Int8MultiArray, "ros2:std_msgs/Int8MultiArray")
  ROS2BasicDataInit(Int16MultiArray, "ros2:std_msgs/Int16MultiArray")
  ROS2BasicDataInit(Int32MultiArray, "ros2:std_msgs/Int32MultiArray")
  ROS2BasicDataInit(Int64MultiArray, "ros2:std_msgs/Int64MultiArray")
  ROS2BasicDataInit(UInt8MultiArray, "ros2:std_msgs/UInt8MultiArray")
  ROS2BasicDataInit(UInt16MultiArray, "ros2:std_msgs/UInt16MultiArray")
  ROS2BasicDataInit(UInt32MultiArray, "ros2:std_msgs/UInt32MultiArray")
  ROS2BasicDataInit(UInt64MultiArray, "ros2:std_msgs/UInt64MultiArray")

  ROS2Point3DInit()
  ROS2QuaternionInit()
  ROS2Vector3DInit()
  ROS2CameraImageInit()
