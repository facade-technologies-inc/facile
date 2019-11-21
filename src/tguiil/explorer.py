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
import pyautogui
from PySide2.QtCore import QThread

from tguiil.application import Application


class Explorer(QThread):
    """
    The explorer class makes use of recursive functions to break down the target gui into its smallest components,
    and then clicking on every clickable component as well as prompting the user for input on any textfields.
    """

    def __init__(self, processID: int, backend: str = 'uia'):
        """
        Initializes explorer.

        :param processID: process ID of target application
        :type processID: int
        :param backend: type of backend to use: either uia or win32
        :type backend: str
        """

        super().__init__()
        self._process = psutil.Process(processID)
        self._backend = backend
        self._isRunning = False

    def run(self) -> int:
        """
        Called when thread is started

        :return: the exit code
        :rtype: int
        """

        # NOTE: Commented lines are for implementation of menu traversal, which needs work.
        app = Application(backend=self._backend)
        app.setProcess(self._process)

        try:
            if self._process.is_running():
                work = [win for win in app.windows()]
                # menu_paths = []

                while len(work) > 0:
                    component = work.pop()

                    for child in component.children():
                        work.append(child)

                    # if component.friendly_class_name() == 'MenuItem':
                    #     menu_paths.append((component.top_level_parent(), component.get_menu_path()))

                    try:
                        if component.is_editable():  # Editable textfields
                            pyautogui.alert('Please enter necessary information, then press OK.')
                    except:
                        pass
                    finally:
                        try:
                            if component.is_clickable() and component.window_text() != 'Cancel':  # Buttons
                                component.set_focus()
                                component.click()
                        except:
                            pass
                        finally:
                            pass

                # for menupath in menu_paths:
                #     window = menupath[0]
                #     window.menu_select(menupath[1])
        finally:
            return 0

    def play(self):
        """
        Runs the Explorer.

        :return: True if the observer is running, False otherwise.
        :rtype: bool
        """

        if not self._process.is_running():
            return False

        if self.isRunning():
            return True

        self.start()
        return self.isRunning()

    def pause(self):
        """
        Stops the Explorer.

        :return: True if the observer is running, False otherwise.
        :rtype: bool
        """

        if self.isRunning():
            self.quit()
            return True
        return False
