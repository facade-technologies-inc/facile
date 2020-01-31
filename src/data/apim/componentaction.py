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
	
This module contains the **ComponentAction** class which is used to tie a user action to a
component from the TGUIM.
"""

from typecheck import typecheck

from data.apim.action import Action
from data.tguim.component import Component

class ComponentAction(Action):
	
	@typecheck
	def __init__(self, targetComponent: Component, codeSpec: str):
		"""
		The ComponentAction class is used to describe a
		:param targetComponent:
		:param codeSpec:
		"""
		self.target = targetComponent
		self.codeSpec = codeSpec
	
	# TODO: Add more methods once we've clearly defined what we're doing with this class.