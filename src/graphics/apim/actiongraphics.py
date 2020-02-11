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

This module contains the ActionGraphics() Class.
"""

import sys
import math

from PySide2.QtWidgets import QGraphicsItem, QApplication, QGraphicsView, QGraphicsScene, \
	QWidget, QStyleOptionGraphicsItem
from PySide2.QtGui import QPainter, QPainterPath, QColor
from PySide2.QtCore import QRectF
from graphics.apim.portgraphics import PortGraphics
from data.apim.action import Action
from data.apim.componentaction import ComponentAction
from data.apim.port import Port

class ActionGraphics(QGraphicsItem):
	"""
	This class defines the graphics for displaying a action in the ActionMenuItem view.
	"""
	
	PEN_WIDTH = 1.0
	MIN_WIDTH = 200
	SPACE = PortGraphics.WIDTH * 2
	TOTAL_PORT_WIDTH = PortGraphics.WIDTH + SPACE
	TOTAL_RECT_HEIGHT = PortGraphics.TOTAL_HEIGHT + 50
	
	def __init__(self, action: 'Action', parent=None) -> 'ActionGraphics':
		"""
		Constructs a Action Graphics object for the given action.
		
		:param action: The action for which this graphics item represents.
		:type action: Action
		:param parent: None
		:type parent: Nonetype
		:return: The graphics of an action.
		:rtype: ActionGraphics
		"""
		QGraphicsItem.__init__(self, parent)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self._action = action
		self._inputPortGraphics = [PortGraphics(p, self) for p in self._action.getInputPorts()]
		self._outputPortGraphics = [PortGraphics(p, self) for p in self._action.getOutputPorts()]
	
	def boundingRect(self) -> QRectF:
		"""
		This function defines the outer bounds of the actions icon.
		
		:return: Creates the bounds for the graphics.
		:rtype: QRectF
		"""
		
		inputPorts = self._action.getInputPorts()
		outputPorts = self._action.getOutputPorts()
		
		x,y,width,height = self.getActionRect(inputPorts,outputPorts)
		
		if inputPorts:
			height += PortGraphics.TOTAL_HEIGHT/2
			y -= PortGraphics.TOTAL_HEIGHT/2
		if outputPorts:
			height += PortGraphics.TOTAL_HEIGHT/2
			
		width += ActionGraphics.PEN_WIDTH
		height += ActionGraphics.PEN_WIDTH
		
		return QRectF(x, y, width, height)
	
	def getActionRect(self, inputPorts: QGraphicsItem, outputPorts: QGraphicsItem) -> list:
		"""
		Gets the bounding rect of the action.
		
		:param inputPorts: Input ports added for the action.
		:type: QGraphicsItem
		:param outputPorts: Output ports added for the action.
		:type: QGraphicsItem
		:return: List of coordinates and dimensions for the bounding rect of the action.
		:rtype: list
		"""
		halfPenWidth = ActionGraphics.PEN_WIDTH / 2
		maxPorts = max(len(inputPorts), len(outputPorts))
		
		width = max(ActionGraphics.TOTAL_PORT_WIDTH * maxPorts, ActionGraphics.MIN_WIDTH)
		height = ActionGraphics.TOTAL_RECT_HEIGHT
		
		x = (-0.5 * width) - halfPenWidth
		y = (-0.5 * height) - halfPenWidth
		
		self._width = width
		self._height = height
		
		return x, y, width, height
		
	def shape(self) -> QPainterPath:
		"""
		Defines the shape of the action icon.
		
		:return: Returns the shape of the action icon.
		:rtype: QPainterPath
		"""
		return QGraphicsItem.shape(self)
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		"""
		Paint the graphics of the action with the ports.

		:param painter: This draws the widget.
		:type painter: QPainter
		:param option: Option for the style of graphic.
		:type option: QStyleOptionGraphicsItem
		:param index: Index for the painted graphic.
		:type index: QWidget
		:return: None
		:rtype: NoneType
		"""
		
		self.placePorts()
		painter.setBrush(QColor(88, 183, 255))
		x, y, width, height = self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts() )
		painter.drawRect(QRectF(x, y, width, height))
		

		
	def placePorts(self) -> None:
		"""
		Place the ports at the right positions on the actions.
		
		:return: None
		:rtype: NoneType
		"""
		
		def spread(y: int , portList: list) -> None:
			"""
			Spreads a single port list evenly.
			
			:param y: The coordinate the ports need to be placed.
			:type: int
			:param portList: The list of ports that need to be placed.
			:type: list
			:return: None
			:rtype: NoneType
			"""
			offset = 0 # offset from center
			if len(portList) % 2 == 0:
				offset = ActionGraphics.TOTAL_PORT_WIDTH / 2
				
			halfLen = (len(portList) - 1) / 2
			for p in range(len(portList)):
				posIdx = math.ceil(halfLen + p)
				negIdx = math.floor(halfLen - p)
				
				posShift = p * ActionGraphics.TOTAL_PORT_WIDTH + offset
				negShift = -posShift
				
				try:
					portList[posIdx].setPos(posShift, y)
					portList[negIdx].setPos(negShift, y)
				except IndexError:
					return
				
		spread(-ActionGraphics.TOTAL_RECT_HEIGHT / 2, self._inputPortGraphics)
		spread(ActionGraphics.TOTAL_RECT_HEIGHT / 2, self._outputPortGraphics)
		
		
if __name__ == "__main__":
	app = QApplication()
	v = QGraphicsView()
	s = QGraphicsScene()
	v.setScene(s)
	action = ComponentAction()
	p1 = Port()
	p2 = Port()
	p3 = Port()
	action.addInputPort(p1)
	action.addInputPort(p2)
	action.addOutputPort(p3)
	
	A = ActionGraphics(action)
	s.addItem(A)
	v.show()
	sys.exit(app.exec_())