#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_Topic.py
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

    self._servicePort_provided = OpenRTM_aist.CorbaPort("service")
    self._Service_provided = Test_i()


    self._d_topic_out = RTC.TimedLong(RTC.Time(0,0),0)
    self._topic_outOut = OpenRTM_aist.OutPort("topic_out", self._d_topic_out)
    
    self._topic_servicePort_provided = OpenRTM_aist.CorbaPort("topic_service")
    self._topic_Service_provided = Test_i()

  def onInitialize(self):
    self.addOutPort("out",self._outOut)
    self._servicePort_provided.registerProvider("service", "TestService", self._Service_provided)
    self.addPort(self._servicePort_provided)
    
    self.addOutPort("topic_out",self._topic_outOut)
    self._topic_outOut.appendProperty("publish_topic","test")
    
    self._topic_servicePort_provided.registerProvider("topic_service", "TestService", self._topic_Service_provided)
    self.addPort(self._topic_servicePort_provided)
    self._topic_servicePort_provided.appendProperty("publish_topic","test")


    return RTC.RTC_OK

  
  
class TestComp2(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    self._d_in = RTC.TimedLong(RTC.Time(0,0),0)
    self._inIn = OpenRTM_aist.InPort("in", self._d_in)

    self._servicePort_required = OpenRTM_aist.CorbaPort("service")
    self._Service_required = OpenRTM_aist.CorbaConsumer(interfaceType=OpenRTM.InPortCdr)


    self._d_topic_in = RTC.TimedLong(RTC.Time(0,0),0)
    self._topic_inIn = OpenRTM_aist.InPort("topic_in", self._d_topic_in)
    
    
    
    self._topic_servicePort_required = OpenRTM_aist.CorbaPort("topic_service")
    self._topic_Service_required = OpenRTM_aist.CorbaConsumer(interfaceType=OpenRTM.InPortCdr)
    
    return
  
  def onInitialize(self):
    self.addInPort("in",self._inIn)

    self._servicePort_required.registerConsumer("service", "TestService", self._Service_required)
    self.addPort(self._servicePort_required)


    self.addInPort("topic_in",self._topic_inIn)
    self._topic_inIn.appendProperty("publish_topic","test")
    
        
    self._topic_servicePort_required.registerConsumer("topic_service", "TestService", self._topic_Service_required)
    self.addPort(self._topic_servicePort_required)
    self._topic_servicePort_required.appendProperty("publish_topic","test")
    
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
  

def MyModuleInit(manager):
  TestComp1Init(manager)
  TestComp2Init(manager)
  com = manager.createComponent("TestComp1")
  com = manager.createComponent("TestComp2")
  




class test_Topic(unittest.TestCase):
  
  def setUp(self):
    #sys.argv.extend(['-o','port.outport.topic_out.publish_topic:test2'])
    #sys.argv.extend(['-o','port.inport.topic_in.publish_topic:test2'])
    #sys.argv.extend(['-o','port.corbaport.topic_service.publish_topic:test2'])
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    
    self.manager.setModuleInitProc(MyModuleInit)
    self.manager.activateManager()
    
    self.comps = []
    self.comps.append(self.manager.getComponent("TestComp10"))
    self.comps.append(self.manager.getComponent("TestComp20"))
    self.comp1 = self.comps[0].getObjRef()
    self.comp2 = self.comps[1].getObjRef()
    
    

  def tearDown(self):
    for comp in self.comps:
        self.manager.unregisterComponent(comp)
        comp_id = comp.getProperties()
        factory = self.manager._factory.find(comp_id)
        factory.destroy(comp)
    self.manager.shutdownNaming()
    time.sleep(0.1)
    
  def test_port(self):
    inport = OpenRTM_aist.get_port_by_name(self.comp2, "TestComp20.in")
    outport = OpenRTM_aist.get_port_by_name(self.comp1, "TestComp10.out")

    self.manager.connectDataPorts(inport, [outport])
    ans = OpenRTM_aist.already_connected(inport, outport)
    self.assertTrue(ans)


    service_required = OpenRTM_aist.get_port_by_name(self.comp2, "TestComp20.service")
    service_provided = OpenRTM_aist.get_port_by_name(self.comp1, "TestComp10.service")
    self.manager.connectServicePorts(service_required, [service_provided])
    ans = OpenRTM_aist.already_connected(service_required, service_provided)
    self.assertTrue(ans)

    ports = self.manager.getPortsOnNameServers("dataports.port_cxt/test.topic_cxt","inport")
    name = ports[0].get_port_profile().name
    self.assertEqual(name, "TestComp20.topic_in")

    orb = self.manager.getORB()
    names = "localhost"
    cns = OpenRTM_aist.CorbaNaming(orb,names)
    bl = cns.listByKind("dataports.port_cxt/test.topic_cxt","inport")
    name = bl[0].binding_name[0].id
    self.assertEqual(name, "TestComp20.topic_in")


    self._d_out = RTC.TimedOctetSeq(RTC.Time(0,0),[])
    self._outOut = OpenRTM_aist.OutPort("out", self._d_out)
    prop = OpenRTM_aist.Properties()
    self._outOut.init(prop)

    naming = self.manager.getNaming()
    naming.bindPortObject("test.port",self._outOut)

    port = cns.resolveStr("test.port")
    self.assertTrue(port is not None)
    
    naming = OpenRTM_aist.NamingOnCorba(orb, "localhost")
    naming.bindPortObject("test2.port",self._outOut)
    
    port = cns.resolveStr("test2.port")
    self.assertTrue(port is not None)

  def test_Topic(self):
    
    inport = OpenRTM_aist.get_port_by_name(self.comp2, "TestComp20.topic_in")
    outport = OpenRTM_aist.get_port_by_name(self.comp1, "TestComp10.topic_out")
    ans = OpenRTM_aist.already_connected(inport, outport)
    self.assertTrue(ans)
    
    
    

    provided = OpenRTM_aist.get_port_by_name(self.comp1, "TestComp10.topic_service")
    required = OpenRTM_aist.get_port_by_name(self.comp2, "TestComp20.topic_service")
    ans = OpenRTM_aist.already_connected(provided, required)
    self.assertTrue(ans)
    

  
  


  


############### test #################
if __name__ == '__main__':
        unittest.main()
