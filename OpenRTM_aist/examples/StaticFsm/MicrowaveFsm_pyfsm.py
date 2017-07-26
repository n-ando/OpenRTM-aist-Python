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
import OpenRTM_aist.StaticFSM_pyfsm as StaticFSM
import OpenRTM_aist.EventPort_pyfsm as EventPort

@StaticFSM.fsm_topstate
class TOP(StaticFSM.Link):
  def on_init(self):
    self.set_state(StaticFSM.State(Operational))


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
  
    

    
@StaticFSM.fsm_substate(TOP)
class Disabled(StaticFSM.Link):
  def on_entry(self):
    print("  Microwave opened")
  def on_exit(self):
    print("  Microwave closed")
  def close(self):
    #self.setStateHistory(OpenRTM_aist.Macho.State(Operational))
    self.set_state(StaticFSM.State(Operational))


@StaticFSM.deephistory
@StaticFSM.fsm_substate(TOP)
class Operational(StaticFSM.Link):
  def open(self):
    self.set_state(StaticFSM.State(Disabled))
  def stop(self):
    self.set_state(StaticFSM.State(Idle))
  def on_init(self):
    self.set_state(StaticFSM.State(Idle))


  






@StaticFSM.fsm_substate(Operational)
class Idle(StaticFSM.Link):
  def minute(self, time_):
    self.set_state(StaticFSM.State(Programmed))
    self.dispatch(StaticFSM.Event(TOP.minute,time_))
    
  def on_entry(self):
    self.data(TOP).resetTimer()
    print("  Microwave ready")





@StaticFSM.fsm_substate(Operational)
class Programmed(StaticFSM.Link):
  def minute(self, time_):
    for t in range(time_.data):
      self.data(TOP).incrementTimer()
    self.data(TOP).printTimer()
  def start(self):
    self.set_state(StaticFSM.State(Cooking))





@StaticFSM.fsm_substate(Programmed)
class Cooking(StaticFSM.Link):
  def tick(self):
    print("  Clock tick")
    tb = self.data(TOP)
    tb.decrementTimer()
    if tb.getRemainingTime() == 0:
      print("  Finished")
      self.set_state(StaticFSM.State(Idle))
    else:
      tb.printTimer()
    
  def on_entry(self):
    print("  Heating on")
  def on_exit(self):
    print("  Heating off")


