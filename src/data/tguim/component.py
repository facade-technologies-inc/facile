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

This module contains the Component class.
"""

from data.entity import Entity
from data.tguim.visibilitybehavior import VisibilityBehavior

class Component(Entity):
	"""
	This class models an individual GUI component in the target gui.
	Components are organized in a tree in the TargetGuiModel class.
	"""
	def __init__(self, parent=None):
		"""
		Constructs a Component object.

		:param parent: The parent component in the component tree.
		:type parent: Component
		"""

		super().__init__()
		# self._properties 	-> See Entity class
		# self._id 			-> See Entity class
		self._superToken = None  # TODO: add SuperToken.
		self._parent: Component = parent
		self._children = []
		self._graphicsItem = None  # TODO: insert Ramos's class.
		self._toVisibilityBehaviors = []
		self._fromVisibilityBehaviors = []
		if parent is not None:
			parent.addChild(self)
	
	def getChildren(self) -> list:
		"""
		Gets a list of the component's children components.

		:return: A list of the component's children components.
		:rtype: list
		"""
		return self._children
	
	def getSiblings(self) -> list:
		"""
		Gets a list of the component's sibling components, including itself.

		:return: A list of the component's sibling components, including itself.
		:rtype: list
		"""

		if self.getParent() is None:
			return [self]
		else:
			return self.getParent().getChildren()

	def childCount(self) -> int:
		"""
		Gets the number of child components the component has.

		:return: The number of child components the component has.
		:rtype: int
		"""

		return len(self._children)
	
	def getParent(self) -> 'Component':
		"""
		Gets the component's parent component.

		:return: The component's parent component.
		:rtype: Component
		"""
		return self._parent

	# TODO: Possibly rename depending on Ramos' class.
	def getParentGraphicsItem(self):
		if self._parent is None:
			return None
		else:
			return self._parent.getGraphicsItem()

	def getPathFromRoot(self) -> list:
		"""
		Gets the path in the tree to the component from the root.
		The path is a list of 2-element tuples where the first element is a component,
		and the second element is the position of that component amongst its siblings.

		:return: The path to the component from the root.
		:rtype: list
		"""
		path = [(self, self.getPositionInSiblings())]
		possibleRoot = self.getParent()
		while possibleRoot is not None:
			path.append((possibleRoot, possibleRoot.getPositionInSiblings()))
			possibleRoot = possibleRoot.getParent()
		return path

	# TODO: possibly rename to match Ramos's class.
	def getGraphicsItem(self):
		"""
		Gets the associated graphics item used to display the component.

		:return: The graphics item used to display the component.
		:rtype: TODO
		"""
		return self._graphicsItem

	def getNthChild(self, n: int) -> 'Component':
		"""
		Gets the Nth child component of the component.

		:param n: The nth index into the component's list of children
		:type n: int
		:return: The nth child of the component. None if index out of range
		:rtype: Component
		"""
		if len(self._children) > n:
			return self._children[n]
		return None

	def getNumDescendants(self) -> int:
		"""
		Gets the number of components descended from this component in the tree.

		:return: The number of descendant components.
		:rtype: int
		"""

		numDescendants = 0

		if len(self.getChildren()) == 0:
			return 0

		for child in self.getChildren():
			numDescendants += 1
			numDescendants += child.getNumDescendants()

		return numDescendants

	def getMaxDepth(self, curDepth: int=1) -> int:
		"""
		Gets How many levels deep the tree goes below the component.

		:param curDepth: The level in the tree the component is at. (Root=1)
		:type: curDepth: int
		:return: How many levels deep the tree goes below the component.
		:rtype: int
		"""

		maxDepth = [curDepth]
		
		for child in self.getChildren():
			maxDepth.append(child.getMaxDepth(curDepth+1))

		return max(maxDepth)

	def getPositionInSiblings(self) -> int:
		"""
		Gets the index of itself in its parent's children list.

		:return: the index of itself in its parent's children list.
		:rtype: int
		"""
		if self._parent == None:
			return 0
		return self._parent.getChildren().index(self)


	def addChild(self, child, pos=0) -> None:
		"""
		Adds a given component to the list of children components.

		:param child: A component object to be added to the children list.
		:type child: Component
		:param pos: Optionally position the child in children list. default=0
		:type pos: int
		:return: None
		:rtype: NoneType
		"""

		self._children.insert(pos, child)

	# TODO: Finish redefining this function. Need graphics classes.
	def remove(self):
		# Check to see if the component is the root. Don't delete the root.
		if self._parent is not None:
			scene = self._graphicsItem.scene()
			siblings = self.getSiblings()
			oldParent = self._parent
			self._parent = None
			siblings.remove(self)  # Removing self from parent's children list.

			scene.removeItem(self._graphicsItem)

			if oldParent:
				oldParent.getGraphicsItem().triggerSceneUpdate()

	def addToVisibilityBehavior(self, newVisBehavior: VisibilityBehavior) -> None:
		"""
		Adds a given visibility behavior (VB) to the list of "to" visibility behaviors.
		"to" VBs are VBs triggered by this component.

		:param newVisBehavior: The VisibilityBehavior object which is triggered by this component.
		:type newVisBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""

		if newVisBehavior not in self._toVisibilityBehaviors:
			self._toVisibilityBehaviors.append(newVisBehavior)

	def removeToVisibilityBehavior(self, visBehavior: VisibilityBehavior) -> None:
		"""
		Removes a given visibility behavior (VB) from the list of "to" visibility behaviors.
		"to" VBs are VBs triggered by this component.

		:param visBehavior: The VisibilityBehavior object which is triggered by this component.
		:type visBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""

		if visBehavior in self._toVisibilityBehaviors:
			self._toVisibilityBehaviors.remove(visBehavior)

	def addFromVisibilityBehavior(self, newVisBehavior: VisibilityBehavior) -> None:
		"""
		Adds a given visibility behavior (VB) to the list of "from" visibility behaviors.
		"from" VBs are VBs that result in this component becoming visible in the target GUI.

		:param newVisBehavior: The VisibilityBehavior object which affects this component.
		:type newVisBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""

		if newVisBehavior not in self._fromVisibilityBehaviors:
			self._fromVisibilityBehaviors.append(newVisBehavior)

	def removeFromVisibilityBehavior(self, visBehavior: VisibilityBehavior) -> None:
		"""
		removes a given visibility behavior (VB) from the list of "from" visibility behaviors.
		"from" VBs are VBs that result in this component becoming visible in the target GUI.

		:param visBehavior: The VisibilityBehavior object which affects this component.
		:type visBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""

		if visBehavior in self._fromVisibilityBehaviors:
			self._fromVisibilityBehaviors.remove(visBehavior)

	def __repr__(self) -> str:
		"""
		Returns the component's id as a string.

		:return: The component's id as a string.
		:rtype: str
		"""
		return str(self._id)