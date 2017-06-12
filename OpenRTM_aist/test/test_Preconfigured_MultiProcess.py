#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_Preconfigured_MultiProcess.py
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
import OpenRTM, OpenRTM__POA

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

class Test_i(OpenRTM__POA.InPortCdr):
  def __init__(self):
    pass
  def put(self, data):
    return OpenRTM.PORT_OK


class TestComp1(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    self._d_out = RTC.TimedLong(RTC.Time(0,0),0)
    self._outOut = OpenRTM_aist.OutPort("out", self._d_out)

    self._d_in = RTC.TimedLong(RTC.Time(0,0),0)
    self._inIn = OpenRTM_aist.InPort("in", self._d_in)

    self._servicePort_provided = OpenRTM_aist.CorbaPort("service")
    self._testService_provided = Test_i()

  def onInitialize(self):
    self.addOutPort("out",self._outOut)
    self.addInPort("in",self._inIn)
    
    self._servicePort_provided.registerProvider("service", "TestService", self._testService_provided)
    self.addPort(self._servicePort_provided)

    return RTC.RTC_OK
  
class TestComp2(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    self._d_out = RTC.TimedLong(RTC.Time(0,0),0)
    self._outOut = OpenRTM_aist.OutPort("out", self._d_out)

    self._d_in = RTC.TimedLong(RTC.Time(0,0),0)
    self._inIn = OpenRTM_aist.InPort("in", self._d_in)

    self._servicePort_required = OpenRTM_aist.CorbaPort("service")
    self._testService_required = OpenRTM_aist.CorbaConsumer(interfaceType=OpenRTM.InPortCdr)


    
    return
  
  def onInitialize(self):
    self.addOutPort("out",self._outOut)
    self.addInPort("in",self._inIn)
    
    
    
    
    self._servicePort_required.registerConsumer("service", "TestService", self._testService_required)
    self.addPort(self._servicePort_required)
    
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


class Test_Preconfigured_MultiProcess(unittest.TestCase):
  
  def setUp(self):
    self.queue = multiprocessing.Queue()
    self.outport_process = multiprocessing.Process(target=runTestComp2, args=(self.queue,))
    self.outport_process.start()
    
    time.sleep(1)
    sys.argv.extend(['-o','naming.type:corba,manager'])
    sys.argv.extend(['-o','naming.formats:test.host_cxt/%n.rtc'])

    RTC2_URL = "rtcloc://localhost:2810/example/TestComp20"
    self.dataPortConnectorName = RTC2_URL+".in"+"^TestComp10.out()"
    self.servicePortConnectorName = "TestComp10.service^"+RTC2_URL+".service()"
    sys.argv.extend(['-o', 'manager.components.preconnect:'+self.dataPortConnectorName+","+self.servicePortConnectorName])
    sys.argv.extend(['-o', 'manager.components.preactivate:'+RTC2_URL])
    #print 'manager.components.preactivate:'+RTC2_URL
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    self.manager.setModuleInitProc(TestComp1ModuleInit)
    self.manager.activateManager()

    self.comp1 = self.manager.getComponent("TestComp10").getObjRef()
    self.comp2 = self.manager._namingManager.string_to_component(RTC2_URL)[0]
    

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

  def test_PreActivation(self):
    state = OpenRTM_aist.is_in_active(self.comp2)
    self.assertTrue(state)

  def test_PreConnection(self):
    inport = OpenRTM_aist.get_port_by_name(self.comp2, "TestComp20.in")
    outport = OpenRTM_aist.get_port_by_name(self.comp1, "TestComp10.out")
    ans = OpenRTM_aist.already_connected(inport, outport)
    self.assertTrue(ans)
    
    provided = OpenRTM_aist.get_port_by_name(self.comp1, "TestComp10.service")
    required = OpenRTM_aist.get_port_by_name(self.comp2, "TestComp20.service")
    ans = OpenRTM_aist.already_connected(provided, required)
    self.assertTrue(ans)
    

############### test #################
if __name__ == '__main__':
        unittest.main()
