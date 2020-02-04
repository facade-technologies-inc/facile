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
	The ApiModel class contains all the information about the API model.
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
		
		:return: A list of all ActionPipelines.
		:rtype: List[ActionPipeline]
		"""
		return self._actionPipelines[:]
	
	def getComponentActions(self) -> List[ComponentAction]:
		pass
		# TODO: Decide how we're going to store component actions and which ones we'll store.
	
	# TODO: Add methods to this class as we see fit