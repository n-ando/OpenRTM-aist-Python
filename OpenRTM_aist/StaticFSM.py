#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file StaticFSM.py
# @brief Static FSM framework based on Macho
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist
import RTC


def FSM_TOPSTATE(TOP):
  OpenRTM_aist.Macho.TOPSTATE(TOP)


def FSM_SUBSTATE(STATE, SUPERSTATE):
  OpenRTM_aist.Macho.SUBSTATE(STATE, SUPERSTATE)


class Machine(OpenRTM_aist.Macho.Machine):
  def __init__(self, TOP, comp):
    super(Machine,self).__init__(TOP, OpenRTM_aist.Macho.TopBase(TOP))
    self._rtComponent = comp
    
    
  def __del__(self):
    pass
  def init_other(self, other):
    pass
  def equal(self, snapshot):
    pass
  def getComp(self):
    return self._rtComponent



class Link(OpenRTM_aist.Macho.Link):
  def __init__(self, instance):
    super(Link,self).__init__(instance)
    self._rtComponent = None
  def __del__(self):
    pass
  def setrtc(self):
    if self._rtComponent:
      return
    machine = self._myStateInstance.machine()
    if machine:
      self._rtComponent = machine.getComp()

  def entry(self):
    self.setrtc()
    if not self._rtComponent:
      self.onEntry()
    else:
      self._rtComponent.postOnFsmStateChange(self._state_name(), RTC.RTC_OK)
      self._rtComponent.preOnFsmEntry(self._state_name())
      self._rtComponent.postOnFsmEntry(self._state_name(), self.onEntry())

  def init(self):
    self.setrtc()
    if not self._rtComponent:
      self.onInit()
    else:
      self._rtComponent.preOnFsmInit(self._state_name())
      self._rtComponent.postOnFsmInit(self._state_name(), self.onInit())


  def exit(self):
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