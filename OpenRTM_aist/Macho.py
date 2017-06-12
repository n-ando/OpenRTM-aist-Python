#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Macho.py
# @brief The Machine Objects class library
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
#
# Copyright (C) 2017
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.





class _EmptyBox:
  def __init__(self):
    pass

_EmptyBox.theEmptyBox = _EmptyBox()




class _KeyData:
  def __init__(self):
    self.instanceGenerator = None
    self.childPredicate = None
    self.name = None
    self.id = 0


class _StateSpecification(object):
  def __init__(self, instance):
    self._myStateInstance = instance
  def isChild(key):
    return False
  isChild = staticmethod(isChild)

  def setState(self, S):
    global _theDefaultInitializer
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _theDefaultInitializer)
    
  def setState1(self,S,p1):
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _Initializer1(p1))
    
  def setState2(self,S,p1,p2):
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _Initializer2(p1,p2))
  def setState3(self,S,p1,p2,p3):
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _Initializer3(p1,p2,p3))
  def setState4(self,S,p1,p2,p3,p4):
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _Initializer4(p1,p2,p3,p4))
  def setState5(self,S,p1,p2,p3,p4,p5):
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _Initializer5(p1,p2,p3,p4,p5))
  def setState6(self,S,p1,p2,p3,p4,p5,p6):
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _Initializer6(p1,p2,p3,p4,p5,p6))
  def setStateHistory(self, S):
    global _theHistoryInitializer
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.setPendingState(instance, _theHistoryInitializer)
  def setStateAlias(self,state):
    state.setState(self._myStateInstance.machine())
  def setStateBox(self, SUPERSTATE, S, box=None):
    global _theDefaultInitializer
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, SUPERSTATE, S)
    m.myPendingBox = box
    m.setPendingState(instance, _theDefaultInitializer)
  def setStateDirect(self, S, box=None):
    global _theDefaultInitializer
    m = self._myStateInstance.machine()
    instance = S._getInstance(m, S.SUPER, S)
    m.myPendingBox = box
    m.setPendingState(instance, _theDefaultInitializer)
  def _restore(self, current):
    self._myStateInstance.machine().myCurrentState = current
  def setStateCurrent(self, current):
    global _theDefaultInitializer
    self._myStateInstance.machine().setPendingState(current, _theDefaultInitializer)
  def _shutdown(self):
    self._myStateInstance.machine().shutdown()
  def _setHistorySuper(self, instance, deep):
    pass
  def exit(self):
    pass
  def entry(self):
    pass
  def init(self):
    pass
  def _getInstance(machine, S=None, C=None):
    instance = machine.getInstances()
    if not instance[0]:
      instance[0] = _RootInstance(machine, 0)
    return instance[0]
  _getInstance = staticmethod(_getInstance)
  def _deleteBox(self, instance):
    pass
  def _saveHistory(self, instance, shallow, deep):
    pass








