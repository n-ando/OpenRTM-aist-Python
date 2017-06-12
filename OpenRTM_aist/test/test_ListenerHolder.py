#!/usr/bin/env python
# -*- Python -*-

#
# \file test_ListenerHolder.py
# \brief test for ListenerHolder class
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

from ListenerHolder import *
import OpenRTM_aist

class MyListener:
  def func(self, *args):
    print "MyListener func args: ", args


class TestListenerHolder(unittest.TestCase):
  def setUp(self):
    self.lholder = ListenerHolder()
    self.listener = MyListener()


  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_addRemoveListener(self):
    self.lholder.addListener(self.listener,True)
    self.lholder.LISTENERHOLDER_CALLBACK(MyListener.func,"test"," ListenerHolder")
    self.lholder.removeListener(self.listener)
    return



############### test #################
if __name__ == '__main__':
        unittest.main()
