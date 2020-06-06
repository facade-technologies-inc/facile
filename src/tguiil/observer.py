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

This module contains the Observer class, which watches the target GUI for changes.
"""

from datetime import datetime
from threading import Lock

import psutil
import pywinauto
from PySide2.QtCore import QThread, Signal, Qt
from PySide2.QtWidgets import QProgressDialog, QMessageBox
from pywinauto.controls.uiawrapper import UIAWrapper
from time import time

from tguiil.application import Application
from tguiil.supertokens import SuperToken
from tguiil.tokens import Token


class Observer(QThread):
	"""
	The observer continually traverses the target GUI and notifies when new components are found.
	It maintains a tree of super tokens to determine whether a component has already been found or not.
	
	To use:
		process = psutil.Popen(["C:\\Program Files\\Notepad++\\notepad++.exe"])
		observer = Observer(process.pid, 'uia')
		observer.newSuperToken.connect(targetGUIModel.addSuperToken)
		observer.start()
	"""
	
	# This signal is emitted when a new component is detected.
	newSuperToken = Signal(SuperToken, SuperToken)  # (new SuperToken, new SuperToken's parent SuperToken)

	# This signal is emitted when the backend has been detected.
	backendDetected = Signal(str)
	
	ignoreTypes = set()
	ignoreTypes.add("SysShadow")
	ignoreTypes.add("ToolTips")
	ignoreTypes.add("MSCTFIME UI")
	ignoreTypes.add("IME")
	ignoreTypes.add("Pane")
	
	# ignoreTypes.add("wxWindowNR")
	# ignoreTypes.add("wxWindow")
	
	def __init__(self, processID: int, captureImages: bool, backend: str = "uia"):
		"""
		Constructs an Observer. The target application must already be started before constructing the Observer.
		
		:raises: NoSuchProcess
		:raises: AccessDenied
		:param processID: The ID of the process to watch.
		:type processID: int
		:param captureImages: If True, capture images of components. If false, don't.
		:type captureImages: bool
		:param backend: "win32", "uia", or "auto"
		:type backend: str
		:return: None
		:rtype: NoneType
		"""
		QThread.__init__(self)
		self._pid = processID
		self._process = psutil.Process(processID)
		self._backend = backend
		self._childMapping = {None: []}  # maps each super token to its list of children.
		
		# maps each super token to the last iteration it was matched on.
		self._lastSuperTokenIterations = {}
		self._iteration = 0
		
		self._playing = False
		self._playingLock = Lock()

		self.capturing = captureImages
	
	def loadSuperTokens(self, tguim: 'TargetGuiModel') -> None:
		"""
		Loads existing super tokens into the observer to avoid duplication of super tokens.

		This method will iterate over all components in the target GUI model and extract the
		SuperToken references. It will build the simple of super tokens internally using
		dictionaries.

		This method is vital because when a new observer is created, it needs to know about
		existing super tokens to avoid duplication.

		.. note::
			This method should be run in Facile's main thread BEFORE the observer is played.

		:param tguim: The target GUI model to load the super tokens from.
		:type tguim: TargetGuiModel
		:return: None
		:rtype: NoneType
		"""
		componentWork = tguim.getRoot().getChildren()[:]
		
		# add all of the top level components to be children of None
		self._childMapping[None] = []
		for component in componentWork:
			superT = component.getSuperToken()
			self._childMapping[None].append(superT)
		
		while componentWork:
			component = componentWork.pop()
			super = component.getSuperToken()
			self._lastSuperTokenIterations[super] = -1
			self._childMapping[super] = []
			for child in component.getChildren():
				self._childMapping[super].append(child.getSuperToken())
				componentWork.append(child)

	def detectBackend(self):
		"""
		This function automatically detects the backend of the target app using a time-based approach.
		Whichever backend detects the largest number of unique components in the same number of seconds is selected.
		"""
		# Let the user know we are detecting the backend
		self.backendDetected.emit('detecting')

		# Time to wait to collect components
		waitTime = 3

		# ---- UIA ---- #
		app = Application(backend="uia")
		app.setProcess(self._process)
		appTimeStamp = app.getStartTime()
		self._iteration = 0

		endTime = time() + waitTime  # In waitTime seconds, stop the loop
		while self._process.is_running():
			if time() > endTime:
				break

			self._iteration += 1

			if not self.isPlaying(): return 0

			componentCount = 0
			# work acts as a stack. Each element is a 2-tuple where the first element
			# is a GUI component and the second element is the parent super token.
			work = [(win, None) for win in app.windows()]
			while len(work) > 0:
				if time() > endTime:
					break

				if not self.isPlaying(): return 0

				curComponent, parentSuperToken = work.pop()
				if curComponent.friendly_class_name() not in Observer.ignoreTypes:
					try:
						token = Token.createToken(appTimeStamp, curComponent, captureImage=self.capturing)

					# List boxes have a ton of children that we probably don't care about.
					# There are probably other types like it where we just want to ignore the
					# children. We can make this type of
					# if token.type == "ListBox":
					#     continue

					except Token.CreationException as e:
						continue

					nextParentSuperToken = self.matchToSuperToken(token, parentSuperToken, detecting=True)
					self._lastSuperTokenIterations[nextParentSuperToken] = self._iteration
				else:
					nextParentSuperToken = parentSuperToken

				children = curComponent.children()
				for child in children:
					work.append((child, nextParentSuperToken))

		uiaComps = len(self._childMapping)  # Number of unique components found
		self._childMapping = {None: []}
		self._lastSuperTokenIterations = {}

		# ---- WIN32 ---- #
		app = Application(backend="win32")
		app.setProcess(self._process)
		appTimeStamp = app.getStartTime()
		self._iteration = 0

		endTime = time() + waitTime  # In waitTime seconds, stop the loop
		while self._process.is_running():
			if time() > endTime:
				break

			self._iteration += 1

			if not self.isPlaying(): return 0

			componentCount = 0
			# work acts as a stack. Each element is a 2-tuple where the first element
			# is a GUI component and the second element is the parent super token.
			work = [(win, None) for win in app.windows()]
			while len(work) > 0:
				if time() > endTime:
					break

				if not self.isPlaying(): return 0

				curComponent, parentSuperToken = work.pop()
				if curComponent.friendly_class_name() not in Observer.ignoreTypes:
					try:
						token = Token.createToken(appTimeStamp, curComponent, captureImage=self.capturing)

					# List boxes have a ton of children that we probably don't care about.
					# There are probably other types like it where we just want to ignore the
					# children. We can make this type of
					# if token.type == "ListBox":
					#     continue

					except Token.CreationException as e:
						continue

					nextParentSuperToken = self.matchToSuperToken(token, parentSuperToken, detecting=True)
					self._lastSuperTokenIterations[nextParentSuperToken] = self._iteration
				else:
					nextParentSuperToken = parentSuperToken

				children = curComponent.children()
				for child in children:
					work.append((child, nextParentSuperToken))

		w32Comps = len(self._childMapping)
		self._childMapping = {None: []}
		self._lastSuperTokenIterations = {}

		if uiaComps > w32Comps:
			self._backend = 'uia'
			self.backendDetected.emit('uia')
		elif uiaComps < w32Comps:
			self._backend = 'win32'
			self.backendDetected.emit('win32')
		else:
			# If they detect the same amount, should probably rerun the test longer, but I doubt this will ever happen.
			# Leaving to default as uia for now
			self._backend = 'uia'
			self.backendDetected.emit('uia')
	
	def run(self) -> int:
		"""
		DO NOT CALL THIS METHOD. This method is run in a new thread when the start() method is called.
		
		:return: the exit code of the thread which should be 0.
		:rtype: int
		"""
		if self._backend == "auto":
			self.detectBackend()

		self._iteration = 0
		app = Application(backend=self._backend)
		app.setProcess(self._process)
		
		appTimeStamp = app.getStartTime()
		while self._process.is_running():
			self._iteration += 1
			
			if not self.isPlaying(): return 0
			
			componentCount = 0
			# work acts as a stack. Each element is a 2-tuple where the first element
			# is a GUI component and the second element is the parent super token.
			work = [(win, None) for win in app.windows()]
			while len(work) > 0:
				
				if not self.isPlaying(): return 0
				
				curComponent, parentSuperToken = work.pop()
				if curComponent.friendly_class_name() not in Observer.ignoreTypes:
					try:
						token = Token.createToken(appTimeStamp, curComponent, captureImage=self.capturing)
					
					# List boxes have a ton of children that we probably don't care about.
					# There are probably other types like it where we just want to ignore the
					# children. We can make this type of
					# if token.type == "ListBox":
					#     continue
					
					except Token.CreationException as e:
						continue
					
					nextParentSuperToken = self.matchToSuperToken(token, parentSuperToken)
					self._lastSuperTokenIterations[nextParentSuperToken] = self._iteration
				else:
					nextParentSuperToken = parentSuperToken
				
				children = curComponent.children()
				for child in children:
					work.append((child, nextParentSuperToken))
	
	def matchToSuperToken(self, token: Token, parentSuperToken: SuperToken, detecting=False) -> SuperToken:
		"""
		Gets the SuperToken that best matches the given token.
		
		The parentSuperToken is necessary in the case that a new SuperToken is created. In this
		case, both the new SuperToken and its parent will be carried in the newSuperToken signal
		which will be emitted.
		
		Having the parent super token also allows us to reduce the search space when finding the
		matched SuperToken.
		
		:param token: The token to find a SuperToken match with.
		:type token: Token
		:param parentSuperToken: The parent of the SuperToken that will be matched with the token.
		:type parentSuperToken: SuperToken
		:param detecting: If the function is called while detecting the backend. Default is False.
		:type detecting: bool
		:return: The SuperToken that gets matched to the provided token.
		:rtype: SuperToken
		"""
		if token.isDialog:
			parentSuperToken = None
		
		# determine if the new token matches any super tokens and how well it matches if it does.
		bestMatch = 0
		bestDecision = Token.Match.NO.value
		selectedSuperToken = None
		potentialMatches = self._childMapping[parentSuperToken]
		
		for superToken in potentialMatches:
			
			if self._lastSuperTokenIterations[superToken] == self._iteration:
				continue
			
			decision, matchVal = superToken.shouldContain(token)
			bestDecision = min(bestDecision, decision.value)
			
			if decision == Token.Match.NO:
				continue
			
			elif decision == Token.Match.EXACT:
				return superToken
			
			elif decision == Token.Match.CLOSE:
				# in the case that multiple SuperTokens closely match the token,
				# we'll use the SuperToken that has the higher match.
				if matchVal > bestMatch:
					bestMatch = matchVal
					selectedSuperToken = superToken

		# At this point, we know the token will be used in the TGUIM.
		token.registerAsAccepted()

		# No match was found
		if selectedSuperToken is None:
			newSuperToken = SuperToken(token, parentSuperToken)

			self._childMapping[parentSuperToken].append(newSuperToken)
			self._childMapping[newSuperToken] = []
			if not detecting:  # this statement is satisfyingly clean
				self.newSuperToken.emit(newSuperToken, parentSuperToken)
			return newSuperToken
		
		# a close match was found
		else:
			selectedSuperToken.addToken(token)
			return selectedSuperToken

	def captureImages(self, status: bool) -> None:
		self.capturing = True
	
	def setPlaying(self, status: bool) -> None:
		"""
		Sets the running flag.
		:param status: True if running, False if not.
		:type status: bool
		:return: None
		:rtype: NoneType
		"""
		self._playingLock.acquire()
		self._playing = status
		self._playingLock.release()
	
	def isPlaying(self) -> bool:
		"""
		Gets the running status.
		:return: True if running, False if not.
		:rtype: bool
		"""
		self._playingLock.acquire()
		running = self._playing
		self._playingLock.release()
		return running
	
	def play(self):
		"""
		Runs the Observer.
		
		:return: True if the observer is running, False otherwise.
		:rtype: bool
		"""
		if not self._process.is_running():
			return False
		
		if self.isRunning():
			return True
		
		self.setPlaying(True)
		self.start()
		return self.isRunning()
	
	def pause(self):
		"""
		Stops the Observer.

		:return: True if the observer is running, False otherwise.
		:rtype: bool
		"""
		self.setPlaying(False)
		if self.isRunning():
			self.quit()
			return True
		return False
	
	def getPID(self) -> int:
		"""
		Gets the Process ID of the process that is being watched by the observer
		
		:return: The process ID of the process that the observer is watching.
		:rtype: int
		"""
		return self._pid
