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
This module contains the Observer class, which watches the target GUI for changes.
"""

from threading import Lock

import psutil
import pywinauto
from PySide2.QtCore import QThread, Signal
from pywinauto.controls.uiawrapper import UIAWrapper

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
	newSuperToken = Signal(SuperToken,
	                       SuperToken)  # (new SuperToken, new SuperToken's parent SuperToken)
	
	ignoreTypes = set()
	ignoreTypes.add("SysShadow")
	ignoreTypes.add("ToolTips")
	ignoreTypes.add("MSCTFIME UI")
	ignoreTypes.add("IME")
	
	# ignoreTypes.add("wxWindowNR")
	# ignoreTypes.add("wxWindow")
	
	def __init__(self, processID: int, backend: str = "uia"):
		"""
		Constructs an Observer. The target application must already be started before constructing the Observer.
		
		:raises: NoSuchProcess
		:raises: AccessDenied
		:param processID: The ID of the process to watch.
		:type processID: int
		:return: None
		:rtype: NoneType
		"""
		QThread.__init__(self)
		self._process = psutil.Process(processID)
		self._backend = backend
		self._childMapping = {None: []}  # maps each super token to its list of children.
		
		self._playing = False
		self._playingLock = Lock()
	
	def run(self) -> int:
		"""
		DO NOT CALL THIS METHOD. This method is run in a new thread when the start() method is called.
		
		:return: the exit code of the thread which should be 0.
		:rtype: int
		"""
		app = Application(backend=self._backend)
		app.setProcess(self._process)
		while self._process.is_running():
			
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
						token = Observer.createToken(curComponent)
						if token.type == "ListBox":  # TODO: Make this more formal (ignore other similar types without checking firendly class name)
							continue
					
					except Token.CreationException as e:
						print(str(e))
					
					nextParentSuperToken = self.matchToSuperToken(token, parentSuperToken)
				else:
					nextParentSuperToken = parentSuperToken
				
				children = curComponent.children()
				for child in children:
					work.append((child, nextParentSuperToken))
	
	@staticmethod
	def createToken(component: pywinauto.base_wrapper.BaseWrapper) -> Token:
		"""
		Create a token from a pywinauto control.
		
		:raises: Token.CreationException
		
		:param component: A pywinauto control from the target GUI.
		:type component: pywinauto.base_wrapper
		:return: The token that was created from the pywinauto control.
		:rtype: Token
		"""
		
		parent = component.parent()
		if parent:
			parentTitle = parent.window_text()
			parentType = parent.friendly_class_name()
		else:
			parentTitle = ""
			parentType = ""
		
		topLevelParent = component.top_level_parent()
		topLevelParentTitle = topLevelParent.window_text()
		topLevelParentType = topLevelParent.friendly_class_name()
		
		# Information we can get about any element
		id = component.control_id()
		isDialog = component.is_dialog()
		isEnabled = component.is_enabled()
		isVisible = component.is_visible()
		processID = component.process_id()
		rectangle = component.rectangle()
		texts = component.texts()[1:]
		title = component.window_text()
		numControls = component.control_count()
		image = None  # component.capture_as_image()
		typeOf = component.friendly_class_name()
		
		# get text of all children that are not editable.
		childrenTexts = []
		for child in component.children():
			if type(child) != pywinauto.controls.win32_controls.EditWrapper:
				try:
					text = child.text()
					if text is None:
						text = child.window_text()
					if text is None:
						text = ""
					childrenTexts.append(text)
				except:
					childrenTexts.append("")
		
		# additional information we can get about uia elements
		try:
			autoID = component.automation_id()
			shownState = component.get_show_state()
			expandState = component.get_expand_state()
		except:
			autoID = None
			expandState = None
			shownState = None
		
		# construct control identifiers
		# There are 4 possible control identifiers:
		#   - title
		#   - friendly class
		#   - title + friendly class
		#   - closest text + friendly class (only if the title is empty)
		
		if title is None:
			title = ""
		
		controlIdentifiers = [title, typeOf, title + typeOf]
		
		# create a new token
		token = Token(id, isDialog, isEnabled, isVisible, processID, typeOf, rectangle, texts,
		              title,
		              numControls, controlIdentifiers, parentTitle, parentType,
		              topLevelParentTitle, topLevelParentType, childrenTexts, image, autoID,
		              expandState, shownState)
		
		return token
	
	def matchToSuperToken(self, token: Token, parentSuperToken: SuperToken) -> SuperToken:
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
		:return: The SuperToken that gets matched to the provided token.
		:rtype: SuperToken
		"""
		
		# determine if the new token matches any super tokens and how well it matches if it does.
		bestMatch = 0
		bestDecision = Token.Match.NO.value
		selectedSuperToken = None
		potentialMatches = self._childMapping[parentSuperToken]
		
		for superToken in potentialMatches:
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
		
		# No match was found
		if selectedSuperToken == None:
			newSuperToken = SuperToken(token, parentSuperToken)
			
			self._childMapping[parentSuperToken].append(newSuperToken)
			self._childMapping[newSuperToken] = []
			self.newSuperToken.emit(newSuperToken, parentSuperToken)
			return newSuperToken
		
		# a close match was found
		else:
			selectedSuperToken.addToken(token)
			return selectedSuperToken
	
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
