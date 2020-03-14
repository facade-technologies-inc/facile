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

import time
from datetime import datetime

import psutil
import pywinauto


class Application(pywinauto.Desktop):
	"""
	This class is an alternative to pywinauto's Application class that will detect windows in all of an application's
	processes.
	
	To use:
		process = psutil.Popen(["path/to/target/application.exe", ...], stdout=PIPE)
		app = Application(backend="uia")
		app.setProcess(process)
		appWindows = app.windows()
	"""
	
	# TODO: If the original process was just used to create other processes and then it disappears, the child processes
	#  are called zombies. currently, this class does not work with applications that fit this description. This class
	#  could be made more robust.
	
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

	def windows1(self) -> list:
		"""
		Gets all windows which belong to the target application and child processes.

		:return: list of windows that belong to the target application and it's children processes
		:type: list[pywinauto.application.WindowSpecification]
		"""

		windows = []
		# pid = self._process.pid
		pids = self.getPIDs()
		for pid in pids:
			while True:
				try:
					wins = pywinauto.Application().connect(process=pid).windows(top_level_only=True)
				except:
					wins = pywinauto.Desktop().connect(process=pid).windows(top_level_only=True)
				else:
					break

			for win in wins:
				if win.process_id() in pids and win.is_dialog():
					windows.append(win)

		return windows

	def getStartTime(self) -> int:
		"""
		Gets the time that the Application instance was created as an int.
		
		:return: The time that the Application instance was created.
		:rtype: int
		"""
		return self._startTime


if __name__ == "__main__":
	desktop = pywinauto.Desktop(backend="uia")
	print(desktop.windows())
	
	# Notepad++ doesn't use multiple processes, so I'm not completely testing this correctly. I should run with the
	# calculator app.
	process = psutil.Popen(['Notepad.exe'])
	app = Application(backend="uia")
	app.setProcess(process)
	time.sleep(10)
	print(app.getPIDs())
	print(app.windows())

	childrenTexts = []
	for child in app.windows()[0].children():
		if type(child) != pywinauto.controls.win32_controls.EditWrapper:
			try:
				text = child.texts()
				if text is None:
					text = child.window_text()
				if text is None:
					text = "-"
				childrenTexts.append(text)
			except:
				childrenTexts.append("*")
	print(childrenTexts)



	# TODO: Change to allow for the
