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
from PySide2.QtGui import QIcon, QPixmap
import icons_rc
import data.statemachine as sm


class ActionItemMenu(QMenu):
	
	def __init__(self):
		"""
		This class is the menu that shows when an action menu item is right clicked in the action menu.
		
		Constructing a ActionItemMenu creates the menu items, but does not connect any actions. To
		connect the menu items to internal logic, use the methods that start with "on".
		"""
		QMenu.__init__(self)
		
		self._addAction = self.addAction("Add to Current Action Pipeline")
		
		# TODO: set action icons
	
	def onAdd(self, func):
		self._addAction.triggered.connect(func)
		
	def prerequest(self) -> None:
		"""
		enables/disables the menu items appropriately before the context menu is requested. This
		function should be called right before the exec_() method is called.
		
		:return: None
		"""
		pass