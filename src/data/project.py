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

This module contains the Project class.
"""

from typing import Dict, Tuple
import json
import os
from subprocess import PIPE

import psutil
from PySide2.QtWidgets import QTreeView, QMessageBox, QProgressDialog
from PySide2.QtCore import Qt, QTimer

from data.tguim.targetguimodel import TargetGuiModel
from data.apim.apimodel import ApiModel
from data.entity import Entity
from qt_models.projectexplorermodel import ProjectExplorerModel
from tguiil.explorer import Explorer
from tguiil.observer import Observer
import data.statemachine as sm


class Project:
	"""
	This class is the top level to a Facile Project.
	It stores information about the target application, the target GUI model, the API model, compilation profiles, etc.
	
	.. note::
		Only one project can be stored in each directory.
		
	.. todo::
		Create custom exceptions and check input in setters
		
	.. todo::
		Store backend as enum instead of string
	"""
	
	def __init__(self, name: str, description: str, exe: str, backend: str,
	             projectDir: str = "~/", startupTimeout: int = 10) -> 'Project':
		"""
		Constructs a Project object.
		
		:param name: The name of the project.
		:type name: str
		:param description: The project description.
		:type description: str
		:param exe: The executable file of the target application.
		:type exe: str
		:param backend: The accessibility technology used to control the target application.
		:type backend: str
		:param projectDir: The directory that the project is stored in.
		:type projectDir: str
		:param startupTimeout: The number of seconds to wait for the target application to startup.
		:type startupTimeout: int
		:return: The constructed project
		:rtype: Project
		"""
		
		self._projectDir = None
		self._description = None
		self._name = None
		self._executable = None
		self._backend = None
		self._startupTimeout = None
		self._targetGUIModel = TargetGuiModel()
		self._apiModel = ApiModel()
		self._process = None
		self._observer = None
		self._explorer = None
		self.autoCloseAppOnExit = None
		self.acaWarningShown = False
		self._notif = None  # This temporarily holds a dialog
		self._timer = None
		
		# project information
		self.setProjectDir(os.path.abspath(projectDir))
		self.setDescription(description)
		self.setName(name)
		
		# target application information
		self.setExecutableFile(exe)
		self.setBackend(backend)
		self.setStartupTimeout(startupTimeout)
	
	def getObserver(self) -> 'Observer':
		"""
		Gets the project's observer
		
		:return: The project's observer
		:rtype: Observer
		"""
		detailedViewAction = sm.StateMachine.instance.view.ui.actionDetailed_View
		captureImages = detailedViewAction.isChecked()

		if self._process is None or not self._process.is_running():
			return None
		else:
			new = False
			if self._observer is None:
				self._observer = Observer(self._process.pid, captureImages, self._backend)
				self._observer.newSuperToken.connect(self._targetGUIModel.createComponent,
				                                     type=Qt.BlockingQueuedConnection)
				self._observer.backendDetected.connect(lambda be: self.setBackend(be))
				new = True
			elif self._observer.getPID() != self._process.pid:
				self._observer.pause()
				self._observer = Observer(self._process.pid, captureImages, self._backend)
				self._observer.newSuperToken.connect(self._targetGUIModel.createComponent,
				                                     type=Qt.BlockingQueuedConnection)
				self._observer.backendDetected.connect(lambda be: self.setBackend(be))
				new = True
			
			if new:
				self._observer.loadSuperTokens(self._targetGUIModel)

			detailedViewAction.triggered.connect(self._observer.captureImages, type=Qt.QueuedConnection)
			
			return self._observer
	
	def getExplorer(self) -> 'Explorer':
		"""
		Gets the project's explorer
		
		:return: The project's explorer
		:rtype: Explorer
		"""
		if self._process is None or not self._process.is_running():
			return None
		else:
			# TODO: Uncomment when Explorer is done
			# self._explorer = Explorer(self._process.pid, self._backend)
			# return self._explorer
			return None
	
	def getTargetGUIModel(self) -> 'TargetGuiModel':
		"""
		Gets the project's target GUI model.
		
		:return: The project's target GUI model.
		:rtype: TargetGuiModel
		"""
		return self._targetGUIModel
	
	def getAPIModel(self) -> 'ApiModel':
		"""
		Gets the project's API model.
		
		:return: The project's API model
		"""
		return self._apiModel
	
	def setProjectDir(self, url: str) -> None:
		"""
		Sets the project's directory.
		
		:param url: The path to the directory where the project should be saved.
		:type url: str
		:return: None
		:rtype: NoneType
		"""
		
		self._projectDir = os.path.abspath(url)
	
	def setDescription(self, description: str) -> None:
		"""
		Sets the project's description
		
		:param description: The project's description.
		:type description: str
		:return: None
		:rtype: NoneType
		"""
		
		self._description = description
	
	def setName(self, name: str) -> None:
		"""
		Sets the name of the project
		
		:param name: The name of the project
		:type name: str
		:return: None
		:rtype: NoneType
		"""
		
		self._name = name
	
	def setExecutableFile(self, exe: str) -> None:
		"""
		Sets the target application of the project.
		
		:param exe: The executable of the target application
		:type exe: str
		:return: None
		:rtype: NoneType
		"""
		
		self._executable = exe
	
	def setBackend(self, backend: str = "auto") -> None:
		"""
		Sets the accessibility technology (backend) used to control the target application.
		The automatic selection is performed in the observer itself on first run.
		Also handles the QMessageBoxes needed to notify the user, because they can't be spawned in the observer's
		thread.
		
		Defaults to auto, but the default should never be used: just a fail-safe.
		
		:param backend: The accessibility technology used to control the target application
		:type backend: str
		:return: None
		:rtype: NoneType
		"""
		if backend.lower() == 'detecting':
			self._backend = backend.lower()

			# Time calculations
			interval = 50  # milliseconds
			totTime = 4800  # milliseconds
			steps = int(totTime/interval)

			# Initializations
			timer = QTimer()
			prog = QProgressDialog("We are currently detecting your application's backend technology...",
										  "Hide", 0, steps)
			self._notif = prog
			self._timer = timer

			# Set values and connect signals
			timer.setInterval(interval)
			timer.timeout.connect(lambda: prog.setValue(prog.value() + 1))
			prog.setAutoClose(True)
			prog.setValue(0)

			# Start timer and open progress dialog
			timer.start()
			self._notif.exec_()

		else:
			if self._backend == 'detecting':
				# Stop timer and close progress dialog if not done already
				self._timer.stop()
				self._notif.close()

				# Display message
				self._notif = QMessageBox(QMessageBox.Information, "Backend Detected",
										  "The backend has been successfully detected: " + backend.upper() + '.',
										  buttons=QMessageBox.Ok)
				self._notif.exec_()

			# Set backend
			self._backend = backend.lower()
	
	def setStartupTimeout(self, timeout: int) -> None:
		"""
		Sets the timeout for the target application startup time.

		:param timeout: the timeour for starting up the target application.
		:type timeout: int
		:return: None
		:rtype: NoneType
		"""
		
		self._startupTimeout = timeout
	
	def getName(self) -> str:
		"""
		Gets the project's name.
		
		:return: The project's name.
		:rtype: str
		"""
		
		return self._name

	def getAPIName(self) -> str:
		"""
		Gets the name of the API.

		:return: The API's name.
		:rtype: str
		"""

		return self._name.replace(" ", "_")
	
	def getExecutableFile(self) -> str:
		"""
		Gets the path to the executable file used to startup the target application.
		
		:return: The target application's executable file.
		:rtype: str
		"""
		
		return self._executable
	
	def getDescription(self) -> str:
		"""
		Gets the project's description.
		
		:return: The project's description.
		:rtype: str
		"""
		
		return self._description
	
	def getBackend(self) -> str:
		"""
		Gets the project's accessibility technology (backend).
		
		:return: The project's accessibility technology (backend)
		:rtype: str
		"""
		
		return self._backend
	
	def getStartupTimeout(self) -> int:
		"""
		Gets the target application's startup timeout.
		
		:return: the target app's startup timeout
		:rtype: int
		"""
		
		return self._startupTimeout
	
	def getProjectDir(self) -> str:
		"""
		Gets the directory that the project is located in.
		
		:return: The project's directory
		:rtype: str
		"""
		
		return self._projectDir
	
	def getProjectFile(self) -> str:
		"""
		Gets the project's main file path (the .fcl file)
		
		:return: The path to the project's .fcl file
		:rtype: str
		"""
		
		return os.path.join(self._projectDir, self._name + ".fcl")

	def startTargetApplication(self) -> None:
		"""
		Starts the target application
		
		:return: None
		:rtype: NoneType
		"""
		self._process = psutil.Popen([self._executable], stdout=PIPE)
	
	def stopTargetApplication(self) -> None:
		"""
		Kills the target application.
		
		:return: None
		:rtype: NoneType
		"""
		try:
			self._process.kill()
		except:
			pass
	
	def getProcess(self) -> psutil.Process:
		"""
		Gets the process of the target application iff it is running.
		
		:return: The process object if the target application is running. None if it is not running.
		:rtype: psutil.Process or NoneType
		"""
		if (self._process is None) or (not self._process.is_running()):
			return None
		return self._process
	
	def getProjectExplorerModel(self, view: QTreeView) -> ProjectExplorerModel:
		"""
		Gets a model that allows a Qt tree view to access the data in a limited manner.
		
		:param view: The view to place the model into
		:type view: QTreeView
		:return: The project explorer model
		:rtype: ProjectExplorerModel
		"""
		return ProjectExplorerModel(self, view)
	
	@staticmethod
	def load(projectFile: str, onEntityCreation = None, onCompletion = None) -> 'Project':
		"""
		Creates a Project object from a .fcl file.
		
		:param projectFile: The project's .fcl file
		:type projectFile: str
		:param onEntityCreation: The function to run when an entity is created (may be None)
		:type onEntityCreation: callable
		:param onCompletion: The function to run when loading is complete
		:type onCompletion: callable
		:return: The project object reconstructed from a .fcl file.
		:rtype: Project
		"""
		
		with open(projectFile) as mainProjectFile:
			projectJSON = json.loads(mainProjectFile.read())
		
		projectDir = os.path.dirname(projectFile)
		name = projectJSON["Project Information"]["Name"]
		description = projectJSON["Project Information"]["Description"]
		exe = projectJSON["Application Information"]["Target Application"]
		backend = projectJSON["Application Information"]["Backend"]
		startupTimeout = projectJSON["Application Information"]["Startup Timeout"]
		autoClose = projectJSON["Settings"]["Close App on Exit"]
		warningShown = projectJSON["Settings"]["AutoClose Warning Shown"]
		
		loadedProject = Project(name, description, exe, backend, projectDir, startupTimeout)
		loadedProject.autoCloseAppOnExit = autoClose
		loadedProject.acaWarningShown = warningShown

		Entity.onCreation = onEntityCreation
		loadedProject._targetGUIModel = TargetGuiModel.fromDict(projectJSON["Data Structures"]["Target GUI Model"])
		loadedProject._apiModel = ApiModel.fromDict(projectJSON["Data Structures"]["API Model"],
													loadedProject._targetGUIModel)

		Entity.onCreation = None
		onCompletion()
		return loadedProject

	@staticmethod
	def getEntityCount(mainFile:str) -> None:
		"""
		Gets the number of entities from a project.

		:param mainFile: The url to the project file (*.fcl)
		:type mainFile: str
		:return:
		"""
		mainProjectFile = open(mainFile)
		contents = mainProjectFile.read()
		projectJSON = json.loads(contents)
		mainProjectFile.close()

		return projectJSON["Project Information"].get("Model Entities", 1_000_000)
	
	def save(self) -> None:
		"""
		Writes a project out to disk as a set of files. (.fcl, .tguim, .apim)
		
		:return: None
		:rtype: NoneType
		"""
		
		projectDict = {}
		projectDict["Project Information"] = {}
		projectDict["Project Information"]["Name"] = self._name
		projectDict["Project Information"]["Description"] = self._description
		projectDict["Project Information"]["Model Entities"] = Entity.count
		projectDict["Application Information"] = {}
		projectDict["Application Information"]["Target Application"] = self._executable
		projectDict["Application Information"]["Backend"] = self._backend
		projectDict["Application Information"]["Startup Timeout"] = self._startupTimeout
		projectDict["Settings"] = {}
		projectDict["Settings"]["Close App on Exit"] = self.autoCloseAppOnExit
		projectDict["Settings"]["AutoClose Warning Shown"] = self.acaWarningShown
		projectDict["Data Structures"] = {}
		projectDict["Data Structures"]["Target GUI Model"] = self._targetGUIModel.asDict()
		projectDict["Data Structures"]["API Model"] = self._apiModel.asDict()

		# save the project file
		with open(self.getProjectFile(), "w") as file:
			s = json.dumps(projectDict, indent=4)
			file.write(s)

	def addToRecents(self) -> None:
		"""
		Adds the project to the recents file.
		
		:return: None
		:rtype: NoneType
		"""
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
		if not self.getProjectFile() in recentProjects:
			recentProjects.insert(0, self.getProjectFile())
			with open(recentsFile, "w") as recents:
				recents.write(json.dumps(recentProjects, indent=4))
	
	@staticmethod
	def getRecents(limit: int = 0) -> list:
		"""
		Gets a list of project files that have recently been opened. The number of returned project locations will be
		limited iff the limit is set to an integer greater than 0.
		
		:param limit: The maximum number of recent projects to return. If limit is less than or equal to zero, the list will not be limited.
		:type limit: int
		:return: a list of all recent project file names
		:rtype: list[str]
		"""
		try:
			with open(os.path.join(os.getcwd(), "temp/recentProjects.json"), "r") as recents:
				recentProjects = json.loads(recents.read())
		
		except FileNotFoundError:
			recentProjects = []
		
		# limit the length of the list
		if limit > 0:
			recentProjects = recentProjects[:limit]
		
		# remove recent projects that don't exist
		filteredProjects = []
		for proj in recentProjects:
			if os.path.exists(proj):
				filteredProjects.append(proj)
		
		return filteredProjects
