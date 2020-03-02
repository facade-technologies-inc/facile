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
"""


import sys, os
pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)


import json
import traceback
#import pywinauto
from typing import Set
from tguiil.application import Application
from tguiil.matchoption import MatchOption
from tguiil.componentfinder import ComponentFinder
from data.tguim.targetguimodel import TargetGuiModel

class BaseApplication():
    def __init__(self, exeLoc: str, options: Set['MatchOption'], name: str, backend: str = 'uia'):
        # Note that app is a custom Desktop instance from pywinauto, not an application instance.
        self.app = Application(backend = backend)
        self._options = options
        self._exeLoc= exeLoc
        self._name = name

    def start(self):
        self.app.start(self._exeLoc)

    def stop(self):
        self.app.kill()

    def findComponent(self, compID: int):
        cf = ComponentFinder(self.app, self._options)

        try:
            with open(os.path.join(pathToThisFile, self._name + ".tguim"), 'r') as tguimFile:
                d = json.loads(tguimFile.read())
                tgm = TargetGuiModel.fromDict(d)
        except:
            print("Couldn't load from {}".format('./' + self._name + '.tguim'))
            traceback.print_exc()
            return
        else:
            comp = tgm.getComponent(compID)
            self.forceShow(comp)
            return cf.find(comp.getSuperToken())

    def forceShow(self, comp: 'Component'):
        """
        Attempts to force show the component using visibility behaviors.

        :return: None
        """

        # comp.wait('exists')
        pass