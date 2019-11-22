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

from tguiil.tokens import Token

class SuperToken: 
	"""
	A super token is used to identify a component in multiple states. They can be ignored if the user
	does not care about specific components.
	"""
	id_counter = 1
	def __init__(self, token, parent: 'SuperToken'):
		""" 
		Constructs a unique identifier and a way to hide certain components

		:param token: The first token to be added to the SuperToken that's being created.
		:type token: Token
		:param parent: The parent of the SuperToken being created.
		:type parent: SuperToken or NoneType
		:return: None
		:rtype: NoneType
		"""
		self.tokens = [token]
		self.id = SuperToken.id_counter
		SuperToken.id_counter += 1
		self.ignoreFlag = False
		
		width = token.rectangle.width()
		height = token.rectangle.height()
		if parent is None:
			px = 0
			py = 0
		else:
			px = parent.tokens[0].rectangle.left
			py = parent.tokens[0].rectangle.top
		self.posRelativeToParent = (token.rectangle.left - px, token.rectangle.top - py, width, height)

	def addToken(self, tokenA): 
		"""
		The addToken function adds a token to the supertoken.

		:param tokenA: Returns the super token of the token to which the component belongs to
		:type tokenA: Token
		:return: None
		:rtype: SuperToken
		"""
		self.tokens.append(tokenA)

	def shouldContain(self, token2):
		"""
		The shouldContain function iterates through the tokens in a list to see if the token
		belongs to a supertoken.

		:param token2: Adds the tokens together if they are equal
		:type token2: Token
		:return: Token
		:rtype: Token
		"""
		DEBUG_TOKEN_COMPARISON = False
		
		bestCloseScore = 0
		for token in self.tokens:
			decision, score = token.isEqualTo(token2)
			
			if DEBUG_TOKEN_COMPARISON:
				print()
				print("/------------------------------------------------")
				print("COMPARE:")
				print("\t", token)
				print("\t", token2)
				print(decision, score)
				print("\\------------------------------------------------")
				print()
			
			if decision == Token.Match.EXACT:
				return Token.Match.EXACT, score
			elif decision == Token.Match.CLOSE:
				if score > bestCloseScore:
					bestCloseScore = score
		
		if bestCloseScore == 0:
			return Token.Match.NO, 0
		
		return Token.Match.CLOSE, bestCloseScore
	
	def __str__(self):
		return "SuperToken:\n\t" + "\n\t".join([str(token) for token in self.tokens])
	
	def __repr__(self):
		return self.__str__()