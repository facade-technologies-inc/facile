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
from typing import Set

from tguiil.tokens import Token
from tguiil.matchoption import MatchOption
from tguiil.application import Application
from tguiil.supertokens import SuperToken

class ComponentNotFoundException(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)

class ComponentFinder:
	"""
	The ComponentFinder can be used to match a super token to a component in the target GUI using
	the specified matching schemes.
	"""
	
	def __init__(self, app: Application, options: Set[MatchOption]):
		"""
		Initialize a component finder object.
		
		:param app: The application instance used to traverse the target GUI.
		:type app: tguiil.application.Application (preffered) OR pywinauto.application.Application
		:param options: The set of matching schemes that will be used to match the super token to a component.
		:type options: Set[MatchOption]
		"""
		self._app = app
		self._matchOptions = options
		
	def find(self, superToken: SuperToken):
		"""
		Finds a superToken in the target GUI.
		
		:param superToken: The super token to find.
		:type superToken: SuperToken
		:return: The component that matches the super token.
		:rtype: pywinauto.base_wrapper
		"""
		
		timestamp = self._app.getStartTime()
		bestCertainty = 0
		closestComponent = None
		
		if self._app.is_process_running():
			work = [win for win in self._app.windows()]

			while len(work) > 0:
				if not self._app.is_process_running():
					msg = "The application stopped before we could locate the component"
					raise ComponentNotFoundException(msg)
				
				curComponent = work.pop()
				
				try:
					token = Token.createToken(timestamp, curComponent)
				except Token.CreationException as e:
					print(str(e))
				else:
					decision, certainty = superToken.shouldContain(token)
					if decision == Token.Match.EXACT:
						if MatchOption.ExactToken in self._matchOptions:
							return curComponent
					elif decision == Token.Match.CLOSE:
						if certainty > bestCertainty:
							closestComponent = curComponent
							bestCertainty = certainty
				
				children = curComponent.children()
				for child in children:
					work.append(child)
			
			if closestComponent:
				if MatchOption.CloseToken in self._matchOptions:
					return closestComponent
			else:
				info = "The selected component could not be\nfound in the target GUI."
				raise ComponentNotFoundException(info)