class Link(_StateSpecification):
  def __init__(self, instance):
    super(Link,self).__init__(instance)
    self.super_obj = self.SUPER(self.SUPER._getInstance(instance.machine(), self.SUPER.SUPER, self.SUPER))
    
    #super_class.__init__(self, instance)
    #self.SUPER.__init__(self, self.SUPER._getInstance(instance.machine()))
    self._myStateInstance = instance
  def key(instance):
    k = _KeyData()
    k.instanceGenerator = Link._getInstance
    k.childPredicate = Link.isChild
    k.name = instance.SUPER._state_name()
    k.id = instance.SUPER.StateID
    return k
  key = staticmethod(key)
  def alias():
    return Alias(Link.key(self))
  alias = staticmethod(alias)
  def isChild(other, SUPER):
    return Link.key(self) == other or SUPER.isChild(other)
  isChild = staticmethod(isChild)
  def isParent(other):
    return other.childPredicate(Link.key(self))
  isParent = staticmethod(isParent)
  def isCurrent(machine):
    return machine.currentState().isChild(Link.key(self))
  isCurrent = staticmethod(isCurrent)
  def isCurrentDirect(machine):
    return Link.key(self) == machine.currentState()
  isCurrentDirect = staticmethod(isCurrentDirect)
  def clearHistory(machine, StateID):
    instance = machine.getInstance(StateID)
    if instance:
      instance.setHistory(0)
  clearHistory = staticmethod(clearHistory)
  def clearHistoryDeep(machine, StateID):
    instance = machine.getInstance(StateID)
    if instance:
      instance.clearHistoryDeep(Machine.theStateCount,instance)
  clearHistoryDeep = staticmethod(clearHistoryDeep)
  def history(machine, StateID):
    instance = machine.getInstance(StateID)
    history = 0
    if instance:
      history = instance.history()
    if history:
      return history.key()
    else:
      return Link.key(self)
  history = staticmethod(history)
  def entry(self):
    pass
  def init(self):
    pass
  def exit(self):
    pass
  def _box(self):
    
    return self._myStateInstance.box()
  def _getInstance(machine, S, C):
    
    instance = machine.getInstances()
    
    if not instance[C.StateID]:
      instance[C.StateID] = _SubstateInstance(machine, S._getInstance(machine, S.SUPER, S), C)
    return instance[C.StateID]
  _getInstance = staticmethod(_getInstance)
  def _deleteBox(self, instance):
    instance.deleteBox()
  def _saveHistory(self,instance,shallow,deep):
    self._setHistorySuper(instance,deep)
  def __getitem__(self, class_):
    obj = self
    while hasattr(obj, "super_obj"):
      obj = obj.super_obj
      
      if isinstance(class_, str):
        if obj.__class__.__name__ == class_:
          return obj
      elif type(obj) == class_:
        return obj
      
    return None
    


class StateID:
  def __init__(self):
    pass
  value = 0

class _StateInstance(object):
  def __init__(self, machine, parent):
    self.myMachine = machine
    self.mySpecification = None
    self.myHistory = None
    self.myParent = parent
    
    self.myBox = None
    self.myBoxPlace = None
  def entry(self,previous,first=True):
    if not self.myParent:
      return
    if first or not previous.isChild(self):
      self.myParent.entry(previous,False)
      self.createBox()
      self.mySpecification.entry()
  def exit(self,next):
    
    if not self.myParent:
      return
    
    if self is next or not next.isChild(self):
      self.mySpecification.exit()
      if self.myBox is not _EmptyBox.theEmptyBox:
        self.mySpecification._deleteBox(self)
      self.myParent.exit(next)
      

  def init(self, history):
    global _theDefaultInitializer
    if history and self.myHistory:
      self.myMachine.setPendingState(self.myHistory, _theDefaultInitializer)
    else:
      self.mySpecification.init()
    self.myHistory = None
    
      
  def entry_next(self,next):
    pass
  def entry_history(self,history):
    pass
  def saveHistory(self,shallow,deep):
    self.mySpecification._saveHistory(self, shallow, deep)
  def setHistorySuper(self, deep):
    if self.myParent:
      self.myParent.saveHistory(self, deep)
  def copy(self, original):
    if original.myHistory:
      history = self.myMachine.getInstance(original.myHistory.id())
      self.setHistory(history)
    if original.myBox:
      self.cloneBox(original.myBox)
  def clone(self, newMachine):
    parent = None
    if self.myParent:
      parent = newMachine.createClone(self.myParent.id(), self.myParent)
    clone = self.create(newMachine, parent)
      
  def shutdown(self):
    self.mySpecification._shutdown()
  def restore(self, instance):
    self.mySpecification._restore(instance)
  def id(self):
    pass
  def key(self):
    pass
  def name(self):
    pass
  def create(self, machine, parent):
    pass
  def createBox(self):
    pass
  def deleteBox(self):
    pass
  def cloneBox(self,box):
    pass
  def setBox(self,box):
    if self.myBoxPlace:
      self.myBoxPlace = None
    self.myBox = box
  def isChild(self,instance):
    
    return self==instance or (self.myParent and self.myParent.isChild(instance))
  def specification(self):
    return self.mySpecification
  def box(self):
    return self.myBox
  def machine(self):
    return self.myMachine
  def setHistory(self,history):
    self.myHistory = history
  def getHistory(self):
    return self.self.myHistory
  

class _RootInstance(_StateInstance):
  def __init__(self, machine, parent):
    super(_RootInstance,self).__init__(machine, parent)
    self.mySpecification = _StateSpecification(self)
  def id(self):
    return 0
  def key(self):
    return 0
  def createBox(self):
    pass
  def deleteBox(self):
    pass
  def cloneBox(self, box):
    pass
  def name(self):
    return "Root"
  def create(self, machine, parent):
    return _RootInstance(machine,parent)

