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

This module contains the VisibilityBehavior class.
"""

from enum import Enum, auto

from data.entity import Entity
from data.properties import Properties
from data.tguim.condition import Condition
from data.apim.componentaction import ComponentAction


class VisibilityBehavior(Entity):
	"""
	This class describes a visibility behavior in the target gui - how a component becomes visible
	 or invisible to the user. E.g. clicking a button (the "from" component) causes a window (the "to" component)
	 to be shown.
	"""
	
	class ReactionType(Enum):
		Show = auto()
		Hide = auto()
	
	def __init__(self, tguim: 'TargetGuiModel', srcComp: 'Component' = None,
	             destComp: 'Component' = None, reactionType: ReactionType = ReactionType.Show) -> \
		'VisibilityBehavior':
		"""
		Constructs a VisibilityBehavior object.
		
		:param tguim: The one and only target GUI model
		:type tguim: TargetGuiModel
		:param srcComp: The "source" component. The one triggering the vis behavior.
		:type srcComp: Component
		:param destComp: The "destination" component. The one whose visibility is affected by the vis behavior.
		:type destComp: Component
		:param reactionType: Show or Hide
		:type reactionType: ReactionType
		:return: A constructed VisibilityBehavior
		:rtype: VisibilityBehavior
		"""
		
		super().__init__()
		self._destComponent = destComp
		self._srcComponent = srcComp
		self._condition = Condition()
		self._tguim = tguim
		self._triggerAction = None
		self.methodName = None
		
		if srcComp and destComp:
			
			predefined = ["Base", "Visibility Behavior"]
			custom = {}
			props = Properties.createPropertiesObject(predefined, custom)
			props.getProperty("ID")[1].setValue(self.getId())
			props.getProperty("Reaction Type")[1].setValue(reactionType)
			props.getProperty("Name")[1].setValue("VB #{}".format(self.getId()))
			props.getProperty("Type")[1].setValue("Visibility Behavior")
			props.getProperty("Source ID")[1].setValue(self._srcComponent.getId())
			props.getProperty("Destination ID")[1].setValue(self._destComponent.getId())
			
			self.setProperties(props)

		self.triggerUpdate()
	
	def getDestComponent(self) -> 'Component':
		"""
		Gets the "Destination" component of the visibility behavior - the component whose visibility is affected.

		:return: The "Destination" component of the visibility behavior.
		:rtype: Component
		"""
		
		return self._destComponent
	
	def getSrcComponent(self) -> 'Component':
		"""
		Gets the "source" component of the visibility behavior - the component that triggers the vis behavior.

		:return: The "source" component of the visibility behavior
		:rtype: Component
		"""
		
		return self._srcComponent
	
	def getCondition(self) -> 'Condition':
		"""
		Gets the Condition object associated with this visibility behavior.

		:return: The Condition object associated with this visibility behavior.
		:rtype: Condition
		"""
		
		return self._condition
	
	def getReactionType(self) -> ReactionType:
		"""
		Gets the reaction type of the visibility behavior.

		:return: The reaction type of the visibility behavior.
		:rtype: ReactionType
		"""
		return self.getProperties().getProperty("Reaction Type")[1].getValue()
	
	def setDestComponent(self, destComp: 'Component') -> None:
		"""
		Sets the "Destination" component of the visibility behavior - the component whose visibility is affected.

		:param destComp: The desired "to/destination" component of the visibility behavior
		:type destComp: Component
		:return: None
		:rtype: NoneType
		"""
		self._destComponent = destComp
	
	def setSrcComponent(self, srcComp: 'Component') -> None:
		"""
		Sets the "from" component of the visibility behavior - the component that triggers the vis behavior.

		:param srcComp: The desired "from/source" component of the visibility behavior
		:type srcComp: Component
		:return: None
		:rtype: NoneType
		"""
		
		self._srcComponent = srcComp
	
	def setReactionType(self, reactType: ReactionType) -> None:
		"""
		Sets the reaction type of the visibility behavior. Input param must be in the set of valid reaction types.

		:param reactType: The reaction of the visibility behavior
		:type reactType: ReactionType
		:return:
		"""
		self.getProperties().getProperty("Reaction Type")[1].setValue(reactType)

	def setTriggerAction(self, action: 'ComponentAction') -> None:
		"""
		Sets the action that triggers this visibility behavior.

		:param action: An action operating on the source component that triggers the visibility behavior.
		:type action: ComponentAction
		:return: None
		:rtype: NoneType
		"""
		self._triggerAction = action
		self.getProperties().getProperty("Trigger Action")[1].setValue(action.getName())
		self.methodName = action.getMethodName()

	def getTriggerAction(self) -> 'ComponentAction':
		"""
		Gets the action that triggers this visibility behavior

		:return:
		"""
		return self._triggerAction
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the visibility behavior.

		.. note::
			This is not just a getter of the __dict__ attribute.
		
		.. todo::
			save the condition

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		d = {}
		d["id"] = self._id
		d["src"] = self._srcComponent.getId()
		d["dest"] = self._destComponent.getId()
		d['properties'] = self.getProperties().asDict()
		# d['triggerAction'] = self._triggerAction.asDict()
		d["methodName"] = self.methodName
		
		return d
	
	@staticmethod
	def fromDict(d: dict, tguim: 'TargetGuiModel') -> 'VisibilityBehavior':
		"""
		Creates a visibility behavior from a dictionary.

		The created visibility behavior isn't "complete" because it only holds the IDs of other
		components and visibility behaviors. Outside of this function, the references are completed.

		.. note::
			The graphics item will not be created here. It must be created later.

		.. todo:
			Restore the condition

		:param d: The dictionary that represents the VisibilityBehavior.
		:type d: dict
		:param tguim: The target GUI model to add the component to
		:type tguim: TargetGuiModel
		:return: The VisibilityBehavior object that was constructed from the dictionary
		:rtype: VisibilityBehavior
		"""
		
		if d is None:
			return None
		
		vb = VisibilityBehavior(tguim)
		vb._id = d['id']
		vb._srcComponent = d['src']
		vb._destComponent = d['dest']
		vb.setProperties(Properties.fromDict(d['properties']))
		reactionType = vb.getProperties().getProperty("Reaction Type")[1].getValue()
		vb.getProperties().getProperty("Reaction Type")[1].setValue(
			VisibilityBehavior.ReactionType[reactionType])
		# vb._triggerAction = ComponentAction.fromDict(d['triggerAction'], tguim)
		methodName = d["methodName"]
		vb.methodName = methodName
		
		# Getting the trigger action from tguim
		# s = methodName.split("_")
		# id = s[1]
		# vb._triggerAction = ComponentAction(tguim.getComponent(id), None)
		return vb
