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

from PySide2.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem
from PySide2.QtGui import QPainter, QColor
from PySide2.QtCore import QRectF, Slot

from graphics.apim.actiongraphics import ActionGraphics
from graphics.apim.wiregraphics import WireGraphics



class ActionPipelineGraphics(ActionGraphics):
	
	VERTICAL_SPACING = 50
	SIDE_MARGIN = 50
	
	def __init__(self, actionPipeline: 'ActionPipeline', parent=None) -> 'ActionPipelineGraphics':
		"""
		Constructs a Action Graphics object for the given action.

		:param actionPipeline: The action pipeline for which this graphics item represents.
		:type actionPipeline: ActionPipeline
		:param parent: The parent graphics item
		:type parent: QGraphicsItem
		:return: The graphics of the action pipeline.
		:rtype: ActionPipelineGraphics
		"""
		ActionGraphics.__init__(self, actionPipeline, parent)
		
		self._actionGraphics = []
		self._wireGraphics = []
		
		self._actionMapping = {}
		self._wireMapping = {}
		
		ActionPipelineGraphics.updateGraphics(self)
	
	@Slot()
	def updateGraphics(self):
		self.prepareGeometryChange()
		self.updateActionGraphics()
		self.updateWireGraphics()
		return ActionGraphics.update(self)
	
	def updateActionGraphics(self) -> None:
		"""
		Syncs the internal action graphics with the action pipeline's internal actions.
		
		:return: None
		:rtype: NoneType
		"""
		
		newOrdering = []
		
		# map all of the actions to action graphics.
		for refAction in self._action.getActions():
			
			# update any action graphics that are already in the mapping.
			if refAction in self._actionMapping:
				self._actionMapping[refAction].updateGraphics()
			
			# create new action graphics that aren't already in the mapping.
			else:
				newActionGraphics = ActionGraphics(refAction, self)
				self._actionGraphics.append(newActionGraphics)
				self._actionMapping[refAction] = newActionGraphics
			
			newOrdering.append(self._actionMapping[refAction])
		
		# remove any actions that don't exist in the reference action pipeline.
		for actionGraphics in self._actionGraphics[:]:
			if actionGraphics not in newOrdering:
				self._actionGraphics.remove(actionGraphics)
				actionGraphics.scene().removeItem(actionGraphics)
		
		# maintain correct ordering of action graphics
		self._actionGraphics.clear()
		for actionGraphics in newOrdering:
			self._actionGraphics.append(actionGraphics)
	
	def updateWireGraphics(self) -> None:
		"""
		Syncs the internal wire graphics with the action pipeline's internal wires.

		:return: None
		:rtype: NoneType
		"""
		
		newOrdering = []
		
		# map all of the wires to wire graphics.
		for refWire in self._action.getWireSet().getWires():
			
			# update any wire graphics that are already in the mapping.
			if refWire in self._wireMapping:
				self._actionMapping[refWire].updateGraphics()
			
			# create new wire graphics that aren't already in the mapping.
			else:
				newWireGraphics = WireGraphics(refWire, self)
				self._wireGraphics.append(newWireGraphics)
				self._wireMapping[refWire] = newWireGraphics
			
			newOrdering.append(self._wireMapping[refWire])
		
		# remove any wire graphics that don't exist in the reference wires.
		for wireGraphics in self._wireGraphics[:]:
			if wireGraphics not in newOrdering:
				self._wireGraphics.remove(wireGraphics)
				wireGraphics.scene().removeItem(wireGraphics)
		
		# maintain correct ordering of wire graphics
		self._wireGraphics.clear()
		for wireGraphics in newOrdering:
			self._wireGraphics.append(wireGraphics)
	
	def placeActions(self) -> None:
		"""
		Moves all of the sub-actions to their proper positions.
		
		:return: None
		:rtype: NoneType
		"""
		inputs = self._action.getInputPorts()
		outputs = self._action.getOutputPorts()
		for i in range(len(self._actionGraphics)):
			actionGraphics = self._actionGraphics[i]
			actionGraphics.setPos(0, -(i+1) * actionGraphics.boundingRect().height() +
			                      self.getActionRect(inputs, outputs)[3]/2)
			
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
		x, y, width, height = ActionGraphics.getActionRect(self, inputPorts, outputPorts)
		
		# resize the action to fit all actions and wires inside.
		count = 0
		maxChildWidth = 0
		for actionGraphics in self._actionGraphics:
			br = actionGraphics.boundingRect()
			y -= br.height()/2 - 50
			height += br.height() + 100
			count += 1
			maxChildWidth = max(maxChildWidth, br.width() + ActionPipelineGraphics.SIDE_MARGIN)
			
		self._width = width #max(width, maxChildWidth)
		self._height = height
		
		x = -width/2
		y = -height/2
		
		return x, y, width, height
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		"""
		Paint the graphics of the action pipeline with ports, wires, and internal graphics.

		:param painter: This draws the widget.
		:type painter: QPainter
		:param option: Option for the style of graphic.
		:type option: QStyleOptionGraphicsItem
		:param index: Index for the painted graphic.
		:type index: QWidget
		:return: None
		:rtype: NoneType
		"""
		
		self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts())
		ActionGraphics.paint(self, painter, option, index)
		self.placeActions()