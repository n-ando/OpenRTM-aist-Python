#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  OutPortSHMProvider.py
# @brief OutPortSHMProvider class
# @date  $Date: 2016-01-12 $
# @author Nobuhiko Miyamoto
#
#



import OpenRTM_aist
import OpenRTM
import OpenRTM__POA
from omniORB import CORBA

import threading

##
# @if jp
# @class OutPortSHMConsumer
#
# @brief OutPortSHMConsumer クラス
#
# 通信手段に 共有メモリ を利用した出力ポートプロバイダーの実装クラス。
#
#
# @else
# @class OutPortSHMConsumer
#
# @brief OutPortSHMConsumer class
#
#
# @endif
#
class OutPortSHMConsumer(OpenRTM_aist.OutPortCorbaCdrConsumer):
  """
  """

  ##
  # @if jp
  # @brief コンストラクタ
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
    OpenRTM_aist.OutPortCorbaCdrConsumer.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortSHMConsumer")

    self._shmem = OpenRTM_aist.SharedMemory()
      
    self._mutex = threading.RLock()
    self._outportcdr = OpenRTM.PortSharedMemory._nil

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
  def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
    self._rtcout.RTC_PARANOID("~OutPortSHMConsumer()")
    CorbaConsumer.__del__(self)
    try:
      if not CORBA.is_nil(self._outportcdr):
        self._outportcdr.close_memory(True)
    except:
      self._rtcout.RTC_WARN("Exception caught from PortSharedMemory.close_memory().")
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      
    oid = OpenRTM_aist.Manager.instance().getPOA().servant_to_id(self._shmem)
    OpenRTM_aist.Manager.instance().getPOA().deactivate_object(oid)

    


  ##
  # @if jp
  # @brief 設定初期化
  #
  # OutPortConsumerの各種設定を行う
  #
  # @param self
  # @param prop コネクタプロパティ
  #
  # @else
  # @brief Initializing configuration
  #
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    
    self._properties = prop
        
    return

  def setObject(self, obj):
    if OpenRTM_aist.CorbaConsumer.setObject(self, obj):
      ref_ = self.getObject()
      if ref_:
        outportcdr = self.getObject()._narrow(OpenRTM__POA.PortSharedMemory)
        if outportcdr is None:
          return False
        outportcdr.setInterface(self._shmem._this())
        return True
    return False
  


  ##
  # @if jp
  # @brief データを読み出す
  #
  # 設定されたデータを読み出す。
  #
  # データのサイズは共有メモリも先頭8byteから取得する
  # データは共有メモリから読み込む
  #
  # @param data 読み出したデータを受け取るオブジェクト
  #
  # @return リターンコード
  #
  # @else
  # @brief Read data
  #
  # Read set data
  #
  # @param data Object to receive the read data
  #
  # @return Return Code
  #
  # @endif
  #
  # virtual ReturnCode get(cdrMemoryStream& data);
  def get(self, data):
    self._rtcout.RTC_PARANOID("get()")
    
    try:
      outportcdr = self.getObject()._narrow(OpenRTM__POA.PortSharedMemory)
      
      self._outportcdr = outportcdr

      guard = OpenRTM_aist.ScopedLock(self._mutex)
      ret = outportcdr.get()
      
      if ret == OpenRTM.PORT_OK:
        self._rtcout.RTC_DEBUG("get() successful")

        
        
        shm_data = self._shmem.read()
        

        data[0] = shm_data
        self.onReceived(data[0])
        self.onBufferWrite(data[0])
        
        if self._buffer.full():
          self._rtcout.RTC_INFO("InPort buffer is full.")
          self.onBufferFull(data[0])
          self.onReceiverFull(data[0])
        
        self._buffer.put(data[0])
        self._buffer.advanceWptr()
        self._buffer.advanceRptr()

        return self.PORT_OK
      return self.convertReturn(ret,data[0])

    except:
      self._rtcout.RTC_WARN("Exception caught from OutPort.get().")
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST




  


def OutPortSHMConsumerInit():
  factory = OpenRTM_aist.OutPortConsumerFactory.instance()
  factory.addFactory("shared_memory",
                     OpenRTM_aist.OutPortSHMConsumer,
                     OpenRTM_aist.Delete)
  return
