#!/usr/bin/env python
# -*- python -*-
#
#  @file README_src.py
#  @brief rtc-template RTComponent's README file generator class
#  @date $Date: 2007/01/11 07:47:03 $
#  @author Noriaki Ando <n-ando@aist.go.jp>
# 
#  Copyright (C) 2004-2005
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
# 
#  $Id: README_gen.py 775 2008-07-28 16:14:45Z n-ando $
#

import os
import time
import gen_base

readme = """#======================================================================
#  RTComponent: [basicInfo.name] specificatioin
#
#  OpenRTM-aist-[version]
#
#  Date: [date] 
#
#  This file is generated by rtc-template with the following argments.
#
[for args in fmtd_args]
#  [if-index args is first][else]  [endif]
[args][if-index args is last][else]\\[endif]

[endfor]
#
#======================================================================
#    Basic Information
#======================================================================
# <rtc-template block="module">
# </rtc-template>
#======================================================================
#    Activity definition
#======================================================================
# <rtc-template block="actions">
# </rtc-template>
#======================================================================
#    InPorts definition
#======================================================================
# <rtc-template block="inport">
# </rtc-template>
#======================================================================
#    OutPorts definition
#======================================================================
# <rtc-template block="outport">
# </rtc-template>
#======================================================================
#    Service definition
#======================================================================
# <rtc-template block="service">
# </rtc-template> 
#======================================================================
#    Configuration definition
#======================================================================
# <rtc-template block="configuration">
# </rtc-template> 
"""

module = """Basic Information:
  Description: [basicInfo.description]

  Version:     [basicInfo.version]

  Author:      [basicInfo.vendor]

  Category:    [basicInfo.category]

  Comp. Type:  [basicInfo.componentType]

  Act. Type:   [basicInfo.activityType]

  MAX Inst.:   [basicInfo.maxInstances]

  Lang:        
  Lang Type:   
"""

inport = """InPorts:
[for inport in dataPorts]
[if inport.portType is DataInPort]
  Name:             [inport.name]

  VarName:          [inport.rtcExt::varname]

  PortNumber:       [inport.rtcDoc::doc.number]

  Description:      [inport.rtcDoc::doc.description]

  Type:             [inport.type]

  InterfaceType:    [inport.interfaceType]

  DataflowType:     [inport.dataflowType]

  SubscriptionType: [inport.subscriptionType]

  MaxOut: 

[endif]
[endfor]
"""

outport = """OutPorts:
[for outport in dataPorts]
[if outport.portType is DataOutPort]
  Name:             [outport.name]

  VarName:          [outport.rtcExt::varname]

  PortNumber:       [outport.rtcDoc::doc.number]

  Description:      [outport.rtcDoc::doc.description]

  Type:             [outport.type]

  InterfaceType:    [outport.interfaceType]

  DataflowType:     [outport.dataflowType]

  SubscriptionType: [outport.subscriptionType]

  MaxOut: 

[endif]
[endfor]
"""
service = """ServicePorts:
[for service in servicePorts]
  PortName:    [service.name]

  Description: [service.rtcDoc::doc.description]

  InterfaceDescription: [service.rtcDoc::doc.ifdescription]

  Position:    [service.rtcExt::position]

  Interfaces:
[for svcif in service.serviceInterface]
    Name:         [svcif.name]

    Description:  [svcif.rtcDoc::doc.description]

    Type:         [svcif.type]

    Direction:    [svcif.direction]

    InstanceName: [svcif.instanceName]

    IDLfile:      [svcif.idlFile]

    FilePath:     [svcif.path]
    
[endfor]

[endfor]

"""

configuration = """Configuration:
[for config in configurationSet.configuration]
  Name:         [config.name]

  Description:  [config.rtcDoc::doc.description]

  Type:         [config.type]

  DefaultValue: [config.defaultValue]

  Range:        [config.rtcDoc::doc.range]

  Unit:         [config.rtcDoc::doc.unit]

  Constraint:   [config.rtcDoc::doc.constraint]


[endfor]"""

class README_gen(gen_base.gen_base):
	def __init__(self, data):
		self.data = data.copy()
		self.data['fname'] = "README." + self.data['basicInfo']['name']
		self.data['version'] = os.popen("rtm-config --version", "r").read()
		self.data['date'] = time.asctime()
		
		self.tags = {}
		self.tags["module"] = module
		self.tags["actions"] = self.CreateActions()
		self.tags["inport"] = inport
		self.tags["outport"] = outport
		self.tags["service"] = service
		self.tags["configuration"] = configuration
		self.gen_tags(self.tags)
		return

	def CreateActions(self):
		actnames = [
			"onInitialize",
			"onFinalize",
			"onActivated",
			"onDeactivated",
			"onAborting",
			"onError",
			"onReset",
			"onExecute",
			"onStateUpdate",
			"onShutdown",
			"onStartup",
			"onRateChanged",
			]
		acttext = """  %s:
    Description:
      [actions.%s.rtcDoc::doc.description]
  
    PreCondition:
      [actions.%s.rtcDoc::doc.preCondition]
  
    PostCondition:
      [actions.%s.rtcDoc::doc.postCondition]


"""
		actions = """Actions:
"""
		for a in actnames:
			actions += acttext % (a,a,a,a)
		return actions

	def print_readme(self):
		self.gen(self.data["fname"], readme, self.data, self.tags)

	def print_all(self):
		self.print_readme()