class _SubstateInstance(_StateInstance):
  def __init__(self, machine, parent, super_class):
    super(_SubstateInstance, self).__init__(machine, parent)
    self.mySpecification = super_class(self)
    
    self.SUPER = super_class
  def __del__(self):
    if self.myBox:
      _deleteBox(self.myBox,self.myBoxPlace)
  def id(self):
    return self.SUPER.StateID
  def key(self):
    return self.SUPER.key(self)
  def create(self, machine, parent):
    _SubstateInstance(machine, parent, self.SUPER)
  def createBox(self):
    if not self.myBox:
      if hasattr(self.SUPER, "Box"):
        self.myBox = _createBox(self.myBoxPlace,self.SUPER.Box)
      else:
        self.myBox = _createBox(self.myBoxPlace)
  def deleteBox(self):
    _deleteBox(self.myBox,self.myBoxPlace)
  def cloneBox(self, box):
    self.myBox = _cloneBox(box)

class _IEventBase:
  def __init__(self):
    pass
  def dispatch(self, instance):
    pass

class IEvent(_IEventBase):
  def __init__(self):
    pass

class _Event6(IEvent):
  def __init__(self, handler, p1, p2, p3, p4, p5, p6):
    self.myHandler = handler
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
    self.myParam4 = p4
    self.myParam5 = p5
    self.myParam6 = p6
  def dispatch(self, instance):
    behaviour = instance.specification()
    getattr(behaviour,self.myHandler)(self.myParam1,self.myParam2,self.myParam3,self.myParam4,self.myParam5,self.myParam6)

class _Event5(IEvent):
  def __init__(self, handler, p1, p2, p3, p4, p5):
    self.myHandler = handler
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
    self.myParam4 = p4
    self.myParam5 = p5
  def dispatch(self, instance):
    behaviour = instance.specification()
    getattr(behaviour,self.myHandler)(self.myParam1,self.myParam2,self.myParam3,self.myParam4,self.myParam5)




class _Event4(IEvent):
  def __init__(self, handler, p1, p2, p3, p4):
    self.myHandler = handler
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
    self.myParam4 = p4
  def dispatch(self, instance):
    behaviour = instance.specification()
    getattr(behaviour,self.myHandler)(self.myParam1,self.myParam2,self.myParam3,self.myParam4)



class _Event3(IEvent):
  def __init__(self, handler, p1, p2, p3):
    self.myHandler = handler
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
  def dispatch(self, instance):
    behaviour = instance.specification()
    getattr(behaviour,self.myHandler)(self.myParam1,self.myParam2,self.myParam3)



class _Event2(IEvent):
  def __init__(self, handler, p1, p2):
    self.myHandler = handler
    self.myParam1 = p1
    self.myParam2 = p2
  def dispatch(self, instance):
    behaviour = instance.specification()
    getattr(behaviour,self.myHandler)(self.myParam1,self.myParam2)




class _Event1(IEvent):
  def __init__(self, handler, p1):
    self.myHandler = handler
    self.myParam1 = p1
  def dispatch(self, instance):
    behaviour = instance.specification()
    getattr(behaviour,self.myHandler)(self.myParam1)



class _Event0(IEvent):
  def __init__(self, handler):
    self.myHandler = handler
  def dispatch(self, instance):
    behaviour = instance.specification()
    
    getattr(behaviour,self.myHandler)()



def Event6(R,p1,p2,p3,p4,p5,p6):
  return _Event6(R,p1,p2,p3,p4,p5,p6)


def Event5(R,p1,p2,p3,p4,p5):
  return _Event5(R,p1,p2,p3,p4,p5)

def Event4(R,p1,p2,p3,p4):
  return _Event4(R,p1,p2,p3,p4)

def Event3(R,p1,p2,p3):
  return _Event3(R,p1,p2,p3)

def Event2(R,p1,p2):
  return _Event2(R,p1,p2)

def Event1(R,p1):
  return _Event1(R,p1)

def Event0(R):
  return _Event0(R)


def execute1(instance, p1):
  behaviour = instance.specification()
  behaviour.init(p1)

def execute2(instance, p1, p2):
  behaviour = instance.specification()
  behaviour.init(p1, p2)

