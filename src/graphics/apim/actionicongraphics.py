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

from PySide2.QtWidgets import QGraphicsItem, QGraphicsSimpleTextItem
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from graphics.apim.actiongraphics import ActionGraphics


class ActionIconGraphics(ActionGraphics):

	TEXT_X_OFFSET = 10
	TEXT_SCALE_FACTOR = 0.99
	TEXT_DEFAULT_SIZE = 16
	
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
		self._textItem = QGraphicsSimpleTextItem(self._action.getName(), self)
		self._textItem.setFont(QFont("Sans Serif", ActionIconGraphics.TEXT_DEFAULT_SIZE, QFont.Bold))
		self._textItem.setBrush(QColor(Qt.white))
		self.updateGraphics()
	
	def createPortGraphics(self) -> None:
		"""
		Override the ActionGraphics createPortGraphics method to not allow context-menu summoning.
		
		:return: None
		:rtype: NoneType
		"""
		self._interactivePorts = False
		return ActionGraphics.createPortGraphics(self)

	def updateGraphics(self) -> None:
		"""
		Updates the text, then calls the super method.

		:return: None
		:rtype: NoneType
		"""
		self._textItem.setText(self._action.getName())
		self._textItem.setFont(QFont("Sans Serif", ActionIconGraphics.TEXT_DEFAULT_SIZE, QFont.Bold))
		br = self.boundingRect()

		# shrink text to fit in action
		numShrinks = 0
		while True:
			tbr = self._textItem.boundingRect()
			if tbr.width() > br.width() - 2 * ActionIconGraphics.TEXT_X_OFFSET:
				numShrinks += 1
				textSize = ActionIconGraphics.TEXT_DEFAULT_SIZE * (ActionIconGraphics.TEXT_SCALE_FACTOR ** numShrinks)
				self._textItem.setFont(QFont("Sans Serif", textSize, QFont.Bold))
			else:
				break

		x = br.x() + ActionIconGraphics.TEXT_X_OFFSET
		y = - tbr.height() / 2
		self._textItem.setPos(x, y)

		return ActionGraphics.updateGraphics(self)