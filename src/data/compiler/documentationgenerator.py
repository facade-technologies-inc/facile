import os
import shutil

from PySide2.QtCore import QObject, Signal

import data.statemachine as sm
from data.compilationprofile import CompilationProfile


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
        self.projectDir = sm.StateMachine.instance._project.getProjectDir()
        self.apiName = sm.StateMachine.instance._project.getAPIName()
        self.projectName = projectName
        self.docType = docType
        self.sphinxFacileDir = os.path.join(os.path.split(__file__)[0], "sphinx_src")
    
    def createDoc(self):
        """
        Create the documentation(s).
        
		:return: None
		:rtype: NoneType
        """
        restorePoint = os.getcwd()
        docDir = os.path.join(self.projectDir, self.apiName, "Documentation")

        # Clear documentation directory
        if os.path.exists(docDir):
            shutil.rmtree(docDir, ignore_errors=True)

        while os.path.exists(docDir):
            pass

        os.mkdir(docDir)

        os.chdir(docDir)
        os.system('xcopy {0} /e 1>nul 2>&1'.format(self.sphinxFacileDir))
        srcDir = os.path.join(self.projectDir, self.apiName, "Documentation", "src")
        os.chdir(srcDir)
        self.modifyConf()

        for type in self.docType:

            if type is CompilationProfile.DocType.Html:
                self.stepStarted.emit("Generating HTML documentation...")
                os.system('cd ../ & RMDIR /Q/S html 1>nul 2>&1')
                os.system('make html 1> ..\\build_html.log 2>&1 & move _build\\html ..\\ 1>nul 2>&1')

            elif type is CompilationProfile.DocType.Txt:
                self.stepStarted.emit("Generating TXT documentation...")
                os.system('cd ../ & RMDIR /Q/S text 1>nul 2>&1')
                os.system('make text 1> ..\\build_text.log 2>&1 & move _build\\text ..\\ 1>nul 2>&1')
                
            elif type is CompilationProfile.DocType.Pdf:
                self.stepStarted.emit("Generating PDF documentation...")
                os.system('cd ../ & RMDIR /Q/S pdf 1>nul 2>&1')
                os.system('make latex 1> ..\\build_pdf.log 2>&1 & cd _build\\latex & make 1>nul 2>&1 & cd ..\\..\\ & move _build\\latex ..\\ 1>nul 2>&1')
            
            elif type is CompilationProfile.DocType.EPub:
                self.stepStarted.emit("Generating EPUB documentation...")
                os.system('cd ../ & RMDIR /Q/S epub 1>nul 2>&1')
                os.system('make epub 1> ..\\build_epub.log 2>&1 & move _build\\epub ..\\ 1>nul 2>&1')

            self.stepComplete.emit()

        # remove the src directory.
        shutil.rmtree(srcDir, ignore_errors=True)

        # step out of directory.
        os.chdir(restorePoint)

        self.finished.emit()
            
    def modifyConf(self):
        """
        Modify conf.py based on the current project
        
		:return: None
		:rtype: NoneType
        """
        f = open("conf.py")
        fileStr = f.read()
        f.close()
        
        f = open("conf.py", "w")
        f.write(fileStr.format(userDefinedProjectName = self.projectName))
        f.close()