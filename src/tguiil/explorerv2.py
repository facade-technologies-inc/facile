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

This module contains the Explorer class, which explores the target GUI.
"""

import psutil
from PySide2.QtCore import QThread

import pyautogui
import time, sys

from psutil import Process
from pywinauto.application import Application
import tguiil.application as cApp


class Explorer(QThread):
    """
    The explorer class makes use of recursive functions to break down the target gui into its smallest components,
    and then clicking on every clickable component as well as prompting the user for input on any textfields.
    """

    def __init__(self, processLoc: str, backend: str = "uia"):
        """
        Constructs an Explorer.

        :raises: NoSuchProcess
        :raises: AccessDenied
        :param processLoc: The path to the process executable
        :type processLoc: string
        :param backend: The type of backend to use, defaulted to uia
        :type backend: string
        """

        super().__init__()
        self._pLoc = processLoc
        self._backend = backend

    def run(self):
        """
        Method that overrides QThread's run function

        :return: None
        :rtype: NoneType
        """

        self.start_process()
