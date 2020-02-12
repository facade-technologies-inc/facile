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
"""

from PySide2.QtWidgets import QGraphicsItem
from graphics.apim.actiongraphics import ActionGraphics


class ActionIconGraphics(ActionGraphics):
	
	def __init__(self, action: 'Action', parent:QGraphicsItem=None) -> 'ActionGraphics':
		"""
		Creates an ActionIconGraphics object.
		
		:param action: The action to create icon graphics for.
		:type action: Action
		:param parent: The parent graphics item.
		:type parent: QGraphicsItem
		"""
		ActionGraphics.__init__(self, action, parent)
		self._interactivePorts = False
	
	def createPortGraphics(self) -> None:
		"""
		Override the ActionGraphics createPortGraphics method to not allow context-menu summoning.
		
		:return: None
		:rtype: NoneType
		"""
		self._interactivePorts = False
		return ActionGraphics.createPortGraphics(self)