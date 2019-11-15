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

This file contains the super tokens class that initializes tokens as a list and a function that
iterates through the tokens in the token list.
"""
class SuperToken: 
	"""
	A super token is used to identify a component in multiple states. They can be ignored if the user
	does not care about specific components.
	"""
	IDENTIFIER = 
	def __init__(self, ignoreFlag = False):
		""" 
		Constructs a unique identifier and a way to hide certain components

		:param ignoreFlag: Allows the user to ignore specific components
		:type ignoreFlag: boolean
		
		:return: None
		:rtype: NoneType
		"""
		self.tokens = [token1]
		self.id = identifier
		self.flag = ignoreFlag

	def addToken(self, tokenA): 
		"""
		The addToken function adds a token to the supertoken.

		:param tokenA: Returns the super token of the token to which the component belongs to
		:type tokenA: Token
		:return: None
		:rtype: SuperToken
		"""
		self.tokens.append(tokenA)

	def shouldContain(token2): 
		"""
		The shouldContain function iterates through the tokens in a list to see if the token
		belongs to a supertoken.

		:param token2: Adds the tokens together if they are equal
		:type token2: Token
		:return: Token
		:rtype: Token
		"""
		for token in self.tokens:
			if token.isEqualTo(token2):
				return Token.Match.EXACT


				######### Return if exact match no match or close match, user will be able to add

