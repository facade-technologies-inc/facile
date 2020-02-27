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
from graphics.apim.actionwrappergraphics import ActionWrapperGraphics
from graphics.apim.wiregraphics import WireGraphics
from graphics.apim.portgraphics import PortGraphics


class ActionPipelineGraphics(ActionGraphics):

	SIDE_MARGIN = 50
	V_SPACE = 50
	HORIZONTAL_ROW_BUFFER = 5
	
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
	def updateGraphics(self) -> None:
		"""
		Updates the graphics and all sub-graphics for the action pipeline.
		
		starts by updating the sub-actions, then sub-wires, then calls teh same method but in the
		ActionGraphics class to update the ports.
		
		:return: None
		:rtype: NoneType
		"""
		self.prepareGeometryChange()
		self.updateActionGraphics()
		ActionGraphics.updateGraphics(self)
		self.updateWireGraphics()
	
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
				newActionGraphics = ActionWrapperGraphics(refAction, self)
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
			
		self.placeActions()
	
	def getPortGraphics(self, port: 'Port') -> PortGraphics:
		"""
		Gets the port graphics for any port that is owned by either this action pipeline or any
		actions inside of the this action pipeline.
		
		.. note:: This function returns None if the port was not found.
		
		:param port: The port to get the PortGraphics for.
		:type port: Port
		:return: The PortGraphics for the port
		:rtype: PortGraphics
		"""
		
		pm = {}
		pm.update(self._inputPortMapping)
		pm.update(self._outputPortMapping)
		for a in self._actionGraphics:
			pm.update(a._inputPortMapping)
			pm.update(a._outputPortMapping)
			
		return pm[port]
		
		pg = ActionGraphics.getPortGraphics(self, port)
		if pg is not None:
			return pg
		
		else:
			for action in self._actionGraphics:
				pg = action.getPortGraphics(port)
				if pg:
					return pg
		
		raise Exception("Port Graphics not found!")

	def updateWireGraphics(self) -> None:
		"""
		Syncs the internal wire graphics with the action pipeline's internal wires.

		:return: None
		:rtype: NoneType
		"""
		
		newOrdering = []

		columnAssignmentLedger, rowAssignmentLedger = self.allocateWireLanes()
		
		# map all of the wires to wire graphics.
		for refWire in self._action.getWireSet().getWires():

			# create new wire graphics that aren't already in the mapping.
			if refWire not in self._wireMapping:
				newWireGraphics = WireGraphics(refWire, self)
				self._wireGraphics.append(newWireGraphics)
				self._wireMapping[refWire] = newWireGraphics

			srcAction = refWire.getSourcePort().getAction().getName()
			srcPort = refWire.getSourcePort().getName()
			dstAction = refWire.getDestPort().getAction().getName()
			dstPort = refWire.getDestPort().getName()
			msg = "WIRE! {}: {} -> {}: {}".format(srcAction, srcPort, dstAction, dstPort)
			print(msg)

			# update any wire graphics that are already in the mapping.
			srcPortGraphics = self.getPortGraphics(refWire.getSourcePort())
			dstPortGraphics = self.getPortGraphics(refWire.getDestPort())

			# Generate the current wire's graphics.
			# Need to determine the wire's starting and ending "rows". A row falls between sub actions.
			if refWire.getSourcePort().getAction() == self._action:
				# If current wire's srcPort belongs to this action, wire's srcActionRow = 0.
				srcActionRow = 0
			else:
				srcActionGFX = self._actionMapping[refWire.getSourcePort().getAction()]
				srcActionRow = self._actionGraphics.index(srcActionGFX) + 1

			if refWire.getDestPort().getAction == self._action:
				# If current wire's dstPort belongs to this action, wire's dstActionRow = # of actions + 1.
				dstActionRow = len(self._actionGraphics) + 1
			else:
				dstActionGFX = self._actionMapping[refWire.getDestPort().getAction()]
				dstActionRow = self._actionGraphics.index(dstActionGFX)
			self._wireMapping[refWire].updateGraphics(srcPortGraphics, dstPortGraphics, srcActionRow, dstActionRow,
													  columnAssignmentLedger, rowAssignmentLedger)
			
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
		selfx, selfy, width, height = self.getActionRect(inputs, outputs)
		
		offset = (ActionGraphics.MAX_HEIGHT + PortGraphics.TOTAL_HEIGHT)/2 + ActionPipelineGraphics.V_SPACE
		
		for i in range(len(self._actionGraphics)):
			actionGraphics = self._actionGraphics[i]
			actionHeight = ActionGraphics.MAX_HEIGHT + ActionPipelineGraphics.V_SPACE
			y = selfy + i * actionHeight + offset
			
			msg = "{} -> ({}, {})".format(actionGraphics.getAction().getName(), str(0), str(y))
			print("Moving Internal Action:", msg)
			
			actionGraphics.setPos(0, y)
			actionGraphics.updateMoveButtonVisibility()

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
		maxChildWidth = 0
		numActions = len(self._actionGraphics)

		for actionGraphics in self._actionGraphics:
			br = actionGraphics.boundingRect()
			curChildWidth = br.width() + ActionPipelineGraphics.SIDE_MARGIN*2
			maxChildWidth = max(maxChildWidth, curChildWidth)

		height = ActionGraphics.MAX_HEIGHT * numActions + \
				 ActionPipelineGraphics.V_SPACE * (numActions + 1) + \
				 PortGraphics.TOTAL_HEIGHT
			
		self._width = max(self._width, maxChildWidth)
		self._height = height

		x = -self._width/2
		y = -self._height/2
		
		return x, y, self._width, self._height
	
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

	def allocateWireLanes(self) -> '(dict[str: list[int]], dict[int: list[int]])':
		wires = [wire for wire in self._action.getWireSet().getWires()]
		colLanes = {"leftColumn": [0, 0], "rightColumn": [0, 0]}  # {col: [total_lanes, lanes_assigned], ...}
		rowLanes = {i: [0, 0] for i in range(len(wires)+1)}  # {row: [total_lanes, lanes_assigned], ...}

		# Heuristic: For the columns to the sides of the actions, just allocate ~1/2 as many lanes as there are wires.
		colLanes["leftColumn"][0] = (len(wires)//2) + 1
		colLanes["rightColumn"][0] = (len(wires)//2) + 1

		# Heuristic: Between actions, just allocate as many lanes as there are adjacent ports.
		if len(self._actionGraphics) > 0:
			# Allocate lanes between the ActionPipeline's input and the first sub Action.
			numPipelineInputs = len(self._action.getInputPorts())
			numfirstSubActionInputs = len(self._actionGraphics[0].getAction().getInputPorts())
			numFirstRowLanes = numPipelineInputs + numfirstSubActionInputs
			rowLanes[0][0] = numFirstRowLanes

			# Allocate lanes between the ActionPipeline's output and the last sub Action.
			numPipelineOutputs = len(self._action.getOutputPorts())
			numLastSubActionOutputs = len(self._actionGraphics[-1].getAction().getOutputPorts())
			numLastRowLanes = numPipelineOutputs + numLastSubActionOutputs
			#print(rowLanes.keys())
			rowLanes[len(rowLanes.keys())-1][0] = numLastRowLanes

			# Allocate lanes between sub Actions.
			if len(self._actionGraphics) > 1:
				for i in range(0, len(self._actionGraphics)-1):
					# Allocate Lanes between ith and (i+1)=jth sub actions.
					numIthOutputs = len(self._actionGraphics[i].getAction().getOutputPorts())
					numJthInputs = len(self._actionGraphics[i+1].getAction().getInputPorts())
					numRowLanes = numIthOutputs + numJthInputs
					rowLanes[i+1][0] = numRowLanes

		return colLanes, rowLanes


	# An unfinished, more complicated (but maybe better?) alternative to allocateWireLanes.
	# def allocateWireLanes(self, wires, actions) -> (dict, dict):
	# 	colLanes = {"left": [0, 0], "right": [0, 0]}         # {col: [total_lanes, lanes_unassigned], ...}
	# 	rowLanes = {i: [0, 0] for i in range(len(wires)+1)}  # {row: [total_lanes, lanes_unassigned], ...}
	#
	# 	# Iterate through the wires, examine their source and destination actions, allocate lanes accordingly.
	# 	for wire in wires:
	# 		srcAction = wire.getSourcePort().getAction()
	# 		dstAction = wire.getDestPort().getAction()
	#
	# 		# If source action is adjacent to destination action.
	# 		srcActionGFX = self._actionMapping[srcAction]  # ...may not work if wire connected to the input/output of self.
	# 		dstActionGFX = self._actionGraphics[dstAction]
	# 		assert(srcActionGFX in self._actionGraphics)
	# 		assert(dstActionGFX in self._actionGraphics)
	# 		if self._actionGraphics.index(dstActionGFX) == self._actionGraphics.index(srcActionGFX) + 1:
	# 			# This wire goes between adjacent actions. Add a lane in between actions.
	# 			rowIndex = self._actionGraphics.index(srcActionGFX)
