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

from typecheck import typecheck
from typing import List

from data.apim.action import Action, ActionException
from data.apim.port import Port, PortException
from data.apim.wireset import WireSet
from data.apim.wire import WireException

class ActionPipeline(Action):
	
	def __init__(self):
		"""
		ActionPipelines are an aggregation of Actions. The internals of the
		ActionPipeline can be connected with wires that carry data. The internal actions are
		executed in the sequence in with they are stored.
		"""
		self.actions = []
		self.wireSet = WireSet()
	
	@typecheck
	def addAction(self, action: Action) -> None:
		"""
		Adds an *Action* (Either ActionPipeline or ComponentAction) as an internal component of
		this action pipeline.
		
		This method does not check to see if the Action exists in another ActionPipeline,
		but the caller should avoid this as it would certainly be invalid.
		
		:raises: ActionException if the action is already in the action list
		
		:param action: The Action to add to this ActionPipeline.
		:type action: Action
		:return: None
		:rtype: NoneType
		"""
		
		if action in self.actions:
			raise ActionException("The action can only be added once.")
		
		self.actions.append(action)
		
	@typecheck
	def removeAction(self, action: Action) -> bool:
		"""
		Removes an action from the action pipeline. All connected wires will be deleted.
		
		:raises: ActionException if the action is not in the ActionPipeline.
		
		:param action: The action to remove
		:type action: Action
		:return: True if the action was successfully deleted. False otherwise.
		:rtype: bool
		"""
		
		if action not in self.actions:
			raise ActionException("The Action does not exist in this Action Pipeline.")
		
		else:
			self.actions.remove(action)
			return True
		
	@typecheck
	def connect(self, portA: Port, portB: Port) -> None:
		"""
		Insert a wire to carry data from port A to port B.
		
		:raises: PortException if either portA or portB do not belong to either this
		ActionPipeline or any of its inner actions.
		:raises: PortException if portB already has an input.
		
		:param portA: The port that will be the source of the wire.
		:type portA: Port
		:param portB: The port that will be the destination of the wire.
		:type portB: Port
		:return: None
		:rtype: NoneType
		"""
		
		# Check for errors
		allowableActions = [self] + self.actions
		
		if portA.action not in allowableActions:
			raise PortException("The source port is invalid")
		
		if portB.action not in allowableActions:
			raise PortException("The destination port is invalid")
		
		if portB.input:
			raise PortException("The destination port already has an input wire.")
		
		# now we can add a wire.
		self.wireSet.addWire(portA, portB)
		
	@typecheck
	def disconnect(self, portA: Port, portB: Port) -> None:
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
		allowableActions = [self] + self.actions
		
		if portA.action not in allowableActions:
			raise PortException("The source port is invalid")
		
		if portB.action not in allowableActions:
			raise PortException("The destination port is invalid")
		
		if portB.input.src != portA:
			raise WireException("There is no wire between the specified ports")
		
		# now we can delete the wire
		self.wireSet.removeWire(portA, portB)
		
	@typecheck
	def changeSequence(self, actionSequence: List[Action]) -> None:
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
		
		if set(actionSequence) != set(self.actions):
			raise ActionException("Different actions detected from original ordering.")
		
		self.actions = actionSequence