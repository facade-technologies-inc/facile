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

This module contains the VisibilityBehavior class.
"""

from data.tguim.condition import Condition
from data.entity import Entity
from data.properties import Properties
from graphics.tguim.visibilitybehaviorgraphics import VBGraphics


VALID_REACTION_TYPES = {"show", "hide"}


class VisibilityBehavior(Entity):
	"""
	This class describes a visibility behavior in the target gui - how a component becomes visible
	 or invisible to the user. E.g. clicking a button (the "from" component) causes a window (the "to" component)
	 to be shown.
	"""

	def __init__(self, tguim: 'TargetGuiModel', srcComp: 'Component'=None, destComp: 'Component'=None,
				 reactionType: str="show") -> 'VisibilityBehavior':
		"""
		 Constructs a VisibilityBehavior object.

		:param tguim: The one and only target GUI model
		:type tguim: TargetGuiModel
		:param srcComp: The "from/source" component. The one triggering the vis behavior.
		:type srcComp: Component
		:param destComp: The "to/destination" component. The one whose visibility is affected by the vis behavior.
		:type destComp: Component
		:param reactionType: "show" or "hide".
		:return: A constructed VisibilityBehavior
		:rtype: VisibilityBehavior
		"""
		
		super().__init__()
		self._destComponent = destComp
		self._srcComponent = srcComp
		self._condition = Condition()
		self._reactionType = None
		self._tguim = tguim
		self._graphicsItem = VBGraphics(self, tguim.getScene())
		# TODO: Add a "trigger action" data member?
		
		if reactionType in VALID_REACTION_TYPES:
			self._reactionType = reactionType
		else:
			self._reactionType = "show"
			raise ValueError("VisibilityBehavior(): reactionType must be one of %r." % VALID_REACTION_TYPES)
		predefined = ["Base", "Visibility Behavior"]
		custom = {}
		props = Properties.createPropertiesObject(predefined, custom)
		props.getProperty("Name")[1].setValue("VB #{}".format(self.getId()))
		props.getProperty("Type")[1].setValue("Visibility Behavior")
		self.setProperties(props)
	
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
	
	def getReactionType(self) -> str:
		"""
		Gets the reaction type of the visibility behavior.

		:return: The reaction type of the visibility behavior.
		:rtype: str
		"""
		return self._reactionType
	
	def getGraphicsItem(self):  # TODO: type hint the return value. Update doc string.
		"""
		Gets the graphics item associated with the visibility behavior.

		:return: return the visibilitybehavior graphics item
		:rtype: VBGraphics
		"""
		return self._graphicsItem
	
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
	
	def setReactionType(self, reactType: str) -> None:
		"""
		Sets the reaction type of the visibility behavior. Input param must be in the set of valid reaction types.

		:param reactType:
		:return:
		"""
		
		if reactType in VALID_REACTION_TYPES:
			self._reactionType = reactType
		else:
			raise ValueError("VisibilityBehavior.setReactionType(): reactionType must be one of %r."
							 % VALID_REACTION_TYPES)



