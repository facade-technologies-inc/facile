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

This module contains the TScene class.
"""

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QGraphicsScene


class TScene(QGraphicsScene):

    itemSelected = Signal(int)

    def __init__(self, targetGUIModel: 'TargetGuiModel'):
        """
        Construct the TScene class

        :param targetGUIModel: get the TargetGuiModel of the project
        :type targetGUIModel: TargetGuiModel
        """
        QGraphicsScene.__init__(self)
        self._targetGuiModel = targetGUIModel


    def getTargetGUIModel(self) -> 'TargetGuiModel':
        """
        Gets the target GUI Model.

        :return The target GUI model
        :rtype data.tguim.targetguimodel.TargetGuiModel
        """
        return self._targetGuiModel

    def emitItemSelected(self, id: int) -> None:
        """
        Emits a signal that carries the ID of the item that was selected

        :param id: The ID of the item that was selected.
        :type id: int
        :return: None
        :rtype: NoneType
        """
        self.itemSelected.emit(id)