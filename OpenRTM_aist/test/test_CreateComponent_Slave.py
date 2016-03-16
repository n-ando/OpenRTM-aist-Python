#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_CreateComponent_Slave.py
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




class TestComp1(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    

  def onInitialize(self):

    return RTC.RTC_OK
  
class TestComp2(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

    
    return
  
  def onInitialize(self):

    
    return RTC.RTC_OK
    
    

    
def TestComp1Init(manager):
  profile = OpenRTM_aist.Properties(defaults_str=testcomp1_spec)
  manager.registerFactory(profile,
                          TestComp1,
                          OpenRTM_aist.Delete)


    
def TestComp2Init(manager):
  profile = OpenRTM_aist.Properties(defaults_str=testcomp2_spec)
  manager.registerFactory(profile,
                          TestComp2,
                          OpenRTM_aist.Delete)
  

def TestComp1ModuleInit(manager):
  TestComp1Init(manager)
  #com = manager.createComponent("TestComp1")

def TestComp2ModuleInit(manager):
  TestComp2Init(manager)
  #com = manager.createComponent("TestComp2")
  

def runTestComp2(q):
    q.get()
    argv = ["dummy"]
    argv.extend(['-o','naming.type:corba,manager'])
    argv.extend(['-o','naming.formats:test.host_cxt/%n.rtc'])
    argv.extend(['-o','manager.instance_name:manager2'])
    argv.extend(['-o','manager.shutdown_on_nortcs:NO'])
    argv.extend(['-o','manager.shutdown_auto:NO'])
    
    manager = OpenRTM_aist.Manager.init(argv)
    manager.setModuleInitProc(TestComp2ModuleInit)
    manager.activateManager()

    
    
    
    #print manager.getManagerServant().findManager_by_name("manager")
    #rtc = manager.getManagerServant().create_component("testSHM_in&manager_name=manager3&language=Python")
    #rtc = manager.getManagerServant().create_component("AbsFunction&manager_name=manager3&language=C++")
    #$print rtc
    #rtc = manager.getManagerServant().create_component("testSHM_in")
    #print rtc
    q.get()
        
    comps = manager.getComponents()[:]
    for comp in comps:
        manager.unregisterComponent(comp)
        comp_id = comp.getProperties()
        factory = manager._factory.find(comp_id)
        factory.destroy(comp)
    manager.shutdownNaming()
    time.sleep(0.1)


class Test_CreateComponent_Slave(unittest.TestCase):
  
  def setUp(self):
    
    
    sys.argv.extend(['-d'])
    sys.argv.extend(['-o','naming.type:corba,manager'])
    sys.argv.extend(['-o','naming.formats:test.host_cxt/%n.rtc'])
    sys.argv.extend(['-o','manager.instance_name:manager'])
    #sys.argv.extend(['-o','logger.log_level:DEBUG'])
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





  def test_createComponent_slave(self):
    self.queue = multiprocessing.Queue()
    self.outport_process = multiprocessing.Process(target=runTestComp2, args=(self.queue,))
    self.outport_process.start()
    self.queue.put("")
    time.sleep(1)
    test_module_name = ["comp&test=0"]
    test_value = self.manager.getManagerServant().get_parameter_by_modulename("test",test_module_name)
    self.assertEqual(test_value,"0")
    self.assertEqual(test_module_name[0],"comp")
    #rtc = self.manager.getManagerServant().create_component("TestComp1&manager_name=manager2")
    #rtc = self.manager.getManagerServant().create_component("TestComp2&manager_address=localhost:2810")
    rtc = self.manager.getManagerServant().create_component("TestComp2&manager_name=manager2")
    slave = self.manager.getManagerServant().findManager_by_name("manager2")
    self.assertTrue(slave is not None)
    rtcs = slave.get_components_by_name("TestComp20")
    name = rtcs[0].get_component_profile().instance_name
    self.assertEqual(name,"TestComp20")
    
    self.queue.put("")
    #rtc = self.manager.getManagerServant().create_component("TestComp2")
    #print rtc
    #comps = self.manager.getComponents()
    #print comps

  def test_createComponent_newProcess(self):
    rtc = self.manager.getManagerServant().create_component("TestComp3&manager_name=manager3&language=Python")
    slave = self.manager.getManagerServant().findManager_by_name("manager3")
    rtcs = slave.get_components_by_name("TestComp30")
    name = rtcs[0].get_component_profile().instance_name
    self.assertEqual(name,"TestComp30")
    
      

############### test #################
if __name__ == '__main__':
        unittest.main()
