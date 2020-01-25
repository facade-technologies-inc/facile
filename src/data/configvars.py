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

This module contains the configVars class (configuration variables).
"""

from PySide2.QtCore import Slot, Signal, QObject


class ConfigVars(QObject):
    """
    This class stores the configuration variables associated with Facile's UI.
    For example, the boolean variables that determine whether Visibility Behaviors
    or Token tags are shown in the TGUIM View are stored here.
    Facile should have only ONE configVars object.
    """

    updateTGUIMView = Signal()

    def __init__(self):
        """
        Constructs a ConfigVars (configuration variables) object.
        """
        QObject.__init__(self)
        self.showBehaviors = True
        self.showTokenTags = True

    @Slot(bool)
    def setShowBehaviors(self, isChecked: bool):
        """
        This is a Slot function.
        Sets the showBehaviors configuration variable to the given input boolean.
        E.g. If showBehaviors is true, visibility behaviors will be shown in the TGUIM View.
        The updateTGUIMView signal is emitted when this function is called.

        :param isChecked: Boolean value that's true if the user selects to show visibility behaviors.
        :type isChecked: bool
        :return: None
        :rtype: NoneType
        """
        self.showBehaviors = isChecked
        self.updateTGUIMView.emit()

    @Slot(bool)
    def setShowTokenTags(self, isChecked: bool):
        """
        This is a Slot function.
        Sets the showTokenTags configuration variable to the given input boolean.
        E.g. If showTokenTags is true, token tags will be shown in the TGUIM View.
        The updateTGUIMView signal is emitted when this function is called.

        :param isChecked:  Boolean value that's true if the user selects to show token tags.
        :type isChecked: bool
        :return: None
        :rtype: NoneType
        """
        self.showTokenTags = isChecked
        self.updateTGUIMView.emit()
