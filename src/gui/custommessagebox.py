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


class MessageBox(QMessageBox):
    """
    Subclass of QMessageBox in order to get normal behavior from it while still having the custom title bar.
    Has only the close button in the top right. No need for other two buttons
    """

    def __init__(self, icon, title: str, text: str, buttons=None, parent=None, flags=None):
        normal = QMessageBox()

        if buttons:
            tmpB = buttons
        else:
            tmpB = normal.buttons()

        if parent:
            tmpP = parent
        else:
            tmpP = normal.parent()

        if flags:
            tmpF = flags
        else:
            tmpF = normal.windowFlags()

        QMessageBox.__init__(self, icon, title, text, buttons=tmpB, parent=tmpP, flags=tmpF)

        # TODO

