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

from tguiil.tokens import Token

class ComponentFinder:

	def __init__(self, pwaApp):
		self._app = pwaApp
		
	def find(self, superToken):
		
		timestamp = self._app.getStartTime()
		bestCertainty = 0
		closestComponent = None
		if self._process.is_running():
			# work acts as a stack. Each element is a 2-tuple where the first element
			# is a GUI component and the second element is the parent super token.
			work = [win for win in self._app.windows()]
			while len(work) > 0:
				curComponent = work.pop()
				try:
					token = Token.createToken(timestamp, curComponent)
				except Token.CreationException as e:
					print(str(e))
				else:
					decision, certainty = self._superToken.shouldContain(token)
					if decision == Token.Match.EXACT:
						self.initiateBlinkSequence(curComponent)
						return
					elif decision == Token.Match.CLOSE:
						if certainty > bestCertainty:
							closestComponent = curComponent
							bestCertainty = certainty
				
				children = curComponent.children()
				for child in children:
					work.append(child)
			
			if closestComponent:
				self.initiateBlinkSequence(closestComponent)
				return
			else:
				info = "The selected component could not be\nfound in the target GUI."
				self.componentNotFound.emit(info)