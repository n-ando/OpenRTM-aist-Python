#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#
# @file OutPortConnector.py
# @brief OutPort Connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import OpenRTM_aist


##
# @if jp
# @class OutPortConnector
# @brief OutPortConnector 基底クラス
#
# OutPort の Push/Pull 各種 Connector を派生させるための
# 基底クラス。
#
# @since 1.0.0
#
# @else
# @class OutPortConnector
# @brief IｎPortConnector base class
#
# The base class to derive subclasses for OutPort's Push/Pull Connectors
#
# @since 1.0.0
#
# @endif
#
class OutPortConnector(OpenRTM_aist.ConnectorBase):

    ##
    # @if jp
    # @brief コンストラクタ
    # @else
    # @brief Constructor
    # @endif
    #
    # OutPortConnector(ConnectorBase::Profile& profile);
    def __init__(self, profile):
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortConnector")
        self._profile = profile
        self._endian = ""
        return

    ##
    # @if jp
    # @brief デストラクタ
    # @else
    # @brief Destructor
    # @endif
    #
    def __del__(self):
        pass


    ##
    # @if jp
    # @brief Profile 取得
    #
    # Connector Profile を取得する
    #
    # @else
    # @brief Getting Profile
    #
    # This operation returns Connector Profile
    #
    # @endif
    #
    # const Profile& profile();
    def profile(self):
        self._rtcout.RTC_TRACE("profile()")
        return self._profile

    ##
    # @if jp
    # @brief Connector ID 取得
    #
    # Connector ID を取得する
    #
    # @else
    # @brief Getting Connector ID
    #
    # This operation returns Connector ID
    #
    # @endif
    #
    # const char* id();
    def id(self):
        self._rtcout.RTC_TRACE("id() = %s", self.profile().id)
        return self.profile().id


    ##
    # @if jp
    # @brief Connector 名取得
    #
    # Connector 名を取得する
    #
    # @else
    # @brief Getting Connector name
    #
    # This operation returns Connector name
    #
    # @endif
    #
    # const char* name();
    def name(self):
        self._rtcout.RTC_TRACE("name() = %s", self.profile().name)
        return self.profile().name

