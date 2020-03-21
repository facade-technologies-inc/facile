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


import sys, os
pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)

import time as t
import json
import traceback
from typing import Set
from tguiil.application import Application
from tguiil.matchoption import MatchOption
from tguiil.componentfinder import ComponentFinder
from data.tguim.targetguimodel import TargetGuiModel

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
        self.app = Application(backend = backend)
        self._options = options
        self._exeLoc= exeLoc
        self._name = name
        self._states = {'visible', 'ready', 'exists', 'enabled', 'active'}

        try:
            with open(os.path.join(pathToThisFile, self._name + ".tguim"), 'r') as tguimFile:
                d = json.loads(tguimFile.read())
                self._tgm = TargetGuiModel.fromDict(d)
        except:
            print("Couldn't load from {}".format('./' + self._name + '.tguim'))
            self._tgm = None
            traceback.print_exc()

    def start(self):
        """
        Starts the target application
        """
        
        self.app.start(self._exeLoc)

    def stop(self):
        """
        Stops the target application and the processes spawned by it
        """
        
        self.app.kill()

    def wait(self, time: float = 1, state: str = None):
        """
        Pauses until state is reached for the active window, otherwise until time (in seconds). Useful when waiting
        for target app to complete execution of a task, or when starting up.
        Wraps around pywinauto's wait function.
        
        :param time: number of seconds to wait. defaults to 1 second, and acts as failsafe if active window couldn't be found
        :type time: float
        :param state: state to wait for ('visible', 'ready', 'exists', 'enabled', 'active')
        :type state: str
        """
        
        if state in self._states:
            try:
                self.app.getActiveWindow().wait(state)
            except:
                t.sleep(time)
        else:
            t.sleep(time)

    def findComponent(self, compID: int):
        """
        Finds the component with ID compID forcing its appearance if not visible.
        
        :param compID: ID of component to find.
        :type compID: int
        """
        
        cf = ComponentFinder(self.app, self._options)

        if self._tgm:
            comp = self._tgm.getComponent(compID)
            self.forceShow(comp)
            return cf.find(comp.getSuperToken())
        else:
            return

    def forceShow(self, comp: 'Component'):
        """
        Attempts to force the component to be visible using visibility behaviors.

        :return: None
        """

        # comp.wait('exists')
        pass