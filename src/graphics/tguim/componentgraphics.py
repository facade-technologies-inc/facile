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

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneContextMenuEvent, QMenu


class ComponentGraphics(QGraphicsItem):
	"""
	This class displays an individual GUI component in the target gui,
	based on the component class.
	"""
	
	MIN_WIDTH = 0
	MIN_HEIGHT = 0
	MARGIN = 20
	PEN_WIDTH = 1.0
	
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
			self.isRoot = True
		else:
			self.isRoot = False
		
		self._dataComponent = dataComponent
		
		# force components to have at least the minimum size
		self._x = rect[0]
		self._y = rect[1]
		self._width = max(rect[2], ComponentGraphics.MIN_WIDTH)
		self._height = max(rect[3], ComponentGraphics.MIN_HEIGHT)
		self.setPos(max(0, rect[0]), max(0, rect[1]))
		self.adjustPositioning()
		self.menu = QMenu()
		showInGui = self.menu.addAction("Show in target GUI")
		showInGui.triggered.connect(
			lambda: self.scene().blinkComponent(self._dataComponent.getId()))
	
	def getNumberOfTokens(self):
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
			parentRect = parent.sceneRect()
			parentIsScene = True
		else:
			parent = self._dataComponent.getParent().getGraphicsItem()
			parentRect = parent.boundingRect()
			parentIsScene = False
		
		siblings = [sibling.getGraphicsItem() for sibling in self._dataComponent.getSiblings()]
		if self in siblings:
			siblings.remove(self)
		
		# Resolve collisions with siblings
		while True:
			collidingSiblings, maxSibX, maxSibY = self.getCollidingComponents(siblings)
			if collidingSiblings:
				self.dumbCollisionResolution(maxSibX, maxSibY, closest=False)
			# self.smartCollisionResolution(collidingSiblings)
			else:
				break
		
		# If component isn't placed inside the parent, expand the parent
		if not parentIsScene and not parent.contains(self):
			width = max(maxSibX, self.x() + self._width)
			height = max(maxSibY, self.y() + self._height)
			parent.prepareGeometryChange()
			if parentIsScene:
				parent.setSceneRect(self.scene.x(), self.scene.y(),
				                    width + ComponentGraphics.MARGIN,
				                    height + ComponentGraphics.MARGIN)
			else:
				parent._width = width
				parent._height = height
				
				if isinstance(parent, ComponentGraphics):
					parent.adjustPositioning()
	
	def dumbCollisionResolution(self, maxX: float, maxY: float, closest=True) -> None:
		"""
		This is a simple collision resolution function. It will move the component to
		either the far right or far bottom of it's siblings.
		
		:param maxX: The maximum x coordinate of all siblings.
		:type maxX: float
		:param maxY: The maximum y coordinate of all siblings
		:type maxY: float
		:param closest: If True, the component will be moved either down or right depending
		on what's closer. If False, the component will be moved depending on proportions of
		the parent (we try to keep even proportions).
		:type closest: bool
		:return: None
		:rtype: NoneType
		"""
		if closest:
			if maxX - self.x() <= maxY - self.y():
				self.setPos(self.x(), maxY)
			else:
				self.setPos(maxX, self.y())
		else:
			moveRightSize = maxX + self._width
			moveDownSize = maxY + self._height
			# we'll move all the way to the bottom
			if moveRightSize >= moveDownSize:
				self.setPos(self.x(), maxY)
			# or we'll move all the way to the right
			else:
				self.setPos(maxX, self.y())
	
	def smartCollisionResolution(self, colliding: list) -> None:
		"""
		This is an algorithm that resolves collisions in a smart way by always pushing one of
		two colliding elements in a right/downward direction.
		
		unlike the dumbCollisionResolution, this algorithm can push items diagonally. This algorithm
		is much less efficient than the dumbCollisionDetection.
		
		:param colliding: All of the elements colliding with our element.
		:type colliding: list[ComponentGraphics]
		:return: None
		:rtype: NoneType
		"""
		raise NotImplemented("This function is not yet implemented")
	
	def getCollidingComponents(self, components: list) -> tuple:
		"""
		Gets all of the components from a list that collide with this component.
		
		:param components: The components to detect collisions with
		:type components: list[ComponentGraphics]
		:return: All of the components that actually collide with this component and the maximum sibling x and y positions.
		:rtype: list[ConponentGraphics], float, float
		"""
		collidingSiblings = []
		maxSibX = 0
		maxSibY = 0
		for sibling in components:
			sibBound = sibling.boundingRect()
			maxSibX = max(maxSibX, sibling.x() + sibBound.width())
			maxSibY = max(maxSibY, sibling.y() + sibBound.height())
			if self.overlapsWith(sibling):
				collidingSiblings.append(sibling)
		return collidingSiblings, maxSibX, maxSibY
	
	def getLabel(self) -> str:
		"""
		Gets the label from this component.
		:return: The label for this component.
		:rtype: str
		"""
		try:
			category, name = self._dataComponent.getProperties().getProperty("Name")
			return name.value()
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
		
		selfBound = self.boundingRect(withMargins=False)
		selfx = self.scenePos().x() + selfBound.x()
		selfy = self.scenePos().y() + selfBound.y()
		
		sibBound = sibling.boundingRect(withMargins=False)
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
		pBound = self.boundingRect()
		px = self.scenePos().x() + pBound.x()
		py = self.scenePos().y() + pBound.y()
		
		cBound = child.boundingRect()
		cx = child.scenePos().x() + cBound.x()
		cy = child.scenePos().y() + cBound.y()
		
		if (px <= cx and
			py <= cy and
			px + pBound.width() >= cx + cBound.width() and
			py + pBound.height() >= cy + cBound.height()):
			return True
		return False
	
	def boundingRect(self, withMargins: bool = True):
		"""
		This pure virtual function defines the outer bounds of the item as a rectangle.

		:return create the bounding of the item
		:rtype QRectF
		"""
		halfWidth = ComponentGraphics.PEN_WIDTH / 2
		if withMargins:
			marginAdjustment = -ComponentGraphics.TRIM + ComponentGraphics.MARGIN * 2 + ComponentGraphics.PEN_WIDTH
			return QRectF(-halfWidth - ComponentGraphics.MARGIN,
			              -halfWidth - ComponentGraphics.MARGIN,
			              self._width + marginAdjustment,
			              self._height + marginAdjustment)
		else:
			noMarginAdjustment = -ComponentGraphics.TRIM + ComponentGraphics.PEN_WIDTH
			return QRectF(ComponentGraphics.MARGIN - halfWidth,
			              ComponentGraphics.MARGIN - halfWidth,
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
		path.addRect(self.boundingRect(withMargins=True))
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
		boundingRect = self.boundingRect(withMargins=False)
		
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
		
		# set background color:
		painter.setBrush(QColor(100, 200, 255))
		
		id = self._dataComponent.getId()
		
		painter.drawRoundedRect(boundingRect, 5, 5)
		
		name = self.getLabel()
		painter.drawText(int(ComponentGraphics.MARGIN * 1.5), int(ComponentGraphics.MARGIN + 30),
		                 name)
		
		token_count = str(self.getNumberOfTokens())
		rectBox = QRectF(self.boundingRect().width() - ComponentGraphics.MARGIN,
		                 -ComponentGraphics.MARGIN,
		                 ComponentGraphics.MARGIN * 2, ComponentGraphics.MARGIN * 2)
		painter.drawRect(rectBox)
		painter.drawText(rectBox.center(), token_count)
	
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
