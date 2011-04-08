#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SdoServiceAdmin.py
# @brief SDO service administration class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import copy
import threading
import OpenRTM_aist


##
# @if jp
#
# @class SDO service administration class
# @brief SDO service 管理クラス
#
# このクラスは、SDO Service を管理するためのクラスである。SDO
# Service は OMG SDO Specification において定義されている、SDOが特定
# の機能のために提供また要求するサービスの一つである。詳細は仕様にお
# いて定義されていないが、本クラスでは以下のように振る舞うサービスで
# あるものとし、これらを管理するためのクラスが本クラスである。
#
# SDO Service においては、SDO/RTCに所有され、ある種のサービスを提供
# するものを SDO Service Provider、他のSDO/RTCやアプリケーションが提
# 供するサービスオブジェクトの参照を受け取り、それらの機能を利用する
# ものを、SDO Service Consumer と呼ぶ。
#
# SDO Service Provider は他のアプリケーションから呼ばれ、SDO/RTC内部
# の機能にアクセスするために用いられる。他のSDO/RTCまたはアプリケー
# ションは、
#
# - SDO::get_service_profiles ()
# - SDO::get_service_profile (in UniqueIdentifier id)
# - SDO::get_sdo_service (in UniqueIdentifier id) 
#
# のいずれかのオペレーションにより、ServiceProfile または SDO
# Service の参照を取得し、機能を利用するためのオペレーションを呼び出
# す。他のSDO/RTCまたはアプリケーション上での参照の破棄は任意のタイ
# ミングで行われ、サービス提供側では、どこからどれだけ参照されている
# かは知ることはできない。一方で、SDO/RTC側も、任意のタイミングでサー
# ビスの提供を停止することもできるため、サービスの利用側では、常に
# サービスが利用できるとは限らないものとしてサービスオペレーションを
# 呼び出す必要がある。
#
# 一方、SDO Service Consumer は当該SDO/RTC以外のSDO/RTCまたはアプリ
# ケーションがサービスの実体を持ち、当該SDO/RTCにオブジェクト参照を
# 含むプロファイルを与えることで、SDO/RTC側からサービスオペレーショ
# ンが呼ばれ外部のSDO/RTCまたはアプリケーションが提供する機能を利用
# できる。また、オブザーバ的なオブジェクトを与えることで、SDO/RTC側
# からのコールバックを実現するためにも利用することができる。コンシュー
# マは、プロバイダとは異なり、SDO Configurationインターフェースから
# 追加、削除が行われる。関連するオペレーションは以下のとおりである。
#
# - Configuration::add_service_profile (in ServiceProfile sProfile)
# - Configuration::remove_service_profile (in UniqueIdentifier id)
#
# 外部のSDO/RTCまたはアプリケーションは、自身が持つSDO Servcie
# Provider の参照をIDおよびinterface type、プロパティとともに
# ServcieProfile にセットしたうえで、add_service_profile() の引数と
# して与えることで、当該SDO/RTCにサービスを与える。この際、IDはUUID
# など一意なIDでなければならない。また、削除する際にはIDにより対象と
# するServiceProfileを探索するため、サービス提供側では削除時までIDを
# 保持しておかなければならない。
#
# 
#
#
#
# @since 1.1.0
#
# @else
#
# @class SDO service administration class
# @brief SDO service administration class
#
#
# @since 1.1.0
#
# @endif
class SdoServiceAdmin:
  """
  """

  
  ##
  # @if jp
  # @brief コンストラクタ
  # コンストラクタ
  # @param 
  # 
  # @else
  # @brief Constructor
  # Constructor
  # @param 
  # @endif
  # SdoServiceAdmin(::RTC::RTObject_impl& rtobj);
  def __init__(self, rtobj):
    self._rtobj = rtobj
    self._consumerTypes = []
    self._allConsumerAllowed = True

    ##
    # @if jp
    # @brief Lock 付き SDO ServiceProfileList
    # @else
    # @brief SDO ServiceProfileList with mutex lock
    # @endif
    self._providerProfiles = []
    self._provider_mutex = threading.RLock()
    
    ##
    # @if jp
    # @brief Lock 付き SDO ServiceProfileList
    # @else
    # @brief SDO ServiceProfileList with mutex lock
    # @endif
    self._consumers = []
    self._consumer_mutex = threading.RLock()

    ##
    # @if jp
    # @brief logger
    # @else
    # @brief logger
    # @endif
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("SdoServiceAdmin")

    self._rtcout.RTC_TRACE("SdoServiceAdmin::SdoServiceAdmin(%s)",
                           rtobj.getProperties().getProperty("instance_name"))

    # getting consumer types from RTC's properties
    prop = copy.deepcopy(self._rtobj.getProperties())
    constypes = prop.getProperty("sdo_service.consumer_types")
    self._consumerTypes = [s.strip() for s in constypes.split(",")]
    self._rtcout.RTC_DEBUG("sdo_service.consumer_types: %s",
                           str(OpenRTM_aist.flatten(self._consumerTypes)))

    # If types include '[Aa][Ll][Ll]', all types allowed in this RTC
    for ctype in self._consumerTypes:
      tmp = ctype.lower()
      if tmp == "all":
        self._allConsumerAllowed = True
        self._rtcout.RTC_DEBUG("sdo_service.consumer_types: ALL")

    return


  ##
  # @if jp
  # @brief 仮想デストラクタ
  # 仮想デストラクタ。
  # 
  # @else
  # @brief Virtual destractor
  # Virtual destractor.
  # @endif
  def __del__(self):
    return

    
  ##
  # @if jp
  # @brief Service Consumer Factory を登録する
  # 
  # @else
  # @brief Add Service Consumer Factory
  # @endif
  # bool addSdoServiceConsumerFactory();
  def addSdoServiceConsumerFactory(self):
    return False


  ##
  # @if jp
  # @brief Service Consumer Factory を削除する
  # 
  # @else
  # @brief Remove Service Consumer Factory
  # @endif
  # bool removeSdoServiceConsumerFactory();
  def removeSdoServiceConsumerFactory(self):
    return False
    

  ##
  # @if jp
  # @brief Service Consumer を追加する
  # 
  # @else
  # @brief Add Service Consumer
  # @endif
  # bool addSdoServiceConsumer(const SDOPackage::ServiceProfile& sProfile);
  def addSdoServiceConsumer(self, sProfile):
    self._rtcout.RTC_TRACE("addSdoServiceConsumer(IFR = %s)",
                           sProfile.interface_type)
    profile = copy.deepcopy(sProfile)

    # Not supported consumer type -> error return
    if not self.isAllowedConsumerType(sProfile):
      self._rtcout.RTC_ERROR("Not supported consumer type. %s", profile.id)
      return False

    if not self.isExistingConsumerType(sProfile):
      self._rtcout.RTC_ERROR("type %s already exists.", profile.id)
      return False
    
    if str(profile.id) ==  "":
      self._rtcout.RTC_WARN("No id specified. It should be given by clients.")
      return False

    # re-initialization
    guard = OpenRTM_aist.ScopedLock(self._consumer_mutex)
    id = str(sProfile.id)
    for i in range(len(self._consumers)):
      if id == str(self._consumers[i].getProfile().id):
        self._rtcout.RTC_INFO("Existing consumer is reinitilized.")
        self._rtcout.RTC_DEBUG("Propeteis are: %s",
                               NVUtil.toString(sProfile.properties))
        return self._consumers[i].reinit(sProfile)
    del guard

    # new pofile
    factory = OpenRTM_aist.SdoServiceConsumerFactory.instance()
    ctype = str(profile.interface_type)
    consumer = factory.createObject(ctype)
    if consumer == None:
      self._rtcout.RTC_ERROR("Hmm... consumer must be created.")
      return False

    # initialize
    if not consumer.init(self._rtobj, sProfile):
      self._rtcout.RTC_WARN("SDO service initialization was failed.")
      self._rtcout.RTC_DEBUG("id:         %s", str(sProfile.id))
      self._rtcout.RTC_DEBUG("IFR:        %s", str(sProfile.interface_type))
      self._rtcout.RTC_DEBUG("properties: %s", OpenRTM_aist.NVUtil.toString(sProfile.properties))
      factory.deleteObject(consumer)
      self._rtcout.RTC_INFO("SDO consumer was deleted by initialization failure")
      return False

    # store consumer
    guard = OpenRTM_aist.ScopedLock(self._consumer_mutex)
    self._consumers.append(consumer)
    del guard

    return True

  
  ##
  # @if jp
  # @brief Service Consumer を削除する
  # 
  # @else
  # @brief Remove Service Consumer
  # @endif
  # bool removeSdoServiceConsumer(const char* id);
  def removeSdoServiceConsumer(self, id):
    if id == None or id[0] == '\0':
      self._rtcout.RTC_ERROR("removeSdoServiceConsumer(): id is invalid.")
      return False

    self._rtcout.RTC_TRACE("removeSdoServiceConsumer(id = %s)", id)

    guard = OpenRTM_aist.ScopedLock(self._consumer_mutex)
    strid = id

    for (idx,cons) in enumerate(self._consumers):
      if strid == str(cons.getProfile().id):
        cons.finalize()
        del self._consumers[idx]
        factory = OpenRTM_aist.SdoServiceConsumerFactory.instance()
        factory.deleteObject(cons)
        self._rtcout.RTC_INFO("SDO service has been deleted: %s", id)
        return True

    self._rtcout.RTC_WARN(("Specified SDO consumer not found: %s", id))
    return False
    

  ##
  # @if jp
  # @brief 許可されたサービス型かどうか調べる
  # 
  # @else
  # @brief If it is allowed service type
  # @endif
  # bool isAllowedConsumerType(const SDOPackage::ServiceProfile& sProfile);
  def isAllowedConsumerType(self, sProfile):
    if self._allConsumerAllowed:
      return True

    for i in range(len(self._consumerTypes)):
      if self._consumerTypes[i] == str(sProfile.interface_type):
        self._rtcout.RTC_DEBUG("%s is supported SDO service.", str(sProfile.interface_type))
        return True
    self._rtcout.RTC_WARN("Consumer type is not supported: %s", str(sProfile.interface_type))
    return False


  ##
  # @if jp
  # @brief 存在するサービス型かどうか調べる
  # 
  # @else
  # @brief If it is existing service type
  # @endif
  # bool isExistingConsumerType(const SDOPackage::ServiceProfile& sProfile);
  def isExistingConsumerType(self, sProfile):
    factory = OpenRTM_aist.SdoServiceConsumerFactory.instance()
    consumerTypes = factory.getIdentifiers()
    for i in range(len(consumerTypes)):
      if consumerTypes[i] == str(sProfile.interface_type):
        self._rtcout.RTC_DEBUG("%s exists in the SDO service factory.", str(sProfile.interface_type))
        self._rtcout.RTC_PARANOID("Available SDO serices in the factory: %s", str(OpenRTM_aist.flatten(consumerTypes)))
        return True
    self._rtcout.RTC_WARN("No available SDO service in the factory: %s",
                          str(sProfile.interface_type))
    return False


  # const std::string getUUID() const;
  def getUUID(self):
    return str(OpenRTM_aist.uuid1())
