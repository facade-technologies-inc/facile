"""
..
	/------------------------------------------------------------------------------\
	|                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
	|------------------------------------------------------------------------------|
	|                                                                              |
	|    Copyright [2019] Facade Technologies Inc.                                 |
	|    All Rights Reserved.                                                      |
	|                                                                              |
	| NOTICE:  All information contained herein is, and remains the property of    |
	| Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
	| and technical concepts contained herein are proprietary to Facade            |
	| Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
	| Patents, patents in process, and are protected by trade secret or copyright  |
	| law.  Dissemination of this information or reproduction of this material is  |
	| strictly forbidden unless prior written permission is obtained from Facade   |
	| Technologies Inc.                                                            |
	|                                                                              |
	\------------------------------------------------------------------------------/
	
This module contains the **Action** class which serves as the base class to the *ComponentAction*
and *ActionPipeline* classes.
"""

from typing import List

import data.apim.port as pt
from data.entity import Entity
from data.properties import Properties


class ActionException(Exception):
	def __init__(self, msg: str):
		Exception.__init__(self, msg)


class Action(Entity):
	
	allPorts = set()
	
	def __init__(self):
		"""
		The **Action** class is the abstract base class of all types of actions.
		It stores all of the common functionality of the derived classes.
		
		The Action class is responsible for managing ports. Actions can have any number of
		inputs and outputs. Each input and output is a port. A single port instance cannot be
		both an input and an output, nor can it be shared between actions.
		
		The action class maintains a set of all ports to prevent misuse of ports.
		
		Each action instance also maintains a list of action wrappers.
		"""
		super().__init__()
		
		predefinedCategories = ["Base", "Action"]
		customCategories = {}
		props = Properties.createPropertiesObject(predefinedCategories, customCategories)
		self.setProperties(props)
		props.getProperty("ID")[1].setValue(self.getId())
		props.getProperty("Type")[1].setValue(type(self).__name__)

		# inputs and outputs are lists of ports.
		self._inputs = []
		self._outputs = []
		
		self._wrappers = set()
		
	def setName(self, name:str) -> None:
		"""
		Sets the name of the action and makes sure the change propagates to all wrappers
		
		:return: None
		:rtype: NoneType
		"""
		Entity.setName(self, name)
		for wrapper in self._wrappers:
			Entity.setName(wrapper, name)
		
	def addInputPort(self, port: 'pt.Port') -> None:
		"""
		Adds a port to the list of inputs for this action.
		
		The port may have wires connected to it when added, but it is not recommended.
		The port instance cannot be used anywhere else.
		
		:raises: PortException if the port is used elsewhere.
		
		:param port: The new port to be added.
		:type port: Port
		:return: None
		:rtype: NoneType
		"""
		if port in Action.allPorts:
			raise pt.PortException("Port is already used. Can't add port to action.")
		
		port.setAction(self)
		
		Action.allPorts.add(port)
		self._inputs.append(port)
		self.synchronizeWrappers()
		self.triggerUpdate()
	
	def addOutputPort(self, port: 'pt.Port') -> None:
		"""
		Adds a port to the list of outputs for this action.
		
		The port may have wires connected to it when added, but it is not recommended.
		The port instance cannot be used anywhere else.
		
		:raises: PortException if the port is used elsewhere.
		
		:param port: The new port to be added.
		:type port: Port
		:return: None
		:rtype: NoneType
		"""
		if port in Action.allPorts:
			raise pt.PortException("Port is already used. Can't add port to action.")
		
		port.setAction(self)
		
		Action.allPorts.add(port)
		self._outputs.append(port)
		self.synchronizeWrappers()
		self.triggerUpdate()
		
	def getInputPorts(self) -> List['pt.Port']:
		"""
		Get the list of input ports for this action.
		
		:return: The list of input ports for this action
		:rtype: List[Port]
		"""
		return self._inputs[:]
		
	def getOutputPorts(self) -> List['pt.Port']:
		"""
		Get the list of output ports for this action.

		:return: The list of output ports for this action
		:rtype: List[Port]
		"""
		return self._outputs[:]
	
	def removePort(self, port: 'pt.Port') -> bool:
		"""
		Removes a port from this action - no need to specify input or output.

		Removing the port from the action does not destroy the port. The caller should take
		special care to remove any wires if desired.

		:raises: PortException if the port is not found.

		:param port: The port instance to be removed.
		:type port: Port
		:return: True if the port was successfully removed, False otherwise.
		:rtype: bool
		"""
		
		if port not in Action.allPorts:
			raise pt.PortException("Port not found in any actions.")
		
		found = False
		if port in self._inputs:
			found = True
			self._inputs.remove(port)
		elif port in self._outputs:
			found = True
			self._outputs.remove(port)
		else:
			raise pt.PortException("Port not found in this action.")
			
		if found:
			Action.allPorts.remove(port)
			port.setAction(None)
		
		self.synchronizeWrappers()
		self.triggerUpdate()
		return found

	def registerWrapper(self, wrapper: 'ActionWrapper') -> None:
		"""
		Register an action wrapper with this action.
		
		:raises: ActionException if the wrapper does not store a reference to this action.
		
		:return: None
		:rtype: NoneType
		"""
		
		if wrapper.getActionReference() is not self:
			raise ActionException("The ActionWrapper must reference this action for this action to "
			                      "reference it.")
		
		self._wrappers.add(wrapper)
		
	def unRegisterWrapper(self, wrapper: 'ActionWrapper') -> None:
		"""
		Un-register an action wrapper with this action.
		
		To maintain synchronized two-way references, the wrapper is required to forget about this
		action before this action can un-register it.
		
		:raises: ActionException if the wrapper is not registered with this action already.
		:raises: ActionException if the wrapper still references this action
		
		:param wrapper: The ActionWrapper to unregister.
		:return: None
		"""
		
		if wrapper not in self._wrappers:
			raise ActionException("Cannot unregister a wrapper that is not registered with this action.")
		
		if wrapper.getActionReference() is self:
			raise ActionException("The Wrapper must forget about the action before the action can forget about the wrapper.")
		
		self._wrappers.remove(wrapper)
		
	def synchronizeWrappers(self) -> None:
		"""
		Synchronizes all wrappers. This function should be called from any function that edits
		the ports of the action.
		
		:return: None
		:rtype: NoneType
		"""
		
		for wrapper in self._wrappers:
			wrapper.synchronizePorts()

	def getMethodSignature(self) -> str:
		"""
		Gives the signature for a method using its name and parameter list. Newline at end.

		:return: Method Signature
		:rtype: str
		"""

		name = self.getMethodName()
		params = self.getParamStr()
		output = "\tdef " + name + "(self" + params + ") -> " + self.getRType() + ":\n"
		return output

	def getRType(self) -> str:
		"""
		Gives str with return type(s), explicitly made for making the method signature.

		:return: return type(s) of the action
		:rtype: str
		"""

		if len(self._outputs) > 1:
			out = '('
			work = []
			for o in self._outputs:
				work.insert(0, o.getDataTypeStr())
			out += work.pop()
			for w in work:
				out += ', ' + work.pop()
			out += ')'
			return out
		elif len(self._outputs) == 1:
			return self._outputs[0].getDataTypeStr()
		else:
			return 'None'

	def getMethodName(self) -> None:
		"""
		Must be overwritten in children classes; raises exception here if not.
		"""
		
		raise ActionException("getMethodName() must be defined in the action type's class.")

	def getParamStr(self) -> str:
		"""
		Generates the string of inputs needed for the action's method definition

		:return: list of parameters needed for the action, starting with a ", ".
		:rtype: str
		"""

		out = ""
		for p in self._inputs:
			out += ", " + p.getName() + ": " + p.getDataTypeStr()
			# If we eventually provide functionality for defaulting values, use this:
			# if p.hasDefault():
			# 	out += " = " + p.getDefaultVal()

		return out

	def getDocStr(self) -> str:
		"""
		Must be overwritten in children classes; raises exception here if not.
		"""
		raise ActionException("getDocStr() must be called from the action type's class.")

	def getMethodCode(self):
		"""
		Must be overwritten in children classes; raises exception here if not.
		"""
		raise ActionException("getMethodCode() must be defined in the action type's class.")

	def getMethod(self) -> str:
		"""
		Generates the entirety of the code needed for the action, including spacing afterwards.

		:return: callable definition (method) that performs the action if executed
		:rtype: str
		"""

		code = self.getMethodSignature()
		code += self.getDocStr()
		code += self.getMethodCode()
		code += '\n'

		return code