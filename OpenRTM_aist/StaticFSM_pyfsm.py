#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file StaticFSM_pyfsm.py
# @brief Static FSM framework based on pyfsm
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import pyfsm
import RTC


def fsm_topstate(TOP):
  ret = pyfsm.topstate(TOP)
  class STATE(ret):
    def __init__(self, instance):
      ret.__init__(self, instance)
    def on_entry(self, *argv):
      OpenRTM_aist.Link.call_entry(self)
      ret.on_entry(self, *argv)
    def on_exit(self, *argv):
      OpenRTM_aist.Link.call_exit(self)
      ret.on_exit(self, *argv)
    def on_init(self, *argv):
      OpenRTM_aist.Link.call_init(self)
      ret.on_init(self, *argv)
  return ret


def fsm_substate(superstate):
  def _fsm_substate(cls):
    ret = pyfsm.substate(superstate)(cls)
    class STATE(ret):
      def __init__(self, instance):
        ret.__init__(self, instance)
      def on_entry(self, *argv):
        OpenRTM_aist.Link.call_entry(self)
        ret.on_entry(self, *argv)
      def on_exit(self, *argv):
        OpenRTM_aist.Link.call_exit(self)
        ret.on_exit(self, *argv)
      def on_init(self, *argv):
        OpenRTM_aist.Link.call_init(self)
        ret.on_init(self, *argv)

    return ret
  return _fsm_substate






class Machine(pyfsm.Machine):
  def __init__(self, TOP, comp):
    self._rtComponent = comp
    super(Machine,self).__init__(TOP)
    
    
    
  def __del__(self):
    pass
  def init_other(self, other):
    pass
  def equal(self, snapshot):
    pass
  def getComp(self):
    return self._rtComponent



class Link(pyfsm.StateDef):
  def __init__(self):
    super(Link,self).__init__()
    self._rtComponent = None
  def __del__(self):
    pass
  def setrtc(self):
    if self._rtComponent:
      return
    machine = self._myStateInstance.machine()
    if machine:
      self._rtComponent = machine.getComp()

  def call_entry(self):
    self.setrtc()
    if not self._rtComponent:
      self.onEntry()
    else:
      self._rtComponent.postOnFsmStateChange(self._state_name(), RTC.RTC_OK)
      self._rtComponent.preOnFsmEntry(self._state_name())
      self._rtComponent.postOnFsmEntry(self._state_name(), self.onEntry())

  def call_init(self):
    self.setrtc()
    if not self._rtComponent:
      self.onInit()
    else:
      self._rtComponent.preOnFsmInit(self._state_name())
      self._rtComponent.postOnFsmInit(self._state_name(), self.onInit())


  def call_exit(self):
    self.setrtc()
    if not self._rtComponent:
      self.onExit()
    else:
      self._rtComponent.preOnFsmExit(self._state_name())
      self._rtComponent.postOnFsmExit(self._state_name(), self.onExit())
      self._rtComponent.preOnFsmStateChange(self._state_name())

  def onEntry(self):
    return RTC.RTC_OK
  def onInit(self):
    return RTC.RTC_OK
  def onExit(self):
    return RTC.RTC_OK


State = pyfsm.State
deephistory = pyfsm.deephistory
Event = pyfsm.Event