#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_DirectPort.py
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
import RTC



  
class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, mes):
        self.mes = mes
    def __del__(self):
        pass
    def __call__(self, info, cdrdata):
        print self.mes

class ConnectorListener(OpenRTM_aist.ConnectorListener):
    def __init__(self, mes):
        self.mes = mes
    def __del__(self):
        pass
    def __call__(self,  info):
        print self.mes



class TestDirectPort(unittest.TestCase):
  
  def setUp(self):
    self.manager = OpenRTM_aist.Manager.init(sys.argv)
    self.manager.activateManager()

    self._d_in = RTC.TimedLong(RTC.Time(0,0),0)
    self._inIn = OpenRTM_aist.InPort("in", self._d_in)
    prop = OpenRTM_aist.Properties()
    self._inIn.init(prop)
    self.inport_obj = self._inIn.getPortRef()

    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,DataListener("InPort:ON_BUFFER_WRITE"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL,DataListener("InPort:ON_BUFFER_FULL"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT,DataListener("InPort:ON_BUFFER_WRITE_TIMEOUT"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE,DataListener("InPort:ON_BUFFER_OVERWRITE"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ,DataListener("InPort:ON_BUFFER_READ"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_SEND,DataListener("InPort:ON_SEND"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,DataListener("InPort:ON_RECEIVED"))
    self._inIn.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY,ConnectorListener("InPort:ON_BUFFER_EMPTY"))
    self._inIn.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_BUFFER_READ_TIMEOUT,ConnectorListener("InPort:ON_BUFFER_READ_TIMEOUT"))
    self._inIn.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY,ConnectorListener("InPort:ON_SENDER_EMPTY"))
    self._inIn.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT,ConnectorListener("InPort:ON_SENDER_TIMEOUT"))
    self._inIn.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR,ConnectorListener("InPort:ON_SENDER_ERROR"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL,DataListener("InPort:ON_RECEIVER_FULL"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT,DataListener("InPort:ON_RECEIVER_TIMEOUT"))
    self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR,DataListener("InPort:ON_RECEIVER_ERROR"))


    self._d_out = RTC.TimedLong(RTC.Time(0,0),0)
    self._outOut = OpenRTM_aist.OutPort("out", self._d_out)
    prop = OpenRTM_aist.Properties()
    self._outOut.init(prop)
    self.outport_obj = self._outOut.getPortRef()

    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,DataListener("OutPort:ON_BUFFER_WRITE"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL,DataListener("OutPort:ON_BUFFER_FULL"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT,DataListener("OutPort:ON_BUFFER_WRITE_TIMEOUT"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE,DataListener("OutPort:ON_BUFFER_OVERWRITE"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ,DataListener("OutPort:ON_BUFFER_READ"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_SEND,DataListener("OutPort:ON_SEND"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,DataListener("OutPort:ON_RECEIVED"))
    self._outOut.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY,ConnectorListener("OutPort:ON_BUFFER_EMPTY"))
    self._outOut.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_BUFFER_READ_TIMEOUT,ConnectorListener("OutPort:ON_BUFFER_READ_TIMEOUT"))
    self._outOut.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY,ConnectorListener("OutPort:ON_SENDER_EMPTY"))
    self._outOut.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT,ConnectorListener("OutPort:ON_SENDER_TIMEOUT"))
    self._outOut.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR,ConnectorListener("OutPort:ON_SENDER_ERROR"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL,DataListener("OutPort:ON_RECEIVER_FULL"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT,DataListener("OutPort:ON_RECEIVER_TIMEOUT"))
    self._outOut.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR,DataListener("OutPort:ON_RECEIVER_ERROR"))    
    

  def tearDown(self):
    self.manager.shutdownManager()

  def test_Push(self):
    print "Push"
    prop = OpenRTM_aist.Properties()
    prop.setProperty("dataport.interface_type","direct")
    prop.setProperty("dataport.dataflow_type","push")
    ret = OpenRTM_aist.connect("con1",prop,self.inport_obj,self.outport_obj)
    
    self._d_out.data = 100
    #for i in range(10):
        #self._outOut.write()
    self._outOut.write()

    ret = self._inIn.isNew()
    self.assertTrue(ret)

    data = self._inIn.read()
    self.assertEqual(data.data, 100)
    self.assertTrue(data is self._d_out)

    self.outport_obj.disconnect_all()



  def test_Pull(self):
    print "Pull"
    prop = OpenRTM_aist.Properties()
    prop.setProperty("dataport.interface_type","direct")
    prop.setProperty("dataport.dataflow_type","pull")
    ret = OpenRTM_aist.connect("con1",prop,self.inport_obj,self.outport_obj)
    
    self._d_out.data = 100
    self._outOut.write()

    #ret = self._inIn.isNew()
    #self.assertTrue(ret)

    data = self._inIn.read()
    self.assertEqual(data.data, 100)
    self.assertTrue(data is self._d_out)

    self.outport_obj.disconnect_all()

############### test #################
if __name__ == '__main__':
        unittest.main()
