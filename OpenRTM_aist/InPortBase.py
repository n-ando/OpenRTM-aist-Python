#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPortBase.py
# @brief RTC::Port implementation for InPort
# @date $Date: 2008-01-13 15:06:40 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import copy
import OpenRTM_aist
import RTC, RTC__POA

##
# @if jp
# @namespace RTC
#
# @brief RT����ݡ��ͥ��
#
# @else
#
# @namespace RTC
#
# @brief RT-Component
#
# @endif
#

##
# @if jp
# @class InPortBase
# @brief InPort �� Port
#
# �ǡ������ϥݡ��Ȥμ������饹��
#
# @since 0.4.0
#
# @else
# @class InPortBase
# @brief Port for InPort
#
# This is an implementation class for the data input port.
#
# @since 0.4.0
#
# @endif
#
class InPortBase(OpenRTM_aist.PortBase, OpenRTM_aist.DataPortStatus):

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param name �ݡ���̾��
    # @param inport �����ǡ������ϥݡ��Ȥ˴�Ϣ�դ���InPort���֥�������
    #               InPort���֥������Ȥǰ����ǡ��������Хåե������פ���ꤹ��
    # @param prop �ݡ��������ѥץ��ѥƥ�
    #
    # @else
    # @brief Constructor
    #
    # Constructor
    #
    # @param name Port name
    # @param inport InPort object that is associated with this data input port.
    #               Specify also the data type and the buffer type used in 
    #               the InPort object.
    # @param prop Property for setting ports
    #
    # @endif
    #
    # InPortBase(const char* name, const char* data_type);
    def __init__(self, name, data_type):
        OpenRTM_aist.PortBase.__init__(self,name)
        self._singlebuffer  = True
        self._thebuffer     = None
        self._properties    = OpenRTM_aist.Properties()
        self._providerTypes = ""
        self._consumerTypes = ""
        self._connectors    = []

        # PortProfile::properties ������
        self.addProperty("port.port_type", "DataInPort")
        self.addProperty("dataport.data_type", data_type)
        self.addProperty("dataport.subscription_type", "Any")
        self._value = None
        self._listeners = OpenRTM_aist.ConnectorListeners()
    
    
    ##
    # @if jp
    # @brief �ǥ��ȥ饯��
    #
    # �ǥ��ȥ饯��
    #
    # @else
    # @brief Destructor
    #
    # Destructor
    #
    # @endif
    #
    def __del__(self):
        self._rtcout.RTC_TRACE("InPortBase destructor")

        if len(self._connectors) != 0:
            self._rtcout.RTC_ERROR("connector.size should be 0 in InPortBase's dtor.")
            for connector in self._connectors:
                connector.disconnect()

        if self._thebuffer is not None:
            OpenRTM_aist.CdrBufferFactory.instance().deleteObject(self._thebuffer)
            if not self._singlebuffer:
                self._rtcout.RTC_ERROR("Although singlebuffer flag is true, the buffer != 0")


    def properties(self):
        self._rtcout.RTC_TRACE("properties()")
        return self._properties


    def init(self):
        self._rtcout.RTC_TRACE("init()")
        if self._singlebuffer:
            self._rtcout.RTC_DEBUG("single buffer mode.")
            self._thebuffer = OpenRTM_aist.CdrBufferFactory.instance().createObject("ring_buffer")

            if self._thebuffer is None:
                self._rtcout.RTC_ERROR("default buffer creation failed")
        else:
            self._rtcout.RTC_DEBUG("multi buffer mode.")

        self.initProviders()
        self.initConsumers()


    def connect(self, connector_profile):
        self._rtcout.RTC_TRACE("InPortBase.connect()")
        
        if OpenRTM_aist.NVUtil.find_index(connector_profile.properties,
                                          "dataport.serializer.cdr.endian") is -1:
            connector_profile.properties.append(OpenRTM_aist.NVUtil.newNV("dataport.serializer.cdr.endian","little,big"))

        return OpenRTM_aist.PortBase.connect(self, connector_profile)
        
    ##
    # @if jp
    #
    # @brief InPort�� activates ����
    #
    # InPort�� activate ���롣
    #
    # @else
    #
    # @brief Activate all Port interfaces
    #
    # This operation activate all interfaces that is registered in the
    # ports.
    #
    # @endif
    #
    # void activateInterfaces();
    def activateInterfaces(self):
        self._rtcout.RTC_TRACE("activateInterfaces()")

        for connector in self._connectors:
            connector.activate()
            self._rtcout.RTC_DEBUG("activate connector: %s %s",
                                   (connector.name(),connector.id()))

        return


    ##
    # @if jp
    #
    # @brief ���Ƥ� Port �Υ��󥿡��ե������� deactivates ����
    #
    # Port ����Ͽ����Ƥ������ƤΥ��󥿡��ե������� deactivate ���롣
    #
    # @else
    #
    # @brief Deactivate all Port interfaces
    #
    # This operation deactivate all interfaces that is registered in the
    # ports.
    #
    # @endif
    #
    # void deactivateInterfaces();
    def deactivateInterfaces(self):
        self._rtcout.RTC_TRACE("deactivateInterfaces()")

        for connector in self._connectors:
            connector.deactivate()
            self._rtcout.RTC_DEBUG("deactivate connector: %s %s",
                                   (connector.name(),connector.id()))
        

    ##
    # @if jp
    # @brief ConnectorDataListener �ꥹ�ʤ��ɲä���
    #
    # �Хåե��񤭹��ߤޤ����ɤ߽Ф����٥�Ȥ˴�Ϣ����Ƽ�ꥹ�ʤ����ꤹ�롣
    #
    # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
    #
    # - ON_BUFFER_WRITE:          �Хåե��񤭹��߻�
    # - ON_BUFFER_FULL:           �Хåե��ե��
    # - ON_BUFFER_WRITE_TIMEOUT:  �Хåե��񤭹��ߥ����ॢ���Ȼ�
    # - ON_BUFFER_OVERWRITE:      �Хåե���񤭻�
    # - ON_BUFFER_READ:           �Хåե��ɤ߽Ф���
    # - ON_SEND:                  InProt�ؤ�������
    # - ON_RECEIVED:              InProt�ؤ�������λ��
    # - ON_SEND_ERTIMEOUT:        OutPort¦�����ॢ���Ȼ�
    # - ON_SEND_ERERROR:          OutPort¦���顼��
    # - ON_RECEIVER_FULL:         InProt¦�Хåե��ե��
    # - ON_RECEIVER_TIMEOUT:      InProt¦�Хåե������ॢ���Ȼ�
    # - ON_RECEIVER_ERROR:        InProt¦���顼��
    #
    # �ꥹ�ʤ� ConnectorDataListener ��Ѿ������ʲ��Υ����˥�������
    # operator() ��������Ƥ���ɬ�פ����롣
    #
    # ConnectorDataListener::
    #         operator()(const ConnectorProfile&, const cdrStream&)
    #
    # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
    # OutPort�˰ܤꡢOutPort���λ��⤷���ϡ�
    # removeConnectorDataListener() �ˤ�������˼�ưŪ�˲��Τ���롣
    # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
    # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
    #
    # @param listener_type �ꥹ�ʥ�����
    # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
    # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
    #
    # @else
    # @brief Adding BufferDataListener type listener
    #
    # This operation adds certain listeners related to buffer writing and
    # reading events.
    # The following listener types are available.
    #
    # - ON_BUFFER_WRITE:          At the time of buffer write
    # - ON_BUFFER_FULL:           At the time of buffer full
    # - ON_BUFFER_WRITE_TIMEOUT:  At the time of buffer write timeout
    # - ON_BUFFER_OVERWRITE:      At the time of buffer overwrite
    # - ON_BUFFER_READ:           At the time of buffer read
    # - ON_SEND:                  At the time of sending to InPort
    # - ON_RECEIVED:              At the time of finishing sending to InPort
    # - ON_SENDER_TIMEOUT:        At the time of timeout of OutPort
    # - ON_SENDER_ERROR:          At the time of error of OutPort
    # - ON_RECEIVER_FULL:         At the time of bufferfull of InPort
    # - ON_RECEIVER_TIMEOUT:      At the time of timeout of InPort
    # - ON_RECEIVER_ERROR:        At the time of error of InPort
    #
    # Listeners should have the following function operator().
    #
    # ConnectorDataListener::
    #         operator()(const ConnectorProfile&, const cdrStream&)
    #
    # The ownership of the given listener object is transferred to
    # this OutPort object in default.  The given listener object will
    # be destroied automatically in the OutPort's dtor or if the
    # listener is deleted by removeConnectorDataListener() function.
    # If you want to keep ownership of the listener object, give
    # "false" value to 3rd argument to inhibit automatic destruction.
    #
    # @param listener_type A listener type
    # @param listener A pointer to a listener object
    # @param autoclean A flag for automatic listener destruction
    #
    # @endif
    #
    # void 
    # addConnectorDataListener(ConnectorDataListenerType type,
    #                          ConnectorDataListener* listener,
    #                          bool autoclean)
    def addConnectorDataListener(self, listener_type, listener, autoclean = True):
        self._rtcout.RTC_TRACE("addConnectorDataListener()")

        if listener_type < OpenRTM_aist.ConnectorDataListenerType.CONNECTOR_DATA_LISTENER_NUM:
            self._listeners.connectorData_[listener_type].addListener(listener, autoclean)

    ##
    # @if jp
    # @brief ConnectorDataListener �ꥹ�ʤ�������
    #
    # ���ꤷ���Ƽ�ꥹ�ʤ������롣
    # 
    # @param listener_type �ꥹ�ʥ�����
    # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
    #
    # @else
    # @brief Removing BufferDataListener type listener
    #
    # This operation removes a specified listener.
    #     
    # @param listener_type A listener type
    # @param listener A pointer to a listener object
    #
    # @endif
    #
    # void removeConnectorDataListener(ConnectorDataListenerType type,
    #                                  ConnectorDataListener* listener)
    def removeConnectorDataListener(self, listener_type, listener):
        self._rtcout.RTC_TRACE("removeConnectorDataListener()")

        if listener_type < OpenRTM_aist.ConnectorDataListenerType.CONNECTOR_DATA_LISTENER_NUM:
            self._listeners.connectorData_[listener_type].removeListener(listener)

  
    ##
    # @if jp
    # @brief ConnectorListener �ꥹ�ʤ��ɲä���
    #
    # �Хåե��񤭹��ߤޤ����ɤ߽Ф����٥�Ȥ˴�Ϣ����Ƽ�ꥹ�ʤ����ꤹ�롣
    #
    # ����Ǥ���ꥹ�ʤΥ����פ�
    #
    # - ON_BUFFER_EMPTY:       �Хåե������ξ��
    # - ON_BUFFER_READTIMEOUT: �Хåե������ǥ����ॢ���Ȥ������
    #
    # �ꥹ�ʤϰʲ��Υ����˥������� operator() ��������Ƥ���ɬ�פ����롣
    #
    # ConnectorListener::operator()(const ConnectorProfile&)
    #
    # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
    # OutPort�˰ܤꡢOutPort���λ��⤷���ϡ�
    # removeConnectorListener() �ˤ�������˼�ưŪ�˲��Τ���롣
    # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
    # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
    #
    # @param listener_type �ꥹ�ʥ�����
    # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
    # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
    #
    # @else
    # @brief Adding ConnectorListener type listener
    #
    # This operation adds certain listeners related to buffer writing and
    # reading events.
    # The following listener types are available.
    #
    # - ON_BUFFER_EMPTY:       At the time of buffer empty
    # - ON_BUFFER_READTIMEOUT: At the time of buffer read timeout
    #
    # Listeners should have the following function operator().
    #
    # ConnectorListener::operator()(const ConnectorProfile&)
    #  
    # The ownership of the given listener object is transferred to
    # this OutPort object in default.  The given listener object will
    # be destroied automatically in the OutPort's dtor or if the
    # listener is deleted by removeConnectorListener() function.
    # If you want to keep ownership of the listener object, give
    # "false" value to 3rd argument to inhibit automatic destruction.
    #
    # @param listener_type A listener type
    # @param listener A pointer to a listener object
    # @param autoclean A flag for automatic listener destruction
    #
    # @endif
    #
    # void addConnectorListener(ConnectorListenerType type,
    #                           ConnectorListener* listener,
    #                           bool autoclean)
    def addConnectorListener(self, listener_type, listener, autoclean):
        self._rtcout.RTC_TRACE("addConnectorListener()")

        if listener_type < OpenRTM_aist.ConnectorListenerType.CONNECTOR_LISTENER_NUM:
            self._listeners.connector_[listener_type].addListener(listener, autoclean)

  
    ##
    # @if jp
    # @brief ConnectorDataListener �ꥹ�ʤ�������
    #
    # ���ꤷ���Ƽ�ꥹ�ʤ������롣
    # 
    # @param listener_type �ꥹ�ʥ�����
    # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
    #
    # @else
    # @brief Removing BufferDataListener type listener
    #
    # This operation removes a specified listener.
    #     
    # @param listener_type A listener type
    # @param listener A pointer to a listener object
    #
    # @endif
    #
    # void removeConnectorListener(ConnectorListenerType type,
    #                              ConnectorListener* listener)
    def removeConnectorListener(self, listener_type, listener):
        self._rtcout.RTC_TRACE("removeConnectorListener()")
        
        if listener_type < OpenRTM_aist.ConnectorListenerType.CONNECTOR_LISTENER_NUM:
            self._listeners.connector_[listener_type].removeListener(listener)


    ##
    # @if jp
    # @brief Interface������������
    #
    # Interface�����������롣
    # ������ ConnectorProfile �˳�Ǽ����Ƥ��� dataflow_type �� push ��
    # �ξ��ϡ����ꤵ�줿 interface_type �� InPortProvider �˴ؤ������
    # �� ConnectorProfile::properties �˽���߸ƤӽФ�¦���᤹��
    #
    #  dataport.dataflow_type
    #
    # @param connector_profile ���ͥ����ץ��ե�����
    #
    # @return ReturnCode_t ���Υ꥿���󥳡���
    #
    # @else
    # @brief Publish interface information
    #
    # Publish interface information.
    # Assign the Provider information that owned by this port
    # to ConnectorProfile#properties
    #
    # @param connector_profile The connector profile
    #
    # @return The return code of ReturnCode_t type
    #
    # @endif
    #
    # ReturnCode_t publishInterfaces(ConnectorProfile& connector_profile);
    def publishInterfaces(self, cprof):
        self._rtcout.RTC_TRACE("publishInterfaces()")

        # prop: [port.outport].
        prop = copy.deepcopy(self._properties)

        conn_prop = OpenRTM_aist.Properties()
        OpenRTM_aist.NVUtil.copyToProperties(conn_prop, cprof.properties)
        prop.mergeProperties(conn_prop.getNode("dataport")) # marge ConnectorProfile

        #
        # ������, ConnectorProfile ����� properties ���ޡ������줿���ᡢ
        # prop["dataflow_type"]: �ǡ����ե���������
        # prop["interface_type"]: ���󥿡��ե�����������
        # �ʤɤ�����������ǽ�ˤʤ롣
        #
        dflow_type = prop.getProperty("dataflow_type")
        dflow_type = OpenRTM_aist.normalize([dflow_type])

        if dflow_type == "push":
            self._rtcout.RTC_DEBUG("dataflow_type = push .... create PushConnector")

            # create InPortProvider
            provider = self.createProvider(cprof, prop)

            if provider == 0:
                return RTC.BAD_PARAMETER

            # create InPortPushConnector
            connector = self.createConnector(cprof, prop, provider_=provider)
            if connector == 0:
                return RTC.RTC_ERROR

            connector.setDataType(self._value)
            provider.setConnector(connector) # So that a provider gets endian information from a connector.

            self._rtcout.RTC_DEBUG("publishInterfaces() successfully finished.")
            return RTC.RTC_OK

        elif dflow_type == "pull":
            self._rtcout.RTC_DEBUG("dataflow_type = pull .... do nothing")
            return RTC.RTC_OK

        self._rtcout.RTC_ERROR("unsupported dataflow_type")
        return RTC.BAD_PARAMETER

    
    ##
    # @if jp
    # @brief Interface����³����
    #
    # Interface����³���롣
    # Port����ͭ����Consumer��Ŭ�礹��Provider�˴ؤ������� 
    # ConnectorProfile#properties ������Ф���
    # Consumer��CORBA���֥������Ȼ��Ȥ����ꤹ�롣
    #
    # @param connector_profile ���ͥ������ץ��ե�����
    #
    # @return ReturnCode_t ���Υ꥿���󥳡���
    #
    # @else
    # @brief Subscribe to the interface
    #
    # Subscribe to interface.
    # Derive Provider information that matches Consumer owned by the Port 
    # from ConnectorProfile#properties and 
    # set the Consumer to the reference of the CORBA object.
    #
    # @param connector_profile The connector profile
    #
    # @return ReturnCode_t The return code of ReturnCode_t type
    #
    # @endif
    #
    # ReturnCode_t subscribeInterfaces(const ConnectorProfile& connector_profile);
    def subscribeInterfaces(self, cprof):
        self._rtcout.RTC_TRACE("subscribeInterfaces()")

        # prop: [port.outport].
        prop = copy.deepcopy(self._properties)
        conn_prop = OpenRTM_aist.Properties()
        OpenRTM_aist.NVUtil.copyToProperties(conn_prop, cprof.properties)
        prop.mergeProperties(conn_prop.getNode("dataport")) # marge ConnectorProfile

        #
        # ������, ConnectorProfile ����� properties ���ޡ������줿���ᡢ
        # prop["dataflow_type"]: �ǡ����ե���������
        # prop["interface_type"]: ���󥿡��ե�����������
        # �ʤɤ�����������ǽ�ˤʤ롣
        #
        dflow_type = prop.getProperty("dataflow_type")
        dtype = [dflow_type]
        OpenRTM_aist.normalize(dtype)
        dflow_type = dtype[0]

        if dflow_type == "push":
            self._rtcout.RTC_DEBUG("dataflow_type = push .... do nothing")

            id = cprof.connector_id
            for connector in self._connectors:
                if connector.id() == id:
                    profile = OpenRTM_aist.ConnectorInfo(cprof.name,
                                                         cprof.connector_id,
                                                         OpenRTM_aist.CORBA_SeqUtil.refToVstring(cprof.ports),
                                                         prop)
                    return connector.setConnectorInfo(profile)

            self._rtcout.RTC_ERROR("subscribeInterfaces(): Not found connector.")
            return RTC.RTC_ERROR
        
        elif dflow_type == "pull":
            self._rtcout.RTC_DEBUG("dataflow_type = pull .... create PullConnector")

            # create OutPortConsumer
            consumer = self.createConsumer(cprof, prop)
            if consumer == 0:
                return RTC.BAD_PARAMETER

            # create InPortPullConnector
            connector = createConnector(cprof, prop, consumer_=consumer)
            if connector == 0:
                return RTC.RTC_ERROR

            self._rtcout.RTC_DEBUG("publishInterface() successfully finished.")
            return RTC.RTC_OK

        self._rtcout.RTC_ERROR("unsupported dataflow_type")
        return RTC.BAD_PARAMETER
        
    
    ##
    # @if jp
    # @brief Interface�ؤ���³��������
    #
    # Interface�ؤ���³�������롣
    # Ϳ����줿ConnectorProfile�˴�Ϣ����Consumer�����ꤵ�줿���Ƥ�Object��
    # ��������³�������롣
    #
    # @param connector_profile ���ͥ������ץ��ե�����
    #
    # @else
    # @brief Disconnect the interface connection
    #
    # Disconnect the interface connection.
    # Release all objects set in Consumer associated with 
    # given ConnectorProfile and unscribe the interface.
    #
    # @param connector_profile The connector profile
    #
    # @endif
    #
    # void unsubscribeInterfaces(const ConnectorProfile& connector_profile);
    def unsubscribeInterfaces(self, connector_profile):
        self._rtcout.RTC_TRACE("unsubscribeInterfaces()")

        id = connector_profile.connector_id
        self._rtcout.RTC_PARANOID("connector_id: %s", id)

        len_ = len(self._connectors)
        for i in range(len_):
            idx = (len_ - 1) - i
            if id == self._connectors[idx].id():
                # Connector's dtor must call disconnect()
                self._connectors[idx].deactivate()
                del self._connectors[idx]
                self._rtcout.RTC_TRACE("delete connector: %s", id)
                return

        self._rtcout.RTC_ERROR("specified connector not found: %s", id)
        return


    ##
    # @if jp
    # @brief InPort provider �ν����
    # @else
    # @brief InPort provider initialization
    # @endif
    #
    # void initProviders();
    def initProviders(self):
        self._rtcout.RTC_TRACE("initProviders()")

        # create InPort providers
        factory = OpenRTM_aist.InPortProviderFactory.instance()
        provider_types = factory.getIdentifiers()

        self._rtcout.RTC_DEBUG("available providers: %s",
                               OpenRTM_aist.flatten(provider_types))

        if self._properties.hasKey("provider_types") and \
                OpenRTM_aist.normalize(self._properties.getProperty("provider_types")) != "all":
            self._rtcout.RTC_DEBUG("allowed providers: %s",
                                   self._properties.getProperty("provider_types"))

            temp_types = provider_types
            provider_types = []
            active_types = OpenRTM_aist.split(self._properties.getProperty("provider_types"), ",")

            temp_types.sort()
            active_types.sort()
            set_intersection = lambda a, b: [x for x in a if x in b]
            provider_types = provider_types + set_intersection(temp_types, active_types)

        # InPortProvider supports "push" dataflow type
        if len(provider_types) > 0:
            self._rtcout.RTC_DEBUG("dataflow_type push is supported")
            self.appendProperty("dataport.dataflow_type", "push")
            self.appendProperty("dataport.interface_type",
                                OpenRTM_aist.flatten(provider_types))

        self._providerTypes = provider_types
        return


    ##
    # @if jp
    # @brief OutPort consumer �ν����
    # @else
    # @brief OutPort consumer initialization
    # @endif
    #
    # void initConsumers();
    def initConsumers(self):
        self._rtcout.RTC_TRACE("initConsumers()")

        # create OuPort consumers
        factory = OpenRTM_aist.OutPortConsumerFactory.instance()
        consumer_types = factory.getIdentifiers()
        self._rtcout.RTC_DEBUG("available consumers: %s",
                               OpenRTM_aist.flatten(consumer_types))

        if self._properties.hasKey("consumer_types") and \
                OpenRTM_aist.normalize(self._properties.getProperty("consumer_types")) != "all":
            self._rtcout.RTC_DEBUG("allowed consumers: %s",
                                   self._properties.getProperty("consumer_types"))

            temp_types = consumer_types
            consumer_types = []
            active_types = OpenRTM_aist.split(self._properties.getProperty("consumer_types"), ",")

            temp_types.sort()
            active_types.sort()
            set_intersection = lambda a, b: [x for x in a if x in b]
            consumer_types = consumer_types + set_intersection(temp_types, active_types)

        # OutPortConsumer supports "pull" dataflow type
        if len(consumer_types) > 0:
            self._rtcout.RTC_PARANOID("dataflow_type pull is supported")
            self.appendProperty("dataport.dataflow_type", "pull")
            self.appendProperty("dataport.interface_type",
                                OpenRTM_aist.flatten(consumer_types))

        self._consumerTypes = consumer_types


    ##
    # @if jp
    # @brief InPort provider ������
    #
    # InPortProvider ��������������� ConnectorProfile �˸������롣
    # �����˼��Ԥ������ 0 ���֤���
    #
    # @else
    # @brief InPort provider creation
    # @endif
    #
    # InPortProvider*
    # createProvider(ConnectorProfile& cprof, coil::Properties& prop);
    def createProvider(self, cprof, prop):
        if not prop.getProperty("interface_type") and \
                not OpenRTM_aist.includes(self._providerTypes, prop.getProperty("interface_type")):
            self._rtcout.RTC_ERROR("no provider found")
            self._rtcout.RTC_DEBUG("interface_type:  %s", prop.getProperty("interface_type"))
            self._rtcout.RTC_DEBUG("interface_types: %s",
                                   OpenRTM_aist.flatten(self._providerTypes))
            return 0

    
        self._rtcout.RTC_DEBUG("interface_type: %s", prop.getProperty("interface_type"))
        provider = OpenRTM_aist.InPortProviderFactory.instance().createObject(prop.getProperty("interface_type"))
    
        if provider != 0:
            self._rtcout.RTC_DEBUG("provider created")
            provider.init(prop.getNode("provider"))

            if not provider.publishInterface(cprof.properties):
                self._rtcout.RTC_ERROR("publishing interface information error")
                OpenRTM_aist.InPortProviderFactory.instance().deleteObject(provider)
                return 0
            return provider

        self._rtcout.RTC_ERROR("provider creation failed")
        return 0


    ##
    # @if jp
    # @brief OutPort consumer ������
    #
    # OutPortConsumer ���������롣
    # �����˼��Ԥ������ 0 ���֤���
    #
    # @else
    # @brief InPort provider creation
    # @endif
    #
    # OutPortConsumer*
    # createConsumer(const ConnectorProfile& cprof, coil::Properties& prop);
    def createConsumer(self, cprof, prop):
        if not prop.getProperty("interface_type") and \
                not OpenRTM_aist.includes(self._consumerTypes, prop.getProperty("interface_type")):
            self._rtcout.RTC_ERROR("no consumer found")
            self._rtcout.RTC_DEBUG("interface_type:  %s", prop.getProperty("interface_type"))
            self._rtcout.RTC_DEBUG("interface_types: %s",
                                   OpenRTM_aist.flatten(self._consumerTypes))
            return 0
    
        self._rtcout.RTC_DEBUG("interface_type: %s", prop.getProperty("interface_type"))
        consumer = OpenRTM_aist.OutPortConsumerFactory.instance().createObject(prop.getProperty("interface_type"))
    
        if consumer != 0:
            self._rtcout.RTC_DEBUG("consumer created")
            consumer.init(prop.getNode("consumer"))

            if not consumer.subscribeInterface(cprof.properties):
                self._rtcout.RTC_ERROR("interface subscription failed.")
                OpenRTM_aist.OutPortConsumerFactory.instance().deleteObject(consumer)
                return 0
            return consumer

        self._rtcout.RTC_ERROR("consumer creation failed")
        return 0


    ##
    # @if jp
    # @brief InPortPushConnector ������
    #
    # Connector ������������������������� m_connectors ����¸���롣
    # �����˼��Ԥ������ 0 ���֤���
    #
    # @else
    # @brief InPortPushConnector creation
    # @endif
    #
    #InPortConnector*
    #createConnector(ConnectorProfile& cprof, coil::Properties& prop,
    #                InPortProvider* provider);
    def createConnector(self, cprof, prop, provider_=None, consumer_=None):
        profile = OpenRTM_aist.ConnectorInfo(cprof.name,
                                             cprof.connector_id,
                                             OpenRTM_aist.CORBA_SeqUtil.refToVstring(cprof.ports),
                                             prop)
        connector = None


        try:
            if provider_ is not None:
                if self._singlebuffer:
                    connector = OpenRTM_aist.InPortPushConnector(profile, provider_,
                                                                 self._listeners,
                                                                 self._thebuffer)
                else:
                    connector = OpenRTM_aist.InPortPushConnector(profile, provider_,
                                                                 self._listeners)

            elif cosumer_ is not None:
                if self._singlebuffer:
                    connector = OpenRTM_aist.InPortPullConnector(profile, consumer_,
                                                                 self._listeners,
                                                                 self._thebuffer)
                else:
                    connector = OpenRTM_aist.InPortPullConnector(profile, consumer_,
                                                                 self._listeners)

            else:
                self._rtcout.RTC_ERROR("provider or consumer is not passed. returned 0;")
                return 0
                

            if connector is None:
                self._rtcout.RTC_ERROR("old compiler? new returned 0;")
                return 0

            self._rtcout.RTC_TRACE("InPortPushConnector created")

            self._connectors.append(connector)
            self._rtcout.RTC_PARANOID("connector push backed: %d", len(self._connectors))
            return connector
        except:
            self._rtcout.RTC_ERROR("InPortPushConnector creation failed")
            return 0

        self._rtcout.RTC_FATAL("never comes here: createConnector()")
        return 0