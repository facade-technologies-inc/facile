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

from data.tguim.condition import Condition
from data.entity import Entity


VALID_REACTION_TYPES = {"show", "hide"}


class VisibilityBehavior(Entity):
    """
    This class describes a visibility behavior in the target gui - how a component becomes visible
     or invisible to the user. E.g. clicking a button (the "from" component) causes a window (the "to" component)
     to be shown.
    """

    def __init__(self, fromComp: 'Component'=None, toComp: 'Component'=None,
                 reactionType: str="show") -> 'VisibilityBehavior':
        """
         Constructs a VisibilityBehavior object.

        :param fromComp: The "from" component. The one triggering the vis behavior.
        :type fromComp: Component
        :param toComp: The "to" component. The one whose visibility is affected by the vis behavior.
        :type toComp: Component
        :param reactionType: "show" or "hide".
        :return: A constructed VisibilityBehavior
        :rtype: VisibilityBehavior
        """

        super().__init__()
        self._toComponent = toComp
        self._fromComponent = fromComp
        self._condition = Condition()
        self._reactionType = None
        self._graphicsItem = None  # TODO: Construct a graphicsItem from the class Ramos creates.
        # TODO: Add a "trigger action" data member?

        if reactionType in VALID_REACTION_TYPES:
            self._reactionType = reactionType
        else:
            self._reactionType = "show"
            raise ValueError("VisibilityBehavior(): reactionType must be one of %r." % VALID_REACTION_TYPES)

    def getToComponent(self) -> 'Component':
        """
        Gets the "to" component of the visibility behavior - the component whose visibility is affected.

        :return: The "to" component of the visibility behavior
        :rtype: Component
        """

        return self._toComponent

    def getFromComponent(self) -> 'Component':
        """
        Gets the "from" component of the visibility behavior - the component that triggers the vis behavior.

        :return: The "from" component of the visibility behavior
        :rtype: Component
        """

        return self._fromComponent

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

        :return:
        :rtype:
        """
        return self._graphicsItem

    def setToComponent(self, toComp: 'Component') -> None:
        """
        Sets the "to" component of the visibility behavior - the component whose visibility is affected.

        :param toComp: The desired "to" component of the visibility behavior
        :type toComp: Component
        :return: None
        :rtype: NoneType
        """
        self._toComponent = toComp

    def setFromComponent(self, fromComp: 'Component') -> None:
        """
        Sets the "from" component of the visibility behavior - the component that triggers the vis behavior.

        :param fromComp: The desired "from" component of the visibility behavior
        :type fromComp: Component
        :return: None
        :rtype: NoneType
        """

        self._fromComponent = fromComp

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



