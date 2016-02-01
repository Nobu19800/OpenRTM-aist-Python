#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortSHMConsumer.py
# @brief InPortSHMConsumer class
# @date  $Date: 2016-01-12 $
# @author Nobuhiko Miyamoto
#


import sys
from omniORB import any
from omniORB import CORBA
import OpenRTM_aist
import OpenRTM
import mmap, os
from omniORB import cdrMarshal
import CORBA

##
# @if jp
#
# @class InPortSHMConsumer
#
# @brief InPortSHMConsumer ���饹
#
# �̿����ʤ� ��ͭ���� �����Ѥ������ϥݡ��ȥ��󥷥塼�ޤμ������饹��
#
#
# @else
# @class InPortCorbaCdrConsumer
#
# @brief InPortCorbaCdrConsumer class
#
#
#
# @endif
#
class InPortSHMConsumer(OpenRTM_aist.InPortCorbaCdrConsumer):
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
  # Constructor
  #
  # @param self
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.InPortCorbaCdrConsumer.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("InPortSHMConsumer")
    self._properties = None
    self._shmem = None
    self.shm_address = ""
    return

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self
  # @param CorbaConsumer
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @param self
  # @param CorbaConsumer
  #
  # @endif
  #
  def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
    self._rtcout.RTC_PARANOID("~InPortSHMConsumer()")
    CorbaConsumer.__del__(self)
    if self._shmem:
      self._shmem.close()
    return

  ##
  # @if jp
  # @brief ��������
  #
  # InPortConsumer�γƼ������Ԥ�
  # �ץ�Х����ǥ��ͥ����ץ�ե�����˶�ͭ����ζ���̾����¸���뤿�ᡢinit�ؿ��Ƕ�ͭ����ν������Ԥ�
  #
  # @param self
  # @param prop ���ͥ����ץ�ѥƥ�
  #
  # @else
  # @brief Initializing configuration
  #
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    
    self._rtcout.RTC_TRACE("init()")
    self._properties = prop
    
    
    self.shm_address = prop.getProperty("shared_memory.address")
    if self.shm_address:
      if self._shmem is None:
        self._shmem = mmap.mmap(0, 256, self.shm_address, mmap.ACCESS_WRITE)
    return

  ##
  # @if jp
  # @brief ��³��ؤΥǡ�������
  #
  # ��³��Υݡ��Ȥإǡ�������������
  # 
  #
  # CORBA�ǥǡ��������������������ơ��ǡ����϶�ͭ����˽񤭹���
  #
  # @param self
  # @param data ��������ǡ���
  # @return �꥿���󥳡���
  #
  # @else
  # @brief Send data to the destination port
  #
  # @param self
  # @param data 
  # @return
  #
  # @endif
  #
  # virtual ReturnCode put(const cdrMemoryStream& data);
  def put(self, data):
    self._rtcout.RTC_PARANOID("put()")

    try:
      ref_ = self.getObject()
      if ref_:
        inportcdr = ref_._narrow(OpenRTM.InPortCdr)
        #print dir(ref_)
        if self._shmem is not None:
          self._shmem.seek(os.SEEK_SET)
          
          self._shmem.write(data)
          data_size = len(data)
          mar_data_size = cdrMarshal(CORBA.TC_ushort, data_size)
          
          return self.convertReturnCode(inportcdr.put(mar_data_size))
      return self.CONNECTION_LOST
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST
    
    
        
    return self.UNKNOWN_ERROR
 

def InPortSHMConsumerInit():
  factory = OpenRTM_aist.InPortConsumerFactory.instance()
  factory.addFactory("shared_memory",
                     OpenRTM_aist.InPortSHMConsumer,
                     OpenRTM_aist.Delete)
