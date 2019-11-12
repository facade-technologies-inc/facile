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


class Token:
	"""
	Token class sets parameters of a token for each state that changes.
	"""

	THRESHOLD = 0

	def __init__(self = None,parentSuperToken = None,picture = None,title = None,typeOf = None,position = None,refs = None,cwTitle = None,cwControlType = None,autoID = None):
		"""
		Constructs parameters for each token. Checks if the tokens attribute changed based on a random variable.

		:return: None
		:rtype: NoneType
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
		The isEqualTo function gives a weight of importance to each attribute. This is based on the tokens when its state is changed.

		:param: token
		:return: int
		:rtype: NoneType
		"""
		total = 0
		if token2.parentst == self.parentst:
			total += 10

		if token2.pic == self.pic:
			total += 1
	
		if token2.t == self.t:
			total += 1

		if token2.type == self.type:
			total += 10

		if token2.pos == self.pos:
			total += 5

		if token2.reference == self.reference:
			total += 1

		if token2.cwt == self.cwt:
			total += 2

		if token2.cwct == self.cwct:
			total += 6

		if token2.autoid == self.autoid:
			total += 10

		if total >= Token.THRESHOLD():
			return 1
		else:
			return 0
	

