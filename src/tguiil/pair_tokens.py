class Token:

	THRESHOLD = 0

	def __init__(self = None,parentSuperToken = None,picture = None,title = None,typeOf = None,position = None,refs = None,cwTitle = None,cwControlType = None,autoID = None):
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


