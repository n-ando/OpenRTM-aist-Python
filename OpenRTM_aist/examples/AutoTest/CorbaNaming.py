#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-


##
# \file CorbaNaming.py
# \brief CORBA naming service helper class
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import omniORB.CORBA as CORBA
import CosNaming
import string

##
# @if jp
# @class CorbaNaming
# @brief CORBA Naming Service εγΠε¦­εγΒε¦Ύεβ―εγ©εβΉ
#
# εαΖεΆ°εβ―εγ©εβΉεα―εΰ΅¤osNaming::NamingContext εα«κ±ΎεαÒε£λεγ©εγ¦ε¥ρεγΌεβ―εγ©εβΉεα§εα¤ε£λεΰ‚
# CosNaming::NamingContext εαΈθ·αεα¤εβªεγΤε¦®εγΌεβ·εγ§εγ³εα¨εα»εαΌιπΈε΅ψμ«ήκ¦Ώεα®
# εβªεγΤε¦®εγΌεβ·εγ§εγ³εβΔθ½πθΐΦε΅ωεβ¶εΆªεα¨εβ¤εΆ­εΰΆε¥νεγΌεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ CosNaming::Name
# εα®θ½£εβΎε£κεα«λφ®η­Ξη―χεα«εβ°ε£λιπΊη±νπ£¨νοΎεβΔη½χεαΒζ»Πε΅ρεβ¶ε¤¬εγΤε¦®εγΌεβ·εγ§εγ³εβ¤θ½πθΐΦε΅ωεβ¶ε€‚
#
# εβªεγΜε¤Ίεβ§εβ―εγ°εΆ±ντήθ―πλω¤ε€Άε΅βεβ¶ε΅δεα―ντήθ―πνϋ΄κΐΈεΆ­ CORBA εγΊε¦Ύεγ εβµεγΌεγΐεΆ­λξ¥ξΈΤε΅χ
# θ½¥κΐΈε€Άε΅σεα®εγΊε¦Ύεγ εβµεγΌεγΐεΆ°εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ°εΆ­κ±ΎεαΞεΆ¨ξª®εΰªεΆ°εβªεγΤε¦®εγΌεβ·εγ§εγ³
# εβΔη®¨νπ¬ε΅ωεβ¶ε€‚
# μΉ±εα¨λΣξκ³¤εα®εγΊε¦Ύεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ°εΆ°θΏΨθ―πεβ¨ε¤¬εγΜε¤Ίεβ§εβ―εγ°εΆ°εγΐε¤¦εγ³εγ²εΆ­εα΄ε΅δεα¦εΰ
# ρΰΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅μκ―ΠηΨªεαΞεΆ¬εα¨η ΄ιπ°εΆ©εβ¤ε€ΆηΌ·ιθ¶νϊ¨εΆ­εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςεγΐε¤¦εγ³εγ‰
# εαΞιΦ°νϊ¨εΆ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε£δεβªεγΜε¤Ίεβ§εβ―εγ°εΆ°εγΐε¤¦εγ³εγ²ε£ςπ£Έε΅ζεαΖεΆªεβ¤εΆ©εαΊε£λεΰ‚
#
# @since 0.4.0
#
# @else
# @class CorbaNaming
# @brief CORBA Naming Service helper class
#
# This class is a wrapper class of CosNaming::NamingContext.
# Almost the same operations which CosNaming::NamingContext has are
# provided, and some operation allows string naming representation of
# context and object instead of CosNaming::Name.
#
# The object of the class would connect to a CORBA naming server at
# the instantiation or immediately after instantiation.
# After that the object invokes operations to the root context of it.
# This class realizes forced binding to deep NamingContext, without binding
# intermediate NamingContexts explicitly.
#
# @since 0.4.0
#
# @endif
class CorbaNaming:
  """
  """



  ##
  # @if jp
  #
  # @brief εβ³εγ³εβΉεγ°ε¦«εβ―εβΏ
  #
  # @param self
  # @param orb ORB
  # @param name_server εγΊε¦Ύεγ εβµεγΌεγΐεΆ°ιπΊι§°(εγ®ε¥υεβ©εγ«εγ°η€¤:None)
  #
  # @else
  #
  # @brief Consructor
  #
  # @endif
  def __init__(self, orb, name_server=None):
    self._orb = orb
    self._nameServer = ""
    self._rootContext = CosNaming.NamingContext._nil
    self._blLength = 100

    if name_server:
      self._nameServer = "corbaloc::" + name_server + "/NameService"
      try:
        obj = orb.string_to_object(self._nameServer)
        self._rootContext = obj._narrow(CosNaming.NamingContext)
        if CORBA.is_nil(self._rootContext):
          print "CorbaNaming: Failed to narrow the root naming context."

      except CORBA.ORB.InvalidName:
        print "Service required is invalid [does not exist]."

    return
  

  ##
  # @if jp
  #
  # @brief εγ®ε¤»εγ°ε¦«εβ―εβΏ
  # 
  # @param self
  # 
  # @else
  # 
  # @brief destructor
  # 
  # @endif
  def __del__(self):
    return


  ##
  # @if jp
  #
  # @brief εγΊε¦Ύεγήε¦µεβ°εβµεγΌεγΖε¤»εα®ιθΪθΨ΅ιμ–
  # 
  # λμ®η®Τε΅υεβΈεΆ΅εγΊε¦Ύεγ εβµεγΌεγΐζΈ΄εΆ°εγΊε¦Ύεγήε¦µεβ°εβµεγΌεγΖε¤»εβΔη―ύλόήη·φεαΞεΆΐεαÒε€‚
  # 
  # @param self
  # @param name_server εγΊε¦Ύεγ εβµεγΌεγΐεΆ°ιπΊι§°
  # 
  # @else
  # 
  # @endif
  def init(self, name_server):
    self._nameServer = "corbaloc::" + name_server + "/NameService"
    obj = self._orb.string_to_object(self._nameServer)
    self._rootContext = obj._narrow(CosNaming.NamingContext)
    if CORBA.is_nil(self._rootContext):
      raise MemoryError

    return


  ##
  # @if jp
  #
  # @brief Object εβ’ bind εαÒε£λ
  #
  # CosNaming::bind() εα¨εα»εαΌιπΈι­²εΆ°ιγΊε΅νεβΔε΅ωεβ¶ε΅μεΰΆηΈΈεα«θΊΌε΅θεβ²ε£μεαήε¥νεγΌεγ εβµεγΌεγΐεΆ°
  # εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ°εΆ­κ±ΎεαΞεΆ¨bind()εαΈηΒΎεα³ιηΊεαΚε£μεβ¶ι¤»εαΈιΚ²εαªεβ¶ε€‚
  #
  # Name <name> εα¨ Object <obj> εβΔη½Ζκ©² NamingContext θΊ΄εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ¶ε€‚
  # c_n εα n νυªνϋ®εα® NameComponent εβΔε΅βεβ²ε£οεαÒεΆªεαÒε£λεα¨εΰ
  # name εα n ιΰ¶εΆ° NameComponent εα¶ε£ιλθΐε£λεα¨εαΊε€Άζ»¥θΊ¶εΆ°εβ°ε΅ζεα«λι±εβΎε£μεβ¶ε€‚
  #
  # cxt->bind(<c_1, c_2, ... c_n>, obj) εα―θ½¥θΊ¶εΆ°λσΊζ½ΨεΆªιπΈι­²εΆ©εα¤ε£λεΰ‚
  # cxt->resolve(<c_1, ... c_(n-1)>)->bind(<c_n>, obj)
  #
  # εαÒεΆ¬εβΎεΆ£εΰ1νυªνϋ®εα¶ε£ιn-1νυªνϋ®εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςπ©£μ³ΊεαΞε€΅Ο-1νυªνϋ®εα®εβ³εγ³εγ¬ε¤―εβΉεγ
  # θΊ΄εΆ­ name <n> εα¨εαΞεΆ¨εΰ€obj εβ’ bind εαÒε£λεΰ‚
  # ιπΊη±νπ©£μ³Ίεα«ιο¤η΄ΆεαÒε£λ <c_1, ... c_(n-1)> εα® NemingContext εα―εΰ
  # bindContext() εβ„ rebindContext() εα§λχΆεα«εγΐε¤¦εγ³εγ²θΈ°εΆΑεα§εαªεαΒε£μεα°εαªεβ²εΆ¬εα¨ε€‚
  # εβ¤ε΅χ <c_1, ... c_(n-1)> εα® NamingContext εαΈη­ΠηΨªεαΞεΆ¬εα¨η ΄ιπ°εΆ­εα―εΰ
  # NotFound θΐ¶η¤Με΅μνωΊντήε΅ωεβ¶ε€‚
  #
  # εαήεΆΆεαΞε€ΆηΌ·ιθ¶εγΐε¤¦εγ³εγ²ε¥υεγ©εβ° force εα true εα®λω¤εΆ±εΰ<c_1, ... c_(n-1)>
  # εαΈη­ΠηΨªεαΞεΆ¬εα¨η ΄ιπ°εΆ­εβ¤ε€Άη«νκΊ°νϊ¨εΆ­εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςεγΐε¤¦εγ³εγ²ε΅χεαªεαΈε£ιεΰ
  # λό€ξ·¤ιΣδεα« obj εβΔηΏνιι name <c_n> εα«εγΐε¤¦εγ³εγ²ε΅ωεβ¶ε€‚
  #
  # εα¨ε΅ϊεβΈεΆ°κΆ΄ιπ°εΆ©εβ¤ε€΅Ο-1νυªνϋ®εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ζΈ΄εΆ­ name<n> εα®εβªεγΜε¤Ίεβ§εβ―εγ
  # (Object εα¤ε£λεα¨εΆ± εβ³εγ³εγ¬ε¤―εβΉεγ) εαΈε¥πεβ¤εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£μεα°
  # AlreadyBound θΐ¶η¤Με΅μνωΊντήε΅ωεβ¶ε€‚
  #
  # @param self
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ° NameComponent
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ Object
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:None)
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name_list εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  # @exception AlreadyBound name <c_n> εα® Object εαΈε΅ωεα§εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bind(self, name_list, obj, force=None):
    if force is None :
      force = True

    try:
      self._rootContext.bind(name_list, obj)
    except CosNaming.NamingContext.NotFound:
      if force:
        self.bindRecursive(self._rootContext, name_list, obj)
      else:
        raise
    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.bindRecursive(err.cxt, err.rest_of_name, obj)
      else:
        raise
    except CosNaming.NamingContext.AlreadyBound:
      self._rootContext.rebind(name_list, obj)


  ##
  # @if jp
  #
  # @brief Object εβ’ bind εαÒε£λ
  #
  # Object εβ’ bind εαÒε£λρϊΦεΆ­θΊΌε΅θεβ¶ηΏνιιΊε΅μλφ®η­Ξη―χπ£¨νοΎεα§εα¤ε£λεαΖεΆªθ½¥κ¦ΜεΆ±εΰ΅Γind()
  # εα¨ιπΈε΅ψεα§εα¤ε£λεΰ£Γind(toName(string_name), obj) εα¨ξ―²ζΎ΅εΰ‚
  #
  # @param self
  # @param string_name εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ°λφ®η­Ξη―χπ£¨νοΎ
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:true)
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² string_name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  # @exception AlreadyBound name <n> εα® Object εαΈε΅ωεα§εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindByString(self, string_name, obj, force=True):
    self.bind(self.toName(string_name), obj, force)


  ##
  # @if jp
  #
  # @brief ρΰΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ς bind εαΞεΆ¬εαΈε£ι Object εβ’ bind εαÒε£λ
  #
  # context εα§θΊΌε΅θεβ²ε£μεα NamingContext εα«κ±ΎεαΞεΆ¨εΰ΅Οame εα§λμ®η®Τε΅υεβΈεΆ΅
  # εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ <c_1, ... c_(n-1)> εβ’ NamingContext εα¨εαΞεΆ¨
  # π©£μ³ΊεαΞεΆ¬εαΈε£ιεΰΆηΏνιι <c_n> εα«κ±ΎεαΞεΆ¨ obj εβ’ bind εαÒε£λεΰ‚
  # εβ¤ε΅χεΰ<c_1, ... c_(n-1)> εα«κ±ΎκΑΨε΅ωεβ‹ NamingContext εαΈεΆ¬εα¨η ΄ιπ°εΆ­εα―
  # λφ°εαήεΆ¬ NamingContext εβΔε¥πεβ¤εγ³εγ²ε΅ωεβ¶ε€‚
  #
  # λό€ξ·¤ιΣδεα« <c_1, c_2, ..., c_(n-1)> εα«κ±ΎκΑΨε΅ωεβ‹ NamingContext εαΈιΘ΅λθ
  # εαΎεαήεΆ±π©£μ³ΊεαΚε£μεαήζΈ΄εΆ©εΰ΅¤osNaming::bind(<c_n>, object) εαΈηΒΎεα³ιηΊεαΚε£μεβ¶ε€‚
  # εαΖεΆ°εα¨εαΊε€Άε΅ωεα§εα«εγΐε¤¦εγ³εγ®ε¤¥εγ³εβ°εαΈη­ΠηΨªεαÒε£μεα° AlreadyBoundθΐ¶η¤Με΅μνωΊντήε΅ωεβ¶ε€‚
  #
  # ρΰΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςπ©£μ³ΊεαÒε£λραΌι¨¶εΆ©εΰΆκ§£μ³ΊεαΞε£θεα¬εΆªεαÒε£λεβ³εγ³εγ¬ε¤―εβΉεγ°εΆª
  # ιπΈε΅ψιπΊη±νεα® NamingContext εα§εα―εαªεα„ Binding εαΈη­ΠηΨªεαÒε£λκΆ΄ιπ°ε€
  # CannotProceed θΐ¶η¤Με΅μνωΊντήε΅χιη¦νπ¬ε£ςθΊ­μ―ΆεαÒε£λεΰ‚
  #
  # @param self
  # @param context bind εβΔλΛλκ©¶ε΅ωεβ¶ε€€NamingContext
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ°εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ
  #
  # @exception CannotProceed <c_1, ..., c_(n-1)> εα«κ±ΎκΑΨε΅ωεβ‹ NamingContext 
  #            εα®εα¬εΆ£εα²εα¨εα¤εαΈε€Άε΅ωεα§εα« NamingContext θ½¥κ¦ΜεΆ° object εα«εγΐε¤¦εγ³εγ‰
  #            εαΚε£μεα¦εα΄ε£κεΰΆη®¨νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName ιπΊη±ν name_list εαΈζΈΊθ­£
  # @exception AlreadyBound name <c_n> εα«εαÒεΆ©εα«θΏΚε£ιεα¶εΆ° object εαΈε¥πεβ¤εγ³εγ‰
  #            εαΚε£μεα¦εα¨ε£λεΰ‚
  # @else
  #
  # @brief
  #
  # @endif
  def bindRecursive(self, context, name_list, obj):
    length = len(name_list)
    cxt = context
    for i in range(length):
      if i == length -1:
        try:
          cxt.bind(self.subName(name_list, i, i), obj)
        except CosNaming.NamingContext.AlreadyBound:
          cxt.rebind(self.subName(name_list, i, i), obj)
        return
      else:
        if self.objIsNamingContext(cxt):
          cxt = self.bindOrResolveContext(cxt,self.subName(name_list, i, i))
        else:
          raise CosNaming.NamingContext.CannotProceed(cxt, self.subName(name_list, i))
    return


  ##
  # @if jp
  #
  # @brief Object εβ’ rebind εαÒε£λ
  #
  # name_list εα§λμ®η®Τε΅υεβΈεΆ΅ Binding εαΈε΅ωεα§εα«κ―ΠηΨªεαÒε£λκΆ΄ιπ°ε£ςρω¤εα¨εΆ¨ bind() εα¨ιπΈε΅ψ
  # εα§εα¤ε£λεΰ¤ε¥πεβ¤εγ³εγ®ε¤¥εγ³εβ°εαΈε΅ωεα§εα«κ―ΠηΨªεαÒε£λκΆ΄ιπ°εΆ­εα―εΰΆθΜ²εαΞε΅δεγΐε¤¦εγ³εγ®ε¤¥εγ³εβ°εα«
  # ξΏ®εαΊθ½ϋεα°ε£ιεβΈε£λεΰ‚
  #
  # @param self
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ° NameComponent
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:true)
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName ιπΊη±ν name_list εαΈζΈΊθ­£
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebind(self, name_list, obj, force=True):
    if force is None:
      force = True
      
    try:
      self._rootContext.rebind(name_list, obj)

    except CosNaming.NamingContext.NotFound:
      if force:
        self.rebindRecursive(self._rootContext, name_list, obj)
      else:
        raise

    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.rebindRecursive(err.cxt, err,rest_of_name, obj)
      else:
        raise
      
    return


  ##
  # @if jp
  #
  # @brief Object εβ’ rebind εαÒε£λ
  #
  # Object εβ’ rebind εαÒε£λρϊΦεΆ­θΊΌε΅θεβ¶ηΏνιιΊε΅μλφ®η­Ξη―χπ£¨νοΎεα§εα¤ε£λεαΖεΆªθ½¥κ¦ΜεΆ± rebind()
  # εα¨ιπΈε΅ψεα§εα¤ε£λεΰ£Σebind(toName(string_name), obj) εα¨ξ―²ζΎ΅εΰ‚
  #
  # @param self
  # @param string_name εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ°λφ®η­Ξη―χπ£¨νοΎ
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:true)
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² string_name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindByString(self, string_name, obj, force=True):
    self.rebind(self.toName(string_name), obj, force)

    return


  ##
  # @if jp
  #
  # @brief ρΰΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ς bind εαΞεΆ¬εαΈε£ι Object εβ’ rebind εαÒε£λ
  #
  # name_list <c_n> εα§λμ®η®Τε΅υεβΈεΆ΅ NamingContext εβ¤ε΅χεαΎεΆ± Object εαΈε΅ωεα§εα«κ―ΠηΨªεαÒε£λ
  # κΆ΄ιπ°ε£ςρω¤εα¨εΆ¨ bindRecursive() εα¨ιπΈε΅ψεα§εα¤ε£λεΰ‚
  #
  # name_list <c_n> εα§λμ®η®Τε΅υεβΈεΆ΅εγΐε¤¦εγ³εγ®ε¤¥εγ³εβ°εαΈε΅ωεα§εα«κ―ΠηΨªεαÒε£λκΆ΄ιπ°εΆ­εα―εΰ
  # λφ°εαΞε΅δεγΐε¤¦εγ³εγ®ε¤¥εγ³εβ°εα«ξΏ®εαΊθ½ϋεα°ε£ιεβΈε£λεΰ‚
  #
  # @param self
  # @param context bind εβΔλΛλκ©¶ε΅ωεβ¶ε€€NamingContext
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ° NameComponent
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ
  #
  # @exception CannotProceed ρΰΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅μπ©£μ³Ίεα§εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName θΊΌε΅θεβ²ε£μεα name_list εαΈζΈΊθ­£εΰ‚
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindRecursive(self, context, name_list, obj):
    length = len(name_list)
    for i in range(length):
      if i == length - 1:
        context.rebind(self.subName(name_list, i, i), obj)
        return
      else:
        if self.objIsNamingContext(context):
          try:
            context = context.bind_new_context(self.subName(name_list, i, i))
          except CosNaming.NamingContext.AlreadyBound:
            obj_ = context.resolve(self.subName(name_list, i, i))
            context = obj_._narrow(CosNaming.NamingContext)
        else:
          raise CosNaming.NamingContext.CannotProceed(context, self.subName(name_list, i))
    return


  ##
  # @if jp
  #
  # @brief NamingContext εβ’ bind εαÒε£λ
  #
  # bind κ±Ύπ³΅εα¨εαΞεΆ¨λμ®η®Τε΅υεβΈεΆ΅κΎΚθΚ² name εαΈθΛηκ―Ξη―χεα®κΆ΄ιπ°εΆ± bindByString() εα¨εΰ
  # εαΪε£μθ½¥κ¦ΜεΆ°κΆ΄ιπ°εΆ± bind() εα¨ιπΈε΅ψεα§εα¤ε£λεΰ‚
  #
  # @param self
  # @param name εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιι
  # @param name_cxt ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ NamingContext
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:True)
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  # @exception AlreadyBound name <c_n> εα® Object εαΈε΅ωεα§εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindContext(self, name, name_cxt, force=True):
    if isinstance(name, basestring):
      self.bind(self.toName(name), name_cxt, force)
    else:
      self.bind(name, name_cxt, force)
    return


  ##
  # @if jp
  #
  # @brief NamingContext εβ’ bind εαÒε£λ
  #
  # bind εαΚε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ°ε΅μ NamingContext εα§εα¤ε£λεαΖεΆªεβΔλÒ¦εα¨εΆ¨
  # bindRecursive() εα¨ιπΈε΅ψεα§εα¤ε£λεΰ‚
  #
  # @param self
  # @param context bind εβΔλΛλκ©¶ε΅ωεβ¶ε€€NamingContext
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ°εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  # @param name_cxt ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ NamingContext
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindContextRecursive(self, context, name_list, name_cxt):
    self.bindRecursive(context, name_list, name_cxt)
    return


  ##
  # @if jp
  #
  # @brief NamingContext εβ’ rebind εαÒε£λ
  #
  # bind κ±Ύπ³΅εα¨εαΞεΆ¨λμ®η®Τε΅υεβΈεΆ΅κΎΚθΚ² name εαΈθΛηκ―Ξη―χεα®κΆ΄ιπ°εΆ± rebindByString() εα¨εΰ
  # εαΪε£μθ½¥κ¦ΜεΆ°κΆ΄ιπ°εΆ± rebind() εα¨ιπΈε΅ψεα§εα¤ε£λεΰ‚
  # εα©εα΅εβ²εΆ°κΆ΄ιπ°ε£βεγΐε¤¦εγ³εγ®ε¤¥εγ³εβ°εαΈε΅ωεα§εα«κ―ΠηΨªεαÒε£λκΆ΄ιπ°εΆ­εα―εΰ
  # λφ°εαΞε΅δεγΐε¤¦εγ³εγ®ε¤¥εγ³εβ°εα«ξΏ®εαΊθ½ϋεα°ε£ιεβΈε£λεΰ‚
  #
  # @param self
  # @param name εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ°εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  # @param name_cxt ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ NamingContext
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:true)
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  #
  # @else
  #
  # @endif
  def rebindContext(self, name, name_cxt, force=True):
    if isinstance(name, basestring):
      self.rebind(self.toName(name), name_cxt, force)
    else:
      self.rebind(name, name_cxt, force)
    return


  ##
  # @if jp
  #
  # @brief ρΰΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςιζΊηΈ°νϊ¨εΆ­ rebind εα— NamingContext εβ’ rebind εαÒε£λ    #
  # bind εαΚε£μεβ¶ε¤¬εγΜε¤Ίεβ§εβ―εγ°ε΅μ NamingContext εα§εα¤ε£λεαΖεΆªεβΔλÒ¦εα¨εΆ¨
  # rebindRecursive() εα¨ιπΈε΅ψεα§εα¤ε£λεΰ‚
  #
  # @param self
  # @param context bind εβΔλΛλκ©¶ε΅ωεβ¶ε€€NamingContext
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ° NameComponent
  # @param name_cxt ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ NamingContext
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindContextRecursive(self, context, name_list, name_cxt):
    self.rebindRecursive(context, name_list, name_cxt)
    return


  ##
  # @if jp
  #
  # @brief Object εβ’ name εα¶ε£ιπ©£μ³ΊεαÒε£λ
  #
  # name εα« bind εαΚε£μεα¦εα¨ε£λεβªεγΜε¤Ίεβ§εβ―εγ°η½βνε§εβΔκΏΘε΅ωεΰ‚
  # εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ <c_1, c_2, ... c_n> εα―ιζΊηΈ°νϊ¨εΆ­π©£μ³ΊεαΚε£μεβ¶ε€‚
  # 
  # κΎΚθΚ² name εα«θΊΌε΅θεβ²ε£μεαήη€¤εαΈθΛηκ―Ξη―χεα®κΆ΄ιπ°εΆ­εα―εαΎεαΤθΧΰιθΪεΆ­ toName() εα«εβ°εΆ¥εα¦
  # NameComponent εα«κ¦²θ½ϋεαΚε£μεβ¶ε€‚
  # 
  # CosNaming::resolve() εα¨εα»εαΌιπΈι­²εΆ°ιγΊε΅νεβΔε΅ωεβ¶ε΅μεΰΆηΈΈεα«θΊΌε΅θεβ²ε£μεα
  # εγΊε¦Ύεγ εβµεγΌεγΐεΆ°εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ°εΆ­κ±ΎεαΞεΆ¨ resolve() εαΈηΒΎεα³ιηΊεαΚε£μεβ¶ι¤»εα
  # νυ°εαªεβ¶ε€‚
  #
  # @param self
  # @param name π©£μ³ΊεαÒεΆ»εαΊε¤¬εγΜε¤Ίεβ§εβ―εγ°εΆ°ιπΊη±νεα®εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  #
  # @return π©£μ³ΊεαΚε£μεαήε¤¬εγΜε¤Ίεβ§εβ―εγ°η½βνε§
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  #
  # @else
  #
  # @endif
  def resolve(self, name):
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name
      
    try:
      obj = self._rootContext.resolve(name_)
      return obj
    except CosNaming.NamingContext.NotFound, ex:
      return None


  ##
  # @if jp
  #
  # @brief λμ®η®Τε΅υεβΈεΆ΅ιπΊη±νεα®εβªεγΜε¤Ίεβ§εβ―εγ°εΆ° bind εβΔκ§£ρω¤εαÒε£λ
  #
  # name εα« bind εαΚε£μεα¦εα¨ε£λεβªεγΜε¤Ίεβ§εβ―εγ°η½βνε§εβΔκ§£ρω¤εαÒε£λεΰ‚
  # εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ <c_1, c_2, ... c_n> εα―ιζΊηΈ°νϊ¨εΆ­π©£μ³ΊεαΚε£μεβ¶ε€‚
  # 
  # κΎΚθΚ² name εα«θΊΌε΅θεβ²ε£μεαήη€¤εαΈθΛηκ―Ξη―χεα®κΆ΄ιπ°εΆ­εα―εαΎεαΤθΧΰιθΪεΆ­ toName() εα«εβ°εΆ¥εα¦
  # NameComponent εα«κ¦²θ½ϋεαΚε£μεβ¶ε€‚
  # 
  # CosNaming::unbind() εα¨εα»εαΌιπΈι­²εΆ°ιγΊε΅νεβΔε΅ωεβ¶ε΅μεΰΆηΈΈεα«θΊΌε΅θεβ²ε£μεα
  # εγΊε¦Ύεγ εβµεγΌεγΐεΆ°εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ°εΆ­κ±ΎεαΞεΆ¨ unbind() εαΈηΒΎεα³ιηΊεαΚε£μεβ¶ι¤»εα
  # νυ°εαªεβ¶ε€‚
  #
  # @param self
  # @param name ιι΄λÒ¦εαÒε£λεβªεγΜε¤Ίεβ§εβ―εγ°εΆ°εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  #
  # @else
  #
  # @endif
  # void unbind(const CosNaming::Name& name)
  #   throw(NotFound, CannotProceed, InvalidName);
  def unbind(self, name):
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name

    self._rootContext.unbind(name_)
    return


  ##
  # @if jp
  #
  # @brief λφ°εαΞε΅δεβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςντήθ―πεαÒε£λ
  #
  # θΊΌε΅θεβ²ε£μεαήε¥νεγΌεγ εβµεγΌεγΐζΈ΄εΆ©ντήθ―πεαΚε£μεα NamingContext εβΔκΏΘε΅ωεΰ‚
  # πΑΘε΅υεβΈεΆ΅ NamingContext εα― bind εαΚε£μεα¦εα¨εΆ¬εα¨ε€‚
  # 
  # @param self
  # 
  # @return ντήθ―πεαΚε£μεαήθΜ²εαΞε΅δ NamingContext
  #
  # @else
  #
  # @endif
  def newContext(self):
    return self._rootContext.new_context()


  ##
  # @if jp
  #
  # @brief λφ°εαΞε΅δεβ³εγ³εγ¬ε¤―εβΉεγ°ε£ς bind εαÒε£λ
  #
  # θΊΌε΅θεβ²ε£μεα name εα«κ±ΎεαΞεΆ¨λφ°εαΞε΅δεβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςεγΐε¤¦εγ³εγ²ε΅ωεβ¶ε€‚
  # ντήθ―πεαΚε£μεαήε€€NamingContext εα―εγΊε¦Ύεγ εβµεγΌεγΐζΈ΄εΆ©ντήθ―πεαΚε£μεαήε£βεα®εα§εα¤ε£λεΰ‚
  # 
  # κΎΚθΚ² name εα«θΊΌε΅θεβ²ε£μεαήη€¤εαΈθΛηκ―Ξη―χεα®κΆ΄ιπ°εΆ­εα―εαΎεαΤθΧΰιθΪεΆ­ toName() εα«εβ°εΆ¥εα¦
  # NameComponent εα«κ¦²θ½ϋεαΚε£μεβ¶ε€‚
  # 
  # @param self
  # @param name NamingContextεα«θ½Πε΅ρεβ¶ηΏνιιΊεΆ°εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  # @param force trueεα®κΆ΄ιπ°ε€Άλ€ΘζΈ­εα®εβ³εγ³εγ¬ε¤―εβΉεγ°ε£ςκΎ·ιθ¶νϊ¨εΆ­εγΐε¤¦εγ³εγ²ε΅ωεβ‹
  #              (εγ®ε¥υεβ©εγ«εγ°η€¤:true)
  #
  # @return ντήθ―πεαΚε£μεαήθΜ²εαΞε΅δ NamingContext
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  # @exception AlreadyBound name <n> εα® Object εαΈε΅ωεα§εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  #
  # @else
  #
  # @endif
  def bindNewContext(self, name, force=True):
    if force is None:
      force = True
      
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name

    try:
      return self._rootContext.bind_new_context(name_)
    except CosNaming.NamingContext.NotFound:
      if force:
        self.bindRecursive(self._rootContext, name_, self.newContext())
      else:
        raise
    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.bindRecursive(err.cxt, err.rest_of_name, self.newContext())
      else:
        raise
    return None


  ##
  # @if jp
  #
  # @brief NamingContext εβΔλΩώεβΆεβ―εγ¬ε¤¥εγΜη·φεαÒε£λ
  #
  # context εα§λμ®η®Τε΅υεβΈεΆ΅ NamingContext εβΔλΩώεβΆεβ―εγ¬ε¤¥εγΜη·φεαÒε£λεΰ‚
  # context εα«θ½ΜεΆ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅μεγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λκΆ΄ιπ°εΆ± NotEmpty θΐ¶η¤Με΅μ
  # νωΊντήε΅ωεβ¶ε€‚
  # 
  # @param self
  # @param context ρύάε¤¤εβ―εγ¬ε¤¥εγΜη·φεαÒε£λ NamingContext
  #
  # @exception NotEmpty κ±Ύπ³΅context εα«θ½ΜεΆ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅μεγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  #
  # @else
  #
  # @else
  #
  # @brief Destroy the naming context
  #
  # Delete the specified naming context.
  # any bindings should be <unbind> in which the given context is bound to
  # some names before invoking <destroy> operation on it. 
  #
  # @param context NamingContext which is destroied.
  #     
  # @exception NotEmpty 
  #
  # @else
  #
  # @endif
  def destroy(self, context):
    context.destroy()


  ##
  # @if jp
  # @brief NamingContext εβΔη«νκΊ°νϊ¨εΆ­θΊ¶εΆ¥εα¦ρύάε¤¤εβ―εγ¬ε¤¥εγΜη·φεαÒε£λ
  #
  # context εα§θΊΌε΅θεβ²ε£μεα NamingContext εα«κ±ΎεαΞεΆ¨εΰ΅Οame εα§λμ®η®Τε΅υεβΈεΆ΅
  # εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ <c_1, ... c_(n-1)> εβ’ NamingContext εα¨εαΞεΆ¨
  # π©£μ³ΊεαΞεΆ¬εαΈε£ιεΰΆηΏνιι <c_n> εα«κ±ΎεαΞεΆ¨ ρύάε¤¤εβ―εγ¬ε¤¥εγΜη·φεβΔκ΅Έε΅ζεΰ‚
  #
  # @param self
  # @param context ρύάε¤¤εβ―εγ¬ε¤¥εγΜη·φεαÒε£λ NamingContext
  #
  # @exception NotEmpty κ±Ύπ³΅context εα«θ½ΜεΆ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅μεγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  #
  # @else
  # @brief Destroy the naming context recursively
  # @endif
  def destroyRecursive(self, context):
    cont = True
    bl = []
    bi = 0
    bl, bi = context.list(self._blLength)
    while cont:
      for i in range(len(bl)):
        if bl[i].binding_type == CosNaming.ncontext:
          obj = context.resolve(bl[i].binding_name)
          next_context = obj._narrow(CosNaming.NamingContext)

          self.destroyRecursive(next_context)
          context.unbind(bl[i].binding_name)
          next_context.destroy()
        elif bl[i].binding_type == CosNaming.nobject:
          context.unbind(bl[i].binding_name)
        else:
          assert(0)
      if CORBA.is_nil(bi):
        cont = False
      else:
        bi.next_n(self._blLength, bl)

    if not (CORBA.is_nil(bi)):
      bi.destroy()
    return


  ##
  # @if jp
  # @brief εαÒεΆ»εα¦εα® Binding εβΔη±κρω¤εαÒε£λ
  #
  # νω»ρμ²εαΚε£μεα¦εα¨ε£λιε¨εα¦εα®Binding εβΔη±κρω¤εαÒε£λεΰ‚
  #
  # @param self
  #
  # @else
  # @brief Destroy all binding
  # @endif
  def clearAll(self):
    self.destroyRecursive(self._rootContext)
    return


  ##
  # @if jp
  # @brief θΊΌε΅θεβ²ε£μεα NamingContext εα® Binding εβΔη½φκΐΞε΅ωεβ‹
  #
  # λμ®η®Τε΅υεβΈεΆ΅ NamingContext εα® Binding εβΔη½φκΐΞε΅ωεβ¶ε€‚
  #
  # @param self
  # @param name_cxt Binding ιοΜηΎΞη―Ύπ³΅ NamingContext
  # @param how_many Binding εβΔη½φκΐΞε΅ωεβ¶λΣξκ³¤εα®μΉ±εα•
  # @param rbl ιοΜηΎΞε΅χεα Binding εβΔζΏΪθ·αεαÒε£λεγΦε¦­εγ€
  # @param rbi ιοΜηΎΞε΅χεα Binding εβΔεΆ΅εα©εβ¶εΆ΅εβΆεΆ°εβ¤εγ¬ε¦®εγΌεβΏ
  #
  # @else
  # @endif
  def list(self, name_cxt, how_many, rbl, rbi):
    bl, bi = name_cxt.list(how_many)

    for i in bl:
      rbl.append(bl)

    rbi.append(bi)
  

  #============================================================
  # interface of NamingContext
  #============================================================

  ##
  # @if jp
  # @brief θΊΌε΅θεβ²ε£μεα NameComponent εα®λφ®η­Ξη―χπ£¨νοΎεβΔκΏΘε΅ω
  #
  # λμ®η®Τε΅υεβΈεΆ΅ NameComponent εβΔθΛηκ―ΞεΆ­κ¦²θ½ϋεαÒε£λεΰ‚
  #
  # @param self
  # @param name_list κ¦²θ½ϋκ±Ύπ³΅ NameComponent
  #
  # @return λφ®η­Ξη―χκ¦²θ½ϋξ·ΐθΫό
  #
  # @exception InvalidName κΎΚθΚ² name_list εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  #
  # @else
  # @brief Get string representation of given NameComponent
  # @endif
  def toString(self, name_list):
    if len(name_list) == 0:
      raise CosNaming.NamingContext.InvalidName

    slen = self.getNameLength(name_list)
    string_name = [""]
    self.nameToString(name_list, string_name, slen)

    return string_name


  ##
  # @if jp
  # @brief θΊΌε΅θεβ²ε£μεαήθΛηκ―Ξη―χπ£¨νοΎεβ’ NameComponent εα«ιθ¬κ§£εαÒε£λ
  #
  # λμ®η®Τε΅υεβΈεΆ΅λφ®η­Ξη―χεβ’ NameComponent εα«κ¦²θ½ϋεαÒε£λεΰ‚
  #
  # @param self
  # @param sname κ¦²θ½ϋκ±Ύπ³΅λφ®η­Ξη―χ
  #
  # @return NameComponent κ¦²θ½ϋξ·ΐθΫό
  #
  # @exception InvalidName κΎΚθΚ² sname εαΈζΈΊθ­£εΰ‚
  #
  # @else
  # @brief Get NameComponent from gien string name representation
  # @endif
  def toName(self, sname):
    if not sname:
      raise CosNaming.NamingContext.InvalidName

    string_name = sname
    name_comps = []

    nc_length = 0
    nc_length = self.split(string_name, "/", name_comps)
    if not (nc_length > 0):
      raise CosNaming.NamingContext.InvalidName

    name_list = [CosNaming.NameComponent("","") for i in range(nc_length)]

    for i in range(nc_length):
      pos = string.rfind(name_comps[i][0:],".")
      if pos == -1:
        name_list[i].id   = name_comps[i]
        name_list[i].kind = ""
      else:
        name_list[i].id   = name_comps[i][0:pos]
        name_list[i].kind = name_comps[i][(pos+1):]

    return name_list


  ##
  # @if jp
  # @brief θΊΌε΅θεβ²ε£μεα addr εα¨ string_name εα¶ε£ι URLπ£¨νοΎεβΔη½φκΐΞε΅ωεβ‹
  #
  # λμ®η®Τε΅υεβΈεΆ΅εβΆεγ²ε¦®εβΉεα¨ιπΊι§°εβΓ¶RLεα«κ¦²θ½ϋεαÒε£λεΰ‚
  #
  # @param self
  # @param addr κ¦²θ½ϋκ±Ύπ³΅εβΆεγ²ε¦®εβΉ
  # @param string_name κ¦²θ½ϋκ±Ύπ³΅ιπΊι§°
  #
  # @return URL κ¦²θ½ϋξ·ΐθΫό
  #
  # @exception InvalidAddress κΎΚθΚ² addr εαΈζΈΊθ­£εΰ‚
  # @exception InvalidName κΎΚθΚ² string_name εαΈζΈΊθ­£εΰ‚
  #
  # @else
  # @brief Get URL representation from given addr and string_name
  # @endif
  def toUrl(self, addr, string_name):
    return self._rootContext.to_url(addr, string_name)


  ##
  # @if jp
  # @brief θΊΌε΅θεβ²ε£μεαήθΛηκ―Ξη―χπ£¨νοΎεβ’ resolve εαΞε¤¬εγΜε¤Ίεβ§εβ―εγ°ε£ςπΑΘε΅ω
  #
  # λμ®η®Τε΅υεβΈεΆ΅λφ®η­Ξη―χπ£¨νοΎεβΓΣesolveεαΞρΌΈε¤¬εγΜε¤Ίεβ§εβ―εγ°ε£ςιοΜηΎΞε΅ωεβ¶ε€‚
  #
  # @param self
  # @param string_name ιοΜηΎΞη―Ύπ³΅εβªεγΜε¤Ίεβ§εβ―εγ°θΛηκ―Ξη―χπ£¨νοΎ
  #
  # @return π©£μ³ΊεαΚε£μεαήε¤¬εγΜε¤Ίεβ§εβ―εγ
  #
  # @exception NotFound ρΰΘζΈ­εα® <c_1, c_2, ..., c_(n-1)> εαΈη­ΠηΨªεαΞεΆ¬εα¨ε€‚
  # @exception CannotProceed θΏΚε£ιεα¶εΆ°νπ¬ιΘ³εα§ιη¦νπ¬ε£ςξΈÒι¶ΤεΆ©εαΊεΆ¬εα¨ε€‚
  # @exception InvalidName κΎΚθΚ² name εα®ιπΊη±νεαΈζΈΊθ­£εΰ‚
  # @exception AlreadyBound name <n> εα® Object εαΈε΅ωεα§εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεΰ‚
  #
  # @else
  # @brief Resolve from name of string representation and get object 
  # @endif
  def resolveStr(self, string_name):
    return self.resolve(self.toName(string_name))


  #============================================================
  # Find functions
  #============================================================

  ##
  # @if jp
  #
  # @brief εβªεγΜε¤Ίεβ§εβ―εγ°εΆ°ιπΊη±νεβΔε¥πεβ¤εγ³εγ²εΆΐεαήεΆ±π©£μ³ΊεαÒε£λ
  #
  # λμ®η®Τε΅υεβΈεΆ΅εβ³εγ³εγ¬ε¤―εβΉεγ°εΆ­κ±ΎεαΞεΆ¨εβªεγΜε¤Ίεβ§εβ―εγ°ε£ς NameComponent εα§λμ®η®Τε΅υεβΈεΆ΅
  # θΏΊι½®εα«εγΐε¤¦εγ³εγ²ε΅ωεβ¶ε€‚
  # ιπΈζΈ€ξ°®θ±ΰεα«λχΆεα«θ½ΜεΆ°π¨Άι΄ εαΈε¥πεβ¤εγ³εγ²θΈ°εΆΑεα®κΆ΄ιπ°εΆ±εΰΆθΞ¤κ―ΠεΆ°εγΐε¤¦εγ³εγ²θΈ°εΆΑπ¨Άι΄ εβ’
  # ιοΜηΎΞε΅ωεβ¶ε€‚
  #
  # @param self
  # @param context bind εβ¤ε΅χεαΎεΆ± resole κ±Ύπ³΅εβ³εγ³εγ¬ε¤―εβΉεγ
  # @param name_list εβªεγΜε¤Ίεβ§εβ―εγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ° NameComponent
  # @param obj ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ Object
  #
  # @return NameComponent εα§λμ®η®Τε΅υεβΈεΆ΅θΏΊι½®εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λεβªεγΜε¤Ίεβ§εβ―εγ
  #
  # @else
  # @brief Bind of resolve the given name component
  # @endif
  def bindOrResolve(self, context, name_list, obj):
    try:
      context.bind_context(name_list, obj)
      return obj
    except CosNaming.NamingContext.AlreadyBound:
      obj = context.resolve(name_list)
      return obj
    return CORBA.Object._nil


  ##
  # @if jp
  #
  # @brief εβ³εγ³εγ¬ε¤―εβΉεγ°εΆ°ιπΊη±νεβΔε¥πεβ¤εγ³εγ²εΆΐεαήεΆ±π©£μ³ΊεαÒε£λ
  #
  # λμ®η®Τε΅υεβΈεΆ΅εβ³εγ³εγ¬ε¤―εβΉεγ°εΆ­κ±ΎεαΞεΆ¨ Contextεβ’ NameComponent εα§λμ®η®Τε΅υεβΈεΆ΅θΏΊι½®εα«
  # εγΐε¤¦εγ³εγ²ε΅ωεβ¶ε€‚
  # Context εαΈι©Ίεα®κΆ΄ιπ°εΆ±λφ°π¨Ύε¤µεγ³εγ¬ε¤―εβΉεγ°ε£ςντήθ―πεαΞεΆ¨εγΐε¤¦εγ³εγ²ε΅ωεβ¶ε€‚
  # ιπΈζΈ€ξ°®θ±ΰεα«λχΆεα«θ½ΜεΆ°π¨Άι΄ εαΈε¥πεβ¤εγ³εγ²θΈ°εΆΑεα®κΆ΄ιπ°εΆ±εΰΆθΞ¤κ―ΠεΆ°εγΐε¤¦εγ³εγ²θΈ°εΆΑπ¨Άι΄ εβ’
  # ιοΜηΎΞε΅ωεβ¶ε€‚
  #
  # @param self
  # @param context bind εβ¤ε΅χεαΎεΆ± resole κ±Ύπ³΅εβ³εγ³εγ¬ε¤―εβΉεγ
  # @param name_list εβ³εγ³εγ¬ε¤―εβΉεγ°εΆ­θ½Πε΅ρεβ¶ηΏνιιΊεΆ° NameComponent
  # @param new_context ρφΆρΰ£θ½Πε΅ρεβ²ε£μεβ‹ Context(εγ®ε¥υεβ©εγ«εγ°η€¤:None)
  #
  # @return NameComponent εα§λμ®η®Τε΅υεβΈεΆ΅θΏΊι½®εα«εγΐε¤¦εγ³εγ²ε΅υεβΈεΆ¨εα¨ε£λContext
  #
  # @else
  # @brief Bind of resolve the given name component
  # @endif
  def bindOrResolveContext(self, context, name_list, new_context=None):
    if new_context is None:
      new_cxt = self.newContext()
    else:
      new_cxt = new_context

    obj = self.bindOrResolve(context, name_list, new_cxt)
    return obj._narrow(CosNaming.NamingContext)


  ##
  # @if jp
  # @brief εγΊε¦Ύεγ εβµεγΌεγΐεΆ°ιπΊη±νεβΔη½φκΐΞε΅ωεβ‹
  #
  # πª­κ°Τε΅χεαήε¥νεγΌεγ εβµεγΌεγΐεΆ°ιπΊη±νεβΔη½φκΐΞε΅ωεβ¶ε€‚
  #
  # @param self
  #
  # @return εγΊε¦Ύεγ εβµεγΌεγΐεΆ°ιπΊη±ν
  #
  # @else
  # @brief Get the name of naming server
  # @endif
  def getNameServer(self):
    return self._nameServer


  ##
  # @if jp
  # @brief εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ°ε£ςιοΜηΎΞε΅ωεβ‹
  #
  # πª­κ°Τε΅χεαήε¥νεγΌεγ εβµεγΌεγΐεΆ°εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ°ε£ςιοΜηΎΞε΅ωεβ¶ε€‚
  #
  # @param self
  #
  # @return εγΊε¦Ύεγ εβµεγΌεγΐεΆ°εγ«εγΌεγ°ε¤µεγ³εγ¬ε¤―εβΉεγ
  #
  # @else
  # @brief Get the root context
  # @endif
  def getRootContext(self):
    return self._rootContext


  ##
  # @if jp
  # @brief εβªεγΜε¤Ίεβ§εβ―εγ°ε΅μεγΊε¦Ύεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅λιθ¤ιθ¥εαÒε£λ
  #
  # λμ®η®Τε΅χεαήκ¦Άι΄ εαΈε¥νεγΌεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅λιθ¤ιθ¥εαÒε£λ
  #
  # @param self
  # @param obj ιθ¤ιθ¥κ±Ύπ³΅π¨Άι΄ 
  #
  # @return ιθ¤ιθ¥ξ·ΐθΫό(εγΊε¦Ύεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ:trueεΰΆε΅ύεβΈζ»¥κ¦–:false)
  #
  # @else
  # @brief Whether the object is NamingContext
  # @endif
  def objIsNamingContext(self, obj):
    nc = obj._narrow(CosNaming.NamingContext)
    if CORBA.is_nil(nc):
      return False
    else:
      return True


  ##
  # @if jp
  # @brief θΊΌε΅θεβ²ε£μεαήηΏνιιΊε΅μεγΊε¦Ύεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅λεα©εα¬ε΅λιθ¤ιθ¥εαÒε£λ
  #
  # NameComponent εβ¤ε΅χεαΎεΆ±λφ®η­Ξη―χεα§λμ®η®Τε΅χεαήκ¦Άι΄ εαΈε¥νεγΌεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ°ε΅λ
  # ιθ¤ιθ¥εαÒε£λ
  #
  # @param self
  # @param name_list ιθ¤ιθ¥κ±Ύπ³΅
  #
  # @return ιθ¤ιθ¥ξ·ΐθΫό(εγΊε¦Ύεγήε¦µεβ°εβ³εγ³εγ¬ε¤―εβΉεγ:trueεΰΆε΅ύεβΈζ»¥κ¦–:false)
  #
  # @else
  # @brief Whether the given name component is NamingContext
  # @endif
  def nameIsNamingContext(self, name_list):
    return self.objIsNamingContext(self.resolve(name_list))


  ##
  # @if jp
  # @brief εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°εΆ°ργ¨ιθ¬ε£ςπΑΘε΅ω
  #
  # λμ®η®Τε΅υεβΈεΆ΅ξ±¨ηΦ΄εα®εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°ε£ςιοΜηΎΞε΅ωεβ¶ε€‚
  # ξ·¤ζΊ¬ζ½Ίι½®εαΈθ·ηκ°Τε΅υεβΈεΆ¨εα¨εΆ¬εα¨η ΄ιπ°εΆ±εΰΆθΧΰκΐΈεΆ°π¨Άι΄ εβΔλÒ¦εα¨εΆ΅εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ
  # εβΔκΏΘε΅ωεΰ‚
  #
  # @param self
  # @param name_list μ¦Ψι΄Άκ±Ύπ³΅NameComponent
  # @param begin ιοΜηΎΞι―¨ηΦ΄ρφ¶η§¶ζ½Ίι½®
  # @param end ιοΜηΎΞι―¨ηΦ΄ξ·¤ζΊ¬ζ½Ίι½®(εγ®ε¥υεβ©εγ«εγ°η€¤:None)
  #
  # @return NameComponent ιοΜηΎΞιµΐθΫό
  #
  # @else
  # @brief Get subset of given name component
  # @endif
  def subName(self, name_list, begin, end = None):
    if end is None or end < 0:
      end = len(name_list) - 1

    sub_len = end - (begin -1)
    objId = ""
    kind  = ""
    
    sub_name = []
    for i in range(sub_len):
      sub_name.append(name_list[begin + i])

    return sub_name


  ##
  # @if jp
  # @brief εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°εΆ°λφ®η­Ξη―χπ£¨νοΎεβΔη½φκΐΞε΅ωεβ‹
  #
  # λμ®η®Τε΅χεαήι―¨ηΦ΄εα®εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°εΆ°λφ®η­Ξη―χπ£¨νοΎεβΔη½φκΐΞε΅ωεβ¶ε€‚
  # λφ®η­Ξη―χπ£¨νοΎεα―εΰ΅―ameComponentεα®μ©¶θ―πεα·άNc[0],Nc[1],Nc[2]ώΏ¥ώΏ¥ώΏ¥}εα®κΆ΄ιπ°ε€
  #   Nc[0]id.Nc[0].kind/Nc[1]id.Nc[1].kind/Nc[2].id/Nc[2].kindώΏ¥ώΏ¥ώΏ¥
  # εα¨εα¨ε΅ζκΏΆκΎΎεΆ©ιοΜηΎΞεΆ©εαΊε£λεΰ‚
  # ιοΜηΎΞε΅χεαήθΛηκ―Ξη―χεα®ρυ·εαΚε΅μλμ®η®Τε΅χεαήλΚΉεαΚζ»¥θΊ΄εΆ°κΆ΄ιπ°εΆ±εΰ
  # λμ®η®Τε΅χεαήλΚΉεαΚεΆ©ιθ®ε£κλν¨εα¦εβ²ε£μεβ¶ε€‚
  #
  # @param self
  # @param name_list ιοΜηΎΞη―Ύπ³΅NameComponent
  # @param string_name ιοΜηΎΞιµΐθΫόλφ®η­Ξη―χ
  # @param slen ιοΜηΎΞη―Ύπ³΅λφ®η­Ξη―χλό€κ¦§ιΰ¤
  #
  # @else
  # @brief Get string representation of name component
  # @endif
  def nameToString(self, name_list, string_name, slen):
    for i in range(len(name_list)):
      for id_ in name_list[i].id:
        if id_ == "/" or id_ == "." or id_ == "\\":
          string_name[0] += "\\"
        string_name[0] += id_

      if name_list[i].id == "" or name_list[i].kind != "":
        string_name[0] += "."

      for kind_ in name_list[i].kind:
        if kind_ == "/" or kind_ == "." or kind_ == "\\":
          string_name[0] += "\\"
        string_name[0] += kind_

      string_name[0] += "/"


  ##
  # @if jp
  # @brief εγΊε¦Ύεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°εΆ°λφ®η­Ξη―χπ£¨νοΎλω¤εΆ°λφ®η­ΞλΚΉεβΔη½φκΐΞε΅ωεβ‹
  #
  # λμ®η®Τε΅χεαήε¥νεγΌεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°ε£ςλφ®η­Ξη―χεα§π£¨νοΎεαΞεΆ΅κΆ΄ιπ°εΆ°ρυ·εαΚε£ςιοΜηΎΞε΅ωεβ¶ε€‚
  # λφ®η­Ξη―χπ£¨νοΎεα―εΰ΅―ameComponentεα®μ©¶θ―πεα·άNc[0],Nc[1],Nc[2]εγ»εγ»εγ»}εα®κΆ΄ιπ°ε€
  #   Nc[0]id.Nc[0].kind/Nc[1]id.Nc[1].kind/Nc[2].id/Nc[2].kindεγ»εγ»εγ»
  # εα¨εα¨ε΅ζκΏΆκΎΎεΆ©ιοΜηΎΞεΆ©εαΊε£λεΰ‚
  #
  # @param self
  # @param name_list ιοΜηΎΞη―Ύπ³΅NameComponent
  #
  # @return λμ®η®Τε΅χεαήε¥νεγΌεγ εβ³εγ³εγΪε¦ΎεγΊε¦µεγ°εΆ°λφ®η­Ξη―χρυ·εα•
  #
  # @else
  # @brief Get string length of the name component's string representation
  # @endif
  def getNameLength(self, name_list):
    slen = 0

    for i in range(len(name_list)):
      for id_ in name_list[i].id:
        if id_ == "/" or id_ == "." or id_ == "\\":
          slen += 1
        slen += 1
      if name_list[i].id == "" or name_list[i].kind == "":
        slen += 1

      for kind_ in name_list[i].kind:
        if kind_ == "/" or kind_ == "." or kind_ == "\\":
          slen += 1
        slen += 1

      slen += 1

    return slen


  ##
  # @if jp
  # @brief λφ®η­Ξη―χεα®ιθ¬η²΄
  #
  # λφ®η­Ξη―χεβΔθ·ηκ°Τε΅χεαήε¥ηεγªεγήε¤Αεα§ιθ¬η²΄εαÒε£λεΰ‚
  #
  # @param self
  # @param input ιθ¬η²΄κ±Ύπ³΅λφ®η­Ξη―χ
  # @param delimiter ιθ¬η²΄ντ¨εγ®ε¦¬εγήε¤Α
  # @param results ιθ¬η²΄ξ·ΐθΫό
  #
  # @return ιθ¬η²΄εαΞεΆ΅λφ®η­Ξη―χεα®π¨Άι΄ λυ°
  #
  # @else
  # @brief Split of string
  # @endif
  def split(self, input, delimiter, results):
    delim_size = len(delimiter)
    found_pos = begin_pos = pre_pos = substr_size = 0

    if input[0:delim_size] == delimiter:
      begin_pos = pre_pos = delim_size

    while 1:
      found_pos = string.find(input[begin_pos:],delimiter)
      
      if found_pos == -1:
        results.append(input[pre_pos:])
        break

      if found_pos > 0 and input[found_pos - 1] == "\\":
        begin_pos += found_pos + delim_size
      else:
        substr_size = found_pos + (begin_pos - pre_pos)
        if substr_size > 0:
          results.append(input[pre_pos:(pre_pos+substr_size)])
        begin_pos += found_pos + delim_size
        pre_pos   = begin_pos

    return len(results)
