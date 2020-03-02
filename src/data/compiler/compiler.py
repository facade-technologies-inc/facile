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

        statem = sm.StateMachine.instance
        self._compProf = compProf
        self._name = statem._project.getName()
        self._saveFolder = compProf.apiFolderDir + '/' # just save it directly where the user wants it.
        self._backend = statem._project.getBackend()
        self._exeLoc = statem._project.getExecutableFile()
        self._opts = compProf.compResOpts
        self._apim = statem._project.getAPIModel()
        self._tguim = statem._project.getTargetGUIModel()

        # List was reduced in size by making custom, "stripped" versions of files that only
        #  have the required functions & dependencies. That way no need to import graphics files and all that.
        self._necessaryFiles = ["./baseFiles/tguiil/componentfinder.py", "./baseFiles/tguiil/application.py",
                                "./baseFiles/tguiil/tokens.py", "./baseFiles/tguiil/supertokens.py",
                                "./baseFiles/tguiil/matchoption.py", "./baseFiles/data/entity.py",
                                "./baseFiles/data/tguim/component.py", "./baseFiles/data/tguim/visibilitybehavior.py",
                                "./baseFiles/data/properties.py", "./baseFiles/data/tguim/condition.py",
                                "./baseFiles/data/tguim/targetguimodel.py", "./baseFiles/data/property.py"]

    def generateCustomApp(self) -> None:
        """
        Creates the custom application class/file.

        :return: None
        """

        with open(self._saveFolder + "application.py", "w+") as f:
            
            f.write('''\
import sys, os
pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)

from typing import Set
from tguiil.matchoption import MatchOption
from baseapplication import BaseApplication

class Application(BaseApplication):
\tdef __init__(self):
\t\tBaseApplication.__init__(self, "''' + self._exeLoc + '", {')

            tmp = ''
            for i in self._opts:
                tmp += ', ' + str(i)

            f.write(tmp[2:])

            f.write('}, "' + self._name + '", "' + self._backend + '''")

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
            dir = os.path.join(self._saveFolder, dir)
            if not os.path.exists(dir):
                os.mkdir(dir)

        curPath = os.path.abspath(__file__)
        dir, filename = os.path.split(curPath)
        for path in self._necessaryFiles:
            # Make sure to copy necessary files into baseFiles dir, and remove unnecessary fns and dependencies.
            copyfile(os.path.join(dir, path), os.path.join(self._saveFolder, path[12:]))

    def saveTGUIM(self):
        """
        Saves the tguim in the API folder. Saves project as well.

        :return: None
        """

        statem = sm.StateMachine.instance
        statem._project.save()
        path = statem._project.getTargetGUIModelFile()
        name = statem._project.getName()

        copyfile(path, self._saveFolder + name + '.tguim')  # tguim saved to root, alongside baseapp and customapp

    def compileAPI(self) -> None:
        """
        Generates the functional API: the final result of compilation.

        :return: None
        """

        self.copyNecessaryFiles()
        self.saveTGUIM()

        curPath = os.path.abspath(__file__)
        dir, filename = os.path.split(curPath)
        copyfile(os.path.join(dir, 'baseapplication.py'), os.path.join(self._saveFolder, 'baseapplication.py'))

        self.generateCustomApp()
