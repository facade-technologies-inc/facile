# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QMainWindow
from .ui.ui_facileview import Ui_MainWindow as Ui_FacileView
from ..model.project import Project


class FacileView(QMainWindow):
    def __init__(self, project=Project()):
        super(FacileView, self).__init__()
        self.ui = Ui_FacileView()
        self.ui.setupUi(self)

        self.setProject(project)
        self.loadProject()
        
    def loadProject(self):
        if self.projectIsEmpty():
            dialog = ProjectSelectorDialog()
            dialog.exec_()
        else:
            # load the project
        
    def setProject(self, project):
        if isinstance(project, Project):
            self._project = project
        else:
            raise Exception("Invalid project type") # TODO: create custom exception class
        
    def projectIsEmpty(self):
        return self._project.isEmpty()

