#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SharedMemory.py
# @brief SharedMemory class
# @date $Date$
# @author Nobuhiko Miyamoto
#

import sys
import mmap, os
import platform, ctypes
from omniORB import cdrMarshal
from omniORB import cdrUnmarshal
import CORBA
import OpenRTM_aist
import OpenRTM__POA




##
# @if jp
#
# @class SharedMemory
#
# @brief SharedMemory クラス
#
# 共有メモリ操作クラス
# CORBAによる通信により、mmapの初期化、終了などがリモートに操作できる
#
#
# @else
# @class SharedMemory
#
# @brief SharedMemory class
#
#
#
# @endif
#
class SharedMemory(OpenRTM__POA.SharedMemory):
  default_size = 8
  default_memory_size = 2*1024*1024


  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @param self
  #
  # @endif
  #
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("SharedMemory")
    self._shmem = None
    self._smInterface = None
    self._shm_address = ""
    self._memory_size = SharedMemory.default_memory_size
    if platform.system() == "Windows":
      pass
    else:
      try:
        self.rt = ctypes.CDLL('librt.so')
      except:
        self.rt = ctypes.CDLL('librt.so.1')
      self.rt.shm_open.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
      self.rt.shm_open.restype = ctypes.c_int
      self.rt.ftruncate.argtypes = [ctypes.c_int, ctypes.c_int]
      self.rt.ftruncate.restype = ctypes.c_int
      self.rt.close.argtypes = [ctypes.c_int]
      self.rt.close.restype = ctypes.c_int
      self.rt.shm_unlink.argtypes = [ctypes.c_char_p]
      self.rt.shm_unlink.restype = ctypes.c_int

      self.fd = -1
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
  # @endif
  #
  def __del__(self):
    self._rtcout.RTC_PARANOID("~SharedMemory()")
    return

  
  ##
  # @if jp
  # @brief 文字列で指定したデータサイズを数値に変換する
  # 1M → 1048576
  # 1k → 1024
  # 100 → 100
  #
  #
  # @param self
  # @param size_str データサイズ(文字列)
  # @return データサイズ(数値)
  #
  # @else
  # @brief 
  #
  # @param self
  # @param size_str 
  # @return 
  #
  # @endif
  #
  # int string_to_MemorySize(string size_str);
  def string_to_MemorySize(self, size_str):
    memory_size = SharedMemory.default_memory_size
    if size_str:
      if size_str[-1] == "M":
        memory_size = 1024 * 1024 * int(size_str[0:-1])
      elif size_str[-1] == "k":
        memory_size = 1024 * int(size_str[0:-1])
      else:
        memory_size = int(size_str[0:-1])
    return memory_size



  ##
  # @if jp
  # @brief 共有メモリの初期化
  # windowsではページングファイル上に領域を確保する
  # Linuxでは/dev/shm以下にファイルを作成する
  # 作成したファイルの内容を仮想アドレスにマッピングする
  # 
  #
  #
  # @param self
  # @param memory_size 共有メモリのサイズ
  # @parama shm_address 空間名
  #
  # @else
  # @brief 
  #
  # @param memory_size 
  # @parama shm_address
  #
  # @endif
  #
  # void create_memory(int memory_size, string shm_address);
  def create_memory(self, memory_size, shm_address):
    
    if self._shmem is None:
      self._rtcout.RTC_TRACE("create():memory_size="+str(memory_size)+",shm_address="+str(shm_address))
      self._memory_size = memory_size
      self._shm_address = shm_address

      if platform.system() == "Windows":
        self._shmem = mmap.mmap(0, self._memory_size, self._shm_address, mmap.ACCESS_WRITE)
      else:
        O_RDWR = 2
        O_CREAT = 64

        S_IRUSR = 256
        S_IWUSR = 128
        S_IRGRP = 32
        S_IWGRP = 16
        S_IROTH = 4

        self.fd = self.rt.shm_open(self._shm_address,O_RDWR | O_CREAT,S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH)
        if self.fd < 0:
          return self.UNKNOWN_ERROR
        self.rt.ftruncate(self.fd, self._memory_size)
        self._shmem = mmap.mmap(self.fd, self._memory_size, mmap.MAP_SHARED)
        self.rt.close( self.fd )

      
      if self._smInterface:
        self._smInterface.open_memory(self._memory_size, self._shm_address)



  ##
  # @if jp
  # @brief 共有メモリのマッピングを行う
  # 
  #
  #
  # @param self
  # @param memory_size 共有メモリのサイズ
  # @parama shm_address 空間名
  #
  # @else
  # @brief 
  #
  # @param memory_size 
  # @parama shm_address
  #
  # @endif
  #
  # void open_memory(int memory_size, string shm_address);
  def open_memory(self, memory_size, shm_address):
    self._rtcout.RTC_TRACE("open():memory_size="+str(memory_size)+",shm_address="+str(shm_address))
    self._memory_size = memory_size
    self._shm_address = shm_address
    if self._shmem is None:
      if platform.system() == "Windows":
        self._shmem = mmap.mmap(0, self._memory_size, self._shm_address, mmap.ACCESS_READ)
      else:
        O_RDWR = 2
        self.fd = self.rt.shm_open(self._shm_address,O_RDWR,0)
        if self.fd < 0:
          return self.UNKNOWN_ERROR
        self.rt.ftruncate(self.fd, self._memory_size)
        self._shmem = mmap.mmap(self.fd, self._memory_size, mmap.MAP_SHARED)
        self.rt.close( self.fd )
    


  ##
  # @if jp
  # @brief マッピングした共有メモリをアンマップする
  # 
  #
  #
  # @param self
  # @param unlink Linuxで/dev/shm以下に作成したファイルを削除する場合にTrueにする
  #
  # @else
  # @brief 
  #
  # @param self
  # @param unlink
  #
  # @endif
  #
  # void close_memory(int memory_size, string shm_address);
  def close_memory(self, unlink):
    self.close(unlink)

  ##
  # @if jp
  # @brief マッピングした共有メモリをアンマップする
  # 
  #
  #
  # @param self
  # @param unlink Linuxで/dev/shm以下に作成したファイルを削除する場合にTrueにする
  #
  # @else
  # @brief
  #
  # @param self
  # @param unlink
  #
  #
  # @endif
  #
  # void close(int memory_size, string shm_address);
  def close(self, unlink=False):
    self._rtcout.RTC_TRACE("open()")
    if self._shmem:
      self._shmem.close()
      if platform.system() == "Windows":
        pass
      else:
        if unlink:
           self.rt.shm_unlink(self._shm_address)
      self._shmem = None

      if self._smInterface:
        self._smInterface.close_memory(False)


  
  ##
  # @if jp
  # @brief データを書き込む
  # 先頭8byteにデータサイズを書き込み、その後ろにデータを書き込む
  # 設定したデータサイズが共有メモリのサイズを上回った場合、共有メモリの初期化を行う
  # 
  #
  #
  # @param self
  # @param data 書き込むデータ
  #
  # @else
  # @brief
  #
  # @param self
  # @param data 
  #
  #
  # @endif
  #
  # void write(cdrMemoryStream& data);
  def write(self, data):
    self._rtcout.RTC_TRACE("write()")
    
    if self._shmem:
      data_size = len(data)

      
      if data_size + SharedMemory.default_size > self._memory_size:
        self._memory_size = data_size + SharedMemory.default_size

        if self._smInterface:
          self._smInterface.close_memory(False)


        self.close_memory(True)
        self.create_memory(self._memory_size, self._shm_address)

        
        
      data_size_cdr = cdrMarshal(CORBA.TC_ulong, data_size)
      
      self._shmem.seek(os.SEEK_SET)
      self._shmem.write(data_size_cdr)
      self._shmem.write(data)


  ##
  # @if jp
  # @brief データを読み込む
  # 
  #
  #
  # @param self
  # @return データ
  #
  # @else
  # @brief 
  #
  # @param self
  # @return
  #
  # @endif
  #
  # void read(::OpenRTM::CdrData_out data);
  def read(self):
    self._rtcout.RTC_TRACE("read()")
    if self._shmem:
      
      self._shmem.seek(os.SEEK_SET)
      
      data_size_cdr = self._shmem.read(SharedMemory.default_size)
      data_size = cdrUnmarshal(CORBA.TC_ulong, data_size_cdr)
      
      
      
      shm_data = self._shmem.read(data_size)
      
      return shm_data
    return ""



  ##
  # @if jp
  # @brief 通信先のCORBAインターフェースを登録する
  # 登録する事により共有メモリの初期化したときに、通信先でもマッピングをやり直すことができる
  # 
  #
  #
  # @param self
  # @param sm SharedMemoryのオブジェクトリファレンス
  #
  # @else
  # @brief 
  #
  #
  # @endif
  #
  # void close(int memory_size, string shm_address);
  def setInterface(self, sm):
    self._smInterface = sm
    

  ##
  # @if jp
  # @brief データの送信を知らせる
  # 
  #
  #
  # @param self
  #
  # @else
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  # PortStatus put();
  def put(self):
    return OpenRTM.UNKNOWN_ERROR

  ##
  # @if jp
  # @brief データの送信を要求する
  # 
  #
  #
  # @param self
  #
  # @else
  # @brief 
  #
  # @param self
  #
  # @endif
  #
  # PortStatus get();
  def get(self):
    return OpenRTM.UNKNOWN_ERROR