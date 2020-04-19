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
from shutil import copyfile

from PySide2.QtCore import QObject, Signal

import data.statemachine as sm
from data.compilationprofile import CompilationProfile


class Compiler(QObject):
    stepStarted = Signal(str)
    stepComplete = Signal()
    finished = Signal()
    
    def __init__(self, compProf: 'CompilationProfile' = None) -> None:
        """
        Initializes the compiler with required information.

        :return: None
        """
        QObject.__init__(self)
        self.statem = sm.StateMachine.instance
        self._compProf = compProf
        self._name = self.statem._project.getName()
        self._apiName = self.statem._project.getAPIName()
        self._backend = self.statem._project.getBackend()
        self._exeLoc = self.statem._project.getExecutableFile()
        self._opts = compProf.compResOpts
        self._apim = self.statem._project.getAPIModel()
        self._tguim = self.statem._project.getTargetGUIModel()
        
        # Save Folders
        self._saveFolder = compProf.apiFolderDir + '/'
        self._srcFolder = os.path.join(self._saveFolder, self._apiName + '/')
        self._docFolder = os.path.join(self._srcFolder, 'Documentation/')
        
        # Make all save folders if they don't exist
        if not os.path.exists(self._saveFolder):  # If the user enters a path that doesn't exist, it is created
            os.mkdir(self._saveFolder)  # TODO: Should notify them of this in compiler dialog
        if not os.path.exists(self._srcFolder):
            os.mkdir(self._srcFolder)
        if not os.path.exists(self._docFolder):
            os.mkdir(self._docFolder)
        
        self._necessaryFiles = ["../../tguiil/componentfinder.py", "../../tguiil/application.py",
                                "../../tguiil/tokens.py", "../../tguiil/supertokens.py",
                                "../../tguiil/matchoption.py", "../../data/entity.py",
                                "../../data/tguim/component.py", "../../data/tguim/visibilitybehavior.py",
                                "../../data/properties.py", "../../data/tguim/condition.py",
                                "../../data/tguim/targetguimodel.py", "../../data/property.py"]
                                # "../../data/apim/componentaction.py", "../../data/apim/action.py",
                                # "../../data/apim/actionspecification.py", "../../data/apim/port.py",
                                # "../../data/apim/wire.py", "../../data/apim/actionpipeline.py",
                                # "../../data/apim/actionwrapper.py", "../../data/apim/wireset.py"]
    
    def generateCustomApp(self) -> None:
        """
        Creates the custom application class/file.

        :return: None
        """
        self.stepStarted.emit("Generating custom application driver")
        with open(self._srcFolder + "application.py", "w+") as f:
            
            # TODO: The Facade Tech watermark thing is a little intense when the user needs
            #  to use it for their own purposes and may want to share their generated API online.
            #  Could make a custom tag. I put the original in for the moment though.

            curPath = os.path.abspath(__file__)
            dir, filename = os.path.split(curPath)
            
            with open(os.path.join(dir, 'application-unfilled.py'), 'r') as g:
                appStr = g.read()
            
            optStr = '{'
            for opt in self._opts:
                optStr += str(opt) + ', '
            optStr = optStr[:-2] + '}'
            
            appStr = appStr.format(exeLoc="'" + self._exeLoc + "'", options=optStr, name="'" + self._name + "'",
                                   backend="'" + self._backend + "'")
            f.write(appStr)
            
            aps, cas = self._apim.getActionsByType()
            vbs = self._tguim.getVisibilityBehaviors()
            alreadyWritten = []
            
            for action in cas:
                alreadyWritten.append(action.getMethodName())
                f.write(action.getMethod())
            for id in vbs:
                vb = vbs[id]
                name = vb.methodName
                if name not in alreadyWritten:
                    f.write(vb.getTriggerAction().getMethod())
            for ap in aps:
                f.write(ap.getMethod())
        self.stepComplete.emit()
    
    def copyNecessaryFiles(self) -> None:
        """
        Adds all necessary files for compiler to work into created directory

        :return: None
        """
        self.stepStarted.emit("Copying necessary files")
        # make necessary directories before copying files
        targetDirs = ['data', 'data/tguim', 'tguiil']  # 'data/apim',
        for dir in targetDirs:
            dir = os.path.join(self._srcFolder, dir)
            if not os.path.exists(dir):
                os.mkdir(dir)
        
        curPath = os.path.abspath(__file__)
        dir, filename = os.path.split(curPath)
        for path in self._necessaryFiles:
            copyfile(os.path.join(dir, path), os.path.join(self._srcFolder, path[6:]))
        self.stepComplete.emit()
    
    def saveTGUIM(self):
        """
        Saves the tguim in the API folder. Saves project as well.

        :return: None
        """
        self.stepStarted.emit("Saving target GUI model")
        self.statem._project.save()
        path = self.statem._project.getTargetGUIModelFile()
        name = self.statem._project.getName()

        copyfile(path, os.path.join(self._srcFolder, name + '.tguim'))  # tguim saved to root, alongside baseapp and customapp
        self.stepComplete.emit()
    
    def compileAPI(self) -> None:
        """
        Generates the functional API: the final result of compilation.

        :return: None
        """
        print("compiling")
        self.copyNecessaryFiles()
        self.saveTGUIM()

        self.stepStarted.emit("Copying base application")
        curPath = os.path.abspath(__file__)
        dir, filename = os.path.split(curPath)
        copyfile(os.path.join(dir, 'baseapplication.py'), os.path.join(self._srcFolder, 'baseapplication.py'))
        self.stepComplete.emit()

        # Create setup.py so user can install install API as a package with pip.
        self.stepStarted.emit("Generating setup.py file")
        setupTempFile = open(os.path.join(dir, "setup-template.txt"), 'r')
        setupStr = setupTempFile.read().format(projectName=self.statem._project.getAPIName(),
                                               projectVersion='0.1.0')  # TODO Add versioning
        setupTempFile.close()
        setupFile = open(os.path.join(self._saveFolder, 'setup.py'), 'w')
        setupFile.write(setupStr)
        setupFile.close()
        self.stepComplete.emit()

        # Create __init__.py so API is a package.
        self.stepStarted.emit("Generating __init__.py file")
        initTempFile = open(os.path.join(dir, "__init__template.txt"), 'r')
        targetAppName = self.statem._project.getExecutableFile().split('/')[-1].split('.')[0]  # '.../app.exe' -> 'app'
        targetAppName = targetAppName[0].upper() + targetAppName[1:]  # 'app' -> 'App'
        initStr = initTempFile.read().format(targetApplicationName=targetAppName)
        initTempFile.close()
        initFile = open(os.path.join(self._srcFolder, '__init__.py'), 'w')
        initFile.write(initStr)
        initFile.close()
        self.stepComplete.emit()
        
        self.generateCustomApp()

        # Auto install API if user selected to do so.
        if self._compProf.installApi:
            self.stepStarted.emit("Installing as python package")
            os.chdir(self._saveFolder)
            os.system(self._compProf.interpExeDir + " -m pip install . 1>install.log 2>&1")
            self.stepComplete.emit()

        self.finished.emit()
