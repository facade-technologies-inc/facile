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

from PySide2.QtCore import QPoint, QTimer, Slot, QRectF
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
		self.smoothFocusTimer.timeout.connect(self.smoothFocusTick)
		self.focusHistory = [] # holds mix of graphics items and rectangles

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

	def smoothFocus(self, item:QGraphicsItem = None, rect:QRectF = None) -> bool:
		"""
		If the item is in the current scene, fit the item in the view interpolating the distance moved over several
		periods of a timer.

		:param item: The item to zoom into.
		:type item: QGraphicsItem
		:param rect: The rectangle to focus on
		:type rect: RectF
		:return: True if the focus succeeded, False otherwise
		:rtype: bool
		"""

		# can't focus on items that aren't in the scene
		if item is not None and item not in self.scene().items():
			return False

		# If no item or rect was given, raise Exception
		if item is None and rect is None:
			raise Exception("Must provide either an item or a rectangle")

		# If both item and rect were passed in, raise Exception
		if item is not None and rect is not None:
			raise Exception("Cannot provide both item and rectangle")

		# if an item was passed in, extract it's rectangle
		if item:
			rect = item.mapToScene(item.boundingRect()).boundingRect()
			padding = 50
		else:
			padding = 0

		# get the currently visible rectangle
		visibleRect = self.mapToScene(self.rect()).boundingRect()

		# Determine if the rect is completely in view
		if rect.x() > visibleRect.x() and \
			rect.y() > visibleRect.y() and \
			rect.x() + rect.width() < visibleRect.x() + visibleRect.width() and \
			rect.y() + rect.height() < visibleRect.y() + visibleRect.height():
			inView = True
		else:
			inView = False

		# Give padding to rect
		rect.setWidth(rect.width() + 2 * padding)
		rect.setHeight(rect.height() + 2 * padding)
		rect.setX(rect.x() - padding)
		rect.setY(rect.y() - padding)

		# Determine how much we WOULD be focusing. Used to determine if we SHOULD focus.
		xDiff = abs(rect.x() - visibleRect.x())
		yDiff = abs(rect.y() - visibleRect.y())
		widthDiff = abs(rect.width() - visibleRect.width())
		heightDiff = abs(rect.height() - visibleRect.height())

		# Filter out values less than threshold (avoid jittering when focus results in little change).
		threshold = 50
		horizontalSignificantDiffs = list(filter(lambda d: d >= threshold, [xDiff, widthDiff]))
		verticalSignificantDiffs = list(filter(lambda d: d >= threshold, [yDiff, heightDiff]))

		# only focus if the difference between the item and the viewing area is great enough or the item is not
		# completely in view.
		if inView and (not horizontalSignificantDiffs or not verticalSignificantDiffs):
			return False

		# determine how much to adjust the viewing rectangle at each tick of the clock.
		self.smoothFocusTicks = 30
		self.xDelta = (visibleRect.x() - rect.x()) / self.smoothFocusTicks
		self.yDelta = (visibleRect.y() - rect.y()) / self.smoothFocusTicks
		self.widthDelta = (visibleRect.width() - rect.width()) / self.smoothFocusTicks
		self.heightDelta = (visibleRect.height() - rect.height()) / self.smoothFocusTicks

		self.visibleRect = visibleRect

		# If focusing is already running, stop it.
		if self.smoothFocusTimer.isActive():
			self.smoothFocusTimer.stop()

		self.curTick = 0
		if item:
			if not hasattr(item, "_zoomable") or item._zoomable is True:
				self.smoothFocusTimer.start(50)
				self._addToHistory(item)
				item._zoomable = True
			else:
				item._zoomable = True
				return False
		else:
			self.smoothFocusTimer.start(50)
			self._addToHistory(rect)

		return True

	def _addToHistory(self, newEntry) -> None:
		"""
		Adds a QGraphicsItem or a QRectF to the focus history.

		The entry will only be added if it is not already the last item in the history

		:param newEntry: The item or rect to add to the history
		:type newEntry: QGraphicsItem or QRectF
		:return: None
		:rtype: NoneType
		"""
		if self.focusHistory:
			lastEntry = self.focusHistory[-1]
			if isinstance(lastEntry, QGraphicsItem) and isinstance(newEntry, QGraphicsItem):
				if lastEntry is not newEntry:
					self.focusHistory.append(newEntry)
			if isinstance(lastEntry, QRectF) and isinstance(newEntry, QRectF):
				if lastEntry != newEntry:
					self.focusHistory.append(newEntry)
		else:
			self.focusHistory.append(newEntry)

	def undoFocus(self) -> None:
		"""
		Removes the last item from the history and focus on it.

		:return: None
		:rtype: NoneType
		"""
		while True:
			if self.focusHistory:
				lastEntry = self.focusHistory.pop()
				if isinstance(lastEntry, QGraphicsItem):
					lastEntry.mousePressEvent(None)
					if self.smoothFocus(item=lastEntry):
						self.focusHistory.pop()
						break
				elif isinstance(lastEntry, QRectF):
					if self.smoothFocus(rect=lastEntry):
						self.focusHistory.pop()
						break
			else:
				break

	def resetView(self) -> None:
		"""
		Clears focus history and fits the scene rect to the view port.

		:return: None
		:rtype: NoneType
		"""
		self.smoothFocus(rect=self.sceneRect())
		#self.focusHistory.clear()

	@Slot()
	def smoothFocusTick(self):
		"""
		Gets called on each iteration of the smoothFocusTick timer.

		:return: None
		"""
		self.curTick += 1

		# calculate the new rectangle to focus on.
		newX = self.visibleRect.x() - self.xDelta * self.curTick
		newY = self.visibleRect.y() - self.yDelta * self.curTick
		newWidth = self.visibleRect.width() - self.widthDelta * self.curTick
		newHeight = self.visibleRect.height() - self.heightDelta * self.curTick

		self.fitInView(newX, newY, newWidth, newHeight, aspectRadioMode=Qt.KeepAspectRatio)

		if self.curTick == self.smoothFocusTicks:
			self.smoothFocusTimer.stop()