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


