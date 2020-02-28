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
work in the gui, converting it into the desired API.
"""

from data.statemachine import StateMachine as sm
from data.compilationprofile import CompilationProfile
from shutil import copyfile

class Compiler():

    def __init__(self, compProf: 'CompilationProfile' = None, name: str = 'MyCustom', backend: str = 'uia') -> None:
        """
        Initializes the compiler with required information.

        :return: None
        """

        self._compProf = compProf
        self._name = name
        self._saveFolder = compProf.apiFolderDir + "/" + self._name + "API/"
        self._backend = backend
        self._exeLoc = compProf.interpExeDir
        self._opts = compProf.compResOpts
        self._apim = sm._project.getAPIModel()

        # List was reduced in size by making custom, "stripped" versions of files that only
        #  have the required functions & dependencies. That way no need to import graphics files and all that.
        self._necessaryFiles = ["./baseFiles/tguiil/componentfinder.py", "./baseFiles/tguiil/application.py",
                                "./baseFiles/tguiil/tokens.py", "./baseFiles/tguiil/supertokens.py",
                                "./baseFiles/tguiil/matchoption.py", "./baseFiles/data/entity.py",
                                "./baseFiles/data/tguim/component.py", "./baseFiles/data/tguim/visibilitybehavior.py",
                                "./baseFiles/data/properties.py", "./baseFiles/data/tguim/condition.py"]

    def generateCustomApp(self) -> None:
        """
        Creates the custom application class/file.

        :return: None
        """

        with open(self._saveFolder +"application.py", "w+") as f:
            
            f.write('''\
                from baseapplication import BaseApplication

                class Application(BaseApplication):
                    def __init__(self):
                        BaseApplication.__init__(self, "''' + self._exeLoc + '", "' + self._opts + '", "' + self._backend + '''")
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

        for path in self._necessaryFiles:
            # Make sure to copy necessary files into baseFiles dir, and remove unnecessary fns and dependencies.
            copyfile(path, self._saveFolder + path[12:])

    def compileAPI(self) -> None:
        """
        Generates the functional API: the final result of compilation.

        :return: None
        """

        self.copyNecessaryFiles()
        copyfile('./baseApplication.py', self._saveFolder)
        self.generateCustomApp()
