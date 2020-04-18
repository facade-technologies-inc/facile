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

from typing import Dict, List

from PySide2.QtWidgets import QGraphicsItem, QApplication, QGraphicsView, QGraphicsScene, \
	QWidget, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent
from PySide2.QtGui import QPainter, QPainterPath, QColor, Qt
from PySide2.QtCore import QRectF, Slot, SIGNAL, QObject
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
	H_SPACE = PortGraphics.WIDTH * 2
	V_SPACE = 50
	TOTAL_PORT_WIDTH = PortGraphics.WIDTH + H_SPACE
	TOTAL_RECT_HEIGHT = PortGraphics.TOTAL_HEIGHT + V_SPACE
	MAX_HEIGHT = TOTAL_RECT_HEIGHT + PortGraphics.TOTAL_HEIGHT
	
	COLOR = QColor(88, 183, 255)
	
	def __init__(self, action: 'Action', parent=None) -> 'ActionGraphics':
		"""
		Constructs a Action Graphics object for the given action.
		
		:param action: The action for which this graphics item represents.
		:type action: Action
		:param parent: None
		:type parent: NoneType
		:return: The graphics of an action.
		:rtype: ActionGraphics
		"""
		QGraphicsItem.__init__(self, parent)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setCursor(Qt.ArrowCursor)
		self._action = action
		QObject.connect(action, SIGNAL('updated()'), self.updateGraphics)
		
		self.color = ActionGraphics.COLOR
		
		self._inputPortGraphics = []
		self._outputPortGraphics = []
		self._wireGraphics = []
		self._actionGraphics = []
		
		self._inputPortMapping = {}
		self._outputPortMapping = {}
		
		self._interactivePorts = True
		ActionGraphics.updateGraphics(self)

		self._width = 0
		self._height = 0

		
	@Slot()
	def updateGraphics(self) -> None:
		"""
		Updates all graphics and sub-graphics for this action.

		:return: None
		:rtype: NoneType
		"""
		self.prepareGeometryChange()
		self.updatePortGraphics()
		return QGraphicsItem.update(self)

	def getAction(self):
		"""
		Returns the ActionGraphics' Action. Used by WireGraphics to get a reference to the ActionPipeline to add a wire.

		:return: The Action associated with the ActionGraphics.
		:rtype: Action
		"""
		return self._action
	
	def getPortGraphics(self, port: Port) -> PortGraphics:
		"""
		Gets the port graphics for any port that is owned by this action.
		
		.. note:: This function returns None if the port was not found.

		:param port: The port to get the PortGraphics for.
		:type port: Port
		:return: The PortGraphics for the port
		:rtype: PortGraphics
		"""
		pm = {}  # pm: "port Mapping"
		pm.update(self._inputPortMapping)
		pm.update(self._outputPortMapping)
		
		return pm.get(port, None)

	def updatePortGraphics(self) -> None:
		"""
		Creates the port graphics for the action.
		
		:return: None
		:rtype: NoneType
		"""
		
		def synchronizePortList(myPortList: List['PortGraphics'], refPortList: List['Port'],
		                         mapping: Dict['Port', 'PortGraphics']) -> None:
			"""
			Synchronizes either the inputs our outputs of the port graphics with the
			corresponding port list in the action.

			:param myPortList: The list of port graphics in this action to synchronize.
			:type myPortList: List['PortGraphics']
			:param refPortList: The list of ports to synchronize with from the reference action.
			:type refPortList: List['Port']
			:param mapping: Maps the ports in the wrapper to the corresponding port in the reference.
			:type mapping: Dict['Port', 'Port']
			:return: None
			:rtype: NoneType
			"""
			
			assert (myPortList is self._inputPortGraphics or myPortList is self._outputPortGraphics)
			
			newOrdering = []
			
			# map all of the reference ports to port graphics.
			for refPort in refPortList:
				
				# update any port graphics that are already in the mapping.
				if refPort in mapping:
					mapping[refPort].update()
				
				# create new ports that aren't already in the mapping.
				else:
					newPortGraphics = PortGraphics(refPort, self, self._interactivePorts)
					myPortList.append(newPortGraphics)
					mapping[refPort] = newPortGraphics
				
				newOrdering.append(mapping[refPort])
			
			# remove any ports that don't exist in the reference action.
			for portGraphics in myPortList[:]:
				if portGraphics not in newOrdering:
					myPortList.remove(portGraphics)
					portGraphics.scene().removeItem(portGraphics)
			
			# maintain correct ordering of ports
			myPortList.clear()
			for port in newOrdering:
				myPortList.append(port)
		
		synchronizePortList(self._inputPortGraphics, self._action.getInputPorts(), self._inputPortMapping)
		synchronizePortList(self._outputPortGraphics, self._action.getOutputPorts(), self._outputPortMapping)
		self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts())
		self.placePorts()
	
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
		height += max(ActionGraphics.PEN_WIDTH, PortGraphics.REQUIRED_PEN_WIDTH)
		
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
	
	def updateActionRect(self) -> None:
		"""
		Updates the action rectangle's width and height attributes
		
		:return: None
		:rtype: NoneType
		"""
		inputPorts = self._action.getInputPorts()
		outputPorts = self._action.getOutputPorts()
		
		self.getActionRect(inputPorts, outputPorts)
		
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
		painter.setBrush(self.color)
		x, y, width, height = self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts())
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
				
		spread(-self._height / 2, self._inputPortGraphics)
		spread(self._height / 2, self._outputPortGraphics)

	def getHeight(self):
		self.updateActionRect()
		return self._height

	def getWidth(self):
		self.updateActionRect()
		return self._width

	def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
		"""
		When a port is clicked, emit the entitySelected signal from the view.
		:param event: the mouse click event
		:type event: QGraphicsSceneMouseEvent
		:return: None
		"""
		event.accept()

		try:
			self.scene().views()[0].entitySelected.emit(self._action)
		except:
			pass
		
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