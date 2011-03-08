#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file test ConfigurationListener.py
# @brief test for ConfigurationListener class
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

from ConfigurationListener import *
import OpenRTM_aist


class TestListener(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        OpenRTM_aist.Manager.instance().shutdownManager()
        return

    def test_ConfigurationParamListener_toString(self):
        return

    def test_ConfigurationSetListener_toString(self):
        return

    def test_ConfigurationSetNameListener_toString(self):
        return

    def test_ConfigurationParamListenerHolder(self):
        return

    def test_ConfigurationSetListenerHolder(self):
        return

    def test_ConfigurationSetNameListenerHolder(self):
        return

############### test #################
if __name__ == '__main__':
    unittest.main()

