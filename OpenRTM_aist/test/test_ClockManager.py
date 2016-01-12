#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test_ClockManager.py
# @brief test for ClockManager class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2012
#     Noriaki Ando
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import time
import sys
import math
sys.path.insert(1,"../")

import unittest
from ClockManager import *



class TestClockManager(unittest.TestCase):
  def setUp(self):
    self._cm = ClockManager.instance()
    return
  
  def test_LogicalClock(self):
    tm = self._cm.getClock("logical").gettime()
    self.assertEqual(0.0,tm.tv_sec)
    self.assertEqual(0.0,tm.tv_usec)
    stm = OpenRTM_aist.TimeValue(1,1)
    tm = self._cm.getClock("logical").settime(stm)
    tm = self._cm.getClock("logical").gettime()
    self.assertEqual(1,tm.tv_sec)
    self.assertEqual(1,tm.tv_usec)
    tm = ClockManager.instance().getClock("logical").gettime()
    self.assertEqual(1,tm.tv_sec)
    self.assertEqual(1,tm.tv_usec)
    return
  
  def test_AdjustedClock(self):
    tm = self._cm.getClock("adjusted").gettime()
    stm = OpenRTM_aist.TimeValue(1,1)
    tm = self._cm.getClock("adjusted").settime(stm)
    tm = self._cm.getClock("adjusted").gettime()
    return
  
  def test_SystemClock(self):
    tm = self._cm.getClock("system").gettime()
    stm = OpenRTM_aist.TimeValue(1,1)
    tm = self._cm.getClock("system").settime(stm)
    return
  
############### test #################
if __name__ == '__main__':
  unittest.main()
