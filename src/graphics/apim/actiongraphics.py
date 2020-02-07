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

from PySide2.QtWidgets import QGraphicsItem, QApplication, QGraphicsView, QGraphicsScene, \
	QWidget, QStyleOptionGraphicsItem
from PySide2.QtGui import QPainter, QPainterPath
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
		self._inputPortGraphics = [PortGraphics(port, self) for port in self._action.getInputPorts()]
		self._outputPortGraphics = [PortGraphics(port, self) for port in self._action.getOutputPorts()]
	
	def boundingRect(self) -> QRectF:
		"""
		This function defines the outer bounds of the actions icon as a rectangle.
		
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
	
	def getActionRect(self, inputPorts, outputPorts):
		halfPenWidth = ActionGraphics.PEN_WIDTH / 2
		maxPorts = max(len(inputPorts), len(outputPorts))
		
		width = max(ActionGraphics.TOTAL_PORT_WIDTH * maxPorts, ActionGraphics.MIN_WIDTH)
		height = ActionGraphics.TOTAL_RECT_HEIGHT
		
		x = (-0.5 * width) - halfPenWidth
		y = (-0.5 * (height + PortGraphics.TOTAL_HEIGHT)) - halfPenWidth
		
		self._width = width
		self._height = height
		
		return x, y, width, height
		
	def shape(self) -> QPainterPath:
		"""
		
		:return:
		"""
		return QGraphicsItem.shape(self)
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		"""
		Paint a checkbox without the label.

		:param painter: This draws the widget.
		:type painter: QStylePainter
		:param option: Option for the style of checkbox.
		:type option: QStyleOptionViewItem
		:param index: Index for the painted checkbox.
		:type index: QModelIndex
		:return: None
		:rtype: NoneType
		"""
		painter.drawRect(self.boundingRect())
		x, y, width, height = self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts() )
		painter.drawRect(QRectF(x, y, width, height))
		self.placePorts()
		
	def placePorts(self):
		
		for p in range(len(self._inputPortGraphics)):
			port = self._inputPortGraphics[p]
			port.setPos(p*ActionGraphics.TOTAL_PORT_WIDTH - self._width/2 + ActionGraphics.SPACE/2,-150)
			
	
	
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