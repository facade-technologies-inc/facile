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

from data.entity import Entity
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
		
		self.initializeSpecifications()
		
	def initializeSpecifications(self) -> None:
		"""
		Read all action specifications from the database.
		
		The specifications are stored in a dictionary mapping each unique target to a list of
		ActionSpecification objects.
		
		:return: None
		:rtype: NoneType
		"""
		curPath = os.path.abspath(__file__)
		path, filename = os.path.split(curPath)
		specDir = os.path.abspath(os.path.join(path,"../../../database/component_actions"))
		if not os.path.exists(specDir):
			specDir = os.path.abspath(os.path.join(path, "../../database/component_actions"))
			
		for file in os.listdir(specDir):
			if file.endswith(".action"):
				filepath = os.path.join(specDir, file)
				aS = ActionSpecification().fromFile(filepath)

				if aS.viableTargets is None:
					continue

				# Map all targets to the specification for easy lookup later.
				for target in aS.viableTargets:
					if target in self._specifications:
						self._specifications[target].append(aS)
					else:
						self._specifications[target] = [aS]
						
	def getSpecifications(self, target: str = "all") -> List[ActionSpecification]:
		"""
		Get all the action specifications for a specific target.
		If target is all, all specifications will be returned.
		
		:param target: The target of the specification to retrieve.
		:type target: str
		:return: A list of action specifications for the given target
		:rtype:
		"""
		# Get all action specifications as a list
		if target == "all":
			specs = set()
			for target in self._specifications:
				specs.update(self._specifications[target])
			return list(specs)
		else:
			return self._specifications.get(target, [])[:]
			
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

	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the API Model.

		.. note::
			This is not just a getter of the __dict__ attribute.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		apimDict = {}

		# store all action pipelines
		apimDict["action pipelines"] = [ap.asDict() for ap in self._actionPipelines]

		# store all action wrappers and component actions
		apimDict["action wrappers"] = []
		apimDict["component actions"] = []
		componentActions = set()
		for ap in self._actionPipelines:
			for aw in ap._actions:
				apimDict["action wrappers"].append(aw.asDict())

				action = aw.getActionReference()
				if type(action) is ComponentAction and action not in componentActions:
					componentActions.add(action)
					apimDict["component actions"].append(action.asDict())

		# store action specifications
		apimDict["action specifications"] = [aSpec.asDict() for aSpec in self.getSpecifications()]

		# NOTE: The ports will be stored in the action they belong to.
		# NOTE: The wire sets will be stored in the action pipeline they belong to.
		# NOTE: The wires will be stored in the wire sets they belong to.

		# from pprint import pprint
		# pprint(apimDict)

		return apimDict

	@staticmethod
	def fromDict(d: dict) -> 'ApiModel':
		"""
		Creates an API Model from the dictionary

		:param d: The dictionary that represents the API model.
		:type d: dict
		:return: The ApiModel object that was constructed from the dictionary
		:rtype: ApiModel
		"""
		apim = ApiModel()
		apim._actionPipelines = [ApiModel.fromDict(dic) for dic in d["action pipelines"]]


		return apim

