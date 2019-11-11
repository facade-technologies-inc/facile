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
import time
from pywinauto.application import Application

import tguiil.application as cApp


class Explorer:

    def __init__(self):
        self.run = 0  # Defines the state of the explorer. Will run if 1, else will stop

    def ch_recurse(self, app, component):

        """
        Recursively called in order to find smallest components and click/expand them if possible.

        :param app: A handle to the application instance
        :type app: pywinauto.application.Application
        :param component: The component to be broken down
        :type component: (variable type, usually stems from pywinauto.base_wrapper.BaseWrapper)
        :return: None
        :rtype: NoneType
        """
        if self.run == 1:
            try:
                for child in component.children():
                    print(child.texts()[0] + ': ' + child.friendly_class_name())
                    # NOTE: All print statements are for verification and debugging purposes

                    if child.children() != []:  # recurse until smallest component with no sub-components
                        # this is the only part that handles recursion, and it does so depth-first
                        print('------child------')
                        self.ch_recurse(app, child)
                        print('-----------------')

                    if child.friendly_class_name() == 'MenuItem':
                        child.set_focus()
                        child.select()
                        # self.ch_recurse(app, child) # TODO: Figure out how to click on items of submenu
                        print('')
                    else:
                        try:
                            if child.is_editable():
                                # Pauses when editable textfield is found
                                pyautogui.alert('Please enter necessary information, then press OK.')
                                print(child.get_value())

                        except:
                            x = 1  # placeholder, excepting adds functionality here

                        finally:
                            try:
                                if child.is_clickable():
                                    child.set_focus()
                                    child.click()
                                    self.search_new_win(app)
                            except:
                                x = 1
                            finally:
                                print('')
            finally:
                return

    def search_new_win(self, app):
        x = 1  # placeholder

    def start(self, pLoc):
        """
        Method that starts the explorer while also starting the target application

        :return: None
        :rtype: NoneType
        """

        pid = psutil.Popen([pLoc])
        self.connect(pid)

    def connect(self, pid):
        """
        Method that starts the explorer while also connecting to the target application

        :return: None
        :rtype: NoneType
        """
        app = cApp.Application(backend="uia")
        app.setProcess(pid)
        pids = app.getPIDs()
        print(pids)

        time.sleep(0.5)  # without this it doesn't work. TODO: May need a way to wait only the necessary amount of time
        nApp = Application(backend='uia').connect(process=pids[0])
        appWindows = nApp.windows()

        self.run = 1
        # TODO: Update every time a new window appears.
        for window in appWindows:
            print('hello')
            self.ch_recurse(app, window)

    def stop(self):
        """
        Method that stops the explorer

        :return: None
        :rtype: NoneType
        """
        self.run = 0  # This will have to be implemented by interrupting the thread I think, but this is the best alt rn


def main():
    expr = Explorer()
    path = pyautogui.prompt('Please enter application path (Default is Notepad).')

    if path == '':
        path = 'Notepad.exe'

    if path is None:
        pyautogui.alert('Cancelled')
    else:
        expr.start(path)


if __name__ == "__main__":
    main()
