  
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

This file contains the super tokens class that initializes tokens as a list and a function that iterates through the tokens in the token list

"""





class SuperToken:

	def __init__(self, token1, identifier, ignoreFlag):

		self.tokens = [token1]
		self.id = identifier
		self.flag = ignoreFlag



	def addToken(tokenA):

		self.tokens.append(tokenA)

	def shouldContain(token2):

		for token in self.tokens:
			if token.isEqualTo(token2):
				self.addToken(token2)
				break


