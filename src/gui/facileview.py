"""
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

This module contains the FacileView class which is the main window of Facile.
Much of Facile is joined together here.
"""
import os
import json
from copy import deepcopy
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import Signal, Slot
from gui.ui.ui_facileview import Ui_MainWindow as Ui_FacileView
from gui.newprojectdialog import NewProjectDialog
from gui.copyprojectdialog import CopyProjectDialog
from gui.manageprojectdialog import ManageProjectDialog
from data.project import Project


class FacileView(QMainWindow):
	"""
	FacileView is the main window for Facile.
	"""
	
	# This signal will be emitted when the project changes to notify all components of Facile.
	projectChanged = Signal(Project)
	
	def __init__(self) -> 'FacileView':
		"""
		Constructs a FacileView object.
		
		:return: The new project object
		:rtype: Project
		"""
		
		super(FacileView, self).__init__()
		self.ui = Ui_FacileView()
		self.ui.setupUi(self)

		self._setProject(None)
		self._connectActions()
		
		# TODO: Move this somewhere else to localize the recent project stuff
		# try to show recent projects
		try:
			with open(os.path.join(os.getcwd(), "temp/recentProjects.json"), "r") as recents:
				recentProjects = json.loads(recents.read())
		except Exception as e:
			print(e)
		else:
			for proj in recentProjects[:10]:
				if os.path.exists(proj):
					action = self.ui.menuRecent_Projects.addAction(proj)
					action.triggered.connect(lambda: self._setProject(Project.load(proj)))
		
	@Slot(Project)
	def _setProject(self, project: Project) -> None:
		"""
		Sets the project object.
		
		:param project: The new Project object to set
		:type project: Project
		:return: None
		:rtype: NoneType
		"""
		
		self._project = project
		
		if not project is None:
			print("Project set: {}".format(project.getName()))
			self.projectChanged.emit(project)
			self._project.save()
			
			# TODO: Move global Facile stuff like this to a better spot.
			# add the new project to the recent projects file
			cwd = os.getcwd()
			tempDir = os.path.join(cwd, "temp")
			recentsFile = os.path.join(tempDir, "recentProjects.json")
			recentProjects = []
			if not os.path.exists(tempDir):
				os.mkdir(tempDir)
			try:
				with open(recentsFile, "r") as recents:
					recentProjects = json.loads(recents.read())
			except:
				pass
			if not project.getMainProjectFile() in recentProjects:
				recentProjects.insert(0, project.getMainProjectFile())
				with open(recentsFile, "w") as recents:
					recents.write(json.dumps(recentProjects, indent=4))
			
	def _connectActions(self) -> None:
		"""
		Connects actions in Facile's GUI to business logic. Actions may be triggered by
		clicking on the toolbar, menu bar, or something else.
		
		:return: None
		:rtype: NoneType
		"""
		
		self.ui.actionFrom_Scratch.triggered.connect(self._onNewProjectFromScratchTriggered)
		self.ui.actionFrom_Existing_Project.triggered.connect(self._onNewProjectFromExistingTriggered)
		self.ui.actionOpen_Project.triggered.connect(self._onOpenProjectTriggered)
		self.ui.actionSave_Project.triggered.connect(self._onSaveProjectTriggered)
		self.ui.actionSave_as.triggered.connect(self._onSaveProjectAsTriggered)
		self.ui.actionManage_Project.triggered.connect(self._onManageProjectTriggered)
	
	@Slot()
	def _onSaveProjectAsTriggered(self) -> None:
		"""
		This slot is run when the user clicks "File -> Save As..."
		
		:return: None
		:rtype: NoneType
		"""
		
		def handler(url: str) -> None:
			"""
			This function is called when the user selects the new directory to save the project in.
			
			:return: None
			:rtype: NoneType
			"""
			
			if os.path.normpath(url) != os.path.normpath(self._project.getProjectDir()):
				for file in os.listdir(url):
					if file[-4:] == ".fcl":
						msg = QMessageBox()
						msg.setIcon(QMessageBox.Critical)
						msg.setText("Error")
						msg.setInformativeText("Please choose a directory that does not already contain a project.")
						msg.setWindowTitle("Error")
						msg.exec_()
						return
			
			newProject = deepcopy(self._project)
			newProject.setProjectDir(url)
			self._setProject(newProject)
			self._onSaveProjectTriggered()
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(os.path.expanduser("~"))
		fileDialog.fileSelected.connect(handler)
		fileDialog.exec_()
	
	@Slot()
	def _onSaveProjectTriggered(self) -> None:
		"""
		This slot is run when the user saves the current project in Facile
		
		:return: None
		:rtype: NoneType
		"""
		
		if self._project is not None:
			self._project.save()
			
	@Slot()
	def _onNewProjectFromScratchTriggered(self) -> None:
		"""
		This slot is run when the user elects to create a new project from scratch.
		
		A NewProjectDialog is opened that allows the user to specify the target application,
		description, location, etc.
		
		:return: None
		:rtype: NoneType
		"""
		
		newProjectDialog = NewProjectDialog()
		newProjectDialog.projectCreated.connect(self._setProject)
		newProjectDialog.exec_()

	@Slot()
	def _onNewProjectFromExistingTriggered(self) -> None:
		"""
		This slot is run when the user elects to create a new project from an existing one.
		A CopyProjectDialog is opened that allows the user to specify the new location, name, and description.
		
		:return: None
		:rtype: NoneType
		"""
		
		copyProjectDialog = CopyProjectDialog()
		copyProjectDialog.projectCreated.connect(self._setProject)
		copyProjectDialog.exec_()
	 
	@Slot()
	def _onOpenProjectTriggered(self) -> None:
		"""
		This slot is run when the user elects to open an existing project.
		
		A file dialog is open with the *.fcl filter. Once the user selects a project, it will be loaded into Facile.
		
		:return: None
		:rtype: NoneType
		"""
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(os.path.expanduser("~"))
		fileDialog.setNameFilter("Facile Project File (*.fcl)")
		fileDialog.fileSelected.connect(lambda url: self._setProject(Project.load(url)))
		fileDialog.exec_()
		
	@Slot()
	def _onManageProjectTriggered(self) -> None:
		"""
		This slot is run when a the user selects "file -> project settings"
		
		:return: None
		:rtype: NoneType
		"""
		
		manageProjectDialog = ManageProjectDialog(self._project)
		manageProjectDialog.projectCreated.connect(self._setProject)
		manageProjectDialog.exec_()