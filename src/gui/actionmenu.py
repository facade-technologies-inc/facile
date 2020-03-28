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

This module contains the ActionMenu() Class.
"""

import sys
import os

sys.path.append(os.path.abspath("../"))

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout

from gui.ui.ui_actionmenu import Ui_Form as Ui_ActionMenu
from gui.actionmenuitem import ActionMenuItem
from data.apim.actionpipeline import ActionPipeline
from data.apim.port import Port
from data.apim.action import Action
import data.statemachine as sm


class ActionMenu(QWidget):
	"""
	ActionMenu is a widget for Facile's API actions.
	"""
	
	actionSelected = Signal(Action)
	
	def __init__(self) -> 'ActionMenu':
		"""
		Constructs a ActionMenu object.

		:return: The new ActionMenu object
		:rtype: ActionMenu
		"""
		super(ActionMenu, self).__init__()
		
		# UI Initialization
		self.ui = Ui_ActionMenu()
		self.ui.setupUi(self)
		
		self.clearActions()
		
	def clearActions(self) -> None:
		"""
		removes all action widgets from the action menu
		
		:return: None
		:rtype: NoneType
		"""
		# Widget Initialization
		self.ui._centralWidget = QWidget()
		self.ui._itemLayout = QVBoxLayout()
		
		self.ui._centralWidget.setLayout(self.ui._itemLayout)
		self.ui.menuItemScrollArea.setWidget(self.ui._centralWidget)
		self.ui._itemLayout.addStretch()
		
	def addAction(self, action: "Action") -> None:
		"""
		Creates an ActionMenuItem for the given action and adds it to this ActionMenu.
		
		:param action: The specific action that will be added as ActionMenuItem.
		:type action: Action
		:return: None
		:rtype: Nonetype
		"""
		if isinstance(action, ActionPipeline):
			sm.StateMachine.instance._project.getAPIModel().addActionPipeline(action)
		menuItem = ActionMenuItem(action)
		self.ui._itemLayout.addWidget(menuItem)
		self.actionSelected.emit(action)

	def setLabelText(self, text: str) -> None:
		"""
		Setting the label for the menu's description.
		
		:param text: Text that will be in the label.
		:type text: str
		:return: None
		:rtype: Nonetype
		"""
		self.ui.menuLabel.setText(text)
		
if __name__ == "__main__":
	app = QApplication()
	w = ActionMenu()
	p1 = Port()
	p2 = Port()
	p3 = Port()
	p4 = Port()
	p5 = Port()
	ap = ActionPipeline()
	ap.addInputPort(p1)
	ap.addInputPort(p2)
	ap.addOutputPort(p3)
	ap.addOutputPort(p4)
	ap.addOutputPort(p5)
	
	for i in range(10):
		ap.getProperties().getProperty("Name")[1].setValue("Action Pipeline" + str(i))
		w.addAction(ap)
		
	w.show()
	
	sys.exit(app.exec_())