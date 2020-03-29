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
        if len(self.docType) == 0:
            return
        
        for type in self.docType:
            os.chdir(self.projectDir)
            os.system('ls'
                      '& xcopy {0} /e'.format(self.sphinxFacileDir))
            # TODO: change conf.py here. So it won't mess up the default file in facile
            
            if type is CompilationProfile.DocType.Html:
                formatChoice = "html"
                os.chdir(self.projectDir)
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
                
            elif type is CompilationProfile.DocType.Doc:
                formatChoice = "text"
                os.chdir(self.projectDir)
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
                
            elif type is CompilationProfile.DocType.Pdf:
                # TODO: fix pdf creation
                formatChoice = "latex"
                os.chdir(self.projectDir)
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
            
            elif type is CompilationProfile.DocType.EPub:
                formatChoice = "epub"
                os.chdir(self.projectDir)
                os.system('cd src'
                          '& make {0}'
                          '& cd _build'
                          '& move {0} {1}\Documentation'.format(formatChoice, self.projectDir))
                
            os.chdir(self.projectDir)
            os.system('RMDIR /Q/S src')


# setDocType = set()
# setDocType.add(CompilationProfile.DocType.Html)
# setDocType.add(CompilationProfile.DocType.Doc)
# setDocType.add(CompilationProfile.DocType.Pdf)
# setDocType.add(CompilationProfile.DocType.EPub)
#
# temp = DocGenerator(setDocType)
# temp.createDoc()