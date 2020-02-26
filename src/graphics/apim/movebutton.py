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
	
This module contains the MoveButton class. Move Buttons have either an upward-facing arrow or
downward-facing arrow. They only emit 1 signal - clicked.
"""
from enum import Enum

from PySide2.QtGui import QPainter, QColor, QPen, Qt
from PySide2.QtCore import Signal, QRectF, QObject
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from graphics.apim.actiongraphics import ActionGraphics
from graphics.apim.portgraphics import PortGraphics

class MoveButton(QObject, QGraphicsItem):
	"""
	The MoveButton classed is a button that can be put in a graphics view. It can only have an up
	or a down arrow currently because that's all that's needed.
	"""
	
	clicked = Signal()
	
	# Shape constants
	PEN_WIDTH = 3
	WIDTH = (ActionGraphics.H_SPACE - PortGraphics.WIDTH) / 2 * 0.98
	HEIGHT = WIDTH * 1.5
	
	# Color constants
	BG_COLOR = QColor(187, 225, 250)
	LINE_COLOR = QColor(50, 130, 184)
	
	BG_COLOR_ON_HOVER = QColor(50, 130, 184)
	LINE_COLOR_ON_HOVER = QColor(15, 76, 117)
	
	class Direction(Enum):
		Up = 1
		Down = 2
	
	def __init__(self, direction, parent=None) -> 'ActionGraphics':
		"""
		Constructs an move button with either an up or down arrow

		:param direction: The direction to draw the button (up or down)
		:type direction: MoveButton.Direction
		:param parent: None
		:type parent: NoneType
		:return: The graphics for the button.
		:rtype: ActionGraphics
		"""
		QObject.__init__(self)
		QGraphicsItem.__init__(self, parent)
		self.setAcceptHoverEvents(True)
		
		self.direction = direction
		self.bgColor = MoveButton.BG_COLOR
		self.lineColor = MoveButton.LINE_COLOR
		
	def boundingRect(self) -> QRectF:
		"""
		Get the bounding rectangle for the button.
		
		:return: The bounding rectangle for the button
		:rtype: QRectF
		"""
		x = -MoveButton.WIDTH / 2
		y = -MoveButton.WIDTH / 2
		return QRectF(x-MoveButton.PEN_WIDTH/2,
		              y-MoveButton.PEN_WIDTH/2,
		              MoveButton.WIDTH + MoveButton.PEN_WIDTH,
		              MoveButton.HEIGHT + MoveButton.PEN_WIDTH)
		
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
		"""
		Paint the graphics of the action wrapper including action name, number, and ports.

		:param painter: This draws the widget.
		:type painter: QPainter
		:param option: Option for the style of graphic.
		:type option: QStyleOptionGraphicsItem
		:param widget: Index for the painted graphic.
		:type widget: QWidget
		:return: None
		:rtype: NoneType
		"""
		
		pen = QPen()
		pen.setColor(self.lineColor)
		pen.setWidth(MoveButton.PEN_WIDTH)
		painter.setPen(pen)
		painter.setBrush(self.bgColor)
		
		x = -MoveButton.WIDTH / 2
		y = -MoveButton.HEIGHT / 2
		
		painter.drawRect(x, y, MoveButton.WIDTH, MoveButton.HEIGHT)
		
		# calculate arrow points as if it were facing down, then flip if necessary.
		vertexX = 0
		vertexY = MoveButton.HEIGHT / 4
		leftX = -MoveButton.WIDTH / 4
		leftY = -MoveButton.HEIGHT / 4
		rightX = MoveButton.WIDTH / 4
		rightY = -MoveButton.HEIGHT / 4
		
		if self.direction == MoveButton.Direction.Up:
			vertexX *= -1
			vertexY *= -1
			leftX *= -1
			leftY *= -1
			rightX *= -1
			rightY *= -1
			
		painter.drawLine(vertexX, vertexY, rightX, rightY)
		painter.drawLine(vertexX, vertexY, leftX, leftY)
		
	def hoverEnterEvent(self, event) -> None:
		"""
		darken button when hovered over.
		
		:param event: The hover event.
		:type event: QGraphicsSceneHoverEvent
		:return: None
		:rtype: NoneType
		"""
		self.bgColor = MoveButton.BG_COLOR_ON_HOVER
		self.lineColor = MoveButton.LINE_COLOR_ON_HOVER
		self.update()
	
	def hoverLeaveEvent(self, event) -> None:
		"""
		lighten button when the mouse leaves the button.

		:param event: The hover event.
		:type event: QGraphicsSceneHoverEvent
		:return: None
		:rtype: NoneType
		"""
		self.bgColor = MoveButton.BG_COLOR
		self.lineColor = MoveButton.LINE_COLOR
		self.update()
		
	def mousePressEvent(self, event) -> None:
		"""
		When the left mouse button is clicked, emit the clicked signal
		
		:param event: the event sent to the item when it is clicked.
		:type event: QGraphicsSceneMouseEvent
		:return: None
		:rtype: NoneType
		"""
		
		if event.buttons() != Qt.LeftButton:
			return
		self.clicked.emit()