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

from data.apim.action import Action
import data.apim.actionpipeline as ap


class ActionWrapper(Action):
	"""
	The purpose of the ActionWrapper class is to prevent copying of action pipelines and other
	actions unnecessarily. The action wrapper allows us to update uses of an action very easily
	in the case that the user edits an action.
	
	To handle the user editing an action, the wrapper just needs to keep the ports synchronized
	with the referenced actions.
	
	The ActionWrapper can be thought of as a black-box for any other action.
	"""
	
	def __init__(self, actionRef: 'Action', parent: 'ap.ActionPipeline') -> 'ActionWrapper':
		"""
		Constructs a WrapperAction that stores a reference to an action.
		
		Since WrapperActions will only be used as internal actions and never stand-alone,
		we can store the parent as well.
		
		The wrapper is added to the parent action pipeline.
		
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
		
		if self not in parent.getActions():
			parent.addAction(self)
		
		self.setName(self._actionRef.getName())
		self._actionRef.registerWrapper(self)
		self.synchronizePorts()
		
	def getActionReference(self) -> 'Action':
		"""
		Gets the action referenced by this wrapper.
		
		:return: The referenced action.
		:rtype: Action
		"""
		return self._actionRef
	
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




