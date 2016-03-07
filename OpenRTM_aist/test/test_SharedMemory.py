#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_SharedMemory.py
# \brief 
# \date $Date: $
# \author Nobuhiko Miyamoto
#


import sys
sys.path.insert(1,"../")

try:
    import unittest2 as unittest
except (ImportError):
    import unittest

import time

#from Manager import *
import OpenRTM_aist
import RTC, OpenRTM



  




class TestSharedMemory(unittest.TestCase):
  
  def setUp(self):
    sys.argv.extend(['-o', 'port.outport.out.shem_default_size:1k'])
    #sys.argv.extend(['-o', 'port.inport.in.shem_default_size:1k'])
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    self.manager.activateManager()

    self._d_in = RTC.TimedOctetSeq(RTC.Time(0,0),[])
    self._inIn = OpenRTM_aist.InPort("in", self._d_in)

    prop = self.manager.getConfig().getNode("port.inport.in")
    self._inIn.init(prop)
    self.inport_obj = self._inIn.getPortRef()


    self._d_out = RTC.TimedOctetSeq(RTC.Time(0,0),[])
    self._outOut = OpenRTM_aist.OutPort("out", self._d_out)
    prop = self.manager.getConfig().getNode("port.outport.out")
    self._outOut.init(prop)
    self.outport_obj = self._outOut.getPortRef()
    
    

  def tearDown(self):
    self.manager.shutdownManager()

  def test_Push(self):
    
    prop = OpenRTM_aist.Properties()
    prop.setProperty("dataport.interface_type","shared_memory")
    prop.setProperty("dataport.dataflow_type","push")
    ret = OpenRTM_aist.connect("con1",prop,self.inport_obj,self.outport_obj)
    
    self._d_out.data = "a"*100
    self._outOut.write()

    ret = self._inIn.isNew()
    self.assertTrue(ret)

    data = self._inIn.read()
    self.assertEqual(data.data, self._d_out.data)

    
    self._d_out.data = "a"*50000
    self._outOut.write()

    data = self._inIn.read()
    self.assertEqual(data.data, self._d_out.data)
    

    self.outport_obj.disconnect_all()



  def test_Pull(self):
    prop = OpenRTM_aist.Properties()
    prop.setProperty("dataport.interface_type","shared_memory")
    prop.setProperty("dataport.dataflow_type","pull")
    ret = OpenRTM_aist.connect("con1",prop,self.inport_obj,self.outport_obj)
    
    self._d_out.data = "a"*100
    self._outOut.write()

    #ret = self._inIn.isNew()
    #self.assertTrue(ret)

    data = self._inIn.read()
    self.assertEqual(data.data, self._d_out.data)

    
    self._d_out.data = "a"*50000
    self._outOut.write()
    

    data = self._inIn.read()
    self.assertEqual(data.data, self._d_out.data)
    

    self.outport_obj.disconnect_all()

############### test #################
if __name__ == '__main__':
        unittest.main()
