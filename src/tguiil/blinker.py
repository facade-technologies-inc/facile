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

This module contains the blinker class which is used to relate the target GUI model
to the actual target GUI.
"""

import psutil
from PySide2.QtCore import QElapsedTimer, QTimer, QThread, Signal

from tguiil.componentfinder import ComponentFinder, ComponentNotFoundException
from tguiil.application import Application
from tguiil.matchoption import MatchOption
from tguiil.tokens import Token


class Blinker(QThread):
	"""
	The Blinker class is used to draw a box around a given element at a specified frequency for a small
	amount of time. Because the box sometimes disappears on its own, this can cause a blinking affect.
	"""
	
	componentNotFound = Signal(str)
	
	INTERVAL_MILLIS = 250
	DURATION_MILLIS = 10_000
	
	colors = ["red", "green", "blue"]
	curColorIdx = 0
	
	def __init__(self, pid: int, backend: str, superToken: 'SuperToken') -> None:
		"""
		Creates a blinker that will draw a box around the component represented by SuperToken periodically
		if the component can be found.
		
		:param pid: The id of the target application's process.
		:type pid: int
		:param backend: either "win32" or "uia" depending on target application.
		:type backend: str
		:param superToken: The supertoken that represents the component that we want to draw a box around.
		:return: None
		:retype: NoneType
		"""
		QThread.__init__(self)
		self._pid = pid
		self._backend = backend
		self._superToken = superToken
		self._color = Blinker.colors[Blinker.curColorIdx % len(Blinker.colors)]
		Blinker.curColorIdx += 1
	
	def run(self) -> None:
		"""
		DO NOT CALL THIS METHOD!
		This method is called automatically when the start() method is called.
		
		This method searches for a Component in the target GUI by traversing
		:return: None
		:rtype: NoneType
		"""
		self._process = psutil.Process(self._pid)
		app = Application(backend=self._backend)
		app.setProcess(self._process)
		
		options = {MatchOption.ExactToken, MatchOption.CloseToken, MatchOption.PWABestMatch}
		finder = ComponentFinder(app, options)
		
		try:
			component = finder.find(self._superToken)
		except ComponentNotFoundException:
			self.componentNotFound.emit("The selected component could not be\nfound in the target GUI.")
		else:
			self.initiateBlinkSequence(component)
	
	def initiateBlinkSequence(self, component: 'Component') -> None:
		"""
		Starts the blink sequence by setting timers and executing an event loop.
		
		NOTE: Because this function executes an event loop, it is blocking.
		
		:param component: The component to select.
		:type component: Component
		:return: None
		:rtype: NoneType
		"""
		self._component = component
		self._component.top_level_parent().set_focus()
		self._timer = QTimer(self)
		self._timer.timeout.connect(lambda: self.tick())
		self._stopWatch = QElapsedTimer()
		self._timer.start(Blinker.INTERVAL_MILLIS)
		self._stopWatch.start()
		self.exec_()
	
	def tick(self) -> None:
		"""
		Draws an outline around the component of interest.
		
		:return: None
		:rtype: NoneType
		"""
		try:
			self._component.draw_outline(colour=self._color, thickness=5)
			self._component.top_level_parent().set_focus()
		except:
			pass
		
		if self._stopWatch.hasExpired(Blinker.DURATION_MILLIS):
			self.stop()
	
	def stop(self) -> None:
		"""
		Stops the blinker regardless of whether it was running or not.
		
		:return: None
		:rtype: NoneType
		"""
		try:
			self._timer.stop()
		except:
			pass
		finally:
			self.quit()
