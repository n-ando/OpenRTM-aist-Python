#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test_RTObjectStateMachine.py
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

import unittest

from RTObjectStateMachine import *
import OpenRTM__POA, RTC
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

class TestRTObjectStateMachine(unittest.TestCase):
  """
  """

  def setUp(self):
    self._mgr = OpenRTM_aist.Manager.instance()
    self._mgr.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)
    self._mgr.registerFactory(profile,
                              TestComp,
                              OpenRTM_aist.Delete)
    self._comp = self._mgr.createComponent("TestComp")
    self._rtsm = RTObjectStateMachine(0, self._comp.getObjRef())

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_getRTObject(self):
    self.assertEqual(self._comp.getObjRef(), self._rtsm.getRTObject())
    return

  def test_isEquivalent(self):
    self.assertEqual(True, self._rtsm.isEquivalent(self._comp.getObjRef()))
    return

  def test_getExecutionContextHandle(self):
    self.assertEqual(0, self._rtsm.getExecutionContextHandle())
    return

  def test_ComponentActionOperations(self):
    self._rtsm.onStartup()
    self._rtsm.onShutdown()
    self._rtsm.onActivated(RTC.INACTIVE_STATE)
    self._rtsm.onDeactivated(RTC.ACTIVE_STATE)
    self._rtsm.onError(RTC.ACTIVE_STATE)
    self._rtsm.onReset(RTC.ERROR_STATE)
    self._rtsm.onExecute(RTC.ACTIVE_STATE)
    self._rtsm.onStateUpdate(RTC.ACTIVE_STATE)
    self._rtsm.onRateChanged()
    self._rtsm.onAction(RTC.ACTIVE_STATE)
    self._rtsm.onModeChanged(RTC.ACTIVE_STATE)
    return

  def test_getState(self):
    self.assertEqual(RTC.INACTIVE_STATE, self._rtsm.getState())
    self.assertEqual(RTC.INACTIVE_STATE, self._rtsm.getStates().curr)
    self.assertEqual(True, self._rtsm.isCurrentState(RTC.INACTIVE_STATE))
    self.assertEqual(True, self._rtsm.isNextState(RTC.INACTIVE_STATE))
    self._rtsm.goTo(RTC.ACTIVE_STATE)
    self.assertEqual(True, self._rtsm.isNextState(RTC.ACTIVE_STATE))
    return


  def test_worker(self):
    self._rtsm.workerPreDo()
    self._rtsm.workerDo()
    self._rtsm.workerPostDo()
    return


  def test_ComponentAction(self):
    self._rtsm.setComponentAction(self._comp.getObjRef())
    self._rtsm.setDataFlowComponentAction(self._comp.getObjRef())
    self._rtsm.setFsmParticipantAction(self._comp.getObjRef())
    self._rtsm.setMultiModeComponentAction(self._comp.getObjRef())
    return



############### test #################
if __name__ == '__main__':
  unittest.main()
