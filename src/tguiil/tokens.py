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
		POS = 5
		REFS = 1
		CWTITLE = 2
		CWCT = 6
		AUTOID = 10

	THRESHOLD = 0

	def __init__(self,parentSuperToken: SuperToken = None,picture: Picture = None,title,typeOf = None,position
	= None,refs = None,cwTitle = None,cwControlType = None,autoID = None):
		"""
		Constructs token objects with given parameters.
		Checks if the tokens attribute changed based on a random variable.

		:param parentSuperToken: parent of tokens
		:type parentSuperToken: superToken
		:return parentSuperToken: None
		:rtype parentSuperToken: NoneType

		:param picture: 
		:type picture:
		:return picture:
		:rtype NoneType:

		:param title: str
		:type title: 

		:param typeOf: str

		:param position: lists of str and ints

		:param refs: lists of str and ints

		:param cwTitle: str

		:param cwControlType: str

		:param autoID: str

		"""
		self.parentst = parentSuperToken
		self.pic = picture
		self.t = title
		self.type = typeOf
		self.pos = position
		self.reference = refs
		self.cwt = cwTitle
		self.cwct = cwControlType
		self.autoid = autoID


	def isEqualTo(token2): 
		""" 
		The isEqualTo function gives a weight of importance to each attribute.
		This is based on the tokens when its state is changed.

		:token2: Token
		"""
		#####################################################################
		#	QUICK CHECK FOR EXACT MATCH
		#####################################################################

		# If all control identifiers and auto IDs match, return Token.Match.EXACT

		#####################################################################
		#	MORE IN DEPTH CHECK FOR CLOSE MATCH (WEIGHTING)
		#####################################################################
		total = 0 

		if token2.parentst == self.parentst:
			total += Token.Weight.PARENTST
			
		if token2.pic == self.pic:
			total += Token.Weight.PIC
	
		if token2.t == self.t:
			total += Token.Weight.TITLE

		if token2.type == self.type:
			total += Token.Weight.TYPE

		if token2.pos == self.pos:
			total += Token.Weight.POS

		if token2.reference == self.reference:
			total += Token.Weight.REFS

		if token2.cwt == self.cwt:
			total += Token.Weight.CWTITLE

		if token2.cwct == self.cwct:
			total += Token.Weight.CWCT

		if token2.autoid == self.autoid:
			total += Token.Weight.AUTOID

		if total >= Token.THRESHOLD():
			return Token.Match.CLOSE

		else: 
			return Token.Match.NO




	

