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
"""
from typing import Set

from enum import Enum


class CompilationProfile:
	class DocType(Enum):
		"""
		Create a Enum class for documentation choice(s).
		"""
		
		EPub = 4
		Doc = 3
		Html = 2
		Pdf = 1
	
	class CompResOpt(Enum):
		"""
		Create a Enum class for Component Resolution Option(s).
		"""
		
		Option1 = 3
		Option2 = 2
		Pywinauto = 1
	
	def __init__(self, docTypes: Set['CompilationProfile.DocType'], compResOpts: Set['CompilationProfile.CompResOpt'],
	             apiFolderDir, interpExeDir):
		"""
		Construct the CompilationProfile containing the information from ApiCompilerDialog.
		"""
		
		self.compResOpts = compResOpts
		self.docTypes = docTypes
		self.apiFolderDir = apiFolderDir
		self.interpExeDir = interpExeDir
