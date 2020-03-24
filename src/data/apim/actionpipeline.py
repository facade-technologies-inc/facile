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
	
This module contains the **ActionPipeline** class which describes a custom function
that will be created in the generated API.
"""

from typing import List

from data.apim.action import Action, ActionException
from data.apim.actionwrapper import ActionWrapper
import data.apim.port as pt
from data.apim.wireset import WireSet
from data.apim.wire import WireException

class ActionPipeline(Action):
	
	def __init__(self):
		"""
		ActionPipelines are an aggregation of ActionWrappers. The internals of the
		ActionPipeline can be connected with wires that carry data. The internal actions are
		executed in the sequence in with they are stored.
		"""
		Action.__init__(self)
		self._actions = []
		self._wireSet = WireSet()
		self._varName = 'a'
		self._varMap = []  # This stores (varName, port) tuples
	
	def addAction(self, action: 'ActionWrapper') -> None:
		"""
		Adds an *ActionWrapper* as an internal part of this action pipeline.
		
		This method does not check to see if the Action exists in another ActionPipeline,
		but the caller should avoid this as it would certainly be invalid.
		
		:raises: ActionException if the action is not a action wrapper
		:raises: ActionException if the wrapper has another parent already.
		:raises: ActionException if the wrapper is already in the action list
		
		:param action: The Action to add to this ActionPipeline.
		:type action: Action
		:return: None
		:rtype: NoneType
		"""
		
		if type(action) != ActionWrapper:
			raise ActionException("The Action being added to the ActionPipeline must be a ActionWrapper")
		
		if action.getParent() is not self:
			raise ActionException("The ActionWrapper already has a different parent.")
		
		if action in self._actions:
			raise ActionException("The action wrapper can only be added once.")
		
		self._actions.append(action)
		
		self.updated.emit()
	
	def removeAction(self, action: 'ActionWrapper') -> bool:
		"""
		Removes an action from the action pipeline. All connected wires will be deleted.
		
		:raises: ActionException if the action is not in the ActionPipeline.
		
		:param action: The action to remove
		:type action: Action
		:return: True if the action was successfully deleted. False otherwise.
		:rtype: bool
		"""
		
		if action not in self._actions:
			raise ActionException("The Action does not exist in this Action Pipeline.")
		
		action.forgetParent()
		
		# remove all the ports, which disconnects the wires
		for port in action.getInputPorts() + action.getOutputPorts():
			self.removePort(port)
			
		self._actions.remove(action)
		self.updated.emit()
		return True
	
	def connect(self, portA: 'pt.Port', portB: 'pt.Port') -> 'Wire':
		"""
		Insert a wire to carry data from port A to port B. Returns a reference to the newly created Wire.
		
		:raises: PortException if either portA or portB do not belong to either this
		ActionPipeline or any of its inner actions.
		:raises: PortException if portB already has an input.
		:raises: WireException if the connection is invalid.
		
		:param portA: The port that will be the source of the wire.
		:type portA: Port
		:param portB: The port that will be the destination of the wire.
		:type portB: Port
		:return: The newly created Wire object connecting the given ports.
		:rtype: Wire
		"""
		
		allowableActions = [self] + self._actions
		
		if portA.getAction() not in allowableActions:
			raise pt.PortException("The source port is invalid")
		
		if portB.getAction() not in allowableActions:
			raise pt.PortException("The destination port is invalid")
		
		if portB.getInputWire() is not None:
			raise pt.PortException("The destination port already has an input wire.")
		
		if not self.connectionIsValid(portA, portB):
			raise WireException("The connection is not a valid configuration.")
		
		newWire = self._wireSet.addWire(portA, portB)
		self.updated.emit()

		return newWire
	
	def disconnect(self, portA: 'Port', portB: 'Port') -> None:
		"""
		Remove the wire spanning from portA to portB.
		
		:raises: PortException if either portA or portB do not belong to either this
		ActionPipeline or any of its inner actions.
		:raises: WireException if A wire does not exist from portA to portB.
		
		:param portA: The source port of the wire to disconnect.
		:type portA: Port
		:param portB: The destination port of the wire to disconnect.
		:type portA: Port
		:return: None
		:rtype: NoneType
		"""
		
		# Check for errors
		allowableActions = [self] + self._actions
		
		if portA.getAction() not in allowableActions:
			raise pt.PortException("The source port is invalid")
		
		if portB.getAction() not in allowableActions:
			raise pt.PortException("The destination port is invalid")
		
		wireFound = False
		if portB.getInputWire() is not None:
			if portB.getInputWire().getSourcePort() == portA:
				wireFound = True
			
		if not wireFound:
			raise WireException("There is no wire between the specified ports")
		
		# now we can delete the wire
		self._wireSet.deleteWire(portA, portB)
		self.updated.emit()
	
	def changeSequence(self, actionSequence: List['Action']) -> None:
		"""
		Change the sequence of action execution.
		
		The Actions in the new list must be the exact instances of the Actions in
		the old list with no duplications.
		
		:raises: ActionException if there is any alteration to the list of actions other than
		reordering the contents.
		
		:param actionSequence: list of actions with the desired sequence of execution
		:type actionSequence: list[Action]
		:return: None
		:rtype: NoneType
		"""
		
		if len(actionSequence) != len(set(actionSequence)):
			raise ActionException("Duplicate Action detected in sequence.")
		
		if set(actionSequence) != set(self._actions):
			raise ActionException("Different set of actions detected from original ordering.")
		
		self._actions = actionSequence
		self.updated.emit()
		
	def removePort(self, port: 'Port') -> bool:
		"""
		Removes a port from this action pipeline or a sub-action - no need to specify input or
		output.

		Removing the port from the action does not destroy the port.
		Removing a port removes all wires connected to the port.

		:raises: PortException if the port is not found.
		:raises: PortException if the port does not belong the ActionPipeline or a child action.
		:raises: PortException if the port does not have an action.

		:param port: The port instance to be removed.
		:type port: Port
		:return: True if the port was successfully removed, False otherwise.
		:rtype: bool
		"""
		
		if port.getAction() is not None:
			if port.getAction() in self._actions or port.getAction() is self:
				removed = Action.removePort(port.getAction(), port)
				self._wireSet.deleteWiresConnectedToPort(port)
				return removed
			else:
				raise pt.PortException("The port does not belong to this action pipeline or any children")
		else:
			raise pt.PortException("The port does not have an action.")
		
		self.updated.emit()
		
	def connectionIsValid(self, portA: 'Port', portB: 'Port') -> bool:
		"""
		Determines if a wire can be used to connect portA to portB. The port B must not have an
		input wire.
		
		Not all wiring configurations are valid. Please follow the wiring table below:
		
		.. table:: Valid Wire Configurations
		
			+------------------+-------------------------------+
			| Source Port      | Destination Port              |
			+==================+===============================+
			| Top-Level Input  | Top-Level Output, Child Input |
			+------------------+-------------------------------+
			| Top-Level Output | NA                            |
			+------------------+-------------------------------+
			| Child Input      | NA                            |
			+------------------+-------------------------------+
			| Child Output     | Top-Level Output, Child Input |
			+------------------+-------------------------------+
			
		:param portA: The source port for the connection.
		:type portA: Port
		:param portB: The destination port for the connection.
		:type portB: Port
		:return: True if the connection is valid, False otherwise.
		:rtype: bool
		"""
		
		def isPortBValid():
			if portB in self.getOutputPorts():
				return True
			elif portB.getAction() in self._actions and portB in portB.getAction().getInputPorts():
				return True
			
		if portB.getInputWire():
			return False
		
		if portA in self.getInputPorts():
			return isPortBValid()
		
		elif portA.getAction() in self._actions and portA in portA.getAction().getOutputPorts():
			return isPortBValid()
		
		return False
	
	def getActions(self) -> List['Action']:
		"""
		Get all of the internal actions of this action pipeline.
		
		:return: All actions in this action pipeline.
		:rtype: List[Action]
		"""
		return self._actions[:]
	
	def getWireSet(self) -> WireSet:
		"""
		Get the wire set for this action pipeline.
		
		.. warning:: The WireSet does not provide the same protections as the ActionPipeline
			class does. It is advised to use methods of the ActionPipeline instead of operating
			on the wireset manually if possible.
		
		:return: This action pipeline's wire set.
		:rtype: WireSet
		"""
		return self._wireSet

	def getMethodName(self) -> str:
		"""
		In this case, just returns unique name of action pipeline, since AP name uniqueness is enforced within the GUI.
		However, should only be called by actionwrapper.

		:return: name of action pipeline
		:rtype: str
		"""

		return self.getName()

	def getMethodCode(self) -> str:
		"""
		Generates the entirety of the code necessary for the action, including space afterwards.

		:return: code 'guts' that will be contained in the action pipeline's call/method
		:rtype: str
		"""

		code = ""

		for p in self.getInputPorts():  # Assumes unique input port names, which should be enforced in gui.
			self._varMap.append((p.getName(), p))

		for	a in self._actions: 
			code += '\t\t' 
			if a.getOutputPorts():  # Getting outputs named and written to code
				o = a.getOutputPorts()[0]
				code += self.getVarName(o)  # only one output
				if len(a.getOutputPorts()) > 1:  # if several outputs
					for o in a.getOutputPorts()[1:]:
						code += ", " + self.getVarName(o)
				code += ' = '
			code += a.getMethodName() + '('

			if a.getInputPorts():
				i = a.getInputPorts()[0]
				code += self.getVarName(i)  # only one input
				if len(a.getInputPorts()) > 1:  # if multiple inputs
					for i in a.getInputPorts()[1:]:
						code += ", " + self.getVarName(i)
			code += ')'
		
		if self.getOutputPorts():
			code += '\n\n\t\treturn '
			o = self.getOutputPorts()[0]
			code += self.getVarName(o)  # only one output
			if len(self.getOutputPorts()) > 1:  # if several outputs
				for o in self.getOutputPorts()[1:]:
					code += ", " + self.getVarName(o)

		code += '\n\n'
		return code

	def getVarName(self, p: 'Port') -> str:
		"""
		Gets the name of a variable associated to a port. If none, creates one and increments max varName used.

		:return: name associated to port
		:rtype: str
		"""

		# Check if port already has name. if so, return immediately.
		allports = [tmp[1] for tmp in self._varMap]
		if p in allports:
			# idk if this is very effective but should get the job done
			return self._varMap[allports.index(p)][0]
		
		# Check if port is connected by wire to other ports.
		cnctdPorts = []
		if p.getInputWire():
			cnctdPorts.append(p.getInputWire().getSourcePort())
		for w in p.getOutputWires():
			cnctdPorts.append(w.getDestPort())
		
		# If so, check if connected ports have names, and assign same name to all.
		newName = True
		for lp in cnctdPorts:
			if lp in allports:
				name = self._varMap[allports.index(lp)][0]
				newName = False
				break

		if newName:
			name = self._varName
			self.incrVarName()

		# adds all connected ports to varMap with their shared variable name, if they aren't in there already.
		self._varMap.append((name, p))
		for tmp in cnctdPorts:
			if tmp not in allports:
				self._varMap.append((name, tmp))

		return name

	def incrVarName(self) -> None:
		"""
		Increments varName from a to z, then to aa, to zz, and so on.

		:return: None
		"""
		
		var = self._varName
		zs = var.rstrip('z')
		num_replacements = len(var) - len(zs)
		newName = zs[:-1] + self.incrChar(zs[-1]) if zs else 'a'
		newName += 'a' * num_replacements

		self._varName = newName

	def incrChar(self, var: str) -> str:
		"""
		Increments character by 1 unless it is 'z', in which case 'a' is returned

		:param var: character of interest
		:type var: str
		:return: incremented char
		:rtype: str
		"""

		return chr(ord(var) + 1) if var != 'z' else 'a'
