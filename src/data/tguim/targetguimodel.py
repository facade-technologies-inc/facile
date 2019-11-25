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

This module contains the TargetGuiModel class.
"""

from collections import OrderedDict

from PySide2.QtCore import QObject, Slot, Signal

from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior
from graphics.tguim.tscene import TScene
from tguiil.supertokens import SuperToken
from data.properties import Properties


class TargetGuiModel(QObject):
	"""
	This class models the structure and behavior of the target gui.
	It contains Components organized in a tree structure, and stores the VisibilityBehaviors.
	New components are constructed and added to the tree when it receives new SuperTokens from
	the Observer.
	"""
	dataChanged = Signal(int)
	
	def __init__(self) -> 'TargetGuiModel':
		"""
		Constructs a TargetGuiModel object.

		:return: The constructed TargetGuiModel object
		:rtype: TargetGuiModel
		"""
		QObject.__init__(self)
		self._scene = TScene(self)
		self._root = Component(self)  # Note: remains constant. Represents the application.
		self._components = OrderedDict()  # Note: Root Component not stored here.
		self._visibilityBehaviors = OrderedDict()
		
		# Allows easy lookup of components given a super token
		self._superTokenToComponentMapping = {None: None}
	
	def getRoot(self) -> 'Component':
		"""
		Gets the root component of the component tree.

		:return: The root component of the component tree.
		:rtype: Component
		"""
		return self._root
	
	def getScene(self) -> 'TScene':
		"""
		Gets the associated graphics scene
		
		:return: The GraphicsScene associated with the TargetGuiModel
		:rtype: TScene
		"""
		return self._scene
	
	def getComponents(self) -> dict:
		"""
		Gets the dictionary of components.

		:return: The dictionary of components.
		:rtype: dict
		"""
		return self._components
	
	def getComponent(self, iD: int) -> 'Component':
		"""
		Gets the component with the specified id.

		:param iD: The component's unique identifier. See Entity class.
		:type iD: int
		:return: Component with the given id
		:rtype: Component
		"""
		
		if iD in self._components:
			return self._components[iD]
		else:
			return None
	
	@Slot()
	def createComponent(self, newSuperToken: 'SuperToken', parentToken: 'SuperToken') -> 'Component':
		"""
		The slot function which is called when the Observer emits the "newSuperToken" signal.
		Creates a new component using info from the SuperToken and adds it to the component tree.

		:param newSuperToken: The SuperToken associated with the component in the target GUI.
		:type newSuperToken: SuperToken
		:param parentToken: The parent SuperToken of the new SuperToken
		:type parentToken: SuperToken
		:return: The component that was created
		:rtype: 'Component'
		"""
		if parentToken is None:
			parentComponent = self._root
		else:
			parentComponent = self._superTokenToComponentMapping[parentToken]
		
		newComponent = Component(self, parentComponent, newSuperToken)
		
		#TODO: Create Properties object based on values from the SuperToken
		predefinedCategories = []
		customCategories = {"Temporary":[{"name":     "Name",
		                                  "type":     str,
		                                  "default":  newSuperToken.tokens[-1].controlIDs[-1],
		                                  "readOnly": False},
		                                 {"name": "Type",
		                                  "type": str,
		                                  "default": newSuperToken.tokens[-1].type,
		                                  "readOnly": True}
		                                 ]}
		properties = Properties.createPropertiesObject(predefinedCategories, customCategories)
		newComponent.setProperties(properties)
		
		self._superTokenToComponentMapping[newSuperToken] = newComponent
		self._components[newComponent.getId()] = newComponent
		self.dataChanged.emit(newComponent.getId())
		return newComponent
	
	def getVisibilityBehaviors(self) -> dict:
		"""
		Gets the dictionary of VisibilityBehaviors.

		:return: The dictionary of VisibilityBehaviors.
		:rtype: dict
		"""
		return self._visibilityBehaviors
	
	def getNthVisibilityBehavior(self, n: int) -> 'VisibilityBehavior':
		"""
		Gets the visibility behavior at a specific position.
		:param n: the index of the visiblity behavior to get
		:type n: int
		:return: The visiblity behavior at index n
		:rtype: VisiblityBehavior
		"""
		
		keys = list(self._visibilityBehaviors.keys())
		keys.sort()
		return self._visibilityBehaviors[keys[n]]
	
	def getVisibilityBehavior(self, iD: int) -> 'VisibilityBehavior':
		"""
		Gets the VisibilityBehavior with the specified id.

		:param iD: The id of the desired VisibilityBehavior
		:type iD: int
		:return: The VisibilityBehavior with the specified id.
		:rtype: VisibilityBehavior
		"""
		if iD in self._visibilityBehaviors:
			return self._visibilityBehaviors[iD]
		else:
			return None
	
	def addVisibilityBehavior(self, newVisBehavior: 'VisibilityBehavior') -> None:
		"""
		Adds a given VisibilityBehavior to the dictionary of VisibilityBehaviors.

		:param newVisBehavior: The VisibilityBehavior object to be added.
		:type newVisBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		if newVisBehavior.getId() not in self._visibilityBehaviors:
			self._visibilityBehaviors[newVisBehavior.getId()] = newVisBehavior
		
		src = newVisBehavior.getSrcComponent()
		dest = newVisBehavior.getDestComponent()
		src.addSrcVisibilityBehavior(newVisBehavior)
		dest.addDestVisibilityBehavior(newVisBehavior)
