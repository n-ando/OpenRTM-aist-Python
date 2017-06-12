#!/usr/bin/env python
# -*- Python -*-

#
#  \file  test_OutPortSHMProvider.py
#  \brief test for OutPortSHMProvider class
#  \date  $Date: 2016/03/26 $
#  \author Nobuhiko Miyamoto
# 

 
from omniORB import any
from omniORB import CORBA

import OpenRTM_aist
import RTC, RTC__POA 
import SDOPackage, SDOPackage__POA
import OpenRTM

import sys
sys.path.insert(1,"../")

import unittest



class DummyBuffer:
  def __init__(self):
    self._cdr = None
    self._empty = True

  def empty(self):
    return self._empty

  def write(self,d):
    self._cdr = d
    self._empty = False
    return 0

  def read(self,cdr):
    cdr[0] = self._cdr
    self._empty = True
    return 0

class TestOutPortSHMProvider(unittest.TestCase):

  def setUp(self):
    OpenRTM_aist.Manager.instance()
    OpenRTM_aist.OutPortSHMProviderInit()
    self._opp = OpenRTM_aist.OutPortSHMProvider()


    #self._shm = OpenRTM_aist.SharedMemory()
    #self._shm_var = self._sh._this()
    return
    


  def test_get(self):
    prop = OpenRTM_aist.Properties()
    self._opp.init(prop)
    
    ret=self._opp.get()
    self.assertEqual(ret,OpenRTM.UNKNOWN_ERROR)

    prop = OpenRTM_aist.Properties()
    cinfo = OpenRTM_aist.ConnectorInfo("",
                                       "",
                                       [],
                                       prop)
    self._opp.setListener(cinfo,OpenRTM_aist.ConnectorListeners())
    buff = DummyBuffer()
    self._opp.setBuffer(buff)
    ret=self._opp.get()
    self.assertEqual(ret,OpenRTM.BUFFER_EMPTY)


    
    #self._opp.setInterface(self._shm_var)
    

    buff.write("abcde")
    ret=self._opp.get()
    self.assertEqual(ret,OpenRTM.PORT_OK)
    data = self._opp.read()
    self.assertEqual(data,"abcde")
    return


############### test #################
if __name__ == '__main__':
        unittest.main()
