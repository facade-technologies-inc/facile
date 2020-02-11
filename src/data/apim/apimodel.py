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
	
This module contains the ApiModel class which is the top-level class for building the API Model.
"""

from typing import List

from PySide2.QtCore import QObject

from data.apim.actionpipeline import ActionPipeline
from data.apim.componentaction import ComponentAction

class ApiModel(QObject):
	"""
	The ApiModel class contains all the information about the API model. There are 2 main parts
	of the API model; action pipelines, and component actions.
	
	Each Action Pipeline is created manually by the user using Facile. When action pipelines are
	created, other actions are inserted into them; however, since the action pipelines can share
	resources (such as the same ComponentAction being used in 2 Action Pipelines), the Action
	Pipelines really only contain wrappers that point to other actions.
	
	The action pipelines are kept in a collection separate from the action pipelines and each one is
	unique - meaning that we never store 2 component actions that have the same component and the
	same action specification.
	"""
	
	def __init__(self):
		"""
		Constructs an ApiModel.
		
		:return: The api model
		:rtype: ApiModel
		"""
		
		self._actionPipelines = []
		self._componentActions = []
		
	def getActionPipelines(self) -> List[ActionPipeline]:
		"""
		Gets a list of all ActionPipelines.
		
		.. note:: A shallow copy of the list is returned rather than the original.
		
		:return: A list of all ActionPipelines.
		:rtype: List[ActionPipeline]
		"""
		return self._actionPipelines[:]
	
	def getComponentActions(self) -> List[ComponentAction]:
		"""
		Gets a list of all ComponentActions
		
		.. note:: A shallow copy of the list is returned rather than the original.
		
		:return: A list of all ComponentActions
		:rtype: List[ComponentAction]
		"""
		return self._componentActions[:]
	
	def addActionPipeline(self, actionPipeline: 'ActionPipeline') -> None:
		"""
		Add an action pipeline to the collection of all action pipelines.
		
		:param actionPipeline: The action pipeline to add to the collection.
		:type actionPipeline: ActionPipeline
		:return: None
		:rtype: NoneType
		"""
		self._actionPipelines.append(actionPipeline)
		
	def addComponentAction(self, componentAction: 'ComponentAction') -> None:
		"""
		Add a component action to the collection of all component actions.
		
		:param actionPipeline: The component action to add to the collection
		:type actionPipeline: ComponentAction
		:return: None
		:rtype: NoneType
		"""
		# TODO: if componentAction is a repeat, don't add it.
		
		self._componentActions.append(componentAction)
		
	def removeActionPipeline(self, actionPipeline: 'ActionPipeline') -> bool:
		"""
		Removes an action pipeline instance from the collection of action pipelines.
		
		:param actionPipeline: The action pipeline to remove
		:type actionPipeline: ActionPipeline
		:return: True if the action pipeline existed before, but is successfully removed. False
		         otherwise.
		:rtype: bool
		"""
		try:
			self._actionPipelines.remove(actionPipeline)
			return True
		except:
			return False