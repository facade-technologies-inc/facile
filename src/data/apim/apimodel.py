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

import os
from typing import List, Tuple

from PySide2.QtCore import QObject, Signal

from data.apim.actionpipeline import ActionPipeline
from data.apim.componentaction import ComponentAction
from data.apim.actionwrapper import ActionWrapper
from data.apim.actionspecification import ActionSpecification

class ApiModel(QObject):
	"""
	The ApiModel class contains all action pipelines in the project.
	
	Each Action Pipeline is created manually by the user using Facile. When action pipelines are
	created, other actions are inserted into them; however, since the action pipelines can share
	resources (such as the same ComponentAction being used in 2 Action Pipelines), the Action
	Pipelines really only contain wrappers that point to other actions.
	"""
	
	newActionPipeline = Signal(ActionPipeline)
	
	def __init__(self):
		"""
		Constructs an ApiModel.
		
		:return: The api model
		:rtype: ApiModel
		"""
		
		self._actionPipelines = []
		self._specifications = {}
		
	def initializeSpecifications(self) -> None:
		"""
		Read all action specifications from the database
		
		:return: None
		:rtype: NoneType
		"""
		specDir = os.path.abspath("../database/component_actions")
		for file in os.listdir(specDir):
			if file.endswith(".action"):
				aS = ActionSpecification(os.path.join(specDir, file))
				for target in aS.viableTargets:
					if target in self._specifications:
						self._specifications[target].append(aS)
					else:
						self._specifications[target] = [aS]
		
	def getActionPipelines(self) -> List[ActionPipeline]:
		"""
		Gets a list of all ActionPipelines.
		
		.. note:: A shallow copy of the list is returned rather than the original.
		
		:return: A list of all ActionPipelines.
		:rtype: List[ActionPipeline]
		"""
		return self._actionPipelines[:]
	
	def addActionPipeline(self, actionPipeline: 'ActionPipeline') -> None:
		"""
		Add an action pipeline to the collection of all action pipelines.
		
		:param actionPipeline: The action pipeline to add to the collection.
		:type actionPipeline: ActionPipeline
		:return: None
		:rtype: NoneType
		"""
		if actionPipeline not in self._actionPipelines:
			self._actionPipelines.append(actionPipeline)
		
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
		
	def getActionsByType(self) -> Tuple[List['ActionPipeline'], List['ComponentAction']]:
		"""
		get lists of all actions separated by type.
		
		.. note:: This method is computationally intensive as it traverses all actions in the
			apim. It should not be called often.
		
		:return: A list of all component actions used by the action pipelines
		:rtype: Tuple[List['ActionPipeline'], List['ComponentAction']]
		"""
		
		componentActions = set()
		
		work = self._actionPipelines[:]
		while work:
			action = work.pop()
			if type(action) == ComponentAction:
				componentActions.add(action)
			elif type(action) == ActionPipeline:
				work += action.getActions()
			elif type(action) == ActionWrapper:
				work.append(action.getActionReference())
			
		return self.getActionPipelines(), list(componentActions)
