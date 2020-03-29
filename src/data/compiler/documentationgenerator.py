import os
import data.statemachine as sm
from data.compilationprofile import CompilationProfile


class DocGenerator:
    """
	This class is used
	"""
    
    def __init__(self, docType: set, projectName: str):
        self.projectDir = sm.StateMachine.instance._project.getProjectDir()
        #self.projectDir = r"C:\Users\ramos\Desktop\FacadeTechnology\FacileAPIs\NotePadAPIDemoExample"
        
        self.projectName = projectName
        self.docType = docType
        self.sphinxFacileDir = r"C:\Users\ramos\Desktop\FacadeTechnology\facile\src\data\compiler\sphinx_src"
    
    def createDoc(self):
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
                os.system('cd Documentation'
                          '& RMDIR /Q/S {0} 2>nul'.format(formatChoice))
                # create new html, move it to Documentation
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
                
            elif type is CompilationProfile.DocType.Doc:
                formatChoice = "text"
                os.chdir(self.projectDir)
                os.system('cd Documentation'
                          '& RMDIR /Q/S {0} 2>nul'.format(formatChoice))
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
                
            elif type is CompilationProfile.DocType.Pdf:
                # TODO: fix pdf creation
                formatChoice = "latex"
                os.chdir(self.projectDir)
                os.system('cd Documentation'
                          '& RMDIR /Q/S {0} 2>nul'.format(formatChoice))
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
            
            elif type is CompilationProfile.DocType.EPub:
                formatChoice = "epub"
                os.chdir(self.projectDir)
                os.system('cd Documentation'
                          '& RMDIR /Q/S {0} 2>nul'.format(formatChoice))
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
                
            os.chdir(self.projectDir)
            os.system('RMDIR /Q/S src')
            
    def modifyConf(self):
        srcDir = '{}\src'.format(self.projectDir)
        os.chdir(srcDir)
        
        f = open("conf.py")
        fileStr = f.read()
        f.close()
        
        f = open("conf.py", "w")
        f.write(fileStr.format(userDefinedProjectName = self.projectName))
        f.close()