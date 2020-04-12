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
    
    This document contains the BaseApplication class
"""

import sys
import os
import time as t
import json
import pywinauto
import traceback
from typing import Set
from tguiil.application import Application
from tguiil.matchoption import MatchOption
from tguiil.componentfinder import ComponentFinder
from data.tguim.targetguimodel import TargetGuiModel

pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)


class WaitException(Exception):
    def __init__(self, msg: str):
        Exception.__init__(self, msg)


class BaseApplication():
    """
    The core of all Facile APIs: contains functions that are necessary for any API. The
    custom generated Application class inherits from this.
    """
    
    def __init__(self, exeLoc: str, options: Set['MatchOption'], name: str, backend: str = 'uia'):
        """
        Initializes a BaseApplication instance.
        
        :param exeLoc: filepath to executable for target application
        :type exeLoc: str
        :param options: options to use when searching for a component
        :type options: set
        :param name: project name (necessary for opening tguim file)
        :type name: str
        :param backend: backend type
        :type backend: str
        """
        
        # Note that app is a custom Desktop instance from pywinauto, not an application instance.
        self.app = Application(backend=backend)
        self._options = options
        self._exeLoc = exeLoc
        self._name = name
        
        try:
            with open(os.path.join(pathToThisFile, self._name + ".tguim"), 'r') as tguimFile:
                d = json.loads(tguimFile.read())
                self._tgm = TargetGuiModel.fromDict(d)
        except Exception as e:
            print("Couldn't load from {}".format('./' + self._name + '.tguim'))
            self._tgm = None
            traceback.print_exc()
    
    def startApp(self):
        """
        Starts the target application, then waits for all processes' active window to be ready.
        """
        
        self.app.start(self._exeLoc)
    
    def stop(self):
        """
        Stops the target application and the processes spawned by it
        """
        
        self.app.kill()
    
    def wait(self, state: str, timeout: int = 60):
        """
        Pauses until state is reached for each process's active window, timing out in timeout seconds.
        Useful when waiting for target app to complete execution of a task, or when starting up.
        Wraps around pywinauto's wait function.
        
        :param state: state to wait for ('visible', 'ready', 'exists', 'enabled', 'active'), or time to wait in s or m
        :type state: str
        :param timeout: Maximum number of seconds to wait for state to be reached. Defaults to a minute, should be longer for apps with more windows.
        :type timeout: float
        """
        
        try:
            if ' s' in state:
                t.sleep(float(state[:-2]))
            elif ' m' in state:
                t.sleep(60 * float(state[:-2]))
            else:
                self.app.wait(state, timeout)
        except Exception as e:
            raise WaitException('Not a valid wait time or state. Please use "x s" or "x m" for x seconds/minutes \
            respectively, or use one of "visible", "ready", "exists", "enabled", "active" as state to wait for.')
    
    def findComponent(self, compID: int) -> 'pywinauto.base_wrapper.BaseWrapper':
        """
        Finds the component with ID compID forcing its appearance if not visible.
        
        :param compID: ID of component to find.
        :type compID: int
        :return: handle to component
        :rtype: pywinauto.base_wrapper.BaseWrapper
        """
        
        cf = ComponentFinder(self.app, self._options)
        
        comp = self.getComponentObject(compID)
        self.forceShow(comp)
        return cf.find(comp.getSuperToken())
        
    def getComponentObject(self, compID: int) -> 'Component':
        """
        Gets the component item for an item with ID compID. Handles possible errors with getting it.
        
        :param compID: ID of component to get the Component object for
        :type compID: int
        :return: The component item for an item with ID compID
        :rtype: Component
        """
        if self._tgm:
            try:
                comp = self._tgm.getComponent(compID)
                if comp:
                    return comp
                else:
                    raise Exception("Could not get component " + str(compID) + " from TGUIM.")
            except Exception as e:
                raise Exception(str(e))
        else:
            raise Exception("No Target GUI Model in this API.")
    
    def forceShow(self, comp: 'Component'):
        """
        Attempts to force the component to be visible using visibility behaviors.
        
        :param comp: Component to show
        :type comp: Component
        """
        
        # comp.wait('exists')
        pass
    
    def selectMenuItem(self, component: 'Component'):
        """
        MenuItems can't be clicked the same way as other components, so this function takes care of this.
        
        :param component: menuItem to be selected
        :type component: Component
        :return: None
        """
        
        curComp = component
        nxtParent = curComp.getParent()
        compPath = [curComp]
        # Getting the lowest level component containing the menu/menuitem that can be force-shown
        while nxtParent.getSuperToken().getTokens()[0].type in ['Menu', 'MenuItem']:
            curComp = nxtParent
            nxtParent = curComp.getParent()
            compPath.append(curComp)
        # Now compPath has the list of components, including the component itself, in the reverse order that component
        # can be found with.
        
        # Create the string that can be input into the menu_select function of pywinauto
        pathStr = ''
        while compPath:
            comp = compPath.pop()
            pathStr += comp.getSuperToken().getTokens()[0].texts[0] + '->'
        pathStr = pathStr[:-2]
        
        # Then get the containing top-level window
        while not nxtParent.getSuperToken().getTokens()[0].isDialog:
            curComp = nxtParent
            nxtParent = nxtParent.getParent()
        
        # Now force show the window, and get its handle
        window = self.findComponent(nxtParent)
        
        # Then finally select the menuItem
        window.menu_select(pathStr)
