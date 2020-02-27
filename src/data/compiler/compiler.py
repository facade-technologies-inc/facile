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

import io
from data.statemachine import StateMachine as sm
from data.compilationprofile import CompilationProfile

class Compiler():

    def __init__(self, compProf: 'CompilationProfile' = None, name: str = 'MyCustom', backend: str = 'uia'):
        """
        Initializes the compiler with required information.
        """

        #TODO: Default location to desirable place? or do it when the user is entering it in the gui?
        #TODO: change var names based on whats actually in compilation profile
        self._compProf = compProf
        self._name = name
        self._saveFolder = compProf.apiFolderDir + "/" + self._name + "API" + "/"
        self._backend = backend
        self._exeLoc = compProf.interpExeDir
        self._apim = sm._project.getAPIModel()
        self._necessaryFiles = ["../../tguiil/componentfinder.py", "../../tguiil/application.py", "../../tguiil/tokens.py", "../../tguiil/supertokens.py", "../../tguiil/matchoption.py"]

    def createCustomApp(self) -> None:
        """
        Creates the custom application class.
        """

        with open(self._saveFolder +"application.py", "w+") as f:
            
            f.write('''\
                from baseapplication import BaseApplication

                class Application(BaseApplication):
                    def __init__(self):
                        BaseApplication.__init__(self, "''' + self._backend + '", "' + self._exeLoc + '''")
            ''')

            aps, cas = self._apim.getActionsByType()

            for action in cas:
                f.write(action.getMethod())
            
            for ap in aps:
                f.write(ap.getMethod())

    def addNecessaryFiles(self):
        """
        Adds all necessary files for compiler to work into created directory
        """

        #TODO: Fill out
        pass



        


