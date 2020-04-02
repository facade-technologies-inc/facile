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
from .baseapplication import BaseApplication
from tguiil.matchoption import MatchOption

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
		
		BaseApplication.__init__(self, {exeLoc}, {options}, {name}, {backend})
	
	def start(self) -> 'Application':
		"""
		Starts the target application, then waits for all processes' active window to be ready.
		Returns self, that way the user can just call Application().start() when initializing their app.
		"""
		
		self.startApp()
		return self

