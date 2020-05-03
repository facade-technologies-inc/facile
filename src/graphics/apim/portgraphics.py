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
from PySide2.QtGui import QPainterPath, QPainter, QPolygon, QColor, Qt, QPen, QFont, QFontMetricsF
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QApplication, QGraphicsView, QStyleOptionGraphicsItem, \
	QWidget, QGraphicsSceneContextMenuEvent, QGraphicsTextItem, QGraphicsSceneMouseEvent

from qt_models.portmenu import PortMenu
import data.apim.port as port
from data.apim.actionwrapper import ActionWrapper

class PortGraphics(QGraphicsItem):
	"""
	This class defines the graphics for displaying a port in the APIM View.

	A port is shaped somewhat like an inverted, elongated pentagon.
	"""
	
	REQUIRED_PEN_WIDTH = 5.0
	OPTIONAL_PEN_WIDTH = 1.0
	WIDTH = 50
	SIDE_HEIGHT = 1.5 * WIDTH
	TAPER_HEIGHT = 0.5 * SIDE_HEIGHT
	TOTAL_HEIGHT = SIDE_HEIGHT + TAPER_HEIGHT
	# Center the shape about the origin of its coordinate system.
	X_POS = -0.5 * WIDTH
	Y_POS = -0.5 * TOTAL_HEIGHT
	
	PEN_COLOR = QColor(Qt.black)
	
	INNER_COLOR = QColor(100, 200, 0)
	OUTER_COLOR = QColor(252, 140, 3)
	
	NAME_FONT = QFont("Times", 15)
	TYPE_FONT = QFont("Times", 15)
	
	def __init__(self, port: 'Port', parent: QGraphicsItem = None, menuEnabled: bool = True):
		"""
		Constructs a portGraphics object for the given Port object.
		
		:param port: The port for which this graphics item represents.
		:type port: Port
		:param parent: A QGraphicsItem (probably an actionGraphics object)
		:type parent: QGraphicsItem
		:param menuEnabled: If true, a context menu will be shown on right-click.
		:type menuEnabled: bool
		"""
		QGraphicsItem.__init__(self, parent)
		self.setAcceptDrops(True)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self._port = port
		self._menuEnabled = menuEnabled
		self.menu = PortMenu()
		
		# If port is required and it's an input, make the border thicker
		if not self._port.isOptional() and self._port in self._port.getAction().getInputPorts():
			self.borderWidth = PortGraphics.REQUIRED_PEN_WIDTH
		else:
			self.borderWidth = PortGraphics.OPTIONAL_PEN_WIDTH
			
		# show port name and type
		if self._menuEnabled:
			fm = QFontMetricsF(PortGraphics.NAME_FONT)
			name = fm.elidedText(self._port.getName(), Qt.ElideRight, PortGraphics.SIDE_HEIGHT)
			self.nameItem = QGraphicsTextItem(name, self)
			self.nameItem.setFont(PortGraphics.NAME_FONT)
			self.nameItem.setRotation(90)
			self.nameItem.setPos(PortGraphics.WIDTH/2 + 5,-PortGraphics.TOTAL_HEIGHT/2)
			
			fm = QFontMetricsF(PortGraphics.TYPE_FONT)
			t = fm.elidedText(type(self._port.getDataType()).__name__, Qt.ElideRight, PortGraphics.SIDE_HEIGHT)
			self.typeItem = QGraphicsTextItem(t, self)
			self.typeItem.setFont(PortGraphics.TYPE_FONT)
			self.typeItem.setRotation(90)
			self.typeItem.setPos(5, -PortGraphics.TOTAL_HEIGHT / 2)

	def getPort(self):
		"""
		Returns the PortGraphics' Port.
		:return:
		"""
		return self._port
	
	def boundingRect(self) -> QRectF:
		"""
		This pure virtual function defines the outer bounds of the item as a rectangle.
		:return: create the bounding of the item
		:rtype: QRectF
		"""
		halfPenWidth = self.borderWidth / 2
		x = PortGraphics.X_POS - halfPenWidth
		y = PortGraphics.Y_POS - halfPenWidth
		
		actualWidth = PortGraphics.WIDTH + self.borderWidth
		actualHeight = PortGraphics.TOTAL_HEIGHT + self.borderWidth
		
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
		
		pen = QPen(PortGraphics.PEN_COLOR)
		pen.setWidth(self.borderWidth)
		painter.setPen(pen)
		
		if type(self._port.getAction()) == ActionWrapper:
			painter.setBrush(PortGraphics.INNER_COLOR)
		else:
			painter.setBrush(PortGraphics.OUTER_COLOR)
		painter.drawPath(self.shape())

	def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
		"""
		Opens a context menu (right click menu) for the component.

		:param event: The event that was generated when the user right-clicked on this item.
		:type event: QGraphicsSceneContextMenuEvent
		:return: None
		:rtype: NoneType
		"""
		return QGraphicsItem.contextMenuEvent(self, event)

		# if not self._menuEnabled:
		# 	return QGraphicsItem.contextMenuEvent(self, event)
		#
		# self.setSelected(True)
		# self.menu.exec_(event.screenPos())
	
	def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
		"""
		When a port is clicked, emit the entitySelected signal from the view.
		:param event: the mouse click event
		:type event: QGraphicsSceneMouseEvent
		:return: None
		"""
		event.ignore()

		try:
			self.scene().views()[0].entitySelected.emit(self._port)
		except:
			pass

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