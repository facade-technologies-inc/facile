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

from PySide2.QtGui import QPainter, QColor, QFont, QFontMetricsF
from PySide2.QtCore import QRectF
from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem

from graphics.apim.actiongraphics import ActionGraphics

class ActionWrapperGraphics(ActionGraphics):
	
	TAG_FONT = QFont("Times", 10)
	TAG_TEXT_COLOR = QColor(0, 0, 0)
	TAG_BACKGROUND_COLOR = QColor(150, 150, 150)
	
	NAME_FONT = QFont("Times", 10)
	NAME_TEXT_COLOR = QColor(0, 0, 0)
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		"""
		Paint the graphics of the action wrapper including action name, number, and ports.

		:param painter: This draws the widget.
		:type painter: QPainter
		:param option: Option for the style of graphic.
		:type option: QStyleOptionGraphicsItem
		:param index: Index for the painted graphic.
		:type index: QWidget
		:return: None
		:rtype: NoneType
		"""
		ActionGraphics.paint(self, painter, option, index)
		
		# Get dimensions of the action
		x, y, width, height = self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts())
		
		# Draw the number tag.
		number = str(self._action.getParent().getActions().index(self._action) + 1)
		offset = 5
		radius = 15
		size = ActionGraphics.H_SPACE/2 - offset*2
		painter.setBrush(QColor(29, 110, 37))
		painter.drawRoundedRect(QRectF(x + offset, y + offset, size, size), radius, radius)
		painter.setPen(ActionWrapperGraphics.TAG_TEXT_COLOR)
		painter.setBrush(ActionWrapperGraphics.TAG_TEXT_COLOR)
		painter.setFont(ActionWrapperGraphics.TAG_FONT)
		fm = QFontMetricsF(ActionWrapperGraphics.TAG_FONT)
		pixelsWide = fm.width(number)
		pixelsHigh = fm.height()
		# TODO: fix text positioning - font metrics aren't working well
		painter.drawText(x+offset+size/2-pixelsWide, y+offset+size/2+pixelsHigh/2, number)
		
		# Draw the name of the action
		painter.setPen(ActionWrapperGraphics.NAME_TEXT_COLOR)
		painter.setBrush(ActionWrapperGraphics.NAME_TEXT_COLOR)
		painter.setFont(ActionWrapperGraphics.NAME_FONT)
		fm = QFontMetricsF(ActionWrapperGraphics.NAME_FONT)
		br = fm.boundingRect(self._action.getName())
		# TODO: fix text positioning - font metrics aren't working well
		painter.drawText(x + offset, br.height(), self._action.getName())
		
