import os
import data.statemachine as sm
from data.compilationprofile import CompilationProfile


class DocGenerator:
    """
	This class is used
	"""
    
    def __init__(self, docType: set):
        self.projectDir = sm.StateMachine.instance._project.getProjectDir()
        #self.projectDir = r"C:\Users\ramos\Desktop\FacadeTechnology\FacileAPIs\NotePadAPIDemoExample"
    
        self.docType = docType
        self.sphinxFacileDir = r"C:\Users\ramos\Desktop\FacadeTechnology\facile\src\data\compiler\sphinx_src"
    
    def createDoc(self):
        for type in self.docType:
            # os.chdir(self.projectDir)
            # os.system('ls'
            #           '& xcopy {0} /e'
            #           '& cd src')
            
            if type is CompilationProfile.DocType.Html:
                os.chdir(self.projectDir)
                formatChoice = "html"
                os.system('ls '
                          '& xcopy {0} /e'
                          '& cd src'
                          '& make {1}'
                          '& cd _build'
                          '& move html {2}\Documentation'
                          '& cd ../..'
                          '& RMDIR /Q/S src'.format(self.sphinxFacileDir, formatChoice, self.projectDir))
                
            elif type is CompilationProfile.DocType.Doc:
                formatChoice = "text"
                os.chdir(self.projectDir)
                os.system('ls '
                          '& xcopy {0} /e'
                          '& cd src'
                          '& make {1}'
                          '& cd _build'
                          '& move {1} {2}\Documentation'
                          '& cd ../..'
                          '& RMDIR /Q/S src'.format(self.sphinxFacileDir, formatChoice, self.projectDir))
                
            elif type is CompilationProfile.DocType.Pdf:
                # TODO: fix pdf creation
                formatChoice = "latex"
                os.chdir(self.projectDir)
                os.system('ls '
                          '& xcopy {0} /e'
                          '& cd src'
                          '& make {1}'
                          '& cd _build'
                          '& move {1} {2}\Documentation'
                          '& cd ../..'
                          '& RMDIR /Q/S src'.format(self.sphinxFacileDir, formatChoice, self.projectDir))
            
            elif type is CompilationProfile.DocType.EPub:
                formatChoice = "epub"
                os.chdir(self.projectDir)
                os.system('ls '
                          '& xcopy {0} /e'
                          '& cd src'
                          '& make {1}'
                          '& cd _build'
                          '& move {1} {2}\Documentation'
                          '& cd ../..'
                          '& RMDIR /Q/S src'.format(self.sphinxFacileDir, formatChoice, self.projectDir))


# setDocType = set()
# setDocType.add(CompilationProfile.DocType.Html)
# setDocType.add(CompilationProfile.DocType.Doc)
# setDocType.add(CompilationProfile.DocType.Pdf)
# setDocType.add(CompilationProfile.DocType.EPub)
#
# temp = DocGenerator(setDocType)
# temp.createDoc()