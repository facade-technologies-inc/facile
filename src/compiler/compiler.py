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

class Compiler():

    def __init__(self, location: str, name: str, exeLoc: str, tguim, apim, caLoc: str, backend: str = 'uia'):
        """
        Initializes the compiler with required information.

        :param location: Absolute path to the folder in which API folder will be created & saved
        :type location: str
        :param name: Name of target application
        :type name: str
        :param exeLoc: absolute path to executable of target application
        :type exeLoc: str
        :param tguim: Target Gui Model
        :type tguim: model (?) TODO: find type
        :param apim: API Model
        :type apim: model (?) TODO: find type
        :param caLoc: absolute path to folder containing files describing component actions TODO: default?
        :type caLoc: str
        :param backend: Type of backend used by target application, defaulted to uia
        :type backend: str
        """

        #TODO: Default location to desirable place? or do it when the user is entering it in the gui?
        self._name = name
        self._location = location + "/" + self._name + "API" + "/"
        self._backend = backend
        self._exeLoc = exeLoc
        self._tguim = tguim
        self._apim = apim
    
    def createBaseApp(self):
        """
        Creates a skeleton for the custom application to build on, and saves it to baseApplication.py in the
        user-specfied directory.
        """

        f = open(self._location + "baseApplication.py", "w+")

        f.write('''\
            class BaseApplication():
                def __init__(self):
                    self.app = pywinauto.Application(backend = "''' + self._backend + '''")
                def start():
                    self.app = self.app.start("''' + self._exeLoc + '''")  # TODO: Double check if this works
                def stop():
                    self.app.kill()
        ''')                                               #TODO: Fill this with all necessary functionality

    def createCustomApp(self):
        """
        Creates the custom application class.
        """

        f = open(self._location +"application.py", "w+")   #TODO: decide if we want to use name.py or just application.py
        
        f.write('''\
            import BaseApplication

            class Application(BaseApplication):
                def __init__(self):
                    super.__init__(self)
        ''')                                               #TODO: Fill this out

        self.createCAMethods(f)
        self.createAPMethods(f)

    def createCAMethods(self, f: io.TextIOWrapper):
        """
        Generates the component action methods.

        :param f: File stream for file being written to
        :type f: io.TextIOWrapper
        """
                
        # TODO: make loops that auto generate methods for comp actions
        pass

    def createAPMethods(self, f: io.TextIOWrapper):
        """
        Generates the action pipeline methods.

        :param f: File stream for file being written to
        :type f: io.TextIOWrapper
        """
                
        # TODO: make loops that auto generate methods for APs
        pass


