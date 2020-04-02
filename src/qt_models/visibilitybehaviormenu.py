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

This module contains the VisibilityBehaviorMenu class
"""

from PySide2.QtWidgets import QMenu

class VisibilityBehaviorMenu(QMenu):
    def __init__(self):
        """
        This class is the menu that shows when a visibility behavior is right clicked in the TGUIM

        Constructing a ActionItemMenu creates the menu items, but does not connect any actions. To
        connect the menu items to internal logic, use the methods that start with "on".
        """
        QMenu.__init__(self)

        self._removeAction = self.addAction("Remove this behavior")
        self._setTriggerAction = self.addAction("Select trigger action")
        # TODO: set action icons

    def onRemove(self, func) -> None:
        """
        Set the function to be run when the remove action is triggered.

        :param func: the function to be run when the add action is triggered.
        :type func: callable
        :return: None
        :rtype: NoneType
        """
        self._removeAction.triggered.connect(func)

    def onSetTrigger(self, func) -> None:
        """
        Set the function to be run when the set trigger action is triggered.

        :param func: the function to be run when the add action is triggered.
        :type func: callable
        :return: None
        :rtype: NoneType
        """
        self._setTriggerAction.triggered.connect(func)

    def prerequest(self) -> None:
        """
        enables/disables the menu items appropriately before the context menu is requested. This
        function should be called right before the exec_() method is called.

        :return: None
        """
        pass