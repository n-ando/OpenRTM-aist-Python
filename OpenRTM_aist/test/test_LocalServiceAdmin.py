#!/usr/bin/env python
# -*- Python -*-

#
# \file test_LocalServiceAdmin.py
# \brief test for LocalServiceAdmin class
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

from LocalServiceAdmin import *
import OpenRTM_aist

class MyLocalService:
  def __init__(self):
    return

  def init(self, props):
    return

  def reinit(self, props):
    return

  def getProfile(self):
    prop = OpenRTM_aist.LocalServiceProfile()
    prop.name = "MyLocalService"
    prop.uuid = "1234"
    p = OpenRTM_aist.Properties()
    p.setProperty("id_", 4321)
    prop.properties = p
    prop.service = self
    return prop

  def finalize(self):
    return

def MyLocalServiceInit():
  factory = OpenRTM_aist.LocalServiceFactory.instance()
  factory.addFactory("MyLocalService",
                     MyLocalService,
                     OpenRTM_aist.Delete)
  return
  


class TestLocalServiceAdmin(unittest.TestCase):
  def setUp(self):
    self.ladmin = LocalServiceAdmin()
    MyLocalServiceInit()
    return

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_init(self):
    prop = OpenRTM_aist.Properties()
    prop.setProperty("enabled_services","MyLocalService")
    self.ladmin.init(prop)
    self.ladmin.getServiceProfiles()
    
    get_prop = [OpenRTM_aist.Properties()]
    prof = self.ladmin.getServiceProfile("MyLocalService", get_prop)
    lsvc = self.ladmin.getService("MyLocalService")
    self.assertNotEqual(None, lsvc)
    self.assertEqual(True, self.ladmin.addLocalService(lsvc))
    self.assertEqual(True, self.ladmin.removeLocalService("MyLocalService"))
    self.ladmin.finalize()
    return



############### test #################
if __name__ == '__main__':
        unittest.main()
