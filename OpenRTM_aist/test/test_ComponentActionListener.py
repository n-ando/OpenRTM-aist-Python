#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_ComponentActionListener.py
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



class TestPostListener(OpenRTM_aist.PostComponentActionListener):
    def __init__(self, mes):
        self.mes = mes
    def __del__(self):
        pass
    def __call__(self, ec_id, ret):
        print self.mes
        

class TestPreListener(OpenRTM_aist.PreComponentActionListener):
    def __init__(self, mes):
        self.mes = mes
    def __del__(self):
        pass
    def __call__(self, ec_id):
        print self.mes


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
    
    #self._servicePort_provided.activateInterfaces()

    self.bindParameter("test1", self._test1, "0")


    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_INITIALIZE, TestPreListener("RTC2:PRE_ON_INITIALIZE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_FINALIZE, TestPreListener("RTC1:PRE_ON_FINALIZE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_STARTUP, TestPreListener("RTC1:PRE_ON_STARTUP"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_SHUTDOWN, TestPreListener("RTC1:PRE_ON_SHUTDOWN"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ACTIVATED, TestPreListener("RTC1:PRE_ON_ACTIVATED"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_DEACTIVATED, TestPreListener("RTC1:PRE_ON_DEACTIVATED"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ABORTING, TestPreListener("RTC1:PRE_ON_ABORTING"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ERROR, TestPreListener("RTC1:PRE_ON_ERROR"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_RESET, TestPreListener("RTC1:PRE_ON_RESET"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_EXECUTE, TestPreListener("RTC1:PRE_ON_EXECUTE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_STATE_UPDATE, TestPreListener("RTC1:PRE_ON_STATE_UPDATE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_RATE_CHANGED, TestPreListener("RTC1:PRE_ON_RATE_CHANGED"))
    
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_INITIALIZE, TestPostListener("RTC1:POST_ON_INITIALIZE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_FINALIZE, TestPostListener("RTC1:POST_ON_FINALIZE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_STARTUP, TestPostListener("RTC1:POST_ON_STARTUP"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_SHUTDOWN, TestPostListener("RTC1:POST_ON_SHUTDOWN"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_ACTIVATED, TestPostListener("RTC1:POST_ON_ACTIVATED"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_DEACTIVATED, TestPostListener("RTC1:POST_ON_DEACTIVATED"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_ABORTING, TestPostListener("RTC1:POST_ON_ABORTING"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_ERROR, TestPostListener("RTC1:POST_ON_ERROR"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_RESET, TestPostListener("RTC1:POST_ON_RESET"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_EXECUTE, TestPostListener("RTC1:POST_ON_EXECUTE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_STATE_UPDATE, TestPostListener("RTC1:POST_ON_STATE_UPDATE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_RATE_CHANGED, TestPostListener("RTC1:POST_ON_RATE_CHANGED"))

    
        

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


    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_INITIALIZE, TestPreListener("RTC2:PRE_ON_INITIALIZE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_FINALIZE, TestPreListener("RTC2:PRE_ON_FINALIZE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_STARTUP, TestPreListener("RTC2:PRE_ON_STARTUP"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_SHUTDOWN, TestPreListener("RTC2:PRE_ON_SHUTDOWN"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ACTIVATED, TestPreListener("RTC2:PRE_ON_ACTIVATED"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_DEACTIVATED, TestPreListener("RTC2:PRE_ON_DEACTIVATED"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ABORTING, TestPreListener("RTC2:PRE_ON_ABORTING"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ERROR, TestPreListener("RTC2:PRE_ON_ERROR"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_RESET, TestPreListener("RTC2:PRE_ON_RESET"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_EXECUTE, TestPreListener("RTC2:PRE_ON_EXECUTE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_STATE_UPDATE, TestPreListener("RTC2:PRE_ON_STATE_UPDATE"))
    self.addPreComponentActionListener(OpenRTM_aist.PreComponentActionListenerType.PRE_ON_RATE_CHANGED, TestPreListener("RTC2:PRE_ON_RATE_CHANGED"))
    
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_INITIALIZE, TestPostListener("RTC2:POST_ON_INITIALIZE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_FINALIZE, TestPostListener("RTC2:POST_ON_FINALIZE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_STARTUP, TestPostListener("RTC2:POST_ON_STARTUP"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_SHUTDOWN, TestPostListener("RTC2:POST_ON_SHUTDOWN"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_ACTIVATED, TestPostListener("RTC2:POST_ON_ACTIVATED"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_DEACTIVATED, TestPostListener("RTC2:POST_ON_DEACTIVATED"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_ABORTING, TestPostListener("RTC2:POST_ON_ABORTING"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_ERROR, TestPostListener("RTC2:POST_ON_ERROR"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_RESET, TestPostListener("RTC2:POST_ON_RESET"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_EXECUTE, TestPostListener("RTC2:POST_ON_EXECUTE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_STATE_UPDATE, TestPostListener("RTC2:POST_ON_STATE_UPDATE"))
    self.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_RATE_CHANGED, TestPostListener("RTC2:POST_ON_RATE_CHANGED"))

    
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
  




class test_ComponentActionListener(unittest.TestCase):
  
  def setUp(self):
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
    while(True):
        time.sleep(10)

############### test #################
if __name__ == '__main__':
        unittest.main()
