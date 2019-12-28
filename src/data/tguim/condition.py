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

This module contains the Condition class.
"""


class Condition:
	"""
	This class defines when a visibility behavior should or should not be taken.
	"""
	
	def __init__(self) -> 'Condition':
		"""
		Constructs a new Condition object.

		:return: The constructed Condition object.
		:rtype: Condition
		"""
		pass
	
	def evaluateCondition(self) -> bool:
		"""
		Determine if visibility behavior should be taken.

		:return: Boolean -> True if visibility behavior should be taken.  False otherwise.
		:rtype: bool
		"""
		return True
