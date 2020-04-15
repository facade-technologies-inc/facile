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

This module contains the TargetGuiModel class.
"""

from collections import OrderedDict

from PySide2.QtCore import QObject, Slot, Signal

from data.entity import Entity
from tguiil.supertokens import SuperToken
from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior


class TargetGuiModel(QObject):
	"""
	This class models the structure and behavior of the target gui.
	It contains Components organized in a tree structure, and stores the VisibilityBehaviors.
	New components are constructed and added to the tree when it receives new SuperTokens from
	the Observer.
	"""
	dataChanged = Signal(int)
	newComponent = Signal(Component)
	newBehavior = Signal(VisibilityBehavior)
	behaviorRemoved = Signal(VisibilityBehavior)

	def __init__(self) -> 'TargetGuiModel':
		"""
		Constructs a TargetGuiModel object.

		:return: The constructed TargetGuiModel object
		:rtype: TargetGuiModel
		"""
		QObject.__init__(self)
		self._root = Component(self)  # Note: remains constant. Represents the application.

		# maps component id to component
		self._components = OrderedDict()  # Note: Root Component not stored here.

		# maps visibility behavior id to visibility behavior
		self._visibilityBehaviors = OrderedDict()

		# Allows easy lookup of components given a super token
		self._superTokenToComponentMapping = {None: None}

	def resolveComponentCollisions(self) -> None:
		"""
		Resolves any component collisions that are present, when called.

		:return: None
		:rtype: NoneType
		"""

		pass
	
	def getRoot(self) -> 'Component':
		"""
		Gets the root component of the component tree.

		:return: The root component of the component tree.
		:rtype: Component
		"""
		return self._root
	
	def getComponents(self) -> dict:
		"""
		Gets the dictionary of components.

		:return: The dictionary of components.
		:rtype: dict
		"""
		return self._components
	
	def getTopLevelWindows(self) -> list:
		"""
		Gets a list of all top-level components in the tguim
		
		:return: list of all top-level components in the tguim
		:rtype: list
		"""
		
		windows = []
		for id, comp in self._components:
			if comp.depth is 0:
				windows.append(comp)
		return windows
	
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
	
	def getEntity(self, iD: int) -> 'Component':
		"""
		Gets the entity with the specified id.

		:param iD: The entity's unique identifier. See Entity class.
		:type iD: int
		:return: Entity with the given id
		:rtype: Entity
		"""
		
		if iD in self._components:
			return self._components[iD]
		elif iD in self._visibilityBehaviors:
			return self._visibilityBehaviors[iD]
		else:
			return None
	
	@Slot()
	def createComponent(self, newSuperToken: 'SuperToken',
	                    parentToken: 'SuperToken') -> 'Component':
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
			if parentComponent is None:
				print('THIS SHOULDNT HAPPEN----------: ' + newSuperToken.getTokens()[0].title)
		
		newComponent = Component(self, parentComponent, newSuperToken)
		
		self._superTokenToComponentMapping[newSuperToken] = newComponent
		self._components[newComponent.getId()] = newComponent
		self.dataChanged.emit(newComponent.getId())
		self.newComponent.emit(newComponent)
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
		self.newBehavior.emit(newVisBehavior)

	def removeVisibilityBehavior(self, vb: 'VisibilityBehavior') -> None:
		"""
		Removes a visibility behavior from the TGUIM completely. This action is not reversible.

		:param vb: The visibility behavior to remove.
		:type vb: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		if vb not in self._visibilityBehaviors.values():
			return

		vb.getSrcComponent().removeSrcVisibilityBehavior(vb)
		vb.getDestComponent().removeDestVisibilityBehavior(vb)
		del self._visibilityBehaviors[vb.getId()]
		self.behaviorRemoved.emit(vb)
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the visibility behavior.

		.. note::
			This is not just a getter of the __dict__ attribute.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		tguimDict = {}
		
		tguimDict["root"] = self._root.asDict()
		
		tguimDict["components"] = {}
		for id, comp in self._components.items():
			tguimDict["components"][int(id)] = comp.asDict()
		
		tguimDict["behaviors"] = {}
		for id, vb in self._visibilityBehaviors.items():
			tguimDict["behaviors"][int(id)] = vb.asDict()
		
		tguimDict["Entity Count"] = Entity.count
		tguimDict["SuperToken Count"] = SuperToken.id_counter
		
		return tguimDict
	
	@staticmethod
	def fromDict(d: dict) -> 'TargetGui':
		"""
		Creates a target GUI model from a dictionary.
		
		This method reconstructs the entire target GUI model in 2 "passes". First, all of the
		components and visibility behaviors are created, but they only store IDs of other
		components and visibility behaviors. Once all of the objects have been created,
		the references are finalized. Children of components are not stored until the 2nd pass
		
		:param d: The dictionary that represents the target GUI model.
		:type d: dict
		:return: The TargetGUIModel object that was constructed from the dictionary
		:rtype: TargetGuiModel
		"""
		tguim = TargetGuiModel()
		tguim._root = Component.fromDict(d["root"], tguim)
		
		# create all components
		for id, comp in sorted(d['components'].items(), key=lambda item: item[1]['timestamp']):
			newComp = Component.fromDict(comp, tguim)
			tguim._components[int(id)] = newComp
			tguim._superTokenToComponentMapping[newComp.getSuperToken()] = newComp
		
		# create all visibility behaviors
		for id, vb in d['behaviors'].items():
			newVB = VisibilityBehavior.fromDict(vb, tguim)
			tguim._visibilityBehaviors[int(id)] = newVB
		
		# connect root's children
		for i in range(len(tguim._root._children)):
			tguim._root._children[i] = tguim._components[tguim._root._children[i]]
		
		# connect all components and visibility behaviors
		for component in tguim._components.values():
			if component._parent in tguim._components:
				component._parent = tguim._components[component._parent]
			else:
				component._parent = tguim._root
			
			for i in range(len(component._children)):
				component._children[i] = tguim._components[component._children[i]]
			
			for i in range(len(component._srcVisibilityBehaviors)):
				component._srcVisibilityBehaviors[i] = tguim._visibilityBehaviors[
					component._srcVisibilityBehaviors[i]]
			
			for i in range(len(component._destVisibilityBehaviors)):
				component._destVisibilityBehaviors[i] = tguim._visibilityBehaviors[
					component._destVisibilityBehaviors[i]]
		
		for vb in tguim._visibilityBehaviors.values():
			vb._srcComponent = tguim._components[vb._srcComponent]
			vb._destComponent = tguim._components[vb._destComponent]


		# Link up all children.
		work = [(tguim._root, None)]
		while work:
			cur, parent = work.pop()

			if parent:
				parent._children.append(cur)
				child_ids = d["components"][str(cur._id)]["children"]
			else:
				child_ids = d["root"]["children"]

			for child in [tguim._components[int(id)] for id in child_ids]:
				work.append((child, cur))

		Entity.count = d["Entity Count"]
		SuperToken.id_counter = d["SuperToken Count"]
		
		return tguim
