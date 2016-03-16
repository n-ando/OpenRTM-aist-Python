#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_string_to_component.py
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
import RTC, RTC__POA
import multiprocessing

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

testcomp2_spec = ["implementation_id", "TestComp2",
                 "type_name",         "TestComp2",
                 "description",       "Test example component",
                 "version",           "1.0",
                 "vendor",            "Nobuhiko Myiyamoto",
                 "category",          "example",
                 "activity_type",     "DataFlowComponent",
                 "max_instance",      "10",
                 "language",          "C++",
                 "lang_type",         "compile",
                 ""]




    
    

    
def TestComp1Init(manager):
  profile = OpenRTM_aist.Properties(defaults_str=testcomp1_spec)
  manager.registerFactory(profile,
                          OpenRTM_aist.DataFlowComponentBase,
                          OpenRTM_aist.Delete)


    
def TestComp2Init(manager):
  profile = OpenRTM_aist.Properties(defaults_str=testcomp2_spec)
  manager.registerFactory(profile,
                          OpenRTM_aist.DataFlowComponentBase,
                          OpenRTM_aist.Delete)
  

def TestComp1ModuleInit(manager):
  TestComp1Init(manager)
  com = manager.createComponent("TestComp1")

def TestComp2ModuleInit(manager):
  TestComp2Init(manager)
  com = manager.createComponent("TestComp2")
  

def runTestComp2(q):
    
    argv = [""]
    argv.extend(['-d'])
    argv.extend(['-o','naming.type:corba,manager'])
    argv.extend(['-o','naming.formats:test.host_cxt/%n.rtc'])

    
    manager = OpenRTM_aist.Manager.init(argv)
    manager.setModuleInitProc(TestComp2ModuleInit)
    manager.activateManager()
    
    
    q.get()
        
    comps = manager.getComponents()[:]
    for comp in comps:
        manager.unregisterComponent(comp)
        comp_id = comp.getProperties()
        factory = manager._factory.find(comp_id)
        factory.destroy(comp)
    manager.shutdownNaming()
    time.sleep(0.1)


class Test_string_to_component(unittest.TestCase):
  
  def setUp(self):
    self.queue = multiprocessing.Queue()
    self.outport_process = multiprocessing.Process(target=runTestComp2, args=(self.queue,))
    self.outport_process.start()
    
    time.sleep(1)
    sys.argv.extend(['-o','naming.type:corba,manager'])
    sys.argv.extend(['-o','naming.formats:test.host_cxt/%n.rtc'])
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    self.manager.setModuleInitProc(TestComp1ModuleInit)
    self.manager.activateManager()
    

  def tearDown(self):
    
    self.queue.put("")
    comps = self.manager.getComponents()[:]
    for comp in comps:
        self.manager.unregisterComponent(comp)
        comp_id = comp.getProperties()
        factory = self.manager._factory.find(comp_id)
        factory.destroy(comp)
    self.manager.shutdownNaming()
    time.sleep(0.1)

  def test_getComponent(self):
      #mgr_sev = self.manager._mgrservant.getObjRef()
      #print mgr_sev.get_components_by_name("example/TestComp10")
      rtcs = self.manager.getNaming().string_to_component("rtcloc://localhost:2810/example/TestComp20")
      name = rtcs[0].get_component_profile().instance_name
      self.assertEqual(name,"TestComp20")
      rtcs = self.manager.getNaming().string_to_component("rtcloc://*/example/TestComp20")
      name = rtcs[0].get_component_profile().instance_name
      self.assertEqual(name,"TestComp20")
      rtcs = self.manager.getNaming().string_to_component("rtcloc://*/*/TestComp20")
      name = rtcs[0].get_component_profile().instance_name
      self.assertEqual(name,"TestComp20")
      #print rtcs
      rtcs = self.manager.getNaming().string_to_component("rtcname://localhost/test.host_cxt/TestComp20")
      name = rtcs[0].get_component_profile().instance_name
      self.assertEqual(name,"TestComp20")
      rtcs = self.manager.getNaming().string_to_component("rtcname://*/test.host_cxt/TestComp20")
      name = rtcs[0].get_component_profile().instance_name
      self.assertEqual(name,"TestComp20")
      rtcs = self.manager.getNaming().string_to_component("rtcname://*/*/TestComp20")
      name = rtcs[0].get_component_profile().instance_name
      self.assertEqual(name,"TestComp20")
      

############### test #################
if __name__ == '__main__':
        unittest.main()
