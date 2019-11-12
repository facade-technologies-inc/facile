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

This module contains the Project class.
"""

import os
import json
import psutil
from subprocess import PIPE
from data.tguim.targetguimodel import TargetGuiModel


class Project:
	"""
	This class is the top level to a Facile Project.
	It stores information about the target application, the target GUI model, the API model, compilation profiles, etc.
	
	NOTE: Only one project can be stored in each directory.
	"""
	
	# TODO: create custom exceptions and check input in setters.
	# TODO: Store backend as enum instead of string
	
	def __init__(self, name: str, description: str, exe: str, backend: str,
				projectDir: str = "~/", startupTimeout: int = 10):
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
		self._APIModel = None
		self._process = None
		
		# project information
		self.setProjectDir(os.path.abspath(projectDir))
		self.setDescription(description)
		self.setName(name)
		
		# target application information
		self.setExecutableFile(exe)
		self.setBackend(backend)
		self.setStartupTimeout(startupTimeout)
		
		self._process = psutil.Popen([self._executable], stdout=PIPE)
		
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
		
	def setBackend(self, backend: str) -> None:
		"""
		Sets the accessibility technology (backend) used to control the target application.
		
		:param backend: The accessibility technology used to control the target application
		:type backend: str
		:return: None
		:rtype: NoneType
		"""
		
		self._backend = backend
		
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
		
	def getMainProjectFile(self) -> str:
		"""
		Gets the project's main file path (the .fcl file)
		
		:return: The path to the project's .fcl file
		:rtype: str
		"""
		
		return os.path.join(self._projectDir, self._name + ".fcl")
	
	def getTargetGUIModelFile(self) -> str:
		"""
		Gets the project's target GUI model file path (.tguim)
		
		:return: The path to the project's .tguim file
		:rtype: str
		"""
		
		return os.path.join(self._projectDir, self._name + ".tguim")
	
	def getAPIModelFile(self) -> str:
		"""
		Gets the project's API model file path (.apim)
		
		:return: The path to the project's .apim file
		:rtype: str
		"""
		
		return os.path.join(self._projectDir, self._name + ".apim")
	
	def startTargetApplication(self) -> None:
		"""
		Starts the target application
		
		:return: None
		:rtype: None
		"""
		self._process = psutil.Popen([self._executable], stdout=PIPE)
		
	def getProcess(self) -> psutil.Process:
		"""
		Gets the process of the target application iff it is running.
		
		:return: The process object if the target application is running. None if it is not running.
		:rtype: psutil.Process or NoneType
		"""
		if (self._process is None) or (not self._process.is_running()):
			return None
		return self._process
		
	
	@staticmethod
	def load(mainFile: str) -> 'Project':
		"""
		Creates a Project object from a .fcl file.
		
		:param mainFile: The project's .fcl file
		:type mainFile: str
		:return: The project object reconstructed from a .fcl file.
		:rtype: Project
		"""
		
		mainProjectFile = open(mainFile)
		contents = mainProjectFile.read()
		projectJSON = json.loads(contents)
		mainProjectFile.close()
		
		projectDir = os.path.dirname(mainFile)
		name = projectJSON["Project Information"]["Name"]
		description = projectJSON["Project Information"]["Description"]
		exe = projectJSON["Application Information"]["Target Application"]
		backend = projectJSON["Application Information"]["Backend"]
		startupTimeout = projectJSON["Application Information"]["Startup Timeout"]
		
		loadedProject = Project(name, description, exe, backend, projectDir, startupTimeout)

		# TODO: Load models and put them in the project object
		#loadedProject.setTargetGUIModel(projectJSON["Model Files"]["Target GUI Model"])
		#loadedProject.setAPIModel(["Model Files"]["API Model"] = self._APIModel)

		return loadedProject
	
	def save(self) -> None:
		"""
		Writes a project out to disk as a set of files. (*.fcl, *.tguim, *.apim)
		
		:return: None
		:rtype: NoneType
		"""
		
		projectDict = {}
		projectDict["Project Information"] = {}
		projectDict["Project Information"]["Name"] = self._name
		projectDict["Project Information"]["Description"] = self._description
		projectDict["Application Information"] = {}
		projectDict["Application Information"]["Target Application"] = self._executable
		projectDict["Application Information"]["Backend"] = self._backend
		projectDict["Application Information"]["Startup Timeout"] = self._startupTimeout
		projectDict["Model Files"] = {}
		projectDict["Model Files"]["Target GUI Model"] = self._targetGUIModel
		projectDict["Model Files"]["API Model"] = self._APIModel
		
		with open(self.getMainProjectFile(), "w") as file:
			file.write(json.dumps(projectDict, indent=4))
		
		# TODO: save models as well.
		