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
# For test script.########
import sys
import os
sys.path.append(os.path.abspath("../../"))
sys.path.append(os.path.abspath("../../gui/rc/"))
##########################

from typing import Dict, List
from PySide2.QtWidgets import QWidget, QGraphicsItem, QStyleOptionGraphicsItem, QApplication, QGraphicsView, \
	QGraphicsScene, QAbstractGraphicsShapeItem
from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QPainter, QColor, QPen, QPainterPathStroker

from data.apim.wire import Wire
from graphics.apim.portgraphics import PortGraphics
import graphics.apim.actionpipelinegraphics as apg

# For test script. ##########
from data.apim.actionpipeline import ActionPipeline
import graphics.apim.actionpipelinegraphics as actPipelineGrfxModule
from data.apim.port import Port
from data.apim.actionwrapper import ActionWrapper
#############################


class WireGraphics(QAbstractGraphicsShapeItem):
	"""

	"""

	PEN_WIDTH = 5
	COLOR = QColor(0,0,0)
	COLOR_ON_SELECTED = QColor(0, 255, 0)

	def __init__(self, wire: 'Wire', actPipelineGFX: "ActionPipelineGraphics" = None):
		"""
		Constructs a WireGraphics object between the given port graphics. Also creates the underlying Wire in the APIM.

		:param wire:
		:type wire:
		:param actPipelineGFX: This is the WireGraphics' parent QGraphicsItem used to instantiate the super class.
		Also used to get a reference to the ActionPipeline for adding newly created wires to the underlying data.
		:type actPipelineGFX: ActionPipelineGraphics
		"""

		QAbstractGraphicsShapeItem.__init__(self, actPipelineGFX)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self._wire = wire
		self._pathPoints = []

	def boundingRect(self) -> QRectF:
		xVals = [x for x, y in self._pathPoints]
		yVals = [y for x, y in self._pathPoints]

		xMax = max(xVals)
		yMax = max(yVals)
		xMin = min(xVals)
		yMin = min(yVals)

		width = xMax - xMin + WireGraphics.PEN_WIDTH
		height = yMax - yMin + WireGraphics.PEN_WIDTH
		x = xMin - WireGraphics.PEN_WIDTH / 2
		y = yMin - WireGraphics.PEN_WIDTH / 2

		return QRectF(x, y, width, height)


	def shape(self) -> QPainterPath:
		"""
		Stroke the shape of the line.

		:return: the arrow path
		:rtype: QPainterPathStroker
		"""
		path = self.buildPath()

		stroker = QPainterPathStroker()
		stroker.setWidth(10)

		return stroker.createStroke(path).simplified()

	def buildPath(self):
		path = QPainterPath()
		path.moveTo(*self._pathPoints[0])
		for point in self._pathPoints[1:]:
			path.lineTo(*point)
			
		# print("Points:")
		# for x,y in self._pathPoints:
		# 	print("\t", x, y)

		return path

	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		path = self.buildPath()

		pen = QPen()
		pen.setWidth(WireGraphics.PEN_WIDTH)
		if self.isSelected():
			pen.setColor(WireGraphics.COLOR_ON_SELECTED)
		else:
			pen.setColor(WireGraphics.COLOR)

		painter.setPen(pen)
		painter.drawPath(path)

	def updateGraphics(self, srcPortGraphics: 'PortGraphics', destPortGraphics: 'PortGraphics', srcRow: int,
					   dstRow: int, colAssignmentLedger: Dict[str, List[int]],
					   rowAssignmentLedger: Dict[int, List[int]]):
		srcPosition = srcPortGraphics.scenePos()
		destPosition = destPortGraphics.scenePos()

		# Claim lanes on the row ledger.
		rowAssignmentLedger[srcRow][1] += 1
		if srcRow != dstRow:
			rowAssignmentLedger[dstRow][1] += 1

		# Set the source point.
		self._pathPoints.append((srcPosition.x(), srcPosition.y() + PortGraphics.TOTAL_HEIGHT/2))

		# TODO: add intermediate points.
		# Move down to first allocated row lane.
		prevX = self._pathPoints[-1][0]
		prevY = self._pathPoints[-1][1]
		rowSpace = apg.ActionPipelineGraphics.V_SPACE
		laneOffset = (rowSpace / (rowAssignmentLedger[srcRow][0]+1)) * rowAssignmentLedger[srcRow][1]
		nextY = prevY + laneOffset
		self._pathPoints.append((prevX, nextY))

		# Does this wire move between adjacent actions?
		# If so, cut over above the destination port's x coordinate.
		if srcRow == dstRow:
			prevY = self._pathPoints[-1][1]
			self._pathPoints.append((destPosition.x(), prevY))
		# Else, decide which column to use, cut over to first available lane in the column,
		# move down to lane in destination row, cut over above the destination port.
		else:
			prevX = self._pathPoints[-1][0]
			prevY = self._pathPoints[-1][1]
			actPipeWidth = self.parentItem().getWidth()
			if srcPosition.x() < 0:
				# Source port is biased left. Go left.
				# Claim lane on the Column ledger.
				colAssignmentLedger["leftColumn"][1] += 1

				laneOffset = (rowSpace / (colAssignmentLedger["leftColumn"][0]+1)) \
							 * colAssignmentLedger["leftColumn"][1]
				leftDist = actPipeWidth / 2 - abs(srcPosition.x()) - apg.ActionPipelineGraphics.SIDE_MARGIN
				self._pathPoints.append((prevX - leftDist - laneOffset, prevY))
			else:
				# Source port is biased right or centered. Go right.
				# Claim lane on the Column ledger.
				colAssignmentLedger["rightColumn"][1] += 1

				laneOffset = (rowSpace / (colAssignmentLedger["rightColumn"][0] + 1)) \
							 * colAssignmentLedger["rightColumn"][1]
				rightDist = actPipeWidth / 2 - srcPosition.x() - apg.ActionPipelineGraphics.SIDE_MARGIN
				self._pathPoints.append((prevX + rightDist + laneOffset, prevY))

			# Move down to destination row. -> V_Space above destination port's y.
			prevX = self._pathPoints[-1][0]
			newY = (destPosition.y() - PortGraphics.TOTAL_HEIGHT/2) - apg.ActionPipelineGraphics.V_SPACE
			laneOffset = (rowSpace / (rowAssignmentLedger[dstRow][0] + 1)) * rowAssignmentLedger[dstRow][1]
			self._pathPoints.append((prevX, newY + laneOffset))

			# Move over to above the destination port.
			prevY = self._pathPoints[-1][1]
			self._pathPoints.append((destPosition.x(), prevY))

		# Set the destination point.
		self._pathPoints.append((destPosition.x(), destPosition.y() - PortGraphics.TOTAL_HEIGHT/2))

		#self.prepareGeometryChange()


