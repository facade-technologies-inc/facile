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
    """
    The explorer class makes use of recursive functions to break down the target gui into its smallest components,
    and then clicking on every clickable component as well as prompting the user for input on any textfields.
    """

    def __init__(self):
        self.run = 0  # Defines the state of the explorer. Will run if 1, else will stop

    def ch_recurse(self, app: Application, component):
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
                    # TODO: NOTE: All print statements are for verification and debugging purposes. Remove at end.

                    if child.children() != [] and child.friendly_class_name() != 'Menu':
                        # this is the only part that handles recursion, and it does so depth-first
                        print('------child------')
                        self.ch_recurse(app, child)
                        print('-----------------')

                    if child.friendly_class_name() == 'Menu' and child.texts()[0] != 'System':
                        # TODO: Finish submenu traversal. After testing traverseSubmenu, uncomment below and
                        #  modify connect function to call ch_recurse
                        # Menus are handled differently due to their nature

                        # for menuitem in child.items():
                        #     menuitem.set_focus()
                        #     menuitem.select()
                        #     submenu = nApp.top_window()
                        #     submenu.wait('ready')
                        #     self.traverseSubmenu(app, submenu)
                        #     # self.ch_recurse(app, submenu)
                        print('')
                    elif child.friendly_class_name() == 'MenuItem':
                        x = 1  # placeholder
                    else:
                        try:
                            if child.is_editable():
                                # Pauses when editable textfield is found
                                # TODO: Uncomment line below after testing
                                # pyautogui.alert('Please enter necessary information, then press OK.')
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

    def traverseSubmenu(self, app: Application, component):
        """
        Recursively called in order to find menus and menuitems and click/expand them if possible. Called only
        within ch_recurse and is therefore providing additional functionality to it without as much cluttering.
        (Basically a ch_recurse function specific to menus)

        :param app: A handle to the application instance
        :type app: pywinauto.application.Application
        :param component: The component to be broken down
        :type component: (variable type, usually stems from pywinauto.base_wrapper.BaseWrapper)
        :return: None
        :rtype: NoneType
        """

        try:
            for child in component.children():
                # Below handles breaking down menu
                if child.friendly_class_name() == 'Menu' and child.texts()[0] != 'System':
                    if child.texts()[0] != 'Application':
                        print(child.texts()[0] + ': ' + child.friendly_class_name())
                        print('------children------')
                        self.traverseSubmenu(app, child)
                        print('--------------------')

                # Below handles menuitems themselves
                elif child.friendly_class_name() == 'MenuItem':
                    print(child.texts()[0] + ': ' + child.friendly_class_name())
                    if child.is_enabled():
                        try:
                            child.set_focus()
                            child.select()
                            # TODO: Find way to reopen submenu
                            submenuWin = app.top_window()
                            submenuWin.wait('ready')
                            # TODO: Items like New, New window, etc should probably be avoided because it will loop
                            #  infinitely otherwise
                            # self.ch_recurse(app, submenuWin)
                            # pyautogui.alert(child.texts()[0] + ' was clicked')
                        except:
                            # Usually occurs after submenu is closed but item is being selected.
                            print('exception2 for ' + child.texts()[0])
                        finally:
                            print('')
                    else:
                        print('(disabled)')
        except:
            print('exception1')  # Haven't seen any of these
        finally:
            return

    def search_new_win(self, app: Application):
        x = 1  # placeholder

    def start(self, pLoc: str):
        """
        Method that starts the target application then connects to it for exploration

        :return: None
        :rtype: NoneType
        """

        pid = psutil.Popen([pLoc])
        self.connect(pid)

    def connect(self, pid: int):
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
            # self.ch_recurse(app, window)

            # Below will be in ch_recurse, but put here just for simpler development/debugging
            for child in window.children():
                if child.friendly_class_name() == 'Menu' and child.texts()[0] != 'System':
                    # TODO: Finish submenu traversal
                    for menuitem in child.items():
                        menuitem.set_focus()
                        menuitem.select()
                        submenu = nApp.top_window()
                        submenu.wait('ready')
                        # self.ch_recurse(nApp, submenu)
                        self.traverseSubmenu(nApp, submenu)
        nApp.kill()  # Only here so that I don't have tons of notepad instances open, TODO: Remove after testing

    def stop(self):
        """
        Method that stops the explorer

        :return: None
        :rtype: NoneType
        """

        self.run = 0  # This will have to be implemented by interrupting the thread I think, but this is the best alt rn


def main():

    # This section is here for standalone testing. TODO: Remove/modify when done

    expr = Explorer()
    path = pyautogui.prompt('Please enter application path (Default is Notepad).', default='Notepad.exe')

    if path == '':
        path = 'Notepad.exe'  # could prompt the user for valid path but that's gonna be handled elsewhere in project

    if path is None:
        pyautogui.alert('Cancelled')
    else:
        expr.start(path)  # This + explorer instance are all that'll be necessary since path will be given to explorer


if __name__ == "__main__":
    main()