def execute3(instance, p1, p2, p3):
  behaviour = instance.specification()
  behaviour.init(p1, p2, p3)

def execute4(instance, p1, p2, p3, p4):
  behaviour = instance.specification()
  behaviour.init(p1, p2, p3, p4)

def execute5(instance, p1, p2, p3, p4, p5):
  behaviour = instance.specification()
  behaviour.init(p1, p2, p3, p4, p5)

def execute6(instance, p1, p2, p3, p4, p5, p6):
  behaviour = instance.specification()
  behaviour.init(p1, p2, p3, p4, p5, p6)
  

class _Initializer:
  def __init__(self):
    pass
  def clone(self):
    pass
  def destroy(self):
    pass
  def adapt(self, key):
    return key
  def execute(self, instance):
    pass

class _StaticInitializer(_Initializer):
  def __init__(self):
    pass
  def clone(self):
    return self
  def destroy(self):
    pass


class _DefaultInitializer(_StaticInitializer):
  def __init__(self):
    pass
  def execute(self, instance):
    instance.init(False)




class _HistoryInitializer(_StaticInitializer):
  def __init__(self):
    pass
  def execute(self, instance):
    instance.init(True)


class _AdaptingInitializer(_Initializer):
  def __init__(self, machine):
    self.myMachine = machine
  def execute(self, instance):
    instance.init(False)
  def clone(self):
    return _AdaptingInitializer(self.myMachine)
  def adapt(self, key):
    id = key.id
    instance = self.myMachine.getInstance(id)
    history = None
    if instance:
      history = instance.history()
    if history:
      return history.key()
    else:
      return key


class _Initializer1(_Initializer):
  def __init__(self, p1):
    self.myParam1 = p1
  def clone(self):
    return _Initializer1(self.myParam1)
  def execute(self, instance):
    execute1(instance, self.myParam1)


class _Initializer2(_Initializer):
  def __init__(self, p1, p2):
    self.myParam1 = p1
    self.myParam2 = p2
  def clone(self):
    return _Initializer2(self.myParam1,self.myParam2)
  def execute(self, instance):
    execute2(instance, self.myParam1,self.myParam2)



class _Initializer3(_Initializer):
  def __init__(self, p1, p2, p3):
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
  def clone(self):
    return _Initializer3(self.myParam1,self.myParam2,self.myParam3)
  def execute(self, instance):
    execute3(instance, self.myParam1,self.myParam2,self.myParam3)




class _Initializer4(_Initializer):
  def __init__(self, p1, p2, p3, p4):
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
    self.myParam4 = p4
  def clone(self):
    return _Initializer4(self.myParam1,self.myParam2,self.myParam3,self.myParam4)
  def execute(self, instance):
    execute4(instance, self.myParam1,self.myParam2,self.myParam3,self.myParam4)




class _Initializer5(_Initializer):
  def __init__(self, p1, p2, p3, p4, p5):
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
    self.myParam4 = p4
    self.myParam5 = p5
  def clone(self):
    return _Initializer5(self.myParam1,self.myParam2,self.myParam3,self.myParam4,self.myParam5)
  def execute(self, instance):
    execute5(instance, self.myParam1,self.myParam2,self.myParam3,self.myParam4,self.myParam5)






class _Initializer6(_Initializer):
  def __init__(self, p1, p2, p3, p4, p5, p6):
    self.myParam1 = p1
    self.myParam2 = p2
    self.myParam3 = p3
    self.myParam4 = p4
    self.myParam5 = p5
    self.myParam6 = p6
  def clone(self):
    return _Initializer6(self.myParam1,self.myParam2,self.myParam3,self.myParam4,self.myParam5,self.myParam6)
  def execute(self, instance):
    execute6(instance, self.myParam1,self.myParam2,self.myParam3,self.myParam4,self.myParam5,self.myParam6)



_theDefaultInitializer = _DefaultInitializer()
_theHistoryInitializer = _HistoryInitializer()



