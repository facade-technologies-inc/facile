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

This file contains the token class that weighs the importance of each attribute of a single token. 
"""
from enum import Enum, unique

class Token: 
	"""
	Token class sets parameters of a token for each state that changes. 
	"""
	@unique
	class Match(Enum):
		EXACT = 1
		CLOSE = 2
		NO = 3

	class Weight(Enum):
		PARENTST = 10
		PIC = 1
		TITLE = 1
		TYPE = 10
		RECT = 5
		REFS = 1
		CWTITLE = 2
		CWCT = 6
		AUTOID = 10

	THRESHOLD = 0

	def __init__(self,picture: PIL.Image = None,title: str,typeOf: str = None,rectangle: win32structures.RECT
	= None,refs: list = None,cwTitle: str = None,cwControlType: str = None,autoID: int = None):
		"""
		Checks if the tokens component state changed based on a random variable.

		:param picture: the image of the component
		:type picture: PIL.Image
		:param title: the title of the component
		:type title: str
		:param typeOf: the characteristics of the component
		:type typeOf: str
		:param rectangle: the coordinates of the component
		:type rectangle: win32structures.RECT
		:param refs: the reference of the component
		:type refs: list
		:param cwTitle: the child window title of the component
		:type cwTitle: str
		:param cwControlType: the child window control type of the component
		:type cwControlType: str
		:param autoID: the unique identifier of the component
		:type autoID: int
		...
		:return: None
		:rtype: NoneType
		"""
		self.pic = picture
		self.title = title
		self.type = typeOf
		self.rectangle = rectangle
		self.reference = refs
		self.cwt = cwTitle
		self.cwct = cwControlType
		self.autoid = autoID

	def isEqualTo(self, token2):
		""" 
		The isEqualTo function gives a weight of importance to each attribute.
		This is based on the tokens when its state is changed.

		:param token2: returns how similar of a match the given token is to the current token
		:type token2: int
		:return: None
		:rtype: NoneType
		"""
		#####################################################################
		#	QUICK CHECK FOR EXACT MATCH
		#####################################################################

		# If all control identifiers and auto IDs match, return Token.Match.EXACT

		#####################################################################
		#	MORE IN DEPTH CHECK FOR CLOSE MATCH (WEIGHTING)
		#####################################################################
		total = 0 

		if token2.pic == self.pic:
			total += Token.Weight.PIC
	
		if token2.t == self.title:
			total += Token.Weight.TITLE

		if token2.type == self.type:
			total += Token.Weight.TYPE

		if token2.rectangle == self.rectangle:
			total += Token.Weight.RECT

		if token2.reference == self.reference:
			total += Token.Weight.REFS

		if token2.cwt == self.cwt:
			total += Token.Weight.CWTITLE

		if token2.cwct == self.cwct:
			total += Token.Weight.CWCT

		if token2.autoid == self.autoid:
			total += Token.Weight.AUTOID

		if total == max(total):
			return Token.Match.EXACT

		elif total >= Token.THRESHOLD():
			return Token.Match.CLOSE

		else: 
			return Token.Match.NO




	

