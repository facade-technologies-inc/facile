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

This module contains the portGraphics class, which is responsible for rendering ports
in the APIM View.
"""
import sys
import os
sys.path.append(os.path.abspath("../../"))

from PySide2.QtCore import QRectF, QPoint
from PySide2.QtGui import QPainterPath, QPainter, QPolygon, QColor, Qt, QPen
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QApplication, QGraphicsView, QStyleOptionGraphicsItem, \
	QWidget, QGraphicsSceneContextMenuEvent
from qt_models.portmenu import PortMenu
import data.apim.port as port

class PortGraphics(QGraphicsItem):
	"""
	This class defines the graphics for displaying a port in the APIM View.
	A port is shaped somewhat like an inverted, elongated pentagon.
	"""
	
	PEN_WIDTH = 1.0
	WIDTH = 50
	SIDE_HEIGHT = 2 * WIDTH
	TAPER_HEIGHT = 0.5 * SIDE_HEIGHT
	TOTAL_HEIGHT = SIDE_HEIGHT + TAPER_HEIGHT
	# Center the shape about the origin of its coordinate system.
	X_POS = -0.5 * WIDTH
	Y_POS = -0.5 * TOTAL_HEIGHT
	
	PEN_COLOR = QColor(Qt.black)
	BRUSH_COLOR = QColor(252, 140, 3)
	
	def __init__(self, port: 'Port', parent: QGraphicsItem = None):
		"""
		Constructs a portGraphics object for the given Port object.
		:param port: The port for which this graphics item represents.
		:type port: Port
		:param parent: A QGraphicsItem (probably an actionGraphics object)
		:type parent: QGraphicsItem
		"""
		QGraphicsItem.__init__(self, parent)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.menu = PortMenu()
		
		#TODO: What else should be in the constructor ?...
	
	def boundingRect(self) -> QRectF:
		"""
		This pure virtual function defines the outer bounds of the item as a rectangle.
		:return: create the bounding of the item
		:rtype: QRectF
		"""
		halfPenWidth = PortGraphics.PEN_WIDTH / 2
		x = PortGraphics.X_POS - halfPenWidth
		y = PortGraphics.Y_POS - halfPenWidth
		
		actualWidth = PortGraphics.WIDTH + PortGraphics.PEN_WIDTH
		actualHeight = PortGraphics.TOTAL_HEIGHT + PortGraphics.PEN_WIDTH
		
		return QRectF(x, y, actualWidth, actualHeight)
	
	def shape(self) -> QPainterPath:
		"""
		Returns the shape of the Port as a QPainterPath. Ports are shaped like an inverted, elongated pentagon.

		:return: The shape of the Port as a QPainterPath.
		:rtype: QPainterPath
		"""
		# Create the polygon (pentagon-like shape)
		poly = QPolygon()
		poly << QPoint(PortGraphics.X_POS, PortGraphics.Y_POS)
		poly << QPoint(PortGraphics.X_POS + PortGraphics.WIDTH, PortGraphics.Y_POS)
		poly << QPoint(PortGraphics.X_POS + PortGraphics.WIDTH, PortGraphics.Y_POS + PortGraphics.SIDE_HEIGHT)
		poly << QPoint(0, PortGraphics.Y_POS + PortGraphics.TOTAL_HEIGHT)
		poly << QPoint(PortGraphics.X_POS, PortGraphics.Y_POS + PortGraphics.SIDE_HEIGHT)
		poly << QPoint(PortGraphics.X_POS, PortGraphics.Y_POS)

		path = QPainterPath()
		path.addPolygon(poly)
		return path
	
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
		"""
		Paints a port. This function is used implicitly by the QGraphicsView to render a port.
		
		:param painter: The painter to paint with.
		:type painter: QPainter
		:param option: provides style options for the item.
		:type option: QStyleOptionGraphicsItem
		:param widget: QWidget
		:type widget: It points to the widget that is being painted on; or make it = None.
		:return: None
		:rtype: NoneType
		"""

		# Make a Qpen to draw the border. Use different pens if Port is selected.
		pen = QPen(PortGraphics.PEN_COLOR)
		pen.setWidth(PortGraphics.PEN_WIDTH)
		painter.setPen(pen)
		
		painter.setBrush(PortGraphics.BRUSH_COLOR)
		painter.drawPath(self.shape())

	def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
		"""
		Opens a context menu (right click menu) for the component.

		:param event: The event that was generated when the user right-clicked on this item.
		:type event: QGraphicsSceneContextMenuEvent
		:return: None
		:rtype: NoneType
		"""
		self.setSelected(True)
		self.menu.exec_(event.screenPos())

if __name__ == "__main__":
	app = QApplication()
	v = QGraphicsView()
	v.setGeometry(500, 500, 500, 500)
	s = QGraphicsScene()
	v.setScene(s)
	p = PortGraphics(port.Port())
	s.addItem(p)
	v.show()
	sys.exit(app.exec_())