class _MachineBase(object):
  def __init__(self):
    self.myCurrentState = None
    self.myPendingState = None
    self.myPendingInit = None
    self.myPendingBox = None
    self.myPendingEvent = None
    self.myInstances = None
  def currentState(self):
    return self.myCurrentState.key()
  def setState(self, instance, init):
    self.setPendingState(instance, init)
    self.rattleOn()
  def setStateAlias(self, state):
    state.setState(self)
    self.rattleOn()
  def setPendingState(self, instance, init):
    self.myPendingState = instance
    self.myPendingInit = init
  def setPendingEvent(self, event):
    self.myPendingEvent = event
  def rattleOn(self):
    while self.myPendingState or self.myPendingEvent:
      while self.myPendingState:
        
        self.myCurrentState.exit(self.myPendingState)
        self.myCurrentState.setHistorySuper(self.myCurrentState)
        previous = self.myCurrentState
        
        self.myCurrentState = self.myPendingState
        if self.myPendingBox:
          self.myCurrentState.setBox(self.myPendingBox)
          self.myPendingBox = None
        
        
        self.myCurrentState.entry(previous)
        self.myPendingState = None
        self.myPendingInit.execute(self.myCurrentState)
        
      if self.myPendingEvent:
        event = self.myPendingEvent
        self.myPendingEvent = None
        event.dispatch(self.myCurrentState)
    self.myPendingInit = None
  def getInstances(self):
    return self.myInstances
  def start(self, instance):
    global _theDefaultInitializer
    self.myCurrentState = _StateSpecification._getInstance(self)
    self.setState(instance, _theDefaultInitializer)
  def startAlias(self, state):
    self.myCurrentState = _StateSpecification._getInstance(self)
    self.setStateAlias(state)
  def shutdown(self):
    global _theDefaultInitializer
    self.setState(_StateSpecification._getInstance(self), _theDefaultInitializer)
    self.myCurrentState = None
  def allocate(self, count):
    
    self.myInstances = [None]*count
    
  def free(self, count):
    i = count
    while i > 0:
      i -=1
      self.myInstances[i] = None
    
  def clearHistoryDeep(self, count, instance):
    for i in range(count):
      s = self.myInstances[i]
      if s and s.isChild(instance):
        s.setHistory(0)
  def copy(self, other, count):
    for i in range(count):
      state = self.myInstances[i]
      if state:
        state.copy(other[i])
  def createClone(self, id, original):
    clone = self.getInstances
    if not clone[id] and original:
      clone[id] = original.clone(self)
    return clone[id]


class Alias:
  def __init__(self):
    self.myInitializer = None
    self.myStateKey = 0
  def __del__(self):
    self.myInitializer.destroy()
  def init_history(self, key, history=False):
    global _theHistoryInitializer
    global _theDefaultInitializer
    self.myStateKey = key
    if history:
      self.myInitializer = _theHistoryInitializer
    else:
      self.myInitializer = _theDefaultInitializer
  def init_Initializer(self, key, init):
    self.myStateKey = key
    self.myInitializer = init
  def init_Alias(self, other):
    self.myStateKey = key
    self.myInitializer = other.myInitializer.clone()
  def equal(self, other):
    if self is other:
      return self
    self.myInitializer.destroy()
    self.myStateKey = other.childPredicate
    self.myInitializer = other.childPredicate

  def Key(self):
    return self.key()
  def isChild(self, k):
    return self.key().childPredicate(k)
  def isParent(self, k):
    return self.key().childPredicate(k)
  def name(self):
    return self.key().name()
  def id(self):
    return self.key().id
  def key(self):
    return self.myInitializer.adapt(self.myStateKey)
  def setState(self, machine):
    machine.setPendingState(self.key().instanceGenerator(machine), self.myInitializer.clone())


def State(S):
  return Alias(S.key())

def State1(S,p1):
  return Alias(S.key(), _Initializer1(p1))

def State2(S,p1,p2):
  return Alias(S.key(), _Initializer2(p1,p2))


def State3(S,p1,p2,p3):
  return Alias(S.key(), _Initializer3(p1,p2,p3))


def State4(S,p1,p2,p3,p4):
  return Alias(S.key(), _Initializer4(p1,p2,p3,p4))


def State5(S,p1,p2,p3,p4,p5):
  return Alias(S.key(), _Initializer5(p1,p2,p3,p4,p5))


def State6(S,p1,p2,p3,p4,p5,p6):
  return Alias(S.key(), _Initializer6(p1,p2,p3,p4,p5,p6))


def StateHistory(S, machine):
  return Alias(S.key(), _AdaptingInitializer(machine))


