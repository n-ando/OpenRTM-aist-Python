#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test_ExecutionContextProfile.py
# @brief test for ExecutionContextProfile class
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

from ExecutionContextProfile import *
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

class MyEC(OpenRTM__POA.ExtTrigExecutionContextService):
  def __init__(self):
    self._ref = self._this()
    return

class TestExecutionContextProfile(unittest.TestCase):

  def setUp(self):
    self._ecprofile = ExecutionContextProfile()
    return

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_setGetObjRef(self):
    ec_ = MyEC()
    self._ecprofile.setObjRef(ec_._ref)
    self.assertEqual(ec_._ref, self._ecprofile.getObjRef())
    return

  def test_setGetRate(self):
    self._ecprofile.setRate(1000.0)
    self.assertEqual(1000.0, self._ecprofile.getRate())
    return

  def test_setGetPeriod(self):
    self.assertEqual(RTC.RTC_OK, self._ecprofile.setPeriod(0.1))
    self.assertEqual(RTC.BAD_PARAMETER, self._ecprofile.setPeriod(-0.1))
    self.assertEqual(0.1, self._ecprofile.getPeriod().toDouble())
    tv_ = OpenRTM_aist.TimeValue(-0.01)
    self.assertEqual(RTC.BAD_PARAMETER, self._ecprofile.setPeriod(tv=tv_))
    tv_ = OpenRTM_aist.TimeValue(0.01)
    self.assertEqual(RTC.RTC_OK, self._ecprofile.setPeriod(tv=tv_))
    self.assertEqual(0.01, self._ecprofile.getPeriod().toDouble())
    self.assertEqual(RTC.BAD_PARAMETER, self._ecprofile.setPeriod())
    return


  def test_getKindString(self):
    self.assertEqual("PERIODIC", self._ecprofile.getKindString(RTC.PERIODIC))
    self.assertEqual("EVENT_DRIVEN", self._ecprofile.getKindString(RTC.EVENT_DRIVEN))
    self.assertEqual("OTHER", self._ecprofile.getKindString(RTC.OTHER))
    self.assertEqual("", self._ecprofile.getKindString(RTC.UNSUPPORTED))
    return

  def test_setGetKind(self):
    self.assertEqual(RTC.RTC_OK, self._ecprofile.setKind(RTC.PERIODIC))
    self.assertEqual(RTC.PERIODIC, self._ecprofile.getKind())
    self.assertEqual(RTC.RTC_OK, self._ecprofile.setKind(RTC.PERIODIC))
    self.assertEqual("EVENT_DRIVEN", self._ecprofile.getKindString(RTC.EVENT_DRIVEN))
    self.assertEqual("OTHER", self._ecprofile.getKindString(RTC.OTHER))
    self.assertEqual("", self._ecprofile.getKindString(RTC.UNSUPPORTED))
    return

  def test_setOwner(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    self.assertEqual(RTC.RTC_OK, self._ecprofile.setOwner(comp.getObjRef()))
    self.assertEqual(comp.getObjRef(), self._ecprofile.getOwner())
    return

  def test_addRemoveComponent(self):
    mgr_ = OpenRTM_aist.Manager.instance()
    mgr_.activateManager()
    profile = OpenRTM_aist.Properties(defaults_str=testcomp_spec)

    mgr_.registerFactory(profile,
                         TestComp,
                         OpenRTM_aist.Delete)

    comp = mgr_.createComponent("TestComp")
    self.assertEqual(0, len(self._ecprofile.getComponentList()))
    self.assertEqual(RTC.RTC_OK, self._ecprofile.addComponent(comp.getObjRef()))
    self.assertEqual(RTC.BAD_PARAMETER, self._ecprofile.addComponent(None))
    self.assertEqual(RTC.BAD_PARAMETER, self._ecprofile.removeComponent(None))
    self.assertEqual(RTC.RTC_OK, self._ecprofile.removeComponent(comp.getObjRef()))
    self.assertEqual(0, len(self._ecprofile.getComponentList()))
    self.assertEqual(RTC.RTC_OK, self._ecprofile.addComponent(comp.getObjRef()))
    self.assertEqual(RTC.RTC_OK, self._ecprofile.addComponent(comp.getObjRef()))
    self.assertEqual(2, len(self._ecprofile.getComponentList()))
    return


  def test_setGetProperties(self):
    prop_ = OpenRTM_aist.Properties()
    prop_.setProperty("test", "test value")
    self._ecprofile.setProperties(prop_)
    self.assertEqual("test value", self._ecprofile.getProperties().getProperty("test"))
    prop_ = OpenRTM_aist.Properties()
    val_ = OpenRTM_aist.NVUtil.copyToProperties(prop_, self._ecprofile.getProfile().properties)
    self.assertEqual("test value", prop_.getProperty("test"))
    return


  def test_lock_unlock(self):
    self._ecprofile.lock()
    self._ecprofile.unlock()
    return


############### test #################
if __name__ == '__main__':
  unittest.main()
