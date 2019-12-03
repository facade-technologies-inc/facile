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

This module contains the ComponentGraphics class.
"""
import sys
import copy
import numpy as np
from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt, QFont, QFontMetricsF
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneContextMenuEvent, QMenu


class ComponentGraphics(QGraphicsItem):
	"""
	This class displays an individual GUI component in the target gui,
	based on the component class.
	"""

	MIN_WIDTH = 0
	MIN_HEIGHT = 0
	MAX_MARGIN = 30
	MIN_MARGIN = 10
	MARGIN_PROP = 0.05
	PEN_WIDTH = 1.0
	TITLEBAR_H = 40  # NOTE: Must be smaller than minimum margin

	TRIM = 1

	def __init__(self, dataComponent: 'Component', rect: tuple = (), parent=None):
		"""
		Constructs a ComponentGraphics object

		:param dataComponent: get the data of a Component
		:type dataComponent: Component
		:param parent: parent ComponentGraphics
		:type parent: ComponentGraphics
		"""

		QGraphicsItem.__init__(self, parent)
		self.setFlag(QGraphicsItem.ItemIsSelectable)

		if parent is None:
			dataComponent.getModel().getScene().addItem(self)
			self.isRoot = True  # TODO: Have to resize scene to smallest possible
		else:
			self.isRoot = False

		self._dataComponent = dataComponent

		# force components to have at least the minimum size
		self._x = rect[0]
		self._y = rect[1]

		# --- This is where the components get resized to avoid collisions. ---

		if self._dataComponent.getParent() is None:
			# No margin: we want the normal size
			# TODO: Might not do anything
			self._margin = 0
			self._width = max(ComponentGraphics.MIN_WIDTH, 2 * rect[2])
			self._height = max(ComponentGraphics.MIN_HEIGHT, 2 * rect[3])
			self.setPos(max(0, 2 * rect[0]), max(0, 2 * rect[1]))
		elif self._dataComponent.getParent().getParent() is None:
			# We want just a titlebar
			self._margin = 0
			self._width = max(ComponentGraphics.MIN_WIDTH, 2 * rect[2])
			self._height = max(ComponentGraphics.MIN_HEIGHT, 2 * rect[3] + ComponentGraphics.TITLEBAR_H)
			self.setPos(max(0, 2 * rect[0]), max(0, 2 * rect[1] + ComponentGraphics.TITLEBAR_H))
		else:
			# Margin is dynamically assigned, with a max/min value to use
			self._margin = max(ComponentGraphics.MIN_MARGIN, min(ComponentGraphics.MAX_MARGIN,
			                                                     ComponentGraphics.MARGIN_PROP * min(rect[2], rect[3])))

			self._width = max(ComponentGraphics.MIN_WIDTH, 2 * (rect[2] - self._margin))
			self._height = max(ComponentGraphics.MIN_HEIGHT,
			                   2 * (rect[3] - self._margin) + ComponentGraphics.TITLEBAR_H)
			self.setPos(max(0, 2 * rect[0] + self._margin),
			            max(0, 2 * rect[1] + self._margin + ComponentGraphics.TITLEBAR_H))

		self.adjustPositioning()
		self.menu = QMenu()
		showInGui = self.menu.addAction("Show in target GUI")
		showInGui.triggered.connect(
			lambda: self.scene().blinkComponent(self._dataComponent.getId()))

	def getNumberOfTokens(self) -> int:
		"""
		Get the number of tokens.

		:return: the number of tokens
		:rtype: int
		"""
		tokensCount = len(self._dataComponent.getSuperToken().tokens)

		return tokensCount

	def adjustPositioning(self) -> None:
		"""
		Places component using the following criteria:
		1. Place teh component where it actually is in the GUI.
		2. If there is a collision with a sibling, the one that is on the bottom and/or right has to move.
		3. Once all sibling collisions are resolved, the parent may need to expand to fit all children inside.
		4. Once the parent is expanded, start at step 2 again, but his time with the parent.

		NOTE: This is a recursive algorithm.

		:return: None
		:rtype: NoneType
		"""

		# We're dealing with the root that should never be drawn.
		if self._dataComponent.getParent() is None:
			return

		# We're dealing with a top-level component
		elif self._dataComponent.getParent().getParent() is None:
			parent = self.scene()
			parentIsScene = True
			self.setFlag(QGraphicsItem.ItemIsMovable)
		else:
			parent = self._dataComponent.getParent().getGraphicsItem()
			parentIsScene = False

		siblings = [sibling.getGraphicsItem() for sibling in self._dataComponent.getSiblings() if
		            sibling is not self._dataComponent]
		if self in siblings:
			siblings.remove(self)

		# Resolve collisions with siblings
		self.checkForCollisions(siblings)

		# If component isn't placed inside the parent, expand the parent
		# if parentIsScene:
		# 	self.expandSelf()
		# el
		if not parentIsScene:
			allContained = True
			for sib in siblings:
				if not parent.contains(sib):
					allContained = False
					break
			
			allContained = parent.contains(self) and allContained
			
			if not allContained:
				self.expandParent(parent, siblings)

	def checkForCollisions(self, siblings: list) -> None:
		"""
		Function that checks for collisions with self

		:param siblings: list of all components that are at the same level as self
		:type siblings: list[ComponentGraphics]
		:return: None
		"""
		while True:  # TODO: Uncomment after testing
			collidingSiblings = self.getCollidingComponents(siblings)
			if collidingSiblings:
				self.resolveCollisions(collidingSiblings)
			else:
				return

	def expandSelf(self) -> None:
		"""
		Expands self based on children

		:return: None
		"""
		maxX = 0
		maxY = 0
		for child in self._dataComponent.getChildren():
			c = child.getGraphicsItem()
			maxX = max(maxX, c.x() + c.boundingRect(True).width())
			maxY = max(maxY, c.y() + c.boundingRect(True).height())

		if maxX >= self._width:
			self._width = maxX + 10
		if maxY >= self._height:
			self._height = maxY + 10

	def expandParent(self, parent: 'ComponentGraphics', siblings: list) -> None:
		"""
		This function expands the parent and is somewhat recursive, just for adaptability.
		
		:param siblings: list of all of self's siblings
		:type siblings: list[ComponentGraphics]
		:param parent: the parent component of self
		:type parent: ComponentGraphics or scene
		:return: None
		"""
		
		parent.prepareGeometryChange()
		
		maxX = 0
		maxY = 0
		for sib in siblings:
			maxX = max(maxX, sib.x() + sib.boundingRect(True).width())
			maxY = max(maxY, sib.y() + sib.boundingRect(True).height())
			
		maxX = max(maxX, self.x() + self.boundingRect(True).width())
		maxY = max(maxY, self.y() + self.boundingRect(True).height())
			
		parent._width = maxX
		parent._height = maxY
		
		#print(parent.getLabel() + ' was expanded.-------------')
		
		if isinstance(parent, ComponentGraphics):
			parent.adjustPositioning()

	def getX(self) -> int:
		"""
		Gets the original x value
		
		:return: int
		"""
		return self._x

	def getY(self):
		"""
		
		:return:
		"""
		return self._y

	def resolveCollisions(self, collidingSiblings: list) -> None:
		"""
		This function will resolve collisions of a component with its siblings.

		:param collidingSiblings: list of siblings colliding with self
		:type collidingSiblings: list
		:return: None
		:rtype: NoneType
		"""
		
		if self in collidingSiblings:
			print("self can't collide with itself")
			sys.exit(10)    #exit with some error code
		
		work = [(self, collidingSiblings)]
		while work:
			cur, siblings = work.pop()
			
			for sib in siblings:
				print("{} vs. {}:".format(cur.getLabel(), sib.getLabel()))
				sb = sib.boundingRect(False)
				cb = cur.boundingRect(False)
				if sib.x() == cur.x() and sib.y() == cur.y():
					angle = 0
					siblingWins = (sb.width()*sb.height() > cb.width()*cb.height())
				else:
					angle = np.rad2deg(np.arctan2((sib.y() - cur.y()), (sib.x() - cur.x())))
					siblingWins = (angle > 135 or angle <= -45)  # or (sib.getX() < self.getX() and sib.getY() < self.getY())
				
				if siblingWins:
					winner = sib
					loser = cur
				else:
					winner = cur
					loser = sib
				
				lop = loser.pos()  # loser old pos
				if angle <= 0:
					loser.setX(winner.x() + winner.boundingRect(True).width() + winner.getMargin())
				
				elif angle >= 90:
					loser.setY(winner.y() + winner.boundingRect(True).height() + winner.getMargin())
				
				else:
					slope = (loser.y() - winner.y())/(loser.x() - winner.x())
					n = slope * winner.boundingRect().height()  # Number of iterations of slope to reach bottom
					m = winner.boundingRect().width() / slope  # Number of iterations of slope to
					# reach right
					
					if n < m:  # bottom is closer
						loser.setX(winner.x() + n)
						loser.setY(winner.y() + winner.boundingRect(True).height() + sib.getMargin())
					else:
						loser.setX(winner.x() + winner.boundingRect(True).width() + sib.getMargin())
						loser.setY(winner.y() + m)
				lnp = loser.pos() # loser new pos
				
				print("\t{}: ({},{}) -> ({},{})".format(loser.getLabel(), lop.x(), lop.y(),
				                                      lnp.x(), lnp.y()))
				
				if winner.overlapsWith(loser):
					print("=======================================================================")
					print("WOAH THIS SHOULDN'T HAPPEN:")
					wb = winner.boundingRect(withMargins=False)
					lb = loser.boundingRect(withMargins=False)
					print("Winner: ", winner.x(), winner.y(), wb.width(), wb.height())
					print("Loser:  ", loser.x(),  loser.y(),  lb.width(), lb.height())
					print("         ({},{}) -> ({},{})".format(lop.x(), lop.y(), lnp.x(), lnp.y()))
					print("=======================================================================")
				
				sibsibs = [sibling.getGraphicsItem() for sibling in
				            sib._dataComponent.getSiblings() if
				            sibling is not sib._dataComponent]
				
				if sib in sibsibs:
					print("sib can't collide with itself")
					sys.exit(10)  # exit with some error code
				
				sibsibCollisions = sib.getCollidingComponents(sibsibs)
				
				if sibsibCollisions:
					work.insert(0, (sib, sibsibCollisions))
					
			

	def getMargin(self) -> float:
		"""
		Returns the margin of self

		:return: margin
		:rtype: float
		"""
		return self._margin

	def itemChange(self, change: 'GraphicsItemChange', value):
		"""
		Overrides the default itemChange function by adding one extra conditional, otherwise normal behavior of the
		function is returned. This function is what prevents top-level components from colliding

		:param change: the type of state change
		:type change: GraphicsItemChange
		:param value: information about the change
		:return: None or Unknown (typeof(value))
		"""
		if change == QGraphicsItem.ItemPositionChange and self.scene():
			delX = value.x() - self.x()
			delY = value.y() - self.y()

			if delX == 0 and delY == 0:
				return value

			translateX = copy.deepcopy(self.boundingRect())
			translateX.translate(dx=delX, dy=0)
			translateY = copy.deepcopy(self.boundingRect())
			translateY.translate(dx=0, dy=delY)

			xOkay = True
			yOkay = True

			# Checking if there's a collision in x or y direction
			for sibling in self._dataComponent.getSiblings():
				sib = sibling.getGraphicsItem()
				if sib == self:
					continue

				if translateX.intersects(sib.boundingRect()):
					xOkay = False
				if translateY.intersects(sib.boundingRect()):
					yOkay = False

			# Decides where to place component based on collision detection
			if xOkay and yOkay:
				return
			elif xOkay:
				self.pos().setX(value.x())
			elif yOkay:
				self.pos().setY(value.y())

		return QGraphicsItem.itemChange(self, change, value)

	# def rectsCollide(self, a: QRectF, b: QRectF):
	# 	ax1 = 0
	# 	ay1 = 0
	# 	ax2 = 0
	# 	ay2 = 0
	# 	ax1, ay1, ax2, ay2 = a.getCoords()
	# 	print(ax1 + ' ' + ay1)
	#
	# 	bx1 = 0
	# 	by1 = 0
	# 	bx2 = 0
	# 	by2 = 0
	# 	bx1, by1, bx2, by2 = b.getCoords()
	# 	print(bx1 + ' ' + by1)
	#
	# 	return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

	def getCollidingComponents(self, components: list) -> list:
		"""
		Gets all of the components from a list that collide with this component.

		:param components: The components to detect collisions with
		:type components: list[ComponentGraphics]
		:return: All of the components that actually collide with this component
		:rtype: list[ComponentGraphics]
		"""
		collidingSiblings = []
		for sibling in components:
			if self.overlapsWith(sibling):
				collidingSiblings.append(sibling)
		return collidingSiblings

	def getLabel(self) -> str:
		"""
		Gets the label from this component.
		:return: The label for this component.
		:rtype: str
		"""
		try:
			category, name = self._dataComponent.getProperties().getProperty("Name")
			return name.getValue()
		except:
			return ""

	def overlapsWith(self, sibling: 'ComponentGraphics') -> bool:
		"""
		Determines if this ComponentGraphics is overlapping with another one.

		Components that share an edge are not necessarily considered to be overlapping.
		This method differs from collidesWithItem because of this.

		:param sibling: The other component to check collision with.
		:type sibling: ComponentGraphics
		:return: True if components overlap, False otherwise.
		:rtype: bool
		"""
		selfBound = self.boundingRect(False)
		selfx = self.scenePos().x() + selfBound.x()
		selfy = self.scenePos().y() + selfBound.y()

		sibBound = sibling.boundingRect(False)
		sibx = sibling.scenePos().x() + sibBound.x()
		siby = sibling.scenePos().y() + sibBound.y()

		if (sibx < selfx + selfBound.width() and
			sibx + sibBound.width() > selfx and
			siby < selfy + selfBound.height() and
			siby + sibBound.height() > selfy):
			return True
		return False

	def contains(self, child: 'ComponentGraphics') -> bool:
		"""
		Determines if one ComponentGraphics item completely contains another one visually.
		rectangles that match exactly are considered to be "containing" each other.

		This method is mostly used to determine if a parent component needs to be "grown" to fit its children
		inside.

		:param child: The component that we would like to determine if it's in the current component.
		:type child: ComponentGraphics
		:return: True if child is visually in the current component
		:rtype: bool
		"""
		pBound = self.boundingRect(True)
		px = self.scenePos().x() + pBound.x()
		py = self.scenePos().y() + pBound.y()

		cBound = child.boundingRect(True)
		cx = child.scenePos().x() + cBound.x()
		cy = child.scenePos().y() + cBound.y()

		if (px <= cx and
			py <= cy and
			px + pBound.width() >= cx + cBound.width() and
			py + pBound.height() >= cy + cBound.height()):
			return True
		return False

	def boundingRect(self, withMargins: bool = False):
		"""
		This pure virtual function defines the outer bounds of the item as a rectangle.
		:return create the bounding of the item
		:rtype QRectF
		"""
		halfWidth = ComponentGraphics.PEN_WIDTH / 2
		if withMargins:
			marginAdjustment = -ComponentGraphics.TRIM + self._margin + ComponentGraphics.PEN_WIDTH
			return QRectF(-halfWidth - self._margin,
			              -halfWidth - self._margin + ComponentGraphics.TITLEBAR_H,
			              self._width + marginAdjustment + self._margin,
			              self._height + marginAdjustment + ComponentGraphics.TITLEBAR_H)
		else:
			noMarginAdjustment = -ComponentGraphics.TRIM + ComponentGraphics.PEN_WIDTH
			return QRectF(-halfWidth,
			              -halfWidth,
			              self._width + noMarginAdjustment,
			              self._height + noMarginAdjustment)

	def shape(self):
		"""
		Returns the shape of this item as a QPainterPath in local coordinates.
		The shape could be used for many things, like collision detection.

		:return Returns the shape of this item as a QPainterPath in local coordinates.
		:rtype QPainterPath
		"""
		path = QPainterPath()
		path.addRect(self.boundingRect())
		return path

	def paint(self, painter, option, widget):
		"""
		Paints the contents of the component. Override the parent paint function

		:param painter: Use a Qpainter object.
		:type painter: QPainter
		:param option: It provides style options for the item.
		:type option: QStyleOptionGraphicsItem
		:param widget: QWidget
		:type widget: It points to the widget that is being painted on; or make it = None.
		:return None
		:rtype NoneType
		"""
		boundingRect = self.boundingRect()

		if self.isRoot or boundingRect.width() == 0 and boundingRect.height() == 0:
			painter.setPen(QPen(QColor(Qt.transparent)))
			painter.setBrush(QColor(Qt.transparent))
			return

		pen = QPen(QColor(100, 200, 255))
		if self.isSelected():
			pen.setStyle(Qt.DashDotLine)
			pen.setColor(QColor(255, 0, 0))
		else:
			pen.setStyle(Qt.SolidLine)
			pen.setColor(QColor(0, 0, 0))
		painter.setPen(pen)

		painter.setBrush(QColor(88, 183, 255))

		id = self._dataComponent.getId()

		painter.drawRoundedRect(boundingRect, 5, 5)
		br = self.boundingRect(withMargins=False)

		# draw name label
		name = self.getLabel()
		# TODO: make a better algorithm on font size in the future
		# 44 width -> only cover 12 words with 5 -> 5Fonts one is 3.6 (added 5)
		# 48 width -> only cover 18 words with 4 -> 4Fonts one is 2.6 (added 5)
		if len(name) * 3.5 > self.boundingRect(withMargins=False).width():
			if len(name) * 2.5 > self.boundingRect(withMargins=False).width():
				nameFont = QFont("Times", 2)
			else:
				nameFont = QFont("Times", 4)
		else:
			nameFont = QFont("Times", 5)
		painter.setFont(nameFont)
		fm = QFontMetricsF(nameFont)
		name = fm.elidedText(name, Qt.ElideRight, br.width() - ComponentGraphics.TITLEBAR_H)

		painter.setBrush(QColor(100, 200, 255))
		painter.drawText(self.boundingRect(withMargins=False).x() + 5, self._margin + 13, name)

		# draw token tag
		token_count = str(self.getNumberOfTokens())
		
		ttX = br.x() + br.width() - ComponentGraphics.TITLEBAR_H
		ttY = br.y()
		ttWidth = ComponentGraphics.TITLEBAR_H
		ttHeight = ComponentGraphics.TITLEBAR_H
		
		rectBox = QRectF(ttX, ttY, ttWidth, ttHeight)
		tokenTagFont = QFont("Times", 10)
		painter.setFont(tokenTagFont)
		painter.setBrush(QColor(255, 0, 0, 127))
		#painter.drawRect(rectBox)
		painter.drawEllipse(rectBox.center(), ttWidth/2-1, ttHeight/2-1)
		painter.setBrush(QColor(100, 200, 255))
		fm = QFontMetricsF(tokenTagFont)
		pixelsWide = fm.width(token_count)
		pixelsHigh = fm.height()
		painter.drawText(ttX+ttWidth/2-pixelsWide/2, ttY+ttHeight/2+pixelsHigh/4, token_count)

	def mousePressEvent(self, event):
		"""
		This event handler is implemented to receive mouse press events for this item.

		:param event: a mouse press event
		:type event: QGraphicsSceneMouseEvent
		"""
		self.setSelected(True)
		self.scene().emitItemSelected(self._dataComponent.getId())

	def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
		"""
		Opens a context menu (right click menu) for the component.

		:param event: The event that was generated when the user right-clicked on this item.
		:type event: QGraphicsSceneContextMenuEvent
		:return: None
		:rtype: NoneType
		"""
		self.setSelected(True)
		selectedAction = self.menu.exec_(event.screenPos())

	def triggerSceneUpdate(self):
		"""
		Update the scene.

		"""
		self.scene().invalidate(self.scene().sceneRect(), QGraphicsScene.ItemLayer)

	def __repr__(self):
		"""
		Returns the componentView id as a string.

		:return Returns the componentView id as a string.
		:rtype str
		"""
		return "Component: {}".format(self._dataComponent.getId())
