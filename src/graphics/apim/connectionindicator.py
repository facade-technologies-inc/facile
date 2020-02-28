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
	
This module contains the ActionIndicator class which is used to show a potential wire connection.
"""

from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtCore import QPointF, QRectF
from PySide2.QtGui import QColor, QPen, Qt

class ConnectionIndicator(QGraphicsItem):
	"""
	This class is used to show a potential wire connection if the user drags between two ports.
	"""
	
	PEN_WIDTH = 5
	BASE_COLOR = QColor(0, 0, 255)
	GOOD_COLOR = QColor(0, 255, 0)
	BAD_COLOR  = QColor(255, 0, 0)
	
	def __init__(self, parent: 'ActionPipelineGraphics'):
		"""
		Constructs a ConnectionIndicator class
		
		:param parent: The ActionPipelineGraphics class that the indicator belongs to.
		:type parent: ActionPipelineGraphics
		"""
		QGraphicsItem.__init__(self, parent)
		self._srcPoint = QPointF(0,0)
		self._destPoint = QPointF(0,0)
		self.setZValue(100) # stack on top of all siblings
		self.color = ConnectionIndicator.BASE_COLOR
		
	def setColor(self, color: QColor) -> None:
		"""
		Sets the color of the indicator.
		
		:param color: The color of the indicator
		:type color: QColor
		:return: None
		:rtype: NoneType
		"""
		self.color = color
		
	def setSrc(self, point: QPointF) -> None:
		"""
		Sets the source position of the indicator.
		
		:param point: The point to set the source to.
		:type point: QPointF
		:return: None
		:rtype: NoneType
		"""
		self._srcPoint = point
		
	def setDest(self, point: QPointF) -> None:
		"""
		Sets the destination position of the indicator.

		:param point: The point to set the destination to.
		:type point: QPointF
		:return: None
		:rtype: NoneType
		"""
		self._destPoint = point
		
	def boundingRect(self) -> QRectF:
		"""
		Gets the bounding rectangle of the indicator.
		
		:return: The bounding rectangle of the indicator
		:rtype: QRectF
		"""
		x = min(self._srcPoint.x(), self._destPoint.x()) - ConnectionIndicator.PEN_WIDTH / 2
		y = min(self._srcPoint.y(), self._destPoint.y()) - ConnectionIndicator.PEN_WIDTH / 2
		width = abs(self._srcPoint.x() - self._destPoint.x()) + ConnectionIndicator.PEN_WIDTH
		height = abs(self._destPoint.y() - self._destPoint.y()) + ConnectionIndicator.PEN_WIDTH
		return QRectF(x, y, width, height)
		
	def paint(self, painter, options, widget):
		pen = QPen()
		pen.setColor(self.color)
		pen.setStyle(Qt.DashLine)
		pen.setCapStyle(Qt.RoundCap)
		pen.setWidth(ConnectionIndicator.PEN_WIDTH)
		painter.setPen(pen)
		painter.drawLine(self._srcPoint, self._destPoint)
		