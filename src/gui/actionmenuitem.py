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

This module contains the ActionMenuItem() Class.
"""

from PySide2.QtWidgets import QWidget, QGraphicsScene, QDialog
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QContextMenuEvent, QPainter, QPixmap
from gui.ui.ui_actionmenuitem import Ui_Form as Ui_ActionMenuItem
from graphics.apim.actionicongraphics import ActionIconGraphics
from data.apim.actionpipeline import ActionPipeline
from data.apim.componentaction import ComponentAction
from data.apim.actionwrapper import ActionWrapper
from qt_models.componentactionitemmenu import ComponentActionItemMenu
from qt_models.actionpipelineitemmenu import ActionPipelineItemMenu
from gui.blackboxeditordialog import BlackBoxEditorDialog
import data.statemachine as sm

class ActionMenuItem(QWidget):
	"""
	ActionMenuItem is a widget for Facile's Action Menu View.
	"""
	
	def __init__(self, action: 'Action') -> 'ActionMenuItem':
		"""
		Constructs a ActionMenuItem object.
		
		:param action: Specified action that will be added as a action menu item.
		:type action: Action
		:return: The new ActionMenuItem object.
		:rtype: ActionMenuItem
		"""
		super(ActionMenuItem, self).__init__()
		
		# UI Initialization
		self.ui = Ui_ActionMenuItem()
		self.ui.setupUi(self)
		self._action = action
		
		#Add ActionGraphics to Graphics View
		self._actionGraphics = ActionIconGraphics(self._action)
		self._scene = QGraphicsScene()
		self._scene.addItem(self._actionGraphics)
		
		# set action name text field and shrink action graphics to fit.
		self.update()
		
		# Create a menu appropriate for this action.
		if type(self._action) == ActionPipeline:
			self.menu = ActionPipelineItemMenu()
			
			def editInternals():
				sm.StateMachine.instance.view._actionPipelinesMenu.actionSelected.emit(action)
				
			def editExternals():
				editInternals()
				BlackBoxEditorDialog(action).exec_()
				self.update()
				apimView = sm.StateMachine.instance.view.ui.apiModelView
				apimView.showAction(self._action)
				
			def delete():
				sm.StateMachine.instance._project.getAPIModel().removeActionPipeline(self._action)
				if sm.StateMachine.instance.getCurrentActionPipeline() == self._action:
					sm.StateMachine.instance.setCurrentActionPipeline(None)
				self.hide()
			
			self.menu.onEditInternals(editInternals)
			self.menu.onEditExternals(editExternals)
			self.menu.onDelete(delete)
				
		elif type(self._action) == ComponentAction:
			self.menu = ComponentActionItemMenu()
			
		def add():
			cap = sm.StateMachine.instance.getCurrentActionPipeline()
			ActionWrapper(self._action, cap)
			sm.StateMachine.instance.view.ui.apiModelView.refresh()
			
		self.menu.onAdd(add)
		
	def getName(self) -> str:
		"""
		Gets the name of the action from the actions property "Name."
		
		:return: Name of action item.
		:rtype: str
		"""
		return self._action.getProperties().getProperty("Name")[1].getValue()
	
	def contextMenuEvent(self, event: QContextMenuEvent) -> None:
		"""
		Opens a context menu (right click menu) for the component.

		:param event: The event that was generated when the user right-clicked on this item.
		:type event: QGraphicsSceneContextMenuEvent
		:return: None
		:rtype: NoneType
		"""
		
		self.menu.exec_(event.globalPos())
	
	def mouseDoubleClickEvent(self, event: QEvent):
		"""
		Handles what happens when the user double clicks this action menu item.
		
		The interface editor opens for this action.
		
		:param event:
		:return:
		"""
		
		if event.buttons() != Qt.LeftButton:
			return
		
		if type(self._action) == ActionPipeline:
			event.accept()
			self.menu.editExternals()
		elif type(self._action) == ComponentAction:
			event.accept()
	
	def mousePressEvent(self, event: QEvent):
		"""
		Handles what happens when the user releases the mouse on this menu item.

		This action is opened in the action pipeline editor view if it is an action pipeline

		:param event:
		:return:
		"""
		sm.StateMachine.instance.view.onEntitySelected(self._action)

		if event.buttons() != Qt.LeftButton:
			return
		
		if type(self._action) == ActionPipeline:
			event.accept()
			self.menu.editInternals()
			
	def update(self):
		"""
		updates the icon for the menu item.
		
		:return: None
		:rtype: NoneType
		"""
		self._actionGraphics.updateGraphics()
		br = self._actionGraphics.boundingRect()
		self._pix = QPixmap(br.width(), br.height())
		self._pix.setMask(self._pix.createHeuristicMask())
		painter = QPainter(self._pix)
		self._scene.render(painter)
		self.ui.actionIcon.setPixmap(self._pix)