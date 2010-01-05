#!/usr/bin/env python
# -*- Python -*-


#  \file test_InPortCorbaCdrProvider.py
#  \brief test for InPortCorbaCdrProvider class
#  \date $Date: 2007/09/20 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2003-2005
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
 

from omniORB import *
from omniORB import any

import sys
sys.path.insert(1,"../")

import unittest

from InPortCorbaCdrProvider import *

import RTC, RTC__POA
import OpenRTM
import OpenRTM_aist


class TestInPortCorbaCdrProvider(unittest.TestCase):
	def setUp(self):
		InPortCorbaCdrProviderInit()
		OpenRTM_aist.CdrRingBufferInit()
		self._prov = OpenRTM_aist.InPortProviderFactory.instance().createObject("corba_cdr")
		self._inp  = OpenRTM_aist.InPort("in",RTC.TimedLong(RTC.Time(0,0),0))
		self._orb  = OpenRTM_aist.Manager.instance().getORB()
		self._buffer = OpenRTM_aist.CdrBufferFactory.instance().createObject("ring_buffer")
		return
	
	def test_init(self):
		self._prov.init(OpenRTM_aist.Properties())
		return

	def test_setBuffer(self):
		self._prov.setBuffer(self._buffer)
		return

	def test_put(self):
		self._prov.setBuffer(self._buffer)
		data=RTC.TimedLong(RTC.Time(0,0),123)
		cdr=cdrMarshal(any.to_any(data).typecode(),data,1)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(cdr),OpenRTM.BUFFER_FULL)
		val=[]
		self.assertEqual(self._buffer.read(val),OpenRTM_aist.BufferStatus.BUFFER_OK)
		get_data=cdrUnmarshal(any.to_any(data).typecode(),val[0],1)
		self.assertEqual(get_data.data,123)
		return



############### test #################
if __name__ == '__main__':
        unittest.main()

