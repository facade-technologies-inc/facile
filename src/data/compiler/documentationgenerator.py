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
        #self.projectDir = r"C:\Users\ramos\Desktop\FacadeTechnology\FacileAPIs\NotePadAPIDemoExample"
        
        self.projectName = projectName
        self.docType = docType
        self.sphinxFacileDir = r"C:\Users\ramos\Desktop\FacadeTechnology\facile\src\data\compiler\sphinx_src"
    
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
            os.system('xcopy {0} /e'.format(self.sphinxFacileDir))
            self.modifyConf()
            
            # TODO: delete the html folder if existed already. So user can create a new one.
            if type is CompilationProfile.DocType.Html:
                formatChoice = "html"
                os.chdir(self.projectDir)
                # remove the old html folder
                # change made here
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 2>nul'.format(self.projectName, formatChoice))
                # create new html, move it to Documentation
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\{2}\Documentation'.format(formatChoice, self.projectDir, self.projectName))
                
            elif type is CompilationProfile.DocType.Doc:
                formatChoice = "text"
                os.chdir(self.projectDir)
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 2>nul'.format(self.projectName, formatChoice))
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\{2}\Documentation'.format(formatChoice, self.projectDir, self.projectName))
                
            elif type is CompilationProfile.DocType.Pdf:
                # TODO: fix pdf creation
                formatChoice = "latex"
                os.chdir(self.projectDir)
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 2>nul'.format(self.projectName, formatChoice))
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& cd latex'
                          '& make'
                          '& cd ..'
                          '& move {0} {1}\{2}\Documentation'.format(formatChoice, self.projectDir, self.projectName))
            
            elif type is CompilationProfile.DocType.EPub:
                formatChoice = "epub"
                os.chdir(self.projectDir)
                os.system('cd {0}'
                          '& cd Documentation'
                          '& RMDIR /Q/S {1} 2>nul'.format(self.projectName, formatChoice))
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\{2}\Documentation'.format(formatChoice, self.projectDir, self.projectName))
                
            os.chdir(self.projectDir)
            os.system('RMDIR /Q/S src')
            
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