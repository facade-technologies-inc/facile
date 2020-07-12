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
import os, json
from shutil import copyfile

from PySide2.QtCore import QObject, Signal

import data.statemachine as sm
from data.compilationprofile import CompilationProfile
from tools.api_compiler.copy_file_manifest import necessary_source_files
from libs.logging import compiler_logger as logger
from libs.logging import log_exceptions
import libs.env as env

curPath = os.path.abspath(os.path.join(env.FACILE_DIR, "tools/api_compiler/compiler.py"))
dir, filename = os.path.split(curPath)

class Compiler(QObject):
    stepStarted = Signal(str)
    stepComplete = Signal()
    finished = Signal()
    
    def __init__(self, compProf: 'CompilationProfile' = None) -> None:
        """
        Initializes the compiler with required information.

        :return: None
        """
        logger.debug("Instantiating compiler")
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
        self._saveFolder = os.path.join(compProf.apiFolderDir, self._name + '_API_Files/')
        self._srcFolder = os.path.join(self._saveFolder, self._apiName + '/')
        self._docFolder = os.path.join(self._srcFolder, 'Documentation/')
        
        # Make all save folders if they don't exist
        if not os.path.exists(self._saveFolder):  # If the user enters a path that doesn't exist, it is created
            os.mkdir(self._saveFolder)  # TODO: Should notify them of this in compiler dialog
        if not os.path.exists(self._srcFolder):
            os.mkdir(self._srcFolder)
        if not os.path.exists(self._docFolder):
            os.mkdir(self._docFolder)
        
        self._necessaryFiles = necessary_source_files
    
    def generateCustomApp(self) -> None:
        """
        Creates the custom application class/file.

        :return: None
        """
        msg = "Generating custom application driver"
        logger.info(msg)
        self.stepStarted.emit(msg)

        with open(os.path.join(self._srcFolder, "application.py"), "w+") as f:
            
            # TODO: The Facade Tech watermark thing is a little intense when the user needs
            #  to use it for their own purposes and may want to share their generated API online.
            #  Could make a custom tag. I put the original in for the moment though.

            logger.debug("Reading application-unfilled.py")
            try:
                with open(os.path.join(dir, 'application-template.py'), 'r') as g:
                    appStr = g.read()
            except Exception as e:
                logger.exception(e)

            logger.debug("Generating options set")
            optStr = '{'
            for opt in self._opts:
                optStr += str(opt) + ', '
            optStr = optStr[:-2] + '}'

            logger.debug("Generating str of required compIDs")
            alreadyWritten = []
            aps, cas = self._apim.getActionsByType()
            compIDs = '['
            for action in cas:
                alreadyWritten.append(action.getTargetComponent().getId())
                compIDs += str(action.getTargetComponent().getId()) + ', '

            # We also want the visibilitybehaviors' triggeractions' components' IDs
            vbs = self._tguim.getVisibilityBehaviors()
            for id in vbs:
                vb = vbs[id]
                name = vb.methodName
                triggerAction = vb.getTriggerAction()
                if name not in alreadyWritten and triggerAction is not None:
                    compIDs += str(triggerAction.getTargetComponent().getId()) + ', '

            compIDs = compIDs[:-2] + ']'  # remove the final ", " and close bracket

            logger.debug("Format BaseApp superclass call with necessary info")
            try:
                appStr = appStr.format(exeLoc="'" + self._exeLoc + "'", options=optStr, name="'" + self._name + "'",
                                       backend="'" + self._backend + "'", reqCompIDs=compIDs)
            except Exception as e:
                logger.exception(e)
            logger.debug("Writing BaseApp")
            f.write(appStr)

            logger.debug("Writing methods generated from actions that are used in action pipelines.")
            alreadyWritten = []
            for action in cas:
                alreadyWritten.append(action.getMethodName())
                f.write(action.getMethod())

            logger.debug("Writing methods generated from actions that are used by visibility behaviors.")
            for id in vbs:
                vb = vbs[id]
                name = vb.methodName
                triggerAction = vb.getTriggerAction()
                if name not in alreadyWritten and triggerAction is not None:
                    f.write(triggerAction.getMethod())

            logger.debug("Writing methods generated from action pipelines.")
            for ap in aps:
                f.write(ap.getMethod())

        logger.info("Finished generating custom application driver.")
        self.stepComplete.emit()

    def copyNecessaryFiles(self) -> None:
        """
        Adds all necessary files for compiler to work into created directory

        :return: None
        """
        self.stepStarted.emit("Copying necessary files")

        # make necessary directories before copying files
        targetDirs = ['data', 'data/tguim', 'tguiil', 'libs']  # 'data/apim',
        for tdir in targetDirs:
            tdir = os.path.join(self._srcFolder, tdir)
            if not os.path.exists(tdir):
                os.mkdir(tdir)

        for path in self._necessaryFiles:
            src = os.path.abspath(os.path.join(env.FACILE_SRC_DIR, path))
            dest = os.path.abspath(os.path.join(self._srcFolder, path))
            logger.info(f"Copying file: {src} -> {dest}")
            try:
                copyfile(src, dest)
            except Exception as e:
                logger.critical("Unable to copy file.")
                logger.exception(e)

        self.stepComplete.emit()
    
    def saveTGUIM(self):
        """
        Saves the tguim in the API folder. Saves project as well.

        :return: None
        """

        msg = "Saving target GUI model"
        self.stepStarted.emit(msg)
        logger.info(msg)
        self.statem._project.save()
        with open(self._srcFolder + "tguim.json", "w+") as f:
            f.write(json.dumps(self._tguim.asDict()))

        self.stepComplete.emit()

    def copyBaseApp(self):
        """
        Copies the BaseApplication file to the API
        """

        msg = "Copying base application"
        self.stepStarted.emit(msg)
        logger.info(msg)
        copyfile(os.path.join(dir, 'baseapplication.py'), os.path.join(self._srcFolder, 'baseapplication.py'))
        self.stepComplete.emit()

    def generateSetupFile(self):
        """
        Generates the setup file for installing the API
        """
        # Create setup.py so user can install install API as a package with pip.
        msg = "Generating setup.py file"
        self.stepStarted.emit(msg)
        logger.info(msg)

        setupTempFile = open(os.path.join(dir, "setup-template.txt"), 'r')
        setupStr = setupTempFile.read().format(projectName=self.statem._project.getAPIName(),
                                               projectVersion='0.1.0')  # TODO Add versioning
        setupTempFile.close()
        setupFile = open(os.path.join(self._saveFolder, 'setup.py'), 'w')
        setupFile.write(setupStr)
        setupFile.close()

        self.stepComplete.emit()

    def generateInitFile(self):
        """
        Generates the init file so the package can be installed as an API
        """
        # Create __init__.py so API is a package.
        msg = "Generating __init__.py file"
        self.stepStarted.emit(msg)
        logger.info(msg)

        initTempFile = open(os.path.join(dir, "__init__template.txt"), 'r')
        targetAppName = self.statem._project.getExecutableFile().split('/')[-1].split('.')[0]  # '.../app.exe' -> 'app'
        targetAppName = targetAppName[0].upper() + targetAppName[1:]  # 'app' -> 'App'
        initStr = initTempFile.read().format(targetApplicationName=targetAppName)
        initTempFile.close()

        initFile = open(os.path.join(self._srcFolder, '__init__.py'), 'w')
        initFile.write(initStr)
        initFile.close()

        self.stepComplete.emit()

    def installAPI(self):
        """
        Installs the generated API to PATH
        """
        msg = "Installing as python package"
        self.stepStarted.emit(msg)
        logger.info(msg)

        os.chdir(self._saveFolder)
        os.system(self._compProf.interpExeDir + " -m pip install . 1>install.log 2>&1")

        logger.info("Finished installing python package")
        self.stepComplete.emit()

    def copyHelpFiles(self):
        """
        Generates files that give the basic structure and outline of a functional script.
        Will only write them if they do not yet exist, to avoid overwriting any existing work in the automate.py file.
        """
        msg = "Copying help files"
        self.stepStarted.emit(msg)
        logger.info(msg)
        if not os.path.exists(self._saveFolder + "automate.py"):
            with open(self._saveFolder + "automate.py", "w+") as f:
                with open(os.path.join(dir, 'automate-template.txt'), 'r') as g:
                    autoStr = g.read()

                f.write(autoStr.format(name=self._name))

            copyfile(os.path.join(dir, 'run-script.bat'), os.path.join(self._saveFolder, 'run-script.bat'))

    @log_exceptions(logger=logger)
    def compileAPI(self):
        """
        Generates the functional API: the final result of compilation.
        """
        logger.info("Compiling API")

        self.copyNecessaryFiles()
        self.saveTGUIM()
        self.copyBaseApp()

        if self._compProf.installApi:
            self.generateSetupFile()
            self.generateInitFile()

        self.generateCustomApp()

        if self._compProf.installApi:
            self.installAPI()

        self.copyHelpFiles()
        self.finished.emit()

        logger.info("Finished compiling API")