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

	This document contains the custom generated Application class
"""

import sys, os

try:
	from .apicore import BaseApplication, MatchOption
except ImportError:
	from apicore import BaseApplication, MatchOption

pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)


class ActionException(Exception):
	def __init__(self, msg: str):
		Exception.__init__(self, msg)


class Application(BaseApplication):
	"""
	This class allows a user to automate a predefined target GUI using functions (action pipelines) defined
	in Facile itself.
	"""
	
	def __init__(self):
		"""
		Initializes the Application class, then initializes its superclass with the necessary information.
		"""
		
		BaseApplication.__init__(self, {exeLoc},
								 {options},
								 {name},
								 {reqCompIDs},
								 backend={backend})
	
	def start(self) -> 'Application':
		"""
		Starts the target application, then waits for all processes' active window to be ready.
		Returns self, that way the user can just call Application().start() when initializing their app.
		"""
		
		self._startApp()
		return self

	# --------------------- Overloading BaseApplication Methods for Documentation --------------------- #

	def stop(self):
		return BaseApplication.stop(self)

	def pause(self, demo=False):
		return BaseApplication.pause(self, demo)

	def wait(self, state: str, timeout: int = 10):
		return BaseApplication.wait(self, state, timeout)

	def _startApp(self):
		return BaseApplication._startApp(self)

	def _generatePathMap(self):
		return BaseApplication._generatePathMap(self)

	def _findComponent(self, fcgvh):
		return BaseApplication._findComponent(self, fcgvh)

	def _getComponentObject(self, hcfgvjh):
		return BaseApplication._getComponentObject(self, hcfgvjh)

	def _getWindowObjectIDFromHandle(self, chtfgj):
		return BaseApplication._getWindowObjectIDFromHandle(self, chtfgj)

	def _forceShow(self, iugkyhgf):
		return BaseApplication._forceShow(self, iugkyhgf)

	def _selectMenuItem(self, kgvhhbj):
		return BaseApplication._selectMenuItem(self, kgvhhbj)

	# ------------------------------------------------------------------------------------------------ #

