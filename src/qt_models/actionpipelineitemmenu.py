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
from qt_models.actionitemmenu import ActionItemMenu


class ActionPipelineItemMenu(ActionItemMenu):
	
	def __init__(self):
		"""
		This class is the menu that shows when an action menu item is right clicked in the
		action pipeline menu.
		
		Constructing a ActionPipelineItemMenu creates the menu items, but does not connect any
		actions. To connect the menu items to internal logic, use the methods that start with "on".
		"""
		ActionItemMenu.__init__(self)
		
		self._editInternal = self.addAction("Edit Action Pipeline Behavior")
		self._editExternal = self.addAction("Edit Action Pipeline Interface")
		self._delete = self.addAction("Delete Action Pipeline")
		
		# TODO: set action icons
	
	def onEditInternals(self, func):
		"""
		Sets the function to be run when the editInternal signal is triggered.
		
		:param func: The function to be run when the editInternal action is triggered.
		:type func: callabe
		:return: None
		:rtype: NoneType
		"""
		self._editInternal.triggered.connect(func)
		
	def onEditExternals(self, func) -> None:
		"""
		Sets the function to be run when the editExternal action is triggered.
		
		:param func: The function to be run when the editExternal action is triggered.
		:type func: callabe
		:return: None
		:rtype: NoneType
		"""
		self._editExternal.triggered.connect(func)
		
	def onDelete(self, func) -> None:
		"""
		Sets the function to be run when the delete action is triggered.

		:param func: The function to be run when the editExternal action is triggered.
		:type func: callabe
		:return: None
		:rtype: NoneType
		"""
		self._delete.triggered.connect(func)
		
	def editInternals(self) -> None:
		"""
		Emulates the user clicking the editInternal action
		
		:return: None
		:rtype: NoneType
		"""
		self._editInternal.trigger()
	
	def editExternals(self) -> None:
		"""
		Emulates the user clicking the editExternal action

		:return: None
		:rtype: NoneType
		"""
		self._editExternal.trigger()
	
	def delete(self) -> None:
		"""
		Emulates the user clicking the delete action

		:return: None
		:rtype: NoneType
		"""
		self._delete.trigger()
		
	def prerequest(self) -> None:
		"""
		enables/disables the menu items appropriately before the context menu is requested. This
		function should be called right before the exec_() method is called.
		
		:return: None
		"""
		pass