class Snapshot(_MachineBase):
  def __init__(self, machine):
    super(Snapshot,self).__init__()
    self.allocate(Machine.theStateCount)
    self.copy(machine.myInstances, Machine.theStateCounta)
    self.myCurrentState = self.getInstances[machine.myCurrentState.id()]
    
  def __del__(self):
    self.free(Machine.theStateCount)

class AfterAdvice:
  def __init__(self, m):
    self.myMachine = m
  def __del__(self):
    pass
    #self.myMachine.rattleOn()
  def __call__(self, func, *args):
    spec = self.myMachine.myCurrentState.specification()
    ret = getattr(spec,func)(*args)
    self.myMachine.rattleOn()
    return ret
    
    #return self.myMachine.myCurrentState.specification()
    
class Machine(_MachineBase):
  theStateCount = 1
  def __init__(self, TOP, TopBase):
    super(Machine,self).__init__()
    self.TOP = TOP
    self.TopBase = TopBase
  def __del__(self):
    pass
  def exit(self):
    self.myCurrentState.shutdown()
    self.free(Machine.theStateCount)
    Machine.theStateCount = 1
  def init(self, box=None):
    self.allocate(Machine.theStateCount)
    top = self.TOP._getInstance(self, self.TopBase, self.TOP)
    if box:
      top.setBox(box)
    self.start(top)
    
  def init_Alias(self, state, box=None):
    self.allocate(Machine.theStateCount)
    top = self.TOP._getInstance(self, self.TopBase, self.TOP)
    if box:
      top.setBox(box)
    self.start(state)
  def init_Snapshot(self, snapshot, box=None):
    self.allocate(Machine.theStateCount)
    self.copy(snapshot.myInstances, Machine.theStateCount)
  def equal(self, snapshot):
    self.myCurrentState.shutdown()
    self.free(Machine.theStateCount)
    self.copy(snapshot.myInstances, Machine.theStateCount)
    self.myCurrentState = self.getInstance(0)
    current = self.getInstance(snapshot.myCurrentState.id())
    current.restore(current)
    self.rattleOn()
    return self
  def __call__(self):
    return AfterAdvice(self)
  def dispatch(self, event, destroy=True):
    event.dispatch(self.myCurrentState)
    if destroy:
      del event
    self.rattleOn()

  def box(self):
    self.myCurrentState.specification().box()

  


  
    
def _createBox(place, B=None):
  if B:
    return B()
  else:
    return _EmptyBox.theEmptyBox


def _deleteBox(box, place):
  pass

def _cloneBox(other):
  return _EmptyBox.theEmptyBox


def TopBase(TOP):
  class TopBase_(_StateSpecification):
    SUPER = _StateSpecification
    StateID = 0
    def __init__(self, instance):
      super(TopBase_,self).__init__(instance)
      self.T = TOP
    def dispatch(self, event):
      self._myStateInstance.machine().setPendingEvent(event)
    def machine(self):
      return self._myStateInstance.machine()

  return TopBase_

  
def TOPSTATE(TOP):
  TOP.SUPER = TopBase(TOP)
  TOP.StateID = Machine.theStateCount
  Machine.theStateCount += 1
  TOP._state_name = staticmethod(lambda  : TOP.__name__)
  
  TOP.box = lambda self: self._box()
  

def SUBSTATE(STATE, SUPERSTATE):
  STATE.SUPER = SUPERSTATE
  STATE.StateID = Machine.theStateCount
  Machine.theStateCount += 1
  STATE._state_name = staticmethod(lambda : STATE.__name__)
  STATE.box = lambda self: self._box()

def DEEPHISTORY(STATE):
  def _saveHistory(self,instance,shallow,deep):
    instance.setHistory(deep)
    self[self.SUPER]._setHistorySuper(instance,deep)
    
  STATE._saveHistory = _saveHistory

  STATE._setHistorySuper = lambda self,instance,deep: instance.setHistorySuper(deep)

def HISTORY(STATE):
  def _saveHistory(self,instance,shallow,deep):
    instance.setHistory(deep)
    self[self.SUPER]._setHistorySuper(instance,deep)
    
  STATE._saveHistory = _saveHistory

  STATE._setHistorySuper = lambda self,instance,deep: instance.setHistorySuper(deep)

    