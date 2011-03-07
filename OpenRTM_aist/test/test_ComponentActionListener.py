#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test_ComponentActionListener.py
# @brief test for ComponentActionListener class
# @date $Date$
# @author Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import sys
sys.path.insert(1,"../")

import unittest

from ComponentActionListener import *
import OpenRTM_aist

class MockPreComponentActionListener(PreComponentActionListener):
  def __init__(self):
    PreComponentActionListener.__init__(self)
    return

  def __call__(self,id):
    return id


class MockPostComponentActionListener(PostComponentActionListener):
  def __init__(self):
    PostComponentActionListener.__init__(self)
    return

  def __call__(self,id,ret):
    return id,ret


class MockPortActionListener(PortActionListener):
  def __init__(self):
    PortActionListener.__init__(self)
    return

  def __call__(self, pprof):
    return pprof


class MockExecutionContextActionListener(ExecutionContextActionListener):
  def __init__(self):
    ExecutionContextActionListener.__init__(self)
    return


class TestListener(unittest.TestCase):
  def setUp(self):
    return

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_PreComponentActionListener_toString(self):
    self.asserEqual("PRE_ON_INITIALIZE",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_INITIALIZE))
    
    self.asserEqual("PRE_ON_FINALIZE",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_FINALIZE))

    self.asserEqual("PRE_ON_STARTUP",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_STARTUP))

    self.asserEqual("PRE_ON_SHUTDOWN",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_SHUTDOWN))

    self.asserEqual("PRE_ON_ACTIVATED",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_ACTIVATED))

    self.asserEqual("PRE_ON_DEACTIVATED",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_DEACTIVATED))

    self.asserEqual("PRE_ON_ABORTING",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_ABORTING))

    self.asserEqual("PRE_ON_ERROR",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_ERROR))

    self.asserEqual("PRE_ON_RESET",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_RESET))

    self.asserEqual("PRE_ON_EXECUTE",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_EXECUTE))

    self.asserEqual("PRE_ON_STATE_UPDATE",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_STATE_UPDATE))

    self.asserEqual("PRE_ON_RATE_CHANGED",
                    PreComponentActionListener.toString(
        PreComponentActionListenerTyep.PRE_ON_RATE_CHANGED))

    return

  def test_PostComponentActionListener_toString(self):
    self.asserEqual("POST_ON_INITIALIZE",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_INITIALIZE))
    
    self.asserEqual("POST_ON_FINALIZE",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_FINALIZE))

    self.asserEqual("POST_ON_STARTUP",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_STARTUP))

    self.asserEqual("POST_ON_SHUTDOWN",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_SHUTDOWN))

    self.asserEqual("POST_ON_ACTIVATED",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_ACTIVATED))

    self.asserEqual("POST_ON_DEACTIVATED",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_DEACTIVATED))

    self.asserEqual("POST_ON_ABORTING",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_ABORTING))

    self.asserEqual("POST_ON_ERROR",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_ERROR))

    self.asserEqual("POST_ON_RESET",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_RESET))

    self.asserEqual("POST_ON_EXECUTE",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_EXECUTE))

    self.asserEqual("POST_ON_STATE_UPDATE",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_STATE_UPDATE))

    self.asserEqual("POST_ON_RATE_CHANGED",
                    PostComponentActionListener.toString(
        PostComponentActionListenerTyep.POST_ON_RATE_CHANGED))

    return

  def test_PortActionListener_toString(self):
    self.asserEqual("ADD_PORT",
                    PortActionListener.toString(
        PortActionListenerTyep.ADD_PORT))

    self.asserEqual("REMOVE_PORT",
                    PortActionListener.toString(
        PortActionListenerTyep.REMOVE_PORT))

    return

  def test_ExecutionContextActionListener_toString(self):
    self.asserEqual("EC_ATTACHED",
                    ExecutionContextActionListener.toString(
        ExecutionContextActionListenerTyep.EC_ATTACHED))

    self.asserEqual("EC_DETACHED",
                    ExecutionContextActionListener.toString(
        ExecutionContextActionListenerTyep.EC_DETACHED))

    return


  def test_PreComponentActionListenerHolder(self):
    preactions = ComponentActionListeners()
    listener = MockPreComponentActionListener("test precomponent")
    preactions.preaction[0].addListener(listener,True)
    preactions.preaction[0].notify("test precomp ec_id")
    preactions.preaction[0].removeListener(listener)
    return

  def test_PostComponentActionListenerHolder(self):
    postactions = ComponentActionListeners()
    listener = MockPostComponentActionListener("test postcomponent")
    postactions.postaction[0].addListener(listener,True)
    postactions.postaction[0].notify("test postcomp ec_id")
    postactions.postaction[0].removeListener(listener)
    return

  def test_PortActionListenerHolder(self):
    portactions = ComponentActionListeners()
    listener = MockPortActionListener("test port")
    portactions.portaction[0].addListener(listener,True)
    portactions.portaction[0].notify("test port pprof")
    portactions.portaction[0].removeListener(listener)
    return

  def test_ExecutionContextActionListenerHolder(self):
    ecactions = ComponentActionListeners()
    listener = MockExecutionContextActionListener("test ec")
    ecactions.ecaction[0].addListener(listener,True)
    ecactions.ecaction[0].notify("test ec ec_id")
    ecactions.ecaction[0].removeListener(listener)
    return


############### test #################
if __name__ == '__main__':
        unittest.main()