if __name__ == "__main__":
	app = QApplication()
	v = QGraphicsView()
	v.setGeometry(500, 500, 500, 500)
	s = QGraphicsScene()
	v.setScene(s)

	# Create top-level actionPipeline.
	actPipeline = ActionPipeline()

	# Add some ports to it.
	inPort1 = Port()
	inPort2 = Port()
	outPort1 = Port()
	actPipeline.addInputPort(inPort1)
	actPipeline.addInputPort(inPort2)
	actPipeline.addOutputPort(outPort1)

	#Sub-Actions
	act1 = ActionPipeline()
	act1.setName("action pipeline 1")
	act2 = ActionPipeline()
	act2.setName("action pipeline 2")

	prt1_1 = Port()
	prt2_1 = Port()
	prt3_1 = Port()
	prt1_2 = Port()
	prt2_2 = Port()
	prt3_2 = Port()

	act1.addInputPort(prt1_1)
	#act1.addInputPort(prt2_1)
	act1.addOutputPort(prt3_1)
	prt3_1.setName("OUTPUT")

	act2.addInputPort(prt1_2)
	act2.addOutputPort(prt2_2)
	act2.addInputPort(prt3_2)

	aw1 = ActionWrapper(act1, actPipeline)
	aw2 = ActionWrapper(act2, actPipeline)

	actPipeline.connect(actPipeline.getInputPorts()[1], actPipeline.getOutputPorts()[0])
	actPipeline.connect(aw1.getOutputPorts()[0], aw2.getInputPorts()[0])
	actPipeline.connect(actPipeline.getInputPorts()[0], aw2.getInputPorts()[1])
	actPipeline.connect(actPipeline.getInputPorts()[1], aw1.getInputPorts()[0])

	# Create the graphics.
	actPipelineGFX = actPipelineGrfxModule.ActionPipelineGraphics(actPipeline)
	s.addItem(actPipelineGFX)

	v.show()
	sys.exit(app.exec_())