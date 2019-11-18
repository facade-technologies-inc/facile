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

import time

import psutil
import pyautogui
import pywinauto
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

        app = Application(backend=self._backend)
        app.setProcess(self._process)

        # Need a general try/finally so that the function still returns
        try:
            # if instead of while because we don't want the explorer to restart after finding all windows
            if self._process.is_running():
                work = [win for win in app.windows()]

                while len(work) > 0:
                    component = work.pop()
                    print(component.window_text())

                    if component.children() != []:
                        for child in component.children():
                            work.append(child)

                    if component.friendly_class_name() == 'MenuItem':
                        component.set_focus()
                        component.select()
                    else:
                        try:
                            # Pauses when editable textfield is found
                            if component.is_editable():
                                pyautogui.alert('Please enter necessary information, then press OK.')
                                print(component.get_value())

                        except:
                            continue

                        finally:
                            try:
                                if component.is_clickable():
                                    component.set_focus()
                                    component.click()
                                    self.search_new_win(app)
                            except:
                                x = 1  # placeholder, python 3.7 doesnt support continue in finally
                            finally:
                                print('')

        finally:
            return 0

    def getSubmenuItems(self, app: Application):
        x = 1


def main():

    # This section is here for standalone testing. TODO: Remove/modify when done
    process = psutil.Popen('Notepad.exe')
    pid = process.pid

    expr = Explorer(pid)
    path = pyautogui.prompt('Please enter application path (Default is Notepad).', default='Notepad.exe')

    if path == '':
        path = 'Notepad.exe'  # could prompt the user for valid path but that's gonna be handled elsewhere in project

    if path is None:
        pyautogui.alert('Cancelled')
    else:
        print('runs')
        expr.run()  # This + explorer instance are all that'll be necessary since path will be given to explorer


if __name__ == "__main__":
    main()
