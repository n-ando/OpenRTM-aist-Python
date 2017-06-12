#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_INSRTObject.py
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
import OpenRTM
import RTC, RTC__POA

testcomp1_spec = ["implementation_id", "TestComp1",
                 "type_name",         "TestComp1",
                 "description",       "Test example component",
                 "version",           "1.0",
                 "vendor",            "Nobuhiko Myiyamoto",
                 "category",          "example",
                 "activity_type",     "DataFlowComponent",
                 "max_instance",      "10",
                 "language",          "C++",
                 "lang_type",         "compile",
                 "conf.default.test1", "0",
                 ""]







    
def TestComp1Init(manager):
  profile = OpenRTM_aist.Properties(defaults_str=testcomp1_spec)
  manager.registerFactory(profile,
                          OpenRTM_aist.DataFlowComponentBase,
                          OpenRTM_aist.Delete)


    

  

def TestComp1ModuleInit(manager):
  TestComp1Init(manager)
  com = manager.createComponent("TestComp1")


  



class test_INSRTObject(unittest.TestCase):
  
  def setUp(self):

    sys.argv.extend(['-p','2810'])
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    self.manager.setModuleInitProc(TestComp1ModuleInit)
    self.manager.activateManager()
    

  def tearDown(self):
    
    comps = self.manager.getComponents()[:]
    for comp in comps:
        self.manager.unregisterComponent(comp)
        comp_id = comp.getProperties()
        factory = self.manager._factory.find(comp_id)
        factory.destroy(comp)
    self.manager.shutdownNaming()
    time.sleep(0.1)

  def test_getComponent(self):
      rtobj = self.manager.getORB().string_to_object("corbaloc:iiop:localhost:2810/example/TestComp10")
      rtc = rtobj._narrow(OpenRTM.DataFlowComponent)
      name = rtc.get_component_profile().instance_name
      self.assertEqual(name, "TestComp10")
      
      
    

############### test #################
if __name__ == '__main__':
        unittest.main()
