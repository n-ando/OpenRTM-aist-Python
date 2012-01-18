#!/usr/bin/env python
# -*- Python -*-

#
# \file test_ManagerActionListener.py
# \brief test for ManagerActionListener class
# \date $Date: 2012/01/13$
# \author Shinji Kurihara
#
# Copyright (C) 2012
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
sys.path.insert(1,"../")

import unittest

from ManagerActionListener import *
import OpenRTM_aist

class MyManagerActionListener:
  def __init__(self):
    return

  def preShutdown(self):
    print "MyManagerActionListener.preShutdown "
    return

  def postShutdown(self):
    print "MyManagerActionListener.postShutdown "
    return

  def preReinit(self):
    print "MyManagerActionListener.preReinit "
    return

  def postReinit(self):
    print "MyManagerActionListener.postReinit "
    return

class MyModuleActionListener:
  def preLoad(self, modname, funcname):
    print "MyModuleActionListener.preLoad "
    return

  def postLoad(self, modname, funcname):
    print "MyModuleActionListener.postLoad "
    return

  def preUnload(self, modname):
    print "MyModuleActionListener.preUnload "
    return

  def postUnload(self, modname):
    print "MyModuleActionListener.postUnload "
    return

class MyRtcLifecycleActionListener:
  def preCreate(self, args):
    print "MyRtcLifecycleActionListener.preCreate "
    return

  def postCreate(self, args):
    print "MyRtcLifecycleActionListener.postCreate "
    return

  def preConfigure(self, prop):
    print "MyRtcLifecycleActionListener.preConfigure "
    return

  def postConfigure(self, prop):
    print "MyRtcLifecycleActionListener.postConfigure "
    return

  def preInitialize(self):
    print "MyRtcLifecycleActionListener.preInitialize "
    return

  def postInitialize(self):
    print "MyRtcLifecycleActionListener.postInitialize "
    return

class MyNamingActionListener:
  def preBind(self, rtobj, name):
    print "MyNamingActionListener.preBind "
    return

  def postBind(self, rtobj, name):
    print "MyNamingActionListener.postBind "
    return

  def preUnbind(self, rtobj, name):
    print "MyNamingActionListener.preUnbind "
    return

  def postUnbind(self, rtobj, name):
    print "MyNamingActionListener.postUnbind "
    return

class MyLocalServiceActionListener:
  def preServiceRegister(self, service_name):
    print "MyLocalServiceActionListener.preServiceRegister "
    return

  def postServiceRegister(self, service_name, service):
    print "MyLocalServiceActionListener.postServiceRegister "
    return

  def preServiceInit(self, prop, service):
    print "MyLocalServiceActionListener.preServiceInit "
    return

  def postServiceInit(self, prop, service):
    print "MyLocalServiceActionListener.postServiceInit "
    return

  def preServiceReinit(self, prop, service):
    print "MyLocalServiceActionListener.preServiceReinit "
    return

  def postServiceReinit(self, prop, service):
    print "MyLocalServiceActionListener.postServiceReinit "
    return

  def preServiceFinalize(self, service_name, service):
    print "MyLocalServiceActionListener.preServiceFinalize "
    return

  def postServiceFinalize(self, service_name, service):
    print "MyLocalServiceActionListener.postServiceFinalize "
    return




class TestManagerActionListener(unittest.TestCase):
  def setUp(self):
    self.ma_listeners = ManagerActionListeners()
    return

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_ManagerActionListenerHolder(self):
    listener = MyManagerActionListener()
    self.ma_listeners.manager_.addListener(listener, True)
    self.ma_listeners.manager_.preShutdown()
    self.ma_listeners.manager_.postShutdown()
    self.ma_listeners.manager_.preReinit()
    self.ma_listeners.manager_.postReinit()
    self.ma_listeners.manager_.removeListener(listener)
    return

  def test_ModuleActionListenerHolder(self):
    listener = MyModuleActionListener()
    self.ma_listeners.module_.addListener(listener, True)
    self.ma_listeners.module_.preLoad("test_mod", "test_preLoad")
    self.ma_listeners.module_.postLoad("test_mod", "test_postLoad")
    self.ma_listeners.module_.preUnload("test_mod")
    self.ma_listeners.module_.postUnload("test_mod")
    self.ma_listeners.module_.removeListener(listener)
    return

  def test_RtcLifecycleActionListenerHolder(self):
    listener = MyRtcLifecycleActionListener()
    self.ma_listeners.rtclifecycle_.addListener(listener, True)
    self.ma_listeners.rtclifecycle_.preCreate("preCreate")
    self.ma_listeners.rtclifecycle_.postCreate("preCreate")
    self.ma_listeners.rtclifecycle_.preConfigure("preConf")
    self.ma_listeners.rtclifecycle_.postConfigure("preConf")
    self.ma_listeners.rtclifecycle_.preInitialize()
    self.ma_listeners.rtclifecycle_.postInitialize()
    self.ma_listeners.rtclifecycle_.removeListener(listener)
    return

  def test_NamingActionListenerHolder(self):
    listener = MyNamingActionListener()
    self.ma_listeners.naming_.addListener(listener, True)
    self.ma_listeners.naming_.preBind(None,"test_rtc")
    self.ma_listeners.naming_.postBind(None,"test_rtc")
    self.ma_listeners.naming_.preUnbind(None,"test_rtc")
    self.ma_listeners.naming_.postUnbind(None,"test_rtc")
    self.ma_listeners.naming_.removeListener(listener)
    return

  def test_LocalServiceActionListenerHolder(self):
    listener = MyLocalServiceActionListener()
    self.ma_listeners.localservice_.addListener(listener, True)
    self.ma_listeners.localservice_.preServiceRegister("servicename")
    self.ma_listeners.localservice_.postServiceRegister("servicename",None)
    self.ma_listeners.localservice_.preServiceInit(None, "servicename")
    self.ma_listeners.localservice_.postServiceInit(None, "servicename")
    self.ma_listeners.localservice_.preServiceReinit(None, "servicename")
    self.ma_listeners.localservice_.postServiceReinit(None, "servicename")
    self.ma_listeners.localservice_.preServiceFinalize(None, "servicename")
    self.ma_listeners.localservice_.postServiceFinalize(None, "servicename")
    self.ma_listeners.localservice_.removeListener(listener)
    return



############### test #################
if __name__ == '__main__':
        unittest.main()
