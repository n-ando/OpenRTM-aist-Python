#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_NumberingPolicy_node.py
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







    
def TestComp1Init(manager):
  profile = OpenRTM_aist.Properties(defaults_str=testcomp1_spec)
  manager.registerFactory(profile,
                          OpenRTM_aist.DataFlowComponentBase,
                          OpenRTM_aist.Delete)


    

  

def TestComp1ModuleInit(manager):
  TestComp1Init(manager)
  com = manager.createComponent("TestComp1")


  

def runTestComp2(q):
    
    argv = [""]
    argv.extend(['-d'])
    argv.extend(['-o','manager.components.naming_policy:node_unique'])
    argv.extend(['-o','naming.type:corba,manager'])

    
    manager = OpenRTM_aist.Manager.init(argv)
    manager.setModuleInitProc(TestComp1ModuleInit)
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


class Test_NumberingPolicy_node(unittest.TestCase):
  
  def setUp(self):
    self.queue = multiprocessing.Queue()
    self.outport_process = multiprocessing.Process(target=runTestComp2, args=(self.queue,))
    self.outport_process.start()
    
    time.sleep(1)
    sys.argv.extend(['-o','manager.components.naming_policy:node_unique'])
    sys.argv.extend(['-o','naming.type:corba,manager'])
    #sys.argv.extend(['-o','manager.instance_name: manager2'])
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
      #prop = OpenRTM_aist.Properties()
      #pp = self.manager.getManagerServant().get_profile().properties
      #OpenRTM_aist.NVUtil.copyToProperties(prop, pp)
      #print prop
      comp = self.manager.getComponent("TestComp11")
      self.assertTrue(comp is not None)
      
    

############### test #################
if __name__ == '__main__':
        unittest.main()
