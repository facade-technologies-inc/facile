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

TODO: make this view draggable
"""

from PySide2.QtWidgets import QGraphicsView, QWidget
from PySide2.QtGui import QWheelEvent
from PySide2.QtCore import QPoint

class FacileGraphicsView(QGraphicsView):
	"""
	This class adds functionality to the QGraphicsView to zoom in and out.
	
	This is primarily used as the view that shows the target GUI model and API model
	"""
	
	ZOOM_FACTOR = 1.25
	
	def __init__(self, parent: QWidget = None) -> None:
		"""
		Create a GraphicsView for Facile.
		:param parent: The widget to embed the graphics view into
		:type parent: QWidget
		:return: None
		:rtype: NoneType
		"""
		super(FacileGraphicsView, self).__init__(parent)
	
	def wheelEvent(self, event: QWheelEvent) -> None:
		"""
		Handle wheel scroll events. This will zoom in or out depending on the
		
		:param event: the wheel scroll event
		:type event: QWheelEvent
		:return: None
		:rtype: NoneType
		"""
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
		self.setTransformationAnchor(QGraphicsView.NoAnchor)
		self.setResizeAnchor(QGraphicsView.NoAnchor)
		
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
		zoomFactor = 1/FacileGraphicsView.ZOOM_FACTOR
		oldPos = self.mapToScene(pos)
		self.scale(zoomFactor, zoomFactor)
		newPos = self.mapToScene(pos)
		
		# Set Anchors
		self.setTransformationAnchor(QGraphicsView.NoAnchor)
		self.setResizeAnchor(QGraphicsView.NoAnchor)
		
		# Move scene to old position
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())
