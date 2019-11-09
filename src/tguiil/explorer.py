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

from pywinauto import application
from subprocess import Popen
from pywinauto import Desktop
import pyautogui


class Explorer:

    def __init__(self):

        """
        Constructs an instance of the Explorer class

        :return: Explorer instance
        :rtype: Explorer
        """
        x = 1  # placeholder, nothing really to instantiate in explorer

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
        #  Maybe send signal to observer to search for new window
        x = 1  # placeholder

    def start(self):
        """
        Method that starts the explorer

        :return: None
        :rtype: NoneType
        """
        app = application.Application(backend='uia').start('Notepad.exe', timeout=60)  # times out after a minute
        top_window = app.top_window()
        # Popen('Notepad.exe', shell=True)
        # Wins = Desktop(backend='uia').windows()
        # topWindow = Wins[0]
        # print(topWindow.friendly_class_name())

        # Menu Traversal first
        # m = topWindow.Menu
        # print(m.items())

        self.ch_recurse(app, top_window)
