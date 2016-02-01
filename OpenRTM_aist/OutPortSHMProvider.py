#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortSHMProvider.py
# @brief OutPortSHMProvider class
# @date  $Date: 2016-01-12 $
# @author Nobuhiko Miyamoto
#
#

import sys
from omniORB import *
from omniORB import any

import OpenRTM_aist
import OpenRTM__POA,OpenRTM
import mmap, os
from omniORB import cdrMarshal
import CORBA

##
# @if jp
# @class OutPortSHMProvider
# @brief OutPortSHMProvider クラス
#
# OutPortProvider 
#
# 通信手段に 共有メモリ を利用した出力ポートプロバイダの実装クラス。
#
#
# @else
# @class OutPortSHMProvider
# @brief OutPortSHMProvider class
#
#
#
# @endif
#
class OutPortSHMProvider(OpenRTM_aist.OutPortCorbaCdrProvider):
  ##
  # @if jp
  # @brief コンストラクタ
  # 共有メモリの空間名はUUIDで作成し、コネクタプロファイルのdataport.shared_memory.addressに保存する
  #
  # コンストラクタ
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.OutPortCorbaCdrProvider.__init__(self)
    self.setInterfaceType("shared_memory")

    self.shm_address = str(OpenRTM_aist.uuid1())
    
    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.shared_memory.address",self.shm_address))

    self._shmem = mmap.mmap(0, 256, self.shm_address, mmap.ACCESS_WRITE)

    

    return


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    oid = self._default_POA().servant_to_id(self)
    self._default_POA().deactivate_object(oid)
    
    self._shmem.close()
    return


  
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    pass


  
  ##
  # @if jp
  # @brief バッファからデータを取得する
  #
  # @return (リターンコード、取得データ)
  #
  # @else
  # @brief Get data from the buffer
  #
  #
  # @return 
  #
  # @endif
  #
  # virtual ::OpenRTM::PortStatus get(::OpenRTM::CdrData_out data);
  def get(self):
    self._rtcout.RTC_PARANOID("OutPortSHMProvider.get()")
    if not self._buffer:
      self.onSenderError()
      return (OpenRTM.UNKNOWN_ERROR, None)

    try:
      if self._buffer.empty():
        self._rtcout.RTC_ERROR("buffer is empty.")
        return (OpenRTM.BUFFER_EMPTY, None)

      cdr = [None]
      ret = self._buffer.read(cdr)

      if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
        if not cdr:
          self._rtcout.RTC_ERROR("buffer is empty.")
          return (OpenRTM.BUFFER_EMPTY, None)
      
    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      return (OpenRTM.UNKNOWN_ERROR, None)

    self._shmem.seek(os.SEEK_SET)
    self._shmem.write(cdr[0])
    
    
    data_size = len(cdr[0])
    mar_data_size = cdrMarshal(CORBA.TC_ushort, data_size)
    
    
    
    return self.convertReturn(ret, mar_data_size)
    
  


def OutPortSHMProviderInit():
  factory = OpenRTM_aist.OutPortProviderFactory.instance()
  factory.addFactory("shared_memory",
                     OpenRTM_aist.OutPortSHMProvider,
                     OpenRTM_aist.Delete)
