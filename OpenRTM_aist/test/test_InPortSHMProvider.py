#!/usr/bin/env python
# -*- Python -*-


#  \file test_InPortSHMProvider.py
#  \brief test for InPortSHMProvider class
#  \date $Date: 2007/09/20 $
#  \author Nobuhiko Miyamoto
# 

 

from omniORB import *
from omniORB import any

import sys
sys.path.insert(1,"../")

import unittest

import RTC, RTC__POA
import OpenRTM
import OpenRTM_aist


class BufferMock:
	def __init__(self):
		self._data = None
		return

	def write(self, data):
		self._data = data
		return OpenRTM_aist.BufferStatus.BUFFER_OK

	def read(self, value):
		if len(value) > 0:
			value[0] = self._data
		else:
			value.append(self._data)
		return OpenRTM_aist.BufferStatus.BUFFER_OK

	def full(self):
		return False


class ConnectorMock:
	def __init__(self, buffer):
		self._buffer = buffer
		return

	def write(self, data):
	    self._buffer.write(data)
	    return OpenRTM_aist.BufferStatus.BUFFER_OK



class TestInPortSHMProvider(unittest.TestCase):
	def setUp(self):
		OpenRTM_aist.InPortSHMProviderInit()
		OpenRTM_aist.CdrRingBufferInit()
		self._prov = OpenRTM_aist.InPortProviderFactory.instance().createObject("shared_memory")
		self._inp  = OpenRTM_aist.InPort("in",RTC.TimedLong(RTC.Time(0,0),0))
		self._orb  = OpenRTM_aist.Manager.instance().getORB()
		self._buffer = BufferMock()
		#self._shm = OpenRTM_aist.SharedMemory()
		
		#self._shm.setInterface(self._prov._this())
		#self._shm.create_memory(1000,"test")
		self._prov.create_memory(1000,"test")
		return
	
	

	

	def test_put(self):
		
		self._con = ConnectorMock(self._buffer)
		self._prov._connector = self._con
		self._prov.setBuffer(self._buffer)
		data = RTC.TimedLong(RTC.Time(0,0),123)
		cdr = cdrMarshal(any.to_any(data).typecode(), data, 1)

		self._prov.write(cdr)

		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		self.assertEqual(self._prov.put(),OpenRTM.PORT_OK)
		val = []
		self.assertEqual(self._buffer.read(val), OpenRTM_aist.BufferStatus.BUFFER_OK)
		get_data = cdrUnmarshal(any.to_any(data).typecode(), val[0], 1)
		self.assertEqual(get_data.data, 123)
		return



############### test #################
if __name__ == '__main__':
        unittest.main()

