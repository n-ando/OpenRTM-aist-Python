#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file NamingServiceNumberingPolicy.py
# @brief Object numbering policy class
# @date $Date: 2016/02/25$
# @author Nobuhiko Miyamoto
#

import string
import OpenRTM_aist
import CosNaming






##
# @if jp
#
# @class NamingServiceNumberingPolicy
# @brief オブジェクト生成時ネーミング・ポリシー(命名規則)管理用クラス
#　ネーミングサービスからRTCを検索してナンバリングを行う
#
#
# @else
#
# @endif
class NamingServiceNumberingPolicy(OpenRTM_aist.NumberingPolicy):
  """
  """

  ##
  # @if jp
  #
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # 
  # @param self
  # 
  # @else
  #
  # @brief virtual destractor
  #
  # @endif
  def __init__(self):
    self._num = 0
    self._objects = []
    self._mgr = OpenRTM_aist.Manager.instance()


  ##
  # @if jp
  #
  # @brief オブジェクト生成時の名称作成
  #
  # 
  # 
  # @param self
  # @param obj 名称生成対象オブジェクト
  #
  # @return 生成したオブジェクト名称
  #
  # @else
  #
  # @endif
  def onCreate(self, obj):
    num = 0
    while True:
      num_str = OpenRTM_aist.otos(num)
      
      name = obj.getTypeName() + num_str
      if not self.find(name):
        return num_str
      else:
        num += 1

  ##
  # @if jp
  #
  # @brief オブジェクト削除時の名称解放
  #
  # 
  # 
  # @param self
  # @param obj 名称解放対象オブジェクト
  #
  # @else
  #
  # @endif
  def onDelete(self, obj):
    pass

  ##
  # @if jp
  #
  # @brief RTCの検索
  #
  # ネーミングサービスからRTCをインスタンス名から検索し、
  # 一致するRTCがある場合はTrueを返す
  # 
  # @param self
  # @param context 現在検索中のコンテキスト
  # @param name RTCのインスタンス名
  #
  # @return 判定
  #
  # @else
  #
  # @endif
  def find_RTC_by_Name(self, context, name):
    length = 500
    bl,bi = context.list(length)
    for i in bl:
      if i.binding_type == CosNaming.ncontext:
        next_context = context.resolve(i.binding_name)
        if self.find_RTC_by_Name(next_context, name):
          return True
      elif i.binding_type == CosNaming.nobject:
        if i.binding_name[0].id == name and i.binding_name[0].kind == "rtc":
          return True
    return False
        
    

  ##
  # @if jp
  #
  # @brief オブジェクトの検索
  #
  # 指定名のインスタンス名のRTCを検索し、
  # 一致するRTCが存在する場合はTrueを返す
  # 
  # @param self
  # @param name RTCのインスタンス名
  #
  # @return 判定
  #
  # @else
  #
  # @endif
  def find(self, name):
    ns = self._mgr._namingManager._names
    for n in ns:
      noc = n.ns
      if noc is None:
        continue
      cns = noc._cosnaming
      if cns is None:
        continue
      root_cxt = cns.getRootContext()
      return self.find_RTC_by_Name(root_cxt, name)



def NamingServiceNumberingPolicyInit():
  OpenRTM_aist.NumberingPolicyFactory.instance().addFactory("ns_unique",
                                                      OpenRTM_aist.NamingServiceNumberingPolicy,
                                                      OpenRTM_aist.Delete)
