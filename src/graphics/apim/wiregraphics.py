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
			
		print("Points:")
		for x,y in self._pathPoints:
			print("\t", x, y)

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

		#print(srcRow, dstRow)
		#To get the action pipeline graphics -> self.getParent()

		# Set the source point.
		self._pathPoints.append((srcPosition.x(), srcPosition.y() + PortGraphics.TOTAL_HEIGHT/2))

		# TODO: add intermediate points.
		# Move down to first allocated row lane. # TODO Right now just going to middle of the row.
		prevX = self._pathPoints[-1][0]
		prevY = self._pathPoints[-1][1]
		nextY = prevY + apg.ActionPipelineGraphics.V_SPACE / 2
		self._pathPoints.append((prevX, nextY))

		# Does this wire move between adjacent actions?
		# If so, cut over above the destination port's x coordinate.
		if srcRow == dstRow:
			prevY = self._pathPoints[-1][1]
			self._pathPoints.append((destPosition.x(), prevY))
		# Else, decide which column to use, cut over to first available lane in the column,
		# move down to lane in destination row, cut over above the destination port.
		else:
			pass

		# Set the destination point.
		#self._pathPoints.append((destPosition.x(), destPosition.y() - PortGraphics.TOTAL_HEIGHT/2))

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
	act2 = ActionPipeline()

	prt1_1 = Port()
	prt2_1 = Port()
	prt3_1 = Port()
	prt1_2 = Port()
	prt2_2 = Port()
	prt3_2 = Port()

	act1.addInputPort(prt1_1)
	#act1.addInputPort(prt2_1)
	act1.addOutputPort(prt3_1)

	act2.addInputPort(prt1_2)
	act2.addOutputPort(prt2_2)
	act2.addInputPort(prt3_2)

	aw1 = ActionWrapper(act1, actPipeline)
	aw2 = ActionWrapper(act2, actPipeline)

	actPipeline.connect(actPipeline.getInputPorts()[0], aw1.getInputPorts()[0])
	actPipeline.connect(aw1.getOutputPorts()[0], aw2.getInputPorts()[0])

	# Create the graphics.
	actPipelineGFX = actPipelineGrfxModule.ActionPipelineGraphics(actPipeline)
	s.addItem(actPipelineGFX)

	v.show()
	sys.exit(app.exec_())