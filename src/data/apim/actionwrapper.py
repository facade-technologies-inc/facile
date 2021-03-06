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
	
This module contains the ActionWrapper class.
"""

from typing import List, Dict

import data.apim.actionpipeline as ap
import data.apim.action as act
import data.properties as ppts

class ActionWrapper(act.Action):
	"""
	The purpose of the ActionWrapper class is to prevent copying of action pipelines and other
	actions unnecessarily. The action wrapper allows us to update uses of an action very easily
	in the case that the user edits an action.
	
	To handle the user editing an action, the wrapper just needs to keep the ports synchronized
	with the referenced actions.
	
	The ActionWrapper can be thought of as a black-box for any other action.
	"""

	def __init__(self, actionRef: 'act.Action', parent: 'ap.ActionPipeline' = None) -> 'ActionWrapper':
		"""
		Constructs a WrapperAction that stores a reference to an action.
		
		Since WrapperActions will only be used as internal actions and never stand-alone,
		we can store the parent as well.
		
		The wrapper is added to the parent action pipeline.

		Both actionRef and parent are optional, but if they are not given, the initializeAfterLink() function must be
		called after they are set manually.
		
		:param actionRef: The action to be referenced.
		:type actionRef: Action
		:param parent: The action that this wrapper is being inserted into.
		:type parent: ActionPipeline
		:return: The action wrapper that is constructed.
		:rtype: ActionWrapper
		"""
		super().__init__()
		
		self._actionRef = actionRef
		self._parent = parent
		self._inputPortMapping = {}
		self._outputPortMapping = {}

		if parent:
			if self not in parent.getActions():
				parent.addAction(self)

		self.setName(self._actionRef.getName())
		self._actionRef.registerWrapper(self)
		self.synchronizePorts()


	def getUnderlyingAction(self) -> 'Action':
		"""
		Gets the action referenced by the possible chain of wrapper actions.

		.. note::
			This is different than getActionReference() which only gets the action referenced by this wrapper.
			This function will recursively get the referenced action until we find an action that is not a wrapper.

		:return: The underlying action of the possible chain of action wrappers.
		:rtype: Action (but definitely not an ActionWrapper)
		"""
		if type(self.getActionReference()) is not ActionWrapper:
			return self.getActionReference()

		return self.getUnderlyingAction()
		
	def getActionReference(self) -> 'Action':
		"""
		Gets the action referenced by this wrapper.
		
		:return: The referenced action.
		:rtype: Action
		"""
		return self._actionRef

	def getChildActions(self) -> List['Action']:
		"""
		A replacement for self.getActionReference(), but returns a list with only one element.

		:return: The referenced action in a 1-element list
		:rtype: List[Action]
		"""
		return [self.getActionReference()]
	
	def forgetActionReference(self) -> None:
		"""
		Sets the action reference to None
		
		:return: None
		:rtype: NoneType
		"""
		self._actionRef = None
	
	def getParent(self) -> 'ap.ActionPipeline':
		"""
		Get the parent ActionPipeline to this action wrapper.
		
		:return: The parent action pipeline
		:rtype: ActionPipeline
		"""
		return self._parent
	
	def forgetParent(self) -> None:
		"""
		Sets the action reference to None
		
		:return: None
		:rtype: NoneType
		"""
		self._parent = None
		
	def synchronizePorts(self):
		"""
		Maintains an exact mirroring of ports between the referenced action and this action wrapper.
		
		:return: None
		:rtype: NoneType
		"""
		self._synchronizePortList(self._inputs, self._actionRef.getInputPorts(), self._inputPortMapping)
		self._synchronizePortList(self._outputs, self._actionRef.getOutputPorts(), self._outputPortMapping)
		
	def _synchronizePortList(self, myPortList: List['Port'], refPortList: List['Port'], mapping: Dict['Port', 'Port']) -> None:
		"""
		Synchronizes either the inputs our outputs of the action wrapper with the
		corresponding port list in the reference action.
		
		:param myPortList: The list of ports in this action to synchronize.
		:type myPortList: List['Port']
		:param refPortList: The list of ports to synchronize with from the reference action.
		:type refPortList: List['Port']
		:param mapping: Maps the ports in the wrapper to the corresponding port in the reference.
		:type mapping: Dict['Port', 'Port']
		:return: None
		:rtype: NoneType
		"""
		
		assert(myPortList is self._inputs or myPortList is self._outputs)
		
		newOrdering = []
		
		# map all of the reference ports to wrapper ports.
		for refPort in refPortList:
			
			# update any ports that are already in the mapping.
			if refPort in mapping:
				mapping[refPort].mirror(refPort)
				
			# create new ports that aren't already in the mapping.
			else:
				newPort = refPort.copy()
				
				if myPortList is self._inputs:
					self.addInputPort(newPort)
				else:
					self.addOutputPort(newPort)
					
				mapping[refPort] = newPort
				
			newOrdering.append(mapping[refPort])
			
		# remove any ports that don't exist in the reference action.
		for port in myPortList:
			if port not in newOrdering:
				
				# we remove the port through the parent because it will remove all wires
				# connected to the port as well.
				if self._parent:
					self._parent.removePort(port)
				
		# maintain correct ordering of ports
		myPortList.clear()
		for port in newOrdering:
			myPortList.append(port)

	def getMethodName(self) -> str:
		"""
		Returns method name using actionRef's getMethodName definition.

		:return: method name
		:rtype: str
		"""

		return self._actionRef.getMethodName()

	def getMethodCode(self) -> str:
		"""
		Returns the code "guts" of the actionRef

		:return: Code to perform referenced action
		:rtype: str
		"""
		
		return self._actionRef.getMethodCode()

	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the action wrapper.

		.. note::
			This is not just a getter of the __dict__ attribute.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""

		actionDict = act.Action.asDict(self)
		actionDict["reference action"] = self._actionRef.getId()

		return actionDict

	@staticmethod
	def fromDict(d: dict, compActs: dict, parent: 'ActionPipeline') -> 'ActionWrapper':
		"""
		Creates an ActionWrapper from the dictionary

		:param d: The dictionary that represents the ActionWrapper.
		:type d: dict
		:param compActs: Dictionary of component actions
		:type compActs: dict
		:param parent: The parent ActionPipeline that contains this actionwrapper
		:type parent:
		:return: The ActionWrapper object that was constructed from the dictionary
		:rtype: ActionWrapper
		"""

		actionRef = compActs[d['reference action']]

		aw = ActionWrapper(actionRef, parent)

		if d['properties']:
			aw.setProperties(ppts.Properties.fromDict(d['properties']))

		return aw
