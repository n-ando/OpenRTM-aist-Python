#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_DirectServicePort.py
# \brief 
# \date $Date: $
# \author Nobuhiko Miyamoto
#


import sys
sys.path.insert(1,"../")

try:
    import unittest2 as unittest
except (ImportError):
    import unittest

import time

#from Manager import *
import OpenRTM_aist
import RTC, RTC__POA
import OpenRTM, OpenRTM__POA



class Test_i(OpenRTM__POA.InPortCdr):
  def __init__(self):
    pass
  def put(self, data):
    return OpenRTM.PORT_OK


  




class TestDirectServicePort(unittest.TestCase):
  
  def setUp(self):
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    #self.manager.setModuleInitProc(MyModuleInit)
    self.manager.activateManager()
    self._servicePort_provided = OpenRTM_aist.CorbaPort("service")
    self._testService_provided = Test_i()

    self._servicePort_required = OpenRTM_aist.CorbaPort("service")
    self._testService_required = OpenRTM_aist.CorbaConsumer(interfaceType=OpenRTM.InPortCdr)


    self._servicePort_provided.registerProvider("service", "TestService", self._testService_provided)
    

    self._servicePort_required.registerConsumer("service", "TestService", self._testService_required)
    
    
    self._servicePort_provided.activateInterfaces()

  def tearDown(self):
    self.manager.shutdownManager()
    time.sleep(0.1)

    
                                      
  def test_Service(self):
    prop = OpenRTM_aist.Properties()
    ret = OpenRTM_aist.connect("con1",prop,self._servicePort_provided.getPortRef(),self._servicePort_required.getPortRef())
    obj = self._testService_required._ptr()
    
    self.assertEqual(obj, self._testService_provided)
  


  


############### test #################
if __name__ == '__main__':
        unittest.main()
