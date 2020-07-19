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

    This document contains the DocGenerator class
"""

import os
import shutil
import subprocess

from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QApplication

import data.statemachine as sm
from data.compilationprofile import CompilationProfile
from libs.logging import compiler_logger as logger
from libs.logging import log_exceptions
import libs.env as env
from multiprocessing.pool import ThreadPool


def nongui(fun):
    """Decorator running the function in non-gui thread while
    processing the gui events."""

    def wrap(*args, **kwargs):
        pool = ThreadPool(processes=1)
        a_sync = pool.apply_async(fun, args, kwargs)
        while not a_sync.ready():
            a_sync.wait(0.01)
            QApplication.processEvents()
        return a_sync.get()

    return wrap


class DocGenerator(QObject):
    """
	This class is used to generate API documentations based on user's preference.
	"""

    stepStarted = Signal(str)
    stepComplete = Signal()
    finished = Signal()
    
    def __init__(self, docType: set, projectName: str):
        """
        Construct the class DocGenerator
        
        :param docType: user's choices on the type(s) of the documentations to be generated
        :type docType: set
        :param projectName: the name of the project
        :type projectName: str
        """
        QObject.__init__(self)
        logger.info("Instantiating the Documentation Generator")
        self.projectDir = sm.StateMachine.instance._project.getProjectDir()
        self.apiName = sm.StateMachine.instance._project.getAPIName()
        self.projectName = projectName
        self.docType = docType

    @nongui
    @log_exceptions(logger=logger)
    def createDoc(self, debug:bool=True):
        """
        Create the documentation(s).

        :param debug: If true, invalid commands will be printed to the console.
        :type debug: bool
        :return: None
        :rtype: NoneType
        """

        logger.debug("Generating documentation")

        restorePoint = os.getcwd()
        docDir = os.path.join(self.projectDir, self.apiName + "_API_Files", self.apiName, "Documentation")
        srcDir = os.path.join(docDir, "src")

        logger.debug("Creating documentation directory")
        if not os.path.exists(docDir):
            os.mkdir(docDir)

        logger.info("Copying the sphinx directory")
        try:
            shutil.copytree(os.path.join(env.FACILE_SPHINX_DIR, "src"), srcDir)
        except FileExistsError as e:
            logger.exception(e)

        logger.info("Copying the contents of the API directory into the sphinx src directory")
        apiDir = os.path.realpath(os.path.join(docDir, "../"))

        try:
            shutil.copytree(apiDir, os.path.join(srcDir, "facile_src"), ignore=lambda x, y: ["Documentation"])
        except FileExistsError as e:
            logger.exception(e)

        os.chdir(srcDir)
        self.modifyConf()

        for type in self.docType:

            if type is CompilationProfile.DocType.Html:
                initMsg = "Generating HTML documentation..."
                logger.info(initMsg)
                self.stepStarted.emit(initMsg)

                if os.path.exists(os.path.abspath('../html')):
                    self.execCommand('cd ../ & RMDIR /Q/S html 1>nul 2>&1', printErrorCode=debug)
                self.execCommand('make html 1> ..\\build_html.log 2>&1 & move _build\\html ..\\ 1>nul 2>&1', printErrorCode=debug)
                logger.info("finished generating HTML documentation")

            elif type is CompilationProfile.DocType.Txt:
                initMsg = "Generating TXT documentation..."
                logger.info(initMsg)
                self.stepStarted.emit(initMsg)

                if os.path.exists(os.path.abspath('../text')):
                    self.execCommand('cd ../ & RMDIR /Q/S text 1>nul 2>&1', printErrorCode=debug)
                self.execCommand('make text 1> ..\\build_text.log 2>&1 & move _build\\text ..\\ 1>nul 2>&1', printErrorCode=debug)
                logger.info("finished generating TXT documentation")

            elif type is CompilationProfile.DocType.Pdf:
                initMsg = "Generating PDF documentation..."
                logger.info(initMsg)
                self.stepStarted.emit(initMsg)

                if os.path.exists(os.path.abspath('../pdf')):
                    self.execCommand('cd ../ & RMDIR /Q/S pdf 1>nul 2>&1', printErrorCode=debug)
                self.execCommand('make latex 1> ..\\build_pdf.log 2>&1', printErrorCode=debug)
                self.execCommand('cd _build\\latex & make 1>nul 2>&1 ', printErrorCode=debug)
                self.execCommand('mkdir ..\\pdf', printErrorCode=debug)
                self.execCommand('xcopy _build\\latex\\*.pdf ..\\pdf 1>nul 2>&1', printErrorCode=debug)
                logger.info("finished generating PDF documentation")
            
            elif type is CompilationProfile.DocType.EPub:
                initMsg = "Generating EPUB documentation..."
                logger.info(initMsg)
                self.stepStarted.emit(initMsg)

                if os.path.exists(os.path.abspath('../epub')):
                    self.execCommand('cd ../ & RMDIR /Q/S epub 1>nul 2>&1', printErrorCode=debug)
                self.execCommand('make epub 1> ..\\build_epub.log 2>&1 & move _build\\epub ..\\ 1>nul 2>&1', printErrorCode=debug)

                logger.info("finished generating EPUB documentation")

            self.stepComplete.emit()

        # step out of directory.
        os.chdir(restorePoint)

        # remove the src directory.
        exit_code = self.execCommand(f'RMDIR /S/Q "{srcDir}" 1>nul 2>&1', printErrorCode=debug)

        if exit_code:
            logger.critical(f"Unable to remove the {srcDir}. This may cause import issues when the API is run.")
        logger.info("Finished creating documentation.")
        self.finished.emit()
            
    def modifyConf(self):
        """
        Modify conf.py based on the current project
        
		:return: None
		:rtype: NoneType
        """

        # make sure conf.py is done being copied.
        while not os.path.exists("conf.py"):
            pass

        f = open("conf.py")
        fileStr = f.read()
        f.close()
        
        f = open("conf.py", "w")
        f.write(fileStr.format(userDefinedProjectName = self.projectName))
        f.close()

    @nongui
    def execCommand(self, command:str, printErrorCode:bool=True) -> int:
        """
        Execute the command and return the error code.
        :param command: The command to execute.
        :type command: str
        :param printErrorCode: If there was an error, print the error code if true.
        :type printErrorCode: bool
        :return: The exit code from the command.
        :rtype: int
        """

        exit_code = subprocess.call(command, shell=True)
        if printErrorCode and exit_code != 0:
            print()
            print(f'CURRENT DIRECTORY: {os.getcwd()}')
            print(f'COMMAND:           {command}')
            print(f'EXIT CODE:         {exit_code}')
            print()
        return exit_code