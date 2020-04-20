import os
import data.statemachine as sm
from data.compilationprofile import CompilationProfile


class DocGenerator:
    """
	This class is used to generate API documentations based on user's preference.
	"""
    
    def __init__(self, docType: set, projectName: str):
        """
        Construct the class DocGenerator
        
        :param docType: user's choices on the type(s) of the documentations to be generated
        :type docType: set
        :param projectName: the name of the project
        :type projectName: str
        """
        self.projectDir = sm.StateMachine.instance._project.getProjectDir()
        self.projectName = projectName
        self.docType = docType
        self.sphinxFacileDir = os.path.join(os.path.split(__file__)[0], "sphinx_src")
    
    def createDoc(self):
        """
        Create the documentation(s).
        
		:return: None
		:rtype: NoneType
        """
        if len(self.docType) == 0:
            return
        
        for type in self.docType:
            os.chdir(self.projectDir)
            os.system('xcopy {0} /e 1>nul 2>&1'.format(self.sphinxFacileDir))
            self.modifyConf()

            if type is CompilationProfile.DocType.Html:
                formatChoice = "html"
                os.chdir(self.projectDir)
                # remove the old html folder
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 1>nul 2>&1'.format(self.projectName, formatChoice))
                # create new html, move it to Documentation
                os.system('cd src'
                          '& make {0} 1> {1}\\{2}\\Documentation\\build_html.log 2>&1'
                          '& cd _build'
                          '& move {0} {1}\{2}\Documentation 1>nul 2>&1'.format(formatChoice, self.projectDir, self.projectName))
                
            elif type is CompilationProfile.DocType.Txt:
                formatChoice = "text"
                os.chdir(self.projectDir)
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 1>nul 2>&1'.format(self.projectName, formatChoice))
                os.system('cd src'
                          '& make {0} 1> {1}\\{2}\\Documentation\\build_text.log 2>&1'
                          '& cd _build'
                          '& move {0} {1}\{2}\Documentation 1>nul 2>&1'.format(formatChoice, self.projectDir, self.projectName))
                
            elif type is CompilationProfile.DocType.Pdf:
                formatChoice = "latex"
                os.chdir(self.projectDir)
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 1>nul 2>&1'.format(self.projectName, formatChoice))
                os.system('cd src'
                          '& make {0} 1> {1}\\{2}\\Documentation\\build_latex.log 2>&1'
                          '& cd _build'
                          '& cd latex'
                          '& make 1> {1}\\{2}\\Documentation\\build_pdf.log 2>&1'
                          '& cd ..'
                          '& move {0} {1}\{2}\Documentation 1>nul 2>&1'.format(formatChoice, self.projectDir, self.projectName))
            
            elif type is CompilationProfile.DocType.EPub:
                formatChoice = "epub"
                os.chdir(self.projectDir)
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 1>nul 2>&1'.format(self.projectName, formatChoice))
                os.system('cd src'
                          '& make {0} 1> {1}\\{2}\\Documentation\\build_epub.log 2>&1'
                          '& cd _build'
                          '& move {0} {1}\{2}\Documentation 1>nul 2>&1'.format(formatChoice, self.projectDir, self.projectName))
                
            os.chdir(self.projectDir)
            os.system('RMDIR /Q/S src 1>nul 2>&1')
            
    def modifyConf(self):
        """
        Modify conf.py based on the current project
        
		:return: None
		:rtype: NoneType
        """
        srcDir = '{}\src'.format(self.projectDir)
        os.chdir(srcDir)
        
        f = open("conf.py")
        fileStr = f.read()
        f.close()
        
        f = open("conf.py", "w")
        f.write(fileStr.format(userDefinedProjectName = self.projectName))
        f.close()