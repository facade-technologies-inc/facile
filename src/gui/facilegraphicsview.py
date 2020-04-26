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
	
This module contains the FacileGraphicsView class which is just like a normal graphics
view, but can be zoomed.
"""

from PySide2.QtCore import QPoint, QTimer
from PySide2.QtGui import QWheelEvent, Qt, QColor, QKeyEvent
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
from PySide2.QtWidgets import QWidget


class FacileGraphicsView(QGraphicsView):
	"""
	This class adds functionality to the QGraphicsView to zoom in and out.
	
	This is primarily used as the view that shows the target GUI model and API model
	"""
	
	ZOOM_FACTOR = 1.05
	
	def __init__(self, parent: QWidget = None) -> None:
		"""
		Create a GraphicsView for Facile.
		:param parent: The widget to embed the graphics view into
		:type parent: QWidget
		:return: None
		:rtype: NoneType
		"""
		super(FacileGraphicsView, self).__init__(parent)

		# set flags
		self.setDragMode(QGraphicsView.ScrollHandDrag)
		self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
		
		# show initial message
		scene = QGraphicsScene()
		box = QGraphicsRectItem(0, 0, 100, 100)
		box.setPen(QColor(Qt.transparent))
		box.setBrush(QColor(Qt.transparent))
		QGraphicsTextItem("Nothing to show here yet!", box)
		scene.addItem(box)
		
		self.setScene(scene)

		self.smoothFocusTimer = QTimer(self)

	def wheelEvent(self, event: QWheelEvent) -> None:
		"""
		Handle wheel scroll events. This will zoom in or out if the Ctrl key is pressed.
		
		:param event: the wheel scroll event
		:type event: QWheelEvent
		:return: None
		:rtype: NoneType
		"""

		# pass the event down to scene first
		QGraphicsView.wheelEvent(self, event)
		if event.isAccepted():
			return

		if event.modifiers() != Qt.ControlModifier:
			return

		# Zoom
		if event.delta() > 0:
			self.zoomIn(event.pos())
		else:
			self.zoomOut(event.pos())

	
	def zoomIn(self, pos: QPoint) -> None:
		"""
		Zoom in one ZOOM_FACTOR
		
		:param pos: The position to zoom into
		:type pos: QPoint
		:return: None
		:rtype: NoneType
		"""
		zoomFactor = FacileGraphicsView.ZOOM_FACTOR
		oldPos = self.mapToScene(pos)
		self.scale(zoomFactor, zoomFactor)
		newPos = self.mapToScene(pos)
		
		# Set Anchors
		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
		
		# Move scene to old position
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())
	
	def zoomOut(self, pos: QPoint) -> None:
		"""
		Zoom out one ZOOM_FACTOR

		:param pos: The position to zoom out from
		:type pos: QPoint
		:return: None
		:rtype: NoneType
		"""
		zoomFactor = 1 / FacileGraphicsView.ZOOM_FACTOR
		oldPos = self.mapToScene(pos)
		self.scale(zoomFactor, zoomFactor)
		newPos = self.mapToScene(pos)
		
		# Set Anchors
		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
		
		# Move scene to old position
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())

	def smoothFocus(self, item:QGraphicsItem) -> None:
		"""
		If the item is in the current scene, fit the item in the view interpolating the distance moved over several
		periods of a timer.

		:param item: The item to zoom into.
		:type item: QGraphicsItem
		:return: None
		:rtype: NoneType
		"""
		ticks = 100
		self.curTick = 0
		padding = 50
		itemRect = item.mapToScene(item.boundingRect()).boundingRect()
		itemRect.setWidth(itemRect.width() + 2*padding)
		itemRect.setHeight(itemRect.height() + 2*padding)
		itemRect.setX(itemRect.x() - padding)
		itemRect.setY(itemRect.y() - padding)
		visibleRect = self.mapToScene(self.rect()).boundingRect()

		xDelta = (visibleRect.x() - itemRect.x()) / ticks
		yDelta = (visibleRect.y() - itemRect.y()) / ticks
		widthDelta = (visibleRect.width() - itemRect.width()) / ticks
		heightDelta = (visibleRect.height() - itemRect.height()) / ticks

		if self.smoothFocusTimer.isActive():
			self.smoothFocusTimer.stop()

		def tick():
			self.curTick += 1

			newX = visibleRect.x() - xDelta*self.curTick
			newY = visibleRect.y() - yDelta * self.curTick
			newWidth = visibleRect.width() - widthDelta * self.curTick
			newHeight = visibleRect.height() - heightDelta * self.curTick

			self.fitInView(newX, newY, newWidth, newHeight, aspectRadioMode=Qt.KeepAspectRatio)

			if self.curTick == ticks:
				self.smoothFocusTimer.stop()

		self.smoothFocusTimer.timeout.connect(tick)
		self.smoothFocusTimer.start(10)
