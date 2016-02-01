#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortSHMProvider.py
# @brief InPortSHMProvider class
# @date  $Date: 2016/01/08 $
# @author Nobuhiko Miyamoto


import sys
from omniORB import *
from omniORB import any

import OpenRTM_aist
import OpenRTM__POA,OpenRTM
import mmap
from omniORB import cdrUnmarshal
import CORBA

##
# @if jp
# @class InPortSHMProvider
# @brief InPortSHMProvider クラス
#
# 通信手段に 共有メモリ を利用した入力ポートプロバイダーの実装クラス。
#
#
# @else
# @class InPortCorbaCdrProvider
# @brief InPortCorbaCdrProvider class
#
#
#
# @endif
#
class InPortSHMProvider(OpenRTM_aist.InPortCorbaCdrProvider):
    
  """
  """

  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  # Interface Typeにはshared_memoryを指定する
  # 共有メモリの空間名はUUIDで作成し、コネクタプロファイルのdataport.shared_memory.addressに保存する
  #
  # self
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # self
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.InPortCorbaCdrProvider.__init__(self)

    # PortProfile setting
    self.setInterfaceType("shared_memory")
    
    
    
    self._buffer = None

    self._profile = None
    self._listeners = None
    self._shmem = None
    
    self.shm_address = str(OpenRTM_aist.uuid1())
    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.shared_memory.address",self.shm_address))
    

    return

  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ
  #
  # @param self
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @param self
  #
  # @endif
  #
  def __del__(self):
    oid = OpenRTM_aist.Manager.instance().getPOA.servant_to_id(self)
    OpenRTM_aist.Manager.instance().getPOA.deactivate_object(oid)
    
    return

  
  # void init(coil::Properties& prop)
  def init(self, prop):
    
    #print prop
    pass



  ##
  # @if jp
  # @brief バッファにデータを書き込む
  #
  # CORBAでデータサイズだけ受信して、共有メモリからデータを取り出しバッファに書き込む
  #
  # @param data 書込対象データ
  #
  # @else
  # @brief 
  #
  # 
  #
  # @param data 
  #
  # @endif
  #
  # ::OpenRTM::PortStatus put(const ::OpenRTM::CdrData& data)
  #  throw (CORBA::SystemException);
  def put(self, data):
    #print self._connector.profile().properties
    #self._connector.profile().properties.setProperty("dataport.dataflow_type","push")
    try:
      self._rtcout.RTC_PARANOID("InPortCorbaCdrProvider.put()")
            
      if not self._buffer:
        self.onReceiverError(data)
        return OpenRTM.PORT_ERROR

      self._rtcout.RTC_PARANOID("received data size: %d", len(data))

      self.onReceived(data)

      if not self._connector:
        return OpenRTM.PORT_ERROR

      data_size = cdrUnmarshal(CORBA.TC_ushort, data)

      #if self._shmem is None:
      self._shmem = mmap.mmap(0, data_size, self.shm_address, mmap.ACCESS_READ)
      #shm_data = cdrUnmarshal(any.to_any(self._connector._dataType).typecode(), self._shmem.read(16),self._connector._endian)
      shm_data = self._shmem.read(data_size)
      #print dir(self._connector._provider._this())
      #print self._connector._provider._this()
      ret = self._connector.write(shm_data)
      

      return self.convertReturn(ret, shm_data)

    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      return OpenRTM.UNKNOWN_ERROR
    return OpenRTM.UNKNOWN_ERROR
    
      
      
      
    return self.convertReturn(ret, data)

  

def InPortSHMProviderInit():
  factory = OpenRTM_aist.InPortProviderFactory.instance()
  factory.addFactory("shared_memory",
                     OpenRTM_aist.InPortSHMProvider,
                     OpenRTM_aist.Delete)
