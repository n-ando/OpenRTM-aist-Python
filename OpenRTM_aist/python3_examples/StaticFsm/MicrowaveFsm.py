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

@OpenRTM_aist.fsm_topstate
class TOP(OpenRTM_aist.Link):
  def on_init(self):
    self.set_state(OpenRTM_aist.Macho.State(Operational))


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

  class Data:
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
  
    

    
@OpenRTM_aist.fsm_substate(TOP)
class Disabled(OpenRTM_aist.Link):
  def on_entry(self):
    print("  Microwave opened")
  def on_exit(self):
    print("  Microwave closed")
  def close(self):
    #self.setStateHistory(OpenRTM_aist.Macho.State(Operational))
    self.set_state(OpenRTM_aist.Macho.State(Operational))
    


@OpenRTM_aist.Macho.deephistory
@OpenRTM_aist.fsm_substate(TOP)
class Operational(OpenRTM_aist.Link):
  def open(self):
    self.set_state(OpenRTM_aist.Macho.State(Disabled))
  def stop(self):
    self.set_state(OpenRTM_aist.Macho.State(Idle))
  def on_init(self):
    self.set_state(OpenRTM_aist.Macho.State(Idle))


  






@OpenRTM_aist.fsm_substate(Operational)
class Idle(OpenRTM_aist.Link):
  def minute(self, time_):
    self.set_state(OpenRTM_aist.Macho.State(Programmed))
    self.dispatch(OpenRTM_aist.Macho.Event(TOP.minute,time_))
    
  def on_entry(self):
    self.data(TOP).resetTimer()
    print("  Microwave ready")





@OpenRTM_aist.fsm_substate(Operational)
class Programmed(OpenRTM_aist.Link):
  def minute(self, time_):
    for t in range(time_.data):
      self.data(TOP).incrementTimer()
    self.data(TOP).printTimer()
  def start(self):
    self.setState(Cooking)





@OpenRTM_aist.fsm_substate(Programmed)
class Cooking(OpenRTM_aist.Link):
  def tick(self):
    print("  Clock tick")
    tb = self.data(TOP)
    tb.decrementTimer()
    if tb.getRemainingTime() == 0:
      print("  Finished")
      self.setState(Idle)
    else:
      tb.printTimer()
    
  def on_entry(self):
    print("  Heating on")
  def on_exit(self):
    print("  Heating off")


