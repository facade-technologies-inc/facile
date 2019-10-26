from datetime import datetime

class Project:
	"""
	This class is the top level to a Facile Project.
	It stores information about the target application, the target GUI model, the API model, compilation profiles, etc.
	"""
	
	
	class TargetApplicationProfile:
		def __init__(self, exe, startupTimeout=60):
			self._executable = exe
			self._startupTimeout = startupTimeout
			
	class ChangeLog:
		
		class Change:
			def __init__(self, timestamp=datetime.now()):
				self._timestamp = timestamp
				self._description
		
		def __init__(self):
			self._changes = []
			
		def getCreationTimestamp(self):
			return self._changes[0].getDate()
	
		def getLastChange(self):
			return self._changes[-1]
		
	class SaveFileLocations:
		def __init__(self):
			self._mainProjectFile
			self._targetGUIModel
			self._APIModel
			self._actionsDatabase
	
	def __init__(self):
		self._targetApp = Project.TargetApplicationProfile()
		self._changelog = Project.ChangeLog()
		self._targetGUIModel = None #TargetGUIModel()
		self._APIModel = None #APIModel()
		