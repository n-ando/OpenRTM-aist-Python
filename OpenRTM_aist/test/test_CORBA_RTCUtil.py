#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_CORBA_RTCUtil.py
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
    

    self._test1 = [0]

  def onInitialize(self):
    self.addOutPort("out",self._outOut)
    self.addInPort("in",self._inIn)
    
    self._servicePort_provided.registerProvider("service", "TestService", self._testService_provided)
    self.addPort(self._servicePort_provided)
    
    
    

    self.bindParameter("test1", self._test1, "0")
    

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
    self.addInPort("in",self._inIn)
    self.addOutPort("out",self._outOut)
    
    
    
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
  

def MyModuleInit(manager):
  TestComp1Init(manager)
  TestComp2Init(manager)
  com = manager.createComponent("TestComp1")
  com = manager.createComponent("TestComp2")
  




class Test_CORBA_RTCUtil(unittest.TestCase):
  
  def setUp(self):
    sys.argv.extend(['-d'])
    sys.argv.extend(['-o', 'exec_cxt.periodic.rate:1000'])
    sys.argv.extend(['-o','naming.type:corba,manager'])
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    self.manager.setModuleInitProc(MyModuleInit)
    self.manager.activateManager()

    
    
    self.comp1 = self.manager.getComponent("TestComp10").getObjRef()
    self.comp2 = self.manager.getComponent("TestComp20").getObjRef()


  def tearDown(self):
    comps = self.manager.getComponents()[:]
    for comp in comps:
        self.manager.unregisterComponent(comp)
        comp_id = comp.getProperties()
        factory = self.manager._factory.find(comp_id)
        factory.destroy(comp)
    self.manager.shutdownNaming()
    time.sleep(0.1)

  def test_Component(self):
    compProf = OpenRTM_aist.get_component_profile(self.comp1)
    self.assertEqual(compProf.getProperty("implementation_id"), "TestComp1")
    ret = OpenRTM_aist.is_existing(self.comp1)
    self.assertTrue(ret)

  def test_EC(self):
    ec = OpenRTM_aist.get_actual_ec(self.comp1,0)
    ec_id = OpenRTM_aist.get_ec_id(self.comp1, ec)
    self.assertEqual(ec_id, 0)

    ret = OpenRTM_aist.add_rtc_to_default_ec(self.comp1, self.comp2)
    self.assertEqual(ret, RTC.RTC_OK)
    

    ret = OpenRTM_aist.is_alive_in_default_ec(self.comp1)
    self.assertEqual(ret, True)

    ret = OpenRTM_aist.set_default_rate(self.comp1, 500)
    self.assertEqual(ret, RTC.RTC_OK)

    rate = OpenRTM_aist.get_default_rate(self.comp1)
    self.assertEqual(int(rate), 500)

    ret = OpenRTM_aist.set_current_rate(self.comp2,1000, 100)
    self.assertEqual(ret, RTC.RTC_OK)
    
    rate = OpenRTM_aist.get_current_rate(self.comp2, 1000)
    self.assertEqual(int(rate), 100)
    
    ret = OpenRTM_aist.activate(self.comp1,0)
    self.assertEqual(ret, RTC.RTC_OK)
    state = OpenRTM_aist.is_in_active(self.comp1, 0)
    self.assertTrue(state)
    
    ret = OpenRTM_aist.deactivate(self.comp1,0)
    self.assertEqual(ret, RTC.RTC_OK)
    state = OpenRTM_aist.is_in_inactive(self.comp1, 0)
    self.assertTrue(state)
    
    #state = OpenRTM_aist.is_in_error(self.comp1, 0)
    #ret = OpenRTM_aist.reset(self.comp1,0)
    #self.assertEqual(ret, RTC.RTC_OK)

    ret = [None]
    ans = OpenRTM_aist.get_state(ret, self.comp1, 0)
    self.assertEqual(ret[0], RTC.INACTIVE_STATE)

    ret = OpenRTM_aist.remove_rtc_to_default_ec(self.comp1, self.comp2)
    self.assertEqual(ret, RTC.RTC_OK)

    
  def test_Port(self):
    port_names = OpenRTM_aist.get_port_names(self.comp1)
    self.assertTrue("TestComp10.out" in port_names)
    
    inport_names = OpenRTM_aist.get_inport_names(self.comp2)
    self.assertTrue("TestComp20.in" in inport_names)
    
    outport_names = OpenRTM_aist.get_outport_names(self.comp1)
    self.assertTrue("TestComp10.out" in outport_names)
    
    svcport_names = OpenRTM_aist.get_svcport_names(self.comp1)
    self.assertTrue("TestComp10.service" in svcport_names)

    rtc1_port_out = OpenRTM_aist.get_port_by_name(self.comp1,"TestComp10.out")
    rtc2_port_out = OpenRTM_aist.get_port_by_name(self.comp2,"TestComp20.out")
    rtc2_port_in = OpenRTM_aist.get_port_by_name(self.comp2,"TestComp20.in")
    rtc1_port_in = OpenRTM_aist.get_port_by_name(self.comp1,"TestComp10.in")
    
    pp = rtc1_port_out.get_port_profile()
    self.assertEqual(pp.name, "TestComp10.out")

    
    prop = OpenRTM_aist.Properties()
    connect_profile = OpenRTM_aist.create_connector("con1",prop,rtc1_port_out,rtc2_port_in)
    ret = OpenRTM_aist.connect("con1",prop,rtc1_port_out,rtc2_port_in)
    self.assertEqual(ret, RTC.RTC_OK)

    con_names = OpenRTM_aist.get_connector_names_by_portref(rtc1_port_out)
    self.assertTrue("con1" in con_names)
    con_names = OpenRTM_aist.get_connector_names(self.comp1,"TestComp10.out")
    self.assertTrue("con1" in con_names)
    con_ids = OpenRTM_aist.get_connector_ids_by_portref(rtc1_port_out)
    con_ids = OpenRTM_aist.get_connector_ids(self.comp1,"TestComp10.out")

    
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertTrue(ret)

    ret = OpenRTM_aist.disconnect(rtc1_port_out.get_connector_profiles()[0])
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    
    
    ret = OpenRTM_aist.connect_multi("con2",prop,rtc1_port_out,[rtc1_port_in,rtc2_port_in])
    self.assertEqual(ret, RTC.RTC_OK)

    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc1_port_in)
    self.assertTrue(ret)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertTrue(ret)
    
    ret = OpenRTM_aist.disconnect_all_by_ref(rtc1_port_out)
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    

    ret = OpenRTM_aist.connect_by_name("con3",prop,self.comp1,"TestComp10.out",self.comp2,"TestComp20.in")
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertTrue(ret)

    ret = OpenRTM_aist.disconnect_by_portref_connector_name(rtc1_port_out, "con3")
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    ret = OpenRTM_aist.connect("con1",prop,rtc1_port_out,rtc2_port_in)
    ret = OpenRTM_aist.disconnect_by_portref_connector_id(rtc1_port_out,rtc1_port_out.get_connector_profiles()[0].connector_id)
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    ret = OpenRTM_aist.connect("con1",prop,rtc1_port_out,rtc2_port_in)
    ret = OpenRTM_aist.disconnect_by_port_name(rtc1_port_out,"TestComp20.in")
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)


    ret = OpenRTM_aist.connect("con1",prop,rtc1_port_out,rtc2_port_in)
    ret = OpenRTM_aist.disconnect_all_by_name("rtcloc://localhost:2810/example/TestComp20.in")
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    ret = OpenRTM_aist.connect("con1",prop,rtc1_port_out,rtc2_port_in)
    ret = OpenRTM_aist.disconnect_by_portname_connector_name("rtcloc://localhost:2810/example/TestComp20.in","con1")
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    ret = OpenRTM_aist.connect("con1",prop,rtc1_port_out,rtc2_port_in)
    ret = OpenRTM_aist.disconnect_by_portname_connector_id("rtcloc://localhost:2810/example/TestComp10.out",rtc1_port_out.get_connector_profiles()[0].connector_id)
    self.assertEqual(ret, RTC.RTC_OK)
    ret = OpenRTM_aist.already_connected(rtc1_port_out,rtc2_port_in)
    self.assertFalse(ret)

    
    

  def test_configuration(self):
    conf = OpenRTM_aist.get_configuration(self.comp1, "default")
    self.assertEqual(conf.getProperty("test1"),"0")

    ret = OpenRTM_aist.get_parameter_by_key(self.comp1,"default","test1")
    self.assertEqual(ret,"0")

    conf = OpenRTM_aist.get_active_configuration(self.comp1)
    self.assertEqual(conf.getProperty("test1"),"0")

    ret = OpenRTM_aist.set_configuration(self.comp1,"default","test1","1")
    self.assertTrue(ret)
    ret = OpenRTM_aist.get_parameter_by_key(self.comp1,"default","test1")
    self.assertEqual(ret,"1")

    ret = OpenRTM_aist.set_active_configuration(self.comp1,"test1","2")
    self.assertTrue(ret)
    ret = OpenRTM_aist.get_parameter_by_key(self.comp1,"default","test1")
    self.assertEqual(ret,"2")

    confsetname = OpenRTM_aist.get_active_configuration_name(self.comp1)
    self.assertEqual(confsetname,"default")

    
    #ec = self.comp1.get_owned_contexts()[0]
    
    #print OpenRTM_aist.get_participants_rtc(ec)
    
    #print ec.add_component(self.comp2)
    #print ec.get_profile()
    #prop = OpenRTM_aist.Properties()
    #conf = self.comp1.get_configuration()
    #print conf.get_configuration_sets()
    #confsets = conf.get_configuration_sets()
    #print confsets
    #OpenRTM_aist.NVUtil.copyToProperties(prop,confsets)
    #print prop
    # self.comp1.get_status_list()

############### test #################
if __name__ == '__main__':
        unittest.main()
