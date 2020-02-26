"""
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

from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtCore import QPointF, QRectF
from PySide2.QtGui import QColor, QPen

class ConnectionIndicator(QGraphicsItem):
	
	PEN_WIDTH = 5
	COLOR = QColor(50, 100, 200)
	
	def __init__(self, parent):
		QGraphicsItem.__init__(self, parent)
		self._srcPoint = QPointF(0,0)
		self._destPoint = QPointF(0,0)
		
	def setSrc(self, point):
		self._srcPoint = point
		
	def setDest(self, point):
		self._destPoint = point
		
	def boundingRect(self):
		x = min(self._srcPoint.x(), self._destPoint.x()) - ConnectionIndicator.PEN_WIDTH / 2
		y = min(self._srcPoint.y(), self._destPoint.y()) - ConnectionIndicator.PEN_WIDTH / 2
		width = abs(self._srcPoint.x() - self._destPoint.x()) + ConnectionIndicator.PEN_WIDTH
		height = abs(self._destPoint.y() - self._destPoint.y()) + ConnectionIndicator.PEN_WIDTH
		return QRectF(x, y, width, height)
		
	def paint(self, painter, options, widget):
		
		pen = QPen()
		pen.setColor(ConnectionIndicator.COLOR)
		pen.setWidth(ConnectionIndicator.PEN_WIDTH)
		
		painter.drawLine(self._srcPoint, self._destPoint)
		