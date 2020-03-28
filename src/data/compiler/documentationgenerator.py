import os
import data.statemachine as sm

#projectDir = sm.StateMachine.instance._project.getProjectDir()
#print(projectDir)
projectDir = r"C:\Users\ramos\Desktop\FacadeTechnology\FacileAPIs\NotePadAPIDemoExample"

formatChoice = "html"

sphinxFacileDir = r"C:\Users\ramos\Desktop\FacadeTechnology\facile\src\data\compiler\sphinx_src"

os.chdir(projectDir)
os.system('ls '
          '& xcopy {0} /e'
          '& cd src'
          '& make {1}'
          '& cd _build'
          '& move html {2}\Documentation'
          '& cd ../..'
          '& RMDIR /Q/S src' .format(sphinxFacileDir, formatChoice, projectDir))