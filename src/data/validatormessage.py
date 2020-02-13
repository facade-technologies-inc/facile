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
from enum import Enum

class ValidatorMessage:
	"""
	Validator Message class is a customized message after validation.
	"""
	
	class Level(Enum):
		"""
		Create a Enum class for different types of message.
		"""
		
		Error = 3
		Warning = 2
		Info = 1
	
	def __init__(self, text: str, level: Enum, entity: int=None):
		"""
		Construct the view for the validator.
		"""
		
		self.text = text
		self.level = level
		self.entity = entity
		self.widget = None