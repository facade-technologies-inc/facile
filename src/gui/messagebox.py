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

This module contains the code for the custom QMessageBox.
"""

from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QResizeEvent
from gui.frame.windows import ModernWindow
import pyautogui


class MessageBox(QMessageBox):
    """
    Subclass of QMessageBox in order to get normal behavior from it while still having the custom title bar.
    Has only the close button in the top right. No need for other two.
    """

    def __init__(self, *args, **kwargs):
        if args:
            QMessageBox.__init__(self, args[0], args[1], args[2],
                                 buttons=kwargs.get('options', QMessageBox.StandardButton.NoButton),
                                 parent=kwargs.get('parent', None),
                                 flags=kwargs.get('flags', Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint))
        else:
            QMessageBox.__init__(self)

        self.origParent = kwargs.get('parent', None)
        self.screenSize = pyautogui.size()
        self.movedToCenter = False

        self._wrapper = ModernWindow(self)
        self._wrapper.btnMaximize.hide()
        self._wrapper.btnMinimize.hide()
        self._wrapper.setMinimumSize(self.minimumSizeHint())
        self.setParent(self._wrapper)

    def exec_(self) -> int:
        """
        Overloads the original exec function to give expected behavior with custom title bar. Returns button clicked.
        :return: integer bit value of button clicked
        :rtype: int
        """
        self.move(0, self._wrapper.titleBar.height())
        self.finished.connect(lambda state: self._wrapper.done(state))
        return self._wrapper.exec_()

    @staticmethod
    def question(parent: 'PySide2.QtWidgets.QWidget', title: str, text: str, options) -> int:
        """
        Overloads question function for QMessageBox to have custom title bar and normal functionality
        :return: integer bit value of button clicked
        :rtype: int
        """
        return MessageBox(QMessageBox.Question, title, text, options=options, parent=parent).exec_()

    def resizeEvent(self, event: QResizeEvent):
        """
        Catches when self is resized, and applies that size + title bar height to wrapper

        :param event: The resize event, storing the new size
        :type event: QResizeEvent
        """
        newSize = event.size()
        newSize.setHeight(newSize.height() + self._wrapper.titleBar.height())
        self._wrapper.resize(newSize)
