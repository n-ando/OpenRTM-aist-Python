#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test_ExecutionContextWorker.py
# @brief test for ExecutionContext's state machine worker class
# @date $Date$
# @author Shinji Kurihara
#
# Copyright (C) 2011
#     Noriaki Ando
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import sys
sys.path.insert(1,"../")
sys.path.insert(1,"../RTM_IDL")

import time
import unittest

from ExecutionContextWorker import *
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

class MyEC3(OpenRTM_aist.ExecutionContextBase,
            RTC__POA.ExecutionContextService,
            OpenRTM_aist.Task):

  def __init__(self, name):
    OpenRTM_aist.ExecutionContextBase.__init__(self, name)
    OpenRTM_aist.Task.__init__(self)
    self.setObjRef(self._this())
    self._svc = False
    return

  def __del__(self, Task=OpenRTM_aist.Task):
    self._svc = False
    return

  def start(self):
    return OpenRTM_aist.ExecutionContextBase.start(self)

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
      OpenRTM_aist.ExecutionContextBase.invokeWorkerPreDo(self)
      OpenRTM_aist.ExecutionContextBase.invokeWorkerDo(self)
      OpenRTM_aist.ExecutionContextBase.invokeWorkerPostDo(self)

    return 0

  def onGetRate(self, rate):
    return rate

class TestExecutionContextWorker(unittest.TestCase):

  def setUp(self):
    self._ecworker = ExecutionContextWorker()

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_setGetECRef(self):
    ec_ = MyEC()
    ref_ = ec_._ref
    self._ecworker.setECRef(ref_)
    self.assertEqual(ref_,self._ecworker.getECRef())

    return


  def test_startStopIsRunning(self):
    self.assertEqual(RTC.RTC_OK, self._ecworker.start())
    self.assertEqual(RTC.PRECONDITION_NOT_MET, self._ecworker.start())
    self.assertEqual(True, self._ecworker.isRunning())
    self.assertEqual(RTC.RTC_OK, self._ecworker.stop())
    self.assertEqual(False, self._ecworker.isRunning())
    self.assertEqual(RTC.PRECONDITION_NOT_MET, self._ecworker.stop())
    return

  def test_actDeactResetState(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)
    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)
    comp = mgr_.createComponent("TestComp")
    ec_ = MyEC3("test")
    self._ecworker.setECRef(ec_._this())
    self.assertEqual(RTC.RTC_OK,self._ecworker.bindComponent(comp))
    self._ecworker.start()
    rtobj_ = [None]

    # INACTIVE -> ACTIVE
    self.assertEqual(RTC.RTC_OK, self._ecworker.activateComponent(comp.getObjRef(),rtobj_))
    self.assertEqual(False, self._ecworker.isAllCurrentState(RTC.ACTIVE_STATE))
    self.assertEqual(True, self._ecworker.isAllNextState(RTC.ACTIVE_STATE))
    self.assertEqual(False, self._ecworker.isOneOfCurrentState(RTC.ACTIVE_STATE))
    self._ecworker.invokeWorker()
    self.assertEqual(RTC.ACTIVE_STATE, self._ecworker.getComponentState(comp.getObjRef()))
    self.assertEqual(True, self._ecworker.isAllCurrentState(RTC.ACTIVE_STATE))
    self.assertEqual(True, self._ecworker.isOneOfCurrentState(RTC.ACTIVE_STATE))

    # ACTIVE -> INACTIVE
    self.assertEqual(RTC.RTC_OK, self._ecworker.deactivateComponent(comp.getObjRef(),rtobj_))
    self.assertEqual(False, self._ecworker.isAllCurrentState(RTC.INACTIVE_STATE))
    self.assertEqual(True, self._ecworker.isOneOfNextState(RTC.INACTIVE_STATE))
    self.assertEqual(True, self._ecworker.isAllNextState(RTC.INACTIVE_STATE))
    self._ecworker.invokeWorker()
    self.assertEqual(RTC.INACTIVE_STATE, self._ecworker.getComponentState(comp.getObjRef()))
    self.assertEqual(True, self._ecworker.isAllCurrentState(RTC.INACTIVE_STATE))

    # INACTIVE -> ACTIVE -> ERROR
    self.assertEqual(RTC.RTC_OK, self._ecworker.activateComponent(comp.getObjRef(),rtobj_))
    self._ecworker.invokeWorker()
    rtobj_[0] = self._ecworker.findComponent(comp.getObjRef())
    rtobj_[0].goTo(RTC.ERROR_STATE)
    self.assertEqual(True, self._ecworker.isOneOfNextState(RTC.ERROR_STATE))
    self._ecworker.invokeWorker()
    self.assertEqual(RTC.ERROR_STATE, self._ecworker.getComponentState(comp.getObjRef()))

    # ERROR -> INACTIVE
    self.assertEqual(RTC.RTC_OK, self._ecworker.resetComponent(comp.getObjRef(),rtobj_))
    self._ecworker.invokeWorker()
    self.assertEqual(RTC.INACTIVE_STATE, self._ecworker.getComponentState(comp.getObjRef()))
    self.assertEqual(True, self._ecworker.isAllCurrentState(RTC.INACTIVE_STATE))
    self._ecworker.stop()
    return

  def waitActivateComplete(self):
    # No implementation.
    return

  def waitDeactivateComplete(self):
    # No implementation.
    return

  def waitResetComplete(self):
    # No implementation.
    return

  def test_getStateString(self):
    self.assertEqual("CREATED_STATE",  self._ecworker.getStateString(RTC.CREATED_STATE))
    self.assertEqual("INACTIVE_STATE", self._ecworker.getStateString(RTC.INACTIVE_STATE))
    self.assertEqual("ACTIVE_STATE",   self._ecworker.getStateString(RTC.ACTIVE_STATE))
    self.assertEqual("ERROR_STATE",    self._ecworker.getStateString(RTC.ERROR_STATE))
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
    self._ecworker.setECRef(ec_._ref)
    self.assertEqual(RTC.RTC_OK, self._ecworker.addComponent(comp.getObjRef()))
    self._ecworker.invokeWorker()
    self.assertEqual(RTC.BAD_PARAMETER, self._ecworker.removeComponent(None))
    self.assertEqual(RTC.RTC_OK, self._ecworker.removeComponent(comp.getObjRef()))
    return

  def test_invokeWorker(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    ec_ = MyEC()
    self._ecworker.setECRef(ec_._ref)
    self.assertEqual(RTC.RTC_OK, self._ecworker.addComponent(comp.getObjRef()))
    self._ecworker.invokeWorkerPreDo()
    self._ecworker.invokeWorkerDo()
    self._ecworker.invokeWorkerPostDo()
    self._ecworker.updateComponentList()
    self.assertEqual(RTC.BAD_PARAMETER, self._ecworker.removeComponent(None))
    self.assertEqual(RTC.RTC_OK, self._ecworker.removeComponent(comp.getObjRef()))
    return


############### test #################
if __name__ == '__main__':
  unittest.main()
