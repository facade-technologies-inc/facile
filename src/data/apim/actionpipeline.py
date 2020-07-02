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

import data.apim.actionwrapper as aw
import data.apim.port as pt
from data.apim.wireset import WireSet
from data.apim.wire import WireException
from data.apim.action import Action, ActionException
from data.properties import Properties

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

		# these variables are just for api compilation purposes
		self._varName = 'a'
		self._varMap = {}  # relates a variable name to a list of all ports that use it
		self._invVarMap = {}  # relates all ports to a variable name
	
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
		
		if type(action) != aw.ActionWrapper:
			raise ActionException("The Action being added to the ActionPipeline must be a ActionWrapper")
		
		if action.getParent() is not self:
			raise ActionException("The ActionWrapper already has a different parent.")
		
		if action in self._actions:
			return
		
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
	
	def disconnect(self, portA: 'Port', portB: 'Port') -> None:  # TODO: Evaluate whether this overload is safe.
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

	def getChildActions(self) -> List['Action']:
		"""
		A replacement for self.getActions()

		:return: All actions in this action pipeline.
		:rtype: List[Action]
		"""
		return self.getActions()
	
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

		return self.getName().replace(' ', '_')
	
	def getDocStr(self) -> str:
		"""
		Generates the docstring for the action. Adds the necessary spacing after docstring.
		If the function has no inputs or outputs, the docstring states this.

		:return: doc string describing action, inputs, and outputs
		:rtype: str
		"""
		
		out = '\t\t"""\n'
		noDoc = True
		
		if self.getAnnotation():
			noDoc = False
			out += '\t\t' + self.getAnnotation() + '\n\n'
		
		if self._inputs or self._outputs:
			noDoc = False
			
			for p in self._inputs:
				out += '\t\t:param ' + p.getName() + ': ' + p.getAnnotation() + '\n'
				out += '\t\t:type ' + p.getName() + ': ' + p.getDataTypeStr() + '\n'
			
			# we can only have one return tag, so we just combine everything.
			if self._outputs:
				annotations = [p.getAnnotation() for p in self._outputs]
				types = [p.getDataTypeStr() for p in self._outputs]
				if len(annotations) > 1:
					out += '\t\t:return: ({})\n'.format(", ".join(annotations))
					out += '\t\t:rtype: ({})\n'.format(", ".join(types))
				else:
					out += '\t\t:return: {}\n'.format(annotations[0])
					out += '\t\t:rtype: {}\n'.format(types[0])
			else:
				out += '\t\t:return: None\n'
				out += '\t\t:rtype: NoneType\n'
		else:
			out += '\t\t:return: None\n'
			out += '\t\t:rtype: NoneType\n'
		
		if noDoc:
			return '\t\t"""\n\t\tThis action has no annotations, inputs, or outputs.\n\t\t"""\n'
		else:
			out += '\t\t"""\n\n'
			return out

	def getMethodCode(self) -> str:
		"""
		Generates the entirety of the code necessary for the action, including space afterwards.

		:return: code 'guts' that will be contained in the action pipeline's call/method
		:rtype: str
		"""

		# If a project is compiled twice in the same run, we need to reinitialize everything.
		self._varMap = {}
		self._invVarMap = {}
		self._varName = 'a'

		code = "\t\ttry:  # The generated code. If it doesn't work, throws an error.\n"

		for p in self.getInputPorts():  # Assumes unique input port names, which should be enforced in gui.
			self._varMap[p.getName()] = [p]  # List of all ports to which the name is tied
			self._invVarMap[p] = p.getName()

		for a in self._actions:
			code += '\t\t\t'
			if a.getOutputPorts():  # Getting outputs named and written to code
				o = a.getOutputPorts()[0]
				code += self.getVarName(o)  # only one output
				if len(a.getOutputPorts()) > 1:  # if several outputs
					for o in a.getOutputPorts()[1:]:
						code += ", " + self.getVarName(o)
				code += ' = '
			code += 'self.' + a.getMethodName() + '('

			if a.getInputPorts():
				# First port
				i = a.getInputPorts()[0]
				if i.isOptional():  # For optional parameters
					code += i.getName() + '='
				inType = i.getDataTypeStr()  # Enforcing data type
				code += inType + '(' + self.getVarName(i) + ')'  # only one input, converts it to necessary type

				# Other ports
				if len(a.getInputPorts()) > 1:  # if multiple inputs
					for i in a.getInputPorts()[1:]:
						code += ", "
						inType = i.getDataTypeStr()
						if i.isOptional():  # For optional parameters
							code += i.getName() + '='
						code += inType + '(' + self.getVarName(i) + ')'
			code += ')\n'

		if self.getOutputPorts():
			code += '\n\t\t\treturn '
			o = self.getOutputPorts()[0]
			outType = o.getDataTypeStr()
			code += outType + '(' + self.getVarName(o) + ')'  # only one output
			if len(self.getOutputPorts()) > 1:  # if several outputs
				for o in self.getOutputPorts()[1:]:
					outType = o.getDataTypeStr()
					code += ", " + outType + '(' + self.getVarName(o) + ')'
			code += '\n'

		code += '\t\texcept Exception as e:\n\t\t\tprint(e)\n\t\t\traise ActionException("The action could not be ' \
				'performed successfully. Please look at the errors above, or message us for support.")\n'

		return code

	def getVarName(self, p: 'Port') -> str:
		"""
		Gets the name of a variable associated to a port. If none, creates one and increments max varName used.

		:return: name associated to port
		:rtype: str
		"""

		# Check if port already has name. if so, return immediately.
		allports = self._invVarMap
		if p in self._invVarMap:
			return self._invVarMap[p]
		
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
				name = self._invVarMap[lp]
				newName = False
				break

		if newName:
			name = self._varName
			self.incrVarName()
			self._varMap[name] = [p]
		else:
			self._varMap[name].append(p)

		self._invVarMap[p] = name

		# adds all connected ports to varMap with their shared variable name, if they aren't in there already.

		for tmp in cnctdPorts:
			if tmp not in allports:
				self._varMap[name].append(tmp)
				self._invVarMap[tmp] = name

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

	def getActionWrappers(self):
		"""
		Returns the action wrappers that this pipeline uses
		"""
		return self._actions

	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the action pipeline.

		.. note::
			This is not just a getter of the __dict__ attribute.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		apDict = Action.asDict(self)

		# just store the id of the action (wrappers) that are owned by the action pipeline
		apDict["actions"] = [action.asDict() for action in self._actions]

		apDict["wire set"] = self._wireSet.asDict()

		return apDict

	@staticmethod
	def fromDict(d: dict) -> 'ActionPipeline':
		"""
		Creates an Action Pipeline from the dictionary

		:param d: The dictionary that represents the action pipeline.
		:type d: dict
		:return: The ActionPipeline object that was constructed from the dictionary
		:rtype: ActionPipeline
		"""
		ap = ActionPipeline()

		ap.actionsDict = d['actions']  # These will be constructed later

		ap._inputs = [pt.Port.fromDict(dic, ap) for dic in d["inputs"]]
		ap._outputs = [pt.Port.fromDict(dic, ap) for dic in d["outputs"]]

		ap.wiresetDict = d['wire set']  # so will these

		if d['properties']:
			ap.setProperties(Properties.fromDict(d['properties']))

		return ap
