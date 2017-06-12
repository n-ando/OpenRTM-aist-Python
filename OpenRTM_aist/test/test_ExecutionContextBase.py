#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test_ExecutionContextBase.py
# @brief test for ExecutionContext base class
# @date $Date: 2007/08/31$
# @author Shinji Kurihara
#
# Copyright (C) 2011
#    Task-intelligence Research Group,
#    Intelligent Systems Research Institute,
#    National Institute of
#       Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.

import sys
sys.path.insert(1,"../")
sys.path.insert(1,"../RTM_IDL")

import time
import unittest

from ExecutionContextBase import *
import OpenRTM__POA, RTC__POA, RTC
import OpenRTM_aist

testcomp_spec = ["implementation_id", "TestComp",
                 "type_name",         "TestComp",
                 "description",       "Test example component",
                 "version",           "1.0",
                 "vendor",            "Shinji Kurihara, AIST",
                 "category",          "example",
                 "activity_type",     "DataFlowComponent",
                 "max_instance",      "10",
                 "language",          "Python",
                 "lang_type",         "compile",
                 ""]

class TestComp(OpenRTM_aist.DataFlowComponentBase):
  def __init_(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

    
def TestCompInit(manager):
  global com
  profile = OpenRTM_aist.Properties(defaults_str=configsample_spec)
  manager.registerFactory(profile,
        TestComp,
        OpenRTM_aist.Delete)


class MyEC(OpenRTM__POA.ExtTrigExecutionContextService):
  def __init__(self):
    self._ref = self._this()
    return


class MyEC2(ExecutionContextBase):
  def __init__(self, name):
    ExecutionContextBase.__init__(self, name)
    return

  def onStarting(self):
    return RTC.RTC_OK

  def onStarted(self):
    return RTC.RTC_OK

  def onGetRate(self, rate):
    return rate


class MyEC3(ExecutionContextBase,
            RTC__POA.ExecutionContextService,
            OpenRTM_aist.Task):

  def __init__(self, name):
    ExecutionContextBase.__init__(self, name)
    OpenRTM_aist.Task.__init__(self)
    self.setObjRef(self._this())
    self._svc = False
    return

  def __del__(self, Task=OpenRTM_aist.Task):
    self._svc = False
    return

  def start(self):
    return ExecutionContextBase.start(self)

  def stop(self):
    self._svc = False
    return

  def open(self, *args):
    self.activate()
    return 0

  def onStarting(self):
    self._svc = True
    self.open(0)
    return RTC.RTC_OK


  def svc(self):
    while self._svc:
      ExecutionContextBase.invokeWorkerPreDo(self)
      ExecutionContextBase.invokeWorkerDo(self)
      ExecutionContextBase.invokeWorkerPostDo(self)

    return 0

  def onGetRate(self, rate):
    return rate

    
class TestExecutioncontextBase(unittest.TestCase):
  def setUp(self):
    self.ecbase = ExecutionContextBase("test")

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_init(self):
    default_conf = ["sync_transition",      "YES",
                    "sync_activation",      "YES",
                    "sync_deactivation",    "YES",
                    "sync_reset",           "YES",
                    "transition_timeout",   "0.5",
                    "activation_timeout",   "0.5",
                    "deactivation_timeout", "0.5",
                    "reset_timeout",        "0.5",
                    ""]

    prop_ = OpenRTM_aist.Properties(defaults_str=default_conf)
    self.ecbase.init(prop_)
    return

  def test_bindComponent(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    ec_ = MyEC()
    self.ecbase.setObjRef(ec_._ref)
    self.assertEqual(RTC.RTC_OK, self.ecbase.bindComponent(comp))
    return

  def test_isRunning(self):
    ecbase = MyEC2("test ec")
    self.assertEqual(False,      ecbase.isRunning())
    self.assertEqual(RTC.RTC_OK, ecbase.start())
    self.assertEqual(True,       ecbase.isRunning())
    self.assertEqual(RTC.RTC_OK, ecbase.stop())
    self.assertEqual(False,      ecbase.isRunning())
    return

  def test_getRate(self):
    # default rate in DefaltConfig: 1000
    # default rate in ExecutionContextProfile.__init__ : 1000000.0
    self.assertEqual(1000000.0, self.ecbase.getRate())
    self.assertEqual(RTC.RTC_OK, self.ecbase.setRate(1000.0))
    self.assertEqual(1000.0, self.ecbase.getRate())
    self.assertEqual(0.001, self.ecbase.getPeriod().toDouble())
    return

  def test_addRemoveComponent(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    ec_ = MyEC()
    self.ecbase.setObjRef(ec_._ref)
    self.assertEqual(ec_._ref, self.ecbase.getObjRef())
    ret = comp.getObjRef()._is_equivalent(comp.getObjRef())
    self.assertEqual(RTC.RTC_OK, self.ecbase.addComponent(comp.getObjRef()))
    self.ecbase.invokeWorker()
    self.assertEqual(RTC.BAD_PARAMETER, self.ecbase.removeComponent(None))
    self.assertEqual(RTC.RTC_OK, self.ecbase.removeComponent(comp.getObjRef()))
    return

  def test_actDeactResetComponent(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    ec_ = MyEC3("test")
    self.assertEqual(RTC.RTC_OK, ec_.bindComponent(comp))
    ec_.start()
    self.assertEqual(RTC.RTC_OK, ec_.activateComponent(comp.getObjRef()))
    self.assertEqual(RTC.ACTIVE_STATE, ec_.getComponentState(comp.getObjRef()))
    self.assertEqual(RTC.ACTIVE_STATE, ec_.getComponentState(comp.getObjRef()))
    time.sleep(0.1)
    self.assertEqual(RTC.RTC_OK, ec_.deactivateComponent(comp.getObjRef()))
    self.assertEqual(RTC.INACTIVE_STATE, ec_.getComponentState(comp.getObjRef()))
    rtobj_ = [None]
    ec_._worker.activateComponent(comp.getObjRef(),rtobj_)
    ec_.waitForActivated(rtobj_[0])
    rtobj_[0].goTo(RTC.ERROR_STATE)
    time.sleep(0.1)
    self.assertEqual(RTC.ERROR_STATE, ec_.getComponentState(comp.getObjRef()))
    self.assertEqual(RTC.RTC_OK, ec_.resetComponent(comp.getObjRef()))
    self.assertEqual(RTC.INACTIVE_STATE, ec_.getComponentState(comp.getObjRef()))
    ec_.stop()
    return

  def test_getStateString(self):
    self.assertEqual("CREATED_STATE",  self.ecbase.getStateString(RTC.CREATED_STATE))
    self.assertEqual("INACTIVE_STATE", self.ecbase.getStateString(RTC.INACTIVE_STATE))
    self.assertEqual("ACTIVE_STATE",   self.ecbase.getStateString(RTC.ACTIVE_STATE))
    self.assertEqual("ERROR_STATE",    self.ecbase.getStateString(RTC.ERROR_STATE))
    return

  def test_getKind(self):
    self.assertEqual(RTC.PERIODIC,  self.ecbase.getKind())
    self.assertEqual(RTC.RTC_OK,  self.ecbase.setKind(RTC.PERIODIC))
    self.assertEqual(RTC.PERIODIC,  self.ecbase.getKind())
    self.assertEqual(RTC.RTC_OK,  self.ecbase.setKind(RTC.EVENT_DRIVEN))
    self.assertEqual(RTC.EVENT_DRIVEN,  self.ecbase.getKind())
    self.assertEqual(RTC.RTC_OK,  self.ecbase.setKind(RTC.OTHER))
    self.assertEqual(RTC.OTHER,  self.ecbase.getKind())
    self.assertEqual("PERIODIC",  self.ecbase.getKindString(RTC.PERIODIC))
    self.assertEqual("EVENT_DRIVEN",  self.ecbase.getKindString(RTC.EVENT_DRIVEN))
    self.assertEqual("OTHER",  self.ecbase.getKindString(RTC.OTHER))
    return

  def test_getSetProfile(self):
    self.assertEqual(RTC.PERIODIC,  self.ecbase.getProfile().kind)
    self.assertEqual(1000000.0,  self.ecbase.getProfile().rate)
    self.assertEqual(RTC.RTC_OK,  self.ecbase.setKind(RTC.EVENT_DRIVEN))
    self.assertEqual(RTC.RTC_OK,  self.ecbase.setRate(1000))
    self.assertEqual(RTC.EVENT_DRIVEN,  self.ecbase.getProfile().kind)
    self.assertEqual(1000.0,  self.ecbase.getProfile().rate)
    return

  def test_setOwner(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    self.ecbase.setOwner(comp.getObjRef())
    self.assertEqual(comp.getObjRef(), self.ecbase.getOwner())
    return

  def test_getComponentList(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    ec_ = MyEC()
    self.ecbase.setObjRef(ec_._ref)
    self.assertEqual(ec_._ref, self.ecbase.getObjRef())
    ret = comp.getObjRef()._is_equivalent(comp.getObjRef())
    self.assertEqual(RTC.RTC_OK, self.ecbase.addComponent(comp.getObjRef()))
    self.assertEqual(1, len(self.ecbase.getComponentList()))
    return

  def test_setProperties(self):
    prop_ = OpenRTM_aist.Properties()
    prop_.setProperty("rate", 10)
    prop_.setProperty("kind", RTC.PERIODIC)
    self.ecbase.setProperties(prop_)
    self.assertEqual("10", self.ecbase.getProperties().getProperty("rate"))
    self.assertEqual("PERIODIC", self.ecbase.getProperties().getProperty("kind"))
    return


  def test_setExecutionRate(self):
    prop_ = OpenRTM_aist.Properties()
    prop_.setProperty("rate", 123)
    self.assertEqual(True, self.ecbase.setExecutionRate(prop_))
    self.assertEqual(123.0, self.ecbase.getRate())
    return

  def test_setTransitionMode(self):
    prop_ = OpenRTM_aist.Properties()
    prop_.setProperty("sync_transition", "NO")
    ret_ = [True]
    self.assertEqual(True, self.ecbase.setTransitionMode(prop_, "sync_transition", ret_))
    self.assertEqual(False, ret_[0])
    return

  def test_setTimeout(self):
    prop_ = OpenRTM_aist.Properties()
    prop_.setProperty("transition_timeout", 321)
    ret_ = [None]
    self.assertEqual(True, self.ecbase.setTimeout(prop_, "transition_timeout", ret_))
    self.assertEqual(321.0, ret_[0].toDouble())
    return


############### test #################
if __name__ == '__main__':
  unittest.main()
