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

from PIL import Image

from PySide2.QtGui import QPainter, QColor, QFont, QFontMetricsF, Qt, QImage, QPixmap
from PySide2.QtCore import QRectF
from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem, QGraphicsSceneContextMenuEvent, QGraphicsPixmapItem, \
	QGraphicsRectItem, QGraphicsTextItem

import data.statemachine as sm
from data.apim.componentaction import ComponentAction
from graphics.apim.actiongraphics import ActionGraphics
from graphics.apim.movebutton import MoveButton
from qt_models.actionwrappermenu import ActionWrapperMenu

class ActionWrapperGraphics(ActionGraphics):
	
	TAG_FONT = QFont("Times", 10)
	TAG_TEXT_COLOR = QColor(0, 0, 0)
	TAG_BACKGROUND_COLOR = QColor(150, 150, 150)
	
	NAME_FONT = QFont("Times", 10)
	NAME_TEXT_COLOR = QColor(0, 0, 0)
	
	COLOR = QColor(188, 183, 255)

	POPUP_ARROW_WIDTH = 40
	POPUP_BUFFER = 10
	
	def __init__(self, action: 'ActionWrapper', parent=None) -> 'ActionGraphics':
		"""
		Constructs an Action Wrapper Graphics object for the given action wrapper.

		:param action: The action wrapper for which this graphics item represents.
		:type action: ActionWrapper
		:param parent: None
		:type parent: NoneType
		:return: The graphics of an action.
		:rtype: ActionGraphics
		"""
		ActionGraphics.__init__(self, action, parent)
		self.setAcceptHoverEvents(True)
		self.color = ActionWrapperGraphics.COLOR
		
		def delete():
			action.getParent().removeAction(action)
			sm.StateMachine.instance.view.ui.apiModelView.refresh()

		self.menu = ActionWrapperMenu()
		self.menu.onDelete(delete)
		
		# create buttons for moving action in sequence
		self.upButton = MoveButton(MoveButton.Direction.Up, self)
		self.downButton = MoveButton(MoveButton.Direction.Down, self)
		self.upButton.clicked.connect(self.promote)
		self.downButton.clicked.connect(self.demote)
		self.upButton.hide()
		self.downButton.hide()
		
		self.updateGraphics()
		
	def updateGraphics(self) -> None:
		"""
		Update the graphics for the action wrapper and all children graphics.
		
		:return: None
		:rtype: NoneType
		"""
		ActionGraphics.updateGraphics(self)
		
		self.updateActionRect()
		
		# update position of move buttons
		hOffset = ActionGraphics.H_SPACE / 4
		vOffset = MoveButton.HEIGHT + 20
		self.upButton.setPos(self._width/2 - hOffset, -self._height/2 + vOffset)
		self.downButton.setPos(self._width/2 - hOffset, self._height/2 - vOffset)

	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		"""
		Paint the graphics of the action wrapper including action name, number, and ports.

		:param painter: This draws the widget.
		:type painter: QPainter
		:param option: Option for the style of graphic.
		:type option: QStyleOptionGraphicsItem
		:param index: Index for the painted graphic.
		:type index: QWidget
		:return: None
		:rtype: NoneType
		"""
		ActionGraphics.paint(self, painter, option, index)
		
		# Get dimensions of the action
		x, y, width, height = self.getActionRect(self._action.getInputPorts(), self._action.getOutputPorts())
		
		# Draw the number tag.
		number = str(self._action.getParent().getActions().index(self._action) + 1)
		offset = 5
		radius = 15
		size = ActionGraphics.H_SPACE/2 - offset*2
		painter.setBrush(QColor(29, 110, 37))
		painter.drawRoundedRect(QRectF(x + offset, y + offset, size, size), radius, radius)
		painter.setPen(ActionWrapperGraphics.TAG_TEXT_COLOR)
		painter.setBrush(ActionWrapperGraphics.TAG_TEXT_COLOR)
		painter.setFont(ActionWrapperGraphics.TAG_FONT)
		fm = QFontMetricsF(ActionWrapperGraphics.TAG_FONT)
		pixelsWide = fm.width(number)
		pixelsHigh = fm.height()
		# TODO: fix text positioning - font metrics aren't working well
		painter.drawText(x+offset+size/2-pixelsWide, y+offset+size/2+pixelsHigh/2, number)
		
		# Draw the name of the action
		painter.setPen(ActionWrapperGraphics.NAME_TEXT_COLOR)
		painter.setBrush(ActionWrapperGraphics.NAME_TEXT_COLOR)
		painter.setFont(ActionWrapperGraphics.NAME_FONT)
		fm = QFontMetricsF(ActionWrapperGraphics.NAME_FONT)
		br = fm.boundingRect(self._action.getName())
		# TODO: fix text positioning - font metrics aren't working well
		t = fm.elidedText(self._action.getName(), Qt.ElideRight, self._width - offset * 2)
		painter.drawText(x + offset, br.height(), t)
	
	def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
		"""
		Opens a context menu (right click menu) for the action wrapper.

		:param event: The event that was generated when the user right-clicked on this item.
		:type event: QGraphicsSceneContextMenuEvent
		:return: None
		:rtype: NoneType
		"""
		self.menu.exec_(event.screenPos())
		
	def updateMoveButtonVisibility(self) -> None:
		"""
		Show the appropriate movement buttons based on location of the action in the action
		pipeline sequence
		
		:return:
		"""
		
		if not self.isUnderMouse():
			self.upButton.hide()
			self.downButton.hide()
			return
		
		totalNumActions = len(self._action.getParent().getActions())
		idx = self._action.getParent().getActions().index(self._action)
		
		if idx == 0:
			self.upButton.hide()
		else:
			self.upButton.show()
		
		if idx == totalNumActions - 1:
			self.downButton.hide()
		else:
			self.downButton.show()
	
	def hoverEnterEvent(self, event) -> None:
		"""
		show move buttons when hovered over.

		Also show image or name of component IF the underlying action is a component action.

		:param event: The hover event.
		:type event: QGraphicsSceneHoverEvent
		:return: None
		:rtype: NoneType
		"""
		self.updateMoveButtonVisibility()
		self._popUp = None

		# If this is a wrapper for a ComponentAction, we'll show a pop-up.
		action = self._action.getUnderlyingAction()
		if type(action) is ComponentAction:

			br = self.boundingRect()
			self._popUp = QGraphicsRectItem(self)
			self._popUp.setPos(br.x() + br.width(), 0)

			self._arrowPixmap = QPixmap(":icon/resources/icons/office/arrow-right.png").scaledToWidth(ActionWrapperGraphics.POPUP_ARROW_WIDTH)
			self._arrowItem = QGraphicsPixmapItem(self._popUp)
			self._arrowItem.setPixmap(self._arrowPixmap)
			self._arrowItem.setPos(ActionWrapperGraphics.POPUP_BUFFER, -self._arrowPixmap.height()/2)

			component = action.getTargetComponent()
			image = component.getFirstImage()

			# If there is an image AND the detailed view is on, we'll show the image for the component.
			if image is not None and sm.StateMachine.instance.configVars.showComponentImages:
				r, g, b = image.split()
				im = Image.merge("RGB", (b, g, r))
				im2 = im.convert("RGBA")
				data = im2.tobytes("raw", "RGBA")
				qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32).scaledToHeight(ActionGraphics.TOTAL_RECT_HEIGHT * 3/4)
				self._pix = QPixmap.fromImage(qim)
				self._pixItem = QGraphicsPixmapItem(self._popUp)
				self._pixItem.setPixmap(self._pix)
				self._pixItem.setPos(ActionWrapperGraphics.POPUP_BUFFER*2 + ActionWrapperGraphics.POPUP_ARROW_WIDTH, -ActionGraphics.TOTAL_RECT_HEIGHT * 3/4/2)

			# If there is no image for the component OR detailed view is off, we'll show text instead.
			else:
				name = component.getName()
				self._nameItem = QGraphicsTextItem(self._popUp)
				self._nameItem.setPlainText(name)
				height = self._nameItem.boundingRect().height()
				self._nameItem.setPos(ActionWrapperGraphics.POPUP_BUFFER*2 + ActionWrapperGraphics.POPUP_ARROW_WIDTH,-height/2)
	
	def hoverLeaveEvent(self, event) -> None:
		"""
		hide buttons when hovered over.

		:param event: The hover event.
		:type event: QGraphicsSceneHoverEvent
		:return: None
		:rtype: NoneType
		"""
		self.updateMoveButtonVisibility()

		if self._popUp:
			self.scene().removeItem(self._popUp)
			self._popUp = None
		
	def promote(self) -> None:
		"""
		Move the action up (sooner) in the sequence of execution.
		
		:return: None
		:rtype: NoneType
		"""
		actionList = self._action.getParent().getActions()
		totalNumActions = len(actionList)
		idx = actionList.index(self._action)
		
		if idx == 0:
			return
		
		temp = actionList[idx-1]
		actionList[idx-1] = actionList[idx]
		actionList[idx] = temp
		
		self._action.getParent().changeSequence(actionList)
		
		for view in self.scene().views():
			view.refresh()
	
	def demote(self) -> None:
		"""
		Move the action down (later) in the sequence of execution.

		:return: None
		:rtype: NoneType
		"""
		actionList = self._action.getParent().getActions()
		totalNumActions = len(actionList)
		idx = actionList.index(self._action)
		
		if idx > totalNumActions - 1:
			return
		
		temp = actionList[idx + 1]
		actionList[idx + 1] = actionList[idx]
		actionList[idx] = temp
		
		self._action.getParent().changeSequence(actionList)
		
		for view in self.scene().views():
			view.refresh()
