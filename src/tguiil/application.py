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

This file contains the Application class - an alternative to pywinauto's Application class that builds off of
pywinauto's Desktop class.
"""

from datetime import datetime

import psutil
import pywinauto

class WaitException(Exception):
	def __init__(self, msg: str):
		Exception.__init__(self, msg)

class Application(pywinauto.Desktop):
	"""
	This class is an alternative to pywinauto's Application class that will detect windows in all of an application's
	processes.
	"""
	
	# TODO: If the original process was just used to create other processes and then it disappears, the child processes
	#  are called zombies. currently, this class does not work with applications that fit this description. This class
	#  could be made more robust.
	
	ignoreTypes = set()
	ignoreTypes.add("SysShadow")
	ignoreTypes.add("ToolTips")
	ignoreTypes.add("MSCTFIME UI")
	ignoreTypes.add("IME")
	ignoreTypes.add("Pane")
	
	def __init__(self, backend: str = "uia") -> None:
		"""
		Constructs an Application instance
		
		:param backend: the accessibility technology to use to deconstruct the target GUI.
		:type backend: str
		:return: None
		:rtype: NoneType
		"""
		pywinauto.Desktop.__init__(self, backend=backend)
		
		# store time stamp as int
		self._startTime = int(datetime.now().strftime("%y%m%d%H%M%S").lstrip("0"))
		self._process = None
		
	def is_process_running(self) -> bool:
		"""
		Determine if the application is running or not.
		
		.. note:: this function is named this way to match pywinauto.application.Application.is_process_running
		
		:return: True if running, False otherwise.
		:rtype: bool
		"""
		if self._process is None:
			return False
		
		for pid in self.getPIDs():
			if psutil.Process(pid = pid).is_running():
				return True
			
		return False
		
	def setProcess(self, process: psutil.Process) -> None:
		"""
		Sets the application's process. This method should be called directly after the Application object is
		instantiated
		
		:param process: the target application's main process
		:type process: psutil.Process
		:return: None
		:rtype: NoneType
		"""
		self._process = process
	
	def getPIDs(self) -> list:
		"""
		Gets the target application's main process ID and all child process IDs.
		
		:return: list of all process IDs belonging to the target application.
		:rtype: list[int]
		"""
		pids = [self._process.pid]
		try:
			for child in self._process.children():
				pids.append(child.pid)
		except:
			pass
		return pids
	
	def windows(self) -> list:
		"""
		Gets all windows which belong to the target application and child processes.
		
		:return: list of windows that belong to the target application and it's children processes
		:type: list[pywinauto.application.WindowSpecification]
		"""
		
		while True:
			try:
				wins = pywinauto.Desktop.windows(self, top_level_only=True)
			except pywinauto.controls.hwndwrapper.InvalidWindowHandle:
				continue
			else:
				break
		
		appWins = []
		pids = self.getPIDs()
		for win in wins:
			if win.process_id() in pids:
				appWins.append(win)
		return appWins
	
	def getActiveWindow(self) -> pywinauto.application.WindowSpecification:
		"""
		Returns the current active window
		:return:
		"""
		
		while True:
			try:
				return pywinauto.Desktop.windows(self, active_only = True)[0]
			except pywinauto.controls.hwndwrapper.InvalidWindowHandle:
				continue
	
	def wait(self, state: str, timeout: float = 120):
		"""
        Pauses until state is reached for all visible windows, timing out in timeout seconds. Useful when waiting
        for target app to complete execution of a task, or when starting up.
        Wraps around pywinauto's wait function.

        :param state: state to wait for ('visible', 'ready', 'exists', 'enabled', 'active')
        :type state: str
        :param timeout: Maximum number of seconds to wait for state to be reached. Defaults to a minute, should be longer for apps with more windows.
        :type timeout: float
        """
		
		# ---- NOTE: Letting pywinauto handle the errors if state isn't a valid state ----
		
		pids = self.getPIDs()
		procSecs = timeout / len(pids)
		success = False
		
		# TODO: Change this to use desktop stuff, for the moment this method is the only one I could find that works.
		#  Info: the only types that '.wait()' works on is windowspecifications, and i couldnt find any desktop methods
		#  that return them. Probably because theyre from pywinauto.application.windowspecification, and might only
		#  be 'gettable' from the application class.
		
		for pid in pids:
			try:
				pywinauto.Application().connect(process=pid).top_window().wait(state, timeout=procSecs)
				success = True  # TODO: Counts as success if one of them works. Reevaluate if this is good or not
			except:
				continue
		
		if not success:
			raise WaitException('Could not connect to process. Please try again')
	
	def getStartTime(self) -> int:
		"""
		Gets the time that the Application instance was created as an int.
		
		:return: The time that the Application instance was created.
		:rtype: int
		"""
		return self._startTime
	
	def start(self, path: str):
		"""
		Starts the application with filepath path, connects to it, then waits for it to be ready.
		
		:param path: filepath to exe
		:type path: str
		:return: None
		"""
		
		process = psutil.Popen([path])
		self.setProcess(process)
		self.wait('ready')
		
	def kill(self):
		"""
		Stops the target application
		
		:return: None
		"""
		
		self._process.kill()
