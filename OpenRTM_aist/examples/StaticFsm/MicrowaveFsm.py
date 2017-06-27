#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Microwave.py
# @brief example StaticFSM
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys

import RTC
import OpenRTM_aist
import OpenRTM_aist.Macho

class TOP(OpenRTM_aist.Link):
  def __init__(self, instance):
    super(TOP,self).__init__(instance)
  def entry(self):
    OpenRTM_aist.Link.entry(self)
  def exit(self):
    OpenRTM_aist.Link.exit(self)
  def init(self):
    OpenRTM_aist.Link.init(self)
    self.setState(Operational)
    

  def open(self):
    pass
  def close(self):
    pass
  def minute(self, time_):
    pass
  def start(self):
    pass
  def stop(self):
    pass
  def tick(self):
    pass

  class Box:
    def __init__(self):
      self.myCookingTime = 0
    def printTimer(self):
      print " Timer set to ", self.myCookingTime, " minutes"
    def incrementTimer(self):
      self.myCookingTime+=1
    def decrementTimer(self):
      self.myCookingTime-=1
    def resetTimer(self):
      self.myCookingTime = 0
    def getRemainingTime(self):
      return self.myCookingTime
  
    
OpenRTM_aist.FSM_TOPSTATE(TOP)
    

class Disabled(TOP):
  def __init__(self, instance):
    super(Disabled,self).__init__(instance)
  def entry(self):
    OpenRTM_aist.Link.entry(self)
    print("  Microwave opened")
  def exit(self):
    OpenRTM_aist.Link.exit(self)
    print("  Microwave closed")
  def close(self):
    self.setStateHistory(Operational)
  def init(self):
    OpenRTM_aist.Link.init(self)

OpenRTM_aist.FSM_SUBSTATE(Disabled,TOP)

class Operational(TOP):
  def __init__(self, instance):
    super(Operational,self).__init__(instance)
  def open(self):
    self.setState(Disabled)
  def stop(self):
    self.setState(Idle)
  def init(self):
    OpenRTM_aist.Link.init(self)
    self.setState(Idle)
  def entry(self):
    OpenRTM_aist.Link.entry(self)
  def exit(self):
    OpenRTM_aist.Link.exit(self)
  



OpenRTM_aist.FSM_SUBSTATE(Operational,TOP)
OpenRTM_aist.Macho.DEEPHISTORY(Operational)


class Idle(Operational):
  def __init__(self, instance):
    super(Idle,self).__init__(instance)
  def minute(self, time_):
    self.setState(Programmed)
    self["TopBase_"].dispatch(OpenRTM_aist.Macho.Event1("minute",time_))
    
  def entry(self):
    OpenRTM_aist.Link.entry(self)
    self[TOP].box().resetTimer()
    print("  Microwave ready")
  def init(self):
    OpenRTM_aist.Link.init(self)
  def exit(self):
    OpenRTM_aist.Link.exit(self)


OpenRTM_aist.FSM_SUBSTATE(Idle,Operational)


class Programmed(Operational):
  def __init__(self, instance):
    super(Programmed,self).__init__(instance)
  def minute(self, time_):
    for t in range(time_.data):
      self[TOP].box().incrementTimer()
    self[TOP].box().printTimer()
  def start(self):
    self.setState(Cooking)
  def entry(self):
    OpenRTM_aist.Link.entry(self)
  def exit(self):
    OpenRTM_aist.Link.exit(self)
  def init(self):
    OpenRTM_aist.Link.init(self)



OpenRTM_aist.FSM_SUBSTATE(Programmed,Operational)


class Cooking(Programmed):
  def __init__(self, instance):
    super(Cooking,self).__init__(instance)
  def tick(self):
    print("  Clock tick")
    tb = self[TOP].box()
    tb.decrementTimer()
    if tb.getRemainingTime() == 0:
      print("  Finished")
      self.setState(Idle)
    else:
      tb.printTimer()
    
  def entry(self):
    OpenRTM_aist.Link.entry(self)
    print("  Heating on")
  def exit(self):
    OpenRTM_aist.Link.exit(self)
    print("  Heating off")
  def init(self):
    OpenRTM_aist.Link.init(self)


OpenRTM_aist.FSM_SUBSTATE(Cooking,Programmed)