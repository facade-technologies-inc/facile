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


# TODO: Import Ramos's QGraphicsScene class. ???
# TODO: Import corresponding QModel classes for the componentTree and the visibility behaviors.
# TODO: Import GuiComponent class.
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
        self._root = None  # TODO: Initialize the root.
        self._componentTreeQModel = None  # TODO: Initialize new QModel here.
        self._visibilityBehaviorsQModel = None   # TODO: Initialize new QModel here.
        self._scene = None  # TODO: Use Ramos' class here. Maybe pass as param?
        self._components = {}  # TODO: Add root "component" to the dict? Maybe it needs to remain inaccessible.
        self._visibilityBehaviors = {}

    # TODO: This getter may not be necessary.
    # def getRoot(self):
    #     # if self._root.isDeleted():
    #     #     return None
    #     return self._root

    # TODO: Want the root to always remain constant.
    # def setRoot(self, newRoot):
    #     if self._root is None:
    #         self._root = newRoot
    #     elif self._root.isDeleted():
    #         self._root = newRoot
    #     self._scene.addItem(newRoot.getNodeItem())

    def getComponentTreeQModel(self):
        return self._componentTreeQModel

    def getScene(self):
        return self._scene

    def getComponents(self):
        return self._components

    def getComponent(self, iD):
        if iD in self._components:
            return self._components[iD]
        else:
            return None

    # Slot function for when the Observer emits the "newSuperToken" signal.
    def createComponent(self, superToken):
        pass  # TODO: define this function.

    def getVisibilityBehaviors(self):
        return self._visibilityBehaviors

    def getVisibilityBehavior(self, iD):
        if iD in self._visibilityBehaviors:
            return self._visibilityBehaviors[iD]
        else:
            return None

    def addVisibilityBehavior(self, newVisBehavior):
        if newVisBehavior.getId() not in self._visibilityBehaviors:
            self._visibilityBehaviors[newVisBehavior.getId()] = newVisBehavior
