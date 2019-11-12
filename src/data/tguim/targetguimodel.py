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

from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior

# TODO: Import Ramos's QGraphicsScene class. ???
# TODO: Import SuperToken class.
# TODO: finish adding doc strings.

class TargetGuiModel:
    """
    This class models the structure and behavior of the target gui.
    It contains Components organized in a tree structure, and stores the VisibilityBehaviors.
    New components are constructed and added to the tree when it receives new SuperTokens from
    the Observer.
    """

    def __init__(self):
        """
        Constructs a TargetGuiModel object.

        :return: The constructed TargetGuiModel object
        :rtype: TargetGuiModel
        """
        self._root = Component()  # Note: remains constant. Represents the application.
        self._scene = None  # TODO: Use Ramos' class here. Maybe pass as param?
        self._components = {}  # Note: Root Component not stored here.
        self._visibilityBehaviors = {}

    def getRoot(self) -> Component:
        """
        Gets the root component of the component tree.

        :return: The root component of the component tree.
        :rtype: Component
        """
        return self._root

    # TODO: Type hint Ramos's scene class and add doc string.
    def getScene(self) -> 'TargetGuiScene':
        return self._scene

    def getComponents(self) -> dict:
        """
        Gets the dictionary of components.

        :return: The dictionary of components.
        :rtype: dict
        """
        return self._components

    def getComponent(self, iD: int) -> Component:
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

    # Slot function for when the Observer emits the "newSuperToken" signal.
    def createComponent(self, superToken: 'SuperToken') -> None:
        """
        The slot function which is called when the Observer emits the "newSuperToken" signal.
        Creates a new component using info from the SuperToken and adds it to the component tree.

        :param superToken: The SuperToken associated with the component in the target GUI.
        :type superToken: SuperToken
        :return: None
        :rtype: NoneType
        """
        pass  # TODO: define this function. Remember to add the comp to the dict.

    def getVisibilityBehaviors(self) -> dict:
        """
        Gets the dictionary of VisibilityBehaviors.

        :return: The dictionary of VisibilityBehaviors.
        :rtype: dict
        """
        return self._visibilityBehaviors

    def getVisibilityBehavior(self, iD: int) -> VisibilityBehavior:
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

    def addVisibilityBehavior(self, newVisBehavior: VisibilityBehavior) -> None:
        """
        Adds a given VisibilityBehavior to the dictionary of VisibilityBehaviors.

        :param newVisBehavior: The VisibilityBehavior object to be added.
        :type newVisBehavior: VisibilityBehavior
        :return: None
        :rtype: NoneType
        """
        if newVisBehavior.getId() not in self._visibilityBehaviors:
            self._visibilityBehaviors[newVisBehavior.getId()] = newVisBehavior
