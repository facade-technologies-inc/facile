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

This file contains the Compiler class - the part of Facile that interprets a user's 
work in the gui, and converts it into the desired API.
"""
import os
import data.statemachine as sm
from data.compilationprofile import CompilationProfile
from shutil import copyfile

class Compiler():

    def __init__(self, compProf: 'CompilationProfile' = None) -> None:
        """
        Initializes the compiler with required information.

        :return: None
        """

        self.statem = sm.StateMachine.instance
        self._compProf = compProf
        self._name = self.statem._project.getName()
        self._backend = self.statem._project.getBackend()
        self._exeLoc = self.statem._project.getExecutableFile()
        self._opts = compProf.compResOpts
        self._apim = self.statem._project.getAPIModel()
        self._tguim = self.statem._project.getTargetGUIModel()
        
        # Save Folders
        self._saveFolder = compProf.apiFolderDir + '/'
        self._srcFolder = os.path.join(self._saveFolder, 'API/')
        self._docFolder = os.path.join(self._saveFolder, 'Documentation/')

        # Make all save folders if they don't exist
        if not os.path.exists(self._saveFolder):  # If the user enters a path that doesn't exist, it is created
            os.mkdir(self._saveFolder)            # TODO: Should notify them of this in compiler dialog
        if not os.path.exists(self._srcFolder):
            os.mkdir(self._srcFolder)
        if not os.path.exists(self._docFolder):
            os.mkdir(self._docFolder)

        # List was reduced in size by making custom, "stripped" versions of files that only
        #  have the required functions & dependencies. That way no need to import graphics files and all that.
        self._necessaryFiles = ["../../tguiil/componentfinder.py", "../../tguiil/application.py",
                                "../../tguiil/tokens.py", "../../tguiil/supertokens.py",
                                "../../tguiil/matchoption.py", "../../data/entity.py",
                                "../../data/tguim/component.py", "../../data/tguim/visibilitybehavior.py",
                                "../../data/properties.py", "../../data/tguim/condition.py",
                                "../../data/tguim/targetguimodel.py", "../../data/property.py"]

    def generateCustomApp(self) -> None:
        """
        Creates the custom application class/file.

        :return: None
        """

        with open(self._srcFolder + "application.py", "w+") as f:
            
            # TODO: The Facade Tech watermark thing is a little intense when the user needs
            #  to use it for their own purposes and may want to share their generated API online.
            #  Could make a custom tag. I put the original in for the moment though.
            
            f.write('''\
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
    
    This document contains the custom generated Application class
"""


import sys, os
pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)

from typing import Set
from tguiil.matchoption import MatchOption
from baseapplication import BaseApplication


class ActionException(Exception):
\tdef __init__(self, msg: str):
\t\tException.__init__(self, msg)

class Application(BaseApplication):
\t"""
\tThis class allows a user to automate a predefined target GUI using functions (action pipelines) defined
\tin Facile itself.
\t"""
\t
\tdef __init__(self):
\t\t"""
\t\tInitializes the Application class, then initializes its superclass with the necessary information.
\t\t"""
\t\t
\t\tBaseApplication.__init__(self, "''' + self._exeLoc + '", {')

            tmp = ''
            for i in self._opts:
                tmp += ', ' + str(i)

            f.write(tmp[2:])

            f.write('}, "' + self._name + '", "' + self._backend + '''")

\tdef start(self) -> 'Application':
\t\t"""
\t\tStarts the target application, then waits for all processes' active window to be ready.
\t\tReturns self, that way the user can just call Application().start() when initializing their app.
\t\t"""

\t\tself.startApp()
\t\treturn self

''')
            aps, cas = self._apim.getActionsByType()

            for action in cas:
                f.write(action.getMethod())

            for ap in aps:
                f.write(ap.getMethod())

    def copyNecessaryFiles(self) -> None:
        """
        Adds all necessary files for compiler to work into created directory

        :return: None
        """
        
        # make necessary directories before copying files
        targetDirs = ['data', 'data/tguim', 'tguiil']
        for dir in targetDirs:
            dir = os.path.join(self._srcFolder, dir)
            if not os.path.exists(dir):
                os.mkdir(dir)

        curPath = os.path.abspath(__file__)
        dir, filename = os.path.split(curPath)
        for path in self._necessaryFiles:
            # Make sure to copy necessary files into baseFiles dir, and remove unnecessary fns and dependencies.
            print(self._srcFolder)
            copyfile(os.path.join(dir, path), os.path.join(self._srcFolder, path[6:]))

    def saveTGUIM(self):
        """
        Saves the tguim in the API folder. Saves project as well.

        :return: None
        """

        self.statem._project.save()
        path = self.statem._project.getTargetGUIModelFile()
        name = self.statem._project.getName()

        copyfile(path, os.path.join(self._srcFolder, name + '.tguim')) # tguim saved to root, alongside baseapp and customapp

    def compileAPI(self) -> None:
        """
        Generates the functional API: the final result of compilation.

        :return: None
        """

        self.copyNecessaryFiles()
        self.saveTGUIM()

        curPath = os.path.abspath(__file__)
        dir, filename = os.path.split(curPath)
        copyfile(os.path.join(dir, 'baseapplication.py'), os.path.join(self._srcFolder, 'baseapplication.py'))

        self.generateCustomApp()
