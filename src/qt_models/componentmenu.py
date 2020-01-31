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
	
This module contains the ComponentMenu class which is the context menu that is seen when a
component is right-clicked.

"""


from PySide2.QtWidgets import QMenu
import data.statemachine as sm

class ComponentMenu(QMenu):
	
	def __init__(self):
		"""
		This class is the menu that shows when a component is right clicked in the TGUIM view.
		
		Constructing a ComponentMenu creates the menu items, but does not connect any actions. To
		connect the menu items to internal logic, use the methods that start with "on". For
		instance, the *onBlink* method connects the "Show in target GUI" menu item to the
		function passed in. Of course, that function should execute code to use the blinker
		appropriately.
		"""
		QMenu.__init__(self)
		
		self.blinkAction = self.addAction("Show in target GUI")
		
	def onBlink(self, func) -> None:
		"""
		Connect the **Show in Target GUI** menu item to internal logic.
		
		:param func: The function to execute when the **Show in Target GUI** menu item is selected.
		:type func: callable
		:return: None
		"""
		self.blinkAction.triggered.connect(func)
		
	def prerequest(self) -> None:
		"""
		enables/disables the menu items appropriately before the context menu is requested. This
		function should be called right before the exec_() method is called.
		
		:return: None
		"""
		if sm.StateMachine.instance._project.getProcess():
			self.blinkAction.setEnabled(True)
		else:
			self.blinkAction.setEnabled(False)