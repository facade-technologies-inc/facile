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

from data.apim.componentaction import ComponentAction


class ActionWrapperMenu(QMenu):
	
	def __init__(self):
		"""
		This class is the menu that shows when an action wrapper graphics item is right-clicked.
		
		Constructing a ActionWrapperMenu creates the menu items, but does not connect any
		actions. To connect the menu items to internal logic, use the methods that start with "on".
		"""
		QMenu.__init__(self)
		
		self._delete = self.addAction("Delete Action")
		
		# TODO: set action icons

		self.focusAction = self.addAction("Focus on target component")
		focusIcon = QIcon()
		focusIcon.addPixmap(QPixmap(":/icon/resources/icons/office/reticle.png"), QIcon.Normal, QIcon.Off)
		self.focusAction.setIcon(focusIcon)

	def onFocusTargetComponent(self, func) -> None:
		"""
		Connect the **Focus** menu item to internal logic.

		:param func: The function to execute when the **Focus** menu item is selected.
		:type func: callable
		:return: None
		"""
		self.focusAction.triggered.connect(func)

	def onDelete(self, func) -> None:
		"""
		Sets the function to be run when the delete action is triggered.

		:param func: The function to be run when the editExternal action is triggered.
		:type func: callabe
		:return: None
		:rtype: NoneType
		"""
		self._delete.triggered.connect(func)
		
	def delete(self) -> None:
		"""
		Emulates the user clicking the delete action

		:return: None
		:rtype: NoneType
		"""
		self._delete.trigger()
		
	def prerequest(self, wrapper) -> None:
		"""
		enables/disables the menu items appropriately before the context menu is requested. This
		function should be called right before the exec_() method is called.

		:param wrapper: The Action wrapper for the graphics item this menu belongs to.
		:type wrapper: ActionWrapper
		:return: None
		"""
		if isinstance(wrapper.getUnderlyingAction(), ComponentAction):
			self.focusAction.setEnabled(True)
		else:
			self.focusAction.setDisabled(True)