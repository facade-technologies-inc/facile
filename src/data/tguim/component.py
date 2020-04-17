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

This module contains the Component class.
"""
from PIL.Image import Image
from datetime import datetime

from datetime import datetime

try: # Facile imports
	from data.entity import Entity
	from data.properties import Properties
	from data.tguim.visibilitybehavior import VisibilityBehavior
	from tguiil.supertokens import SuperToken
except ImportError: # API imports
	from ..entity import Entity
	from ..properties import Properties
	from .visibilitybehavior import VisibilityBehavior
	from ...tguiil.supertokens import SuperToken



class Component(Entity):
	"""
	This class models an individual GUI component in the target gui.
	Components are organized in a tree in the TargetGuiModel class.
	"""
	
	def __init__(self, tguim: 'TargetGuiModel', parent: 'Component' = None, superToken: 'SuperToken' = None):
		"""
		Constructs a Component object.

		:param tguim: The TargetGuiModel that the component belongs to.
		:type tguim: TargetGuiModel
		:param parent: The parent component in the component tree.
		:type parent: Component
		:param superToken: The SuperToken associated with the new Component
		:type superToken: SuperToken
		"""
		
		super().__init__()
		self._superToken: 'SuperToken' = superToken
		self._parent: 'Component' = parent
		self._children = []
		self._srcVisibilityBehaviors = []
		self._destVisibilityBehaviors = []
		self._model = tguim
		self.timestamp = datetime.now().timestamp()
		self.depth = -1  # -1 if root, 0 if window, etc.
		self.isExtraComponent = False
		self.loadedFromTGUIM = False  # This is only set to true when loaded from a tguim file,
										# then promptly set back to false
		
		if parent is not None:
			parent.addChild(self)
			
			propToken = superToken.getTokens()[0]
			predefinedCategories = ["Base", "GUI Component", "Visual"]
			customCategories = {}
			props = Properties.createPropertiesObject(predefinedCategories, customCategories)
			assert(props is not None)
			# Set base property values
			props.getProperty("ID")[1].setValue(self.getId())
			props.getProperty("Name")[1].setValue(propToken.controlIDs[-1])
			props.getProperty("Type")[1].setValue("Component")
			
			# Set component property values
			props.getProperty("Title")[1].setValue(propToken.title)
			props.getProperty("Parent Title")[1].setValue(propToken.parentTitle)
			props.getProperty("Class Name")[1].setValue(propToken.type)
			props.getProperty("Is Dialog")[1].setValue(propToken.isDialog)
			
			# Set visual property values
			geometry = superToken.posRelativeToParent
			props.getProperty("X")[1].setValue(geometry[0])
			props.getProperty("Y")[1].setValue(geometry[1])
			props.getProperty("Width")[1].setValue(geometry[2])
			props.getProperty("Height")[1].setValue(geometry[3])
			# props.getProperty("Has Moved")[1].setValue(self._graphicsItem.getNumMoves() != 0)
			
			self.setProperties(props)
			
			nxtParent = parent
			while nxtParent:
				self.depth += 1
				nxtParent = nxtParent.getParent()

		self.triggerUpdate()
	
	def getSuperToken(self) -> 'SuperToken':
		"""
		Gets the component's SuperToken
		
		:return: The component's SuperToken
		:rtype: SuperToken
		"""
		return self._superToken
	
	def getSrcVisibilityBehaviors(self):
		"""
		Gets all the visibility behaviors coming out from this component

		:return: The list of all the visibility behaviors coming out from this component
		:rtype: List of VisibilityBehavior
		"""
		return self._srcVisibilityBehaviors
	
	def getDestVisibilityBehaviors(self):
		"""
		Gets all the visibility behaviors coming into this component

		:return: The list of all the visibility behaviors coming into this component
		:rtype: List of VisibilityBehavior
		"""
		return self._destVisibilityBehaviors
	
	def getModel(self) -> 'TargetGuiModel':
		"""
		Gets the target GUI model that this component belongs to.
		
		:return: the target GUI model that this component belongs to.
		:rtype: TargetGuiModel
		"""
		return self._model
	
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
			return self.getParent().getChildren()[:]  # Modified to return actual siblings not copies (removed [:])
	
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
	
	def getMaxDepth(self, curDepth: int = 1) -> int:
		"""
		Gets How many levels deep the tree goes below the component.

		:param curDepth: The level in the tree the component is at. (Root=1)
		:type: curDepth: int
		:return: How many levels deep the tree goes below the component.
		:rtype: int
		"""
		
		maxDepth = [curDepth]
		
		for child in self.getChildren():
			maxDepth.append(child.getMaxDepth(curDepth + 1))
		
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
	
	def addDestVisibilityBehavior(self, newVisBehavior: VisibilityBehavior) -> None:
		"""
		Adds a given visibility behavior (VB) to the list of "Destination" visibility behaviors.
		This component is the destination for the VB.

		:param newVisBehavior: The VisibilityBehavior that affects the visibility of this component.
		:type newVisBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		
		if newVisBehavior not in self._destVisibilityBehaviors:
			self._destVisibilityBehaviors.append(newVisBehavior)
	
	def removeDestVisibilityBehavior(self, visBehavior: VisibilityBehavior) -> None:
		"""
		Removes a given visibility behavior (VB) from the list of "Destination" visibility behaviors.
		This component is the destination for the VB.

		:param visBehavior: The VisibilityBehavior that affects the visibility of this component.
		:type visBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		
		if visBehavior in self._destVisibilityBehaviors:
			self._destVisibilityBehaviors.remove(visBehavior)
	
	def addSrcVisibilityBehavior(self, newVisBehavior: VisibilityBehavior) -> None:
		"""
		Adds a given visibility behavior (VB) to the list of "Source" visibility behaviors.
		"Source" VBs are VBs coming out from this component.

		:param newVisBehavior: The VisibilityBehavior that is triggered by ('coming out from') this component.
		:type newVisBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		
		if newVisBehavior not in self._srcVisibilityBehaviors:
			self._srcVisibilityBehaviors.append(newVisBehavior)
	
	def removeSrcVisibilityBehavior(self, visBehavior: VisibilityBehavior) -> None:
		"""
		removes a given visibility behavior (VB) from the list of "Source" visibility behaviors.
		"Source" VBs are VBs coming out from this component.

		:param visBehavior: The VisibilityBehavior that is triggered by ('coming out from') this component.
		:type visBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		
		if visBehavior in self._srcVisibilityBehaviors:
			self._srcVisibilityBehaviors.remove(visBehavior)
	
	def __repr__(self) -> str:
		"""
		Returns the component's id as a string.

		:return: The component's id as a string.
		:rtype: str
		"""
		return str(self._id)
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the component.
		
		NOTE: this is not just a getter of the __dict__ attribute.
		
		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		d = {}
		d["id"] = self._id
		d["srcBehaviors"] = [vb.getId() for vb in self._srcVisibilityBehaviors]
		d["destBehaviors"] = [vb.getId() for vb in self._destVisibilityBehaviors]
		d['children'] = [c.getId() for c in self._children]
		d['isEC'] = self.isExtraComponent
		d['depth'] = self.depth
		d['timestamp'] = self.timestamp
		
		if self._properties:
			d['properties'] = self.getProperties().asDict()
		else:
			d['properties'] = None
		
		if self._superToken:
			d['superToken'] = self._superToken.asDict()
		else:
			d['superToken'] = None
		
		if self._parent:
			d["parent"] = self._parent.getId()
		else:
			d["parent"] = None
		
		return d
	
	@staticmethod
	def fromDict(d: dict, tguim: 'TargetGuiModel') -> 'Component':
		"""
		Creates a Component from a dictionary.

		The created component isn't "complete" because it only holds the IDs of other components
		and visibility behaviors. Outside of this function, the references are completed. The
		children references are not set here because they need to be set one at a time while the
		graphics items are being created.

		:param d: The dictionary that represents the Component.
		:type d: dict
		:param tguim: The target GUI model to add the component to
		:type tguim: TargetGuiModel
		:return: The Component object that was constructed from the dictionary
		:rtype: Component
		"""
		
		if d is None:
			return None
		
		superToken = SuperToken.fromDict(d['superToken'])
		comp = Component(tguim, superToken=superToken)
		# comp._children = d['children'] # need to add children one at a time since graphics are
		# created later
		comp._id = d["id"]
		comp._srcVisibilityBehaviors = d['srcBehaviors']
		comp._destVisibilityBehaviors = d['destBehaviors']
		comp.setProperties(Properties.fromDict(d['properties']))
		comp._parent = d['parent']
		comp.timestamp = d['timestamp']
		comp.depth = d['depth']
		comp.isExtraComponent = d['isEC']
		comp.loadedFromTGUIM = True
		
		return comp

	def getFirstImage(self) -> 'PIL.Image':
		"""
		If any of the tokens in this component's supertoken have a valid image, return the first image.

		If no tokens have images, return None.
		:return: The first image out of all tokens in this component's super token.
		:rtype: PIL.Image
		"""
		for token in self._superToken.tokens:
			if token.pic:
				return token.pic