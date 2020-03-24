import sys, os
pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)

import time
from typing import Set
from tguiil.matchoption import MatchOption
from baseapplication import BaseApplication

class Application(BaseApplication):
	def __init__(self):
		BaseApplication.__init__(self, "C:/Windows/notepad.exe", set([MatchOption.CloseToken, MatchOption.PWABestMatch, MatchOption.ExactToken]), "Notepad1", "uia")

	def _52_write(self, value: str) -> None:
		"""
		Write to a component.

		:param value: Value to be written.
		:type value: str
		:return: None
		:rtype: NoneType
		"""

		comp = self.findComponent(52)

		try:
			comp.type_keys(value, with_spaces=True)
		except:
			print("The action 'write' was not executed correctly on component with ID 52. Please contact support to fix this issue.")


	def _52_read(self) -> str:
		"""
		Read from a component.

		:return: (Value obtained from reading component text.)
		:rtype: (str)
		"""

		comp = self.findComponent(52)

		try:
			return comp.get_value()
		except:
			print("The action 'read' was not executed correctly on component with ID 52. Please contact support to fix this issue.")


	def default(self, default: str) -> None:
		"""
		Add a comment here...

		:param default: Add a comment here...
		:type default: str
		:return: None
		:rtype: NoneType
		"""

		self._52_write(default)

	def default2(self, default: str, default2: str) -> None:
		"""
		Add a comment here...

		:param default: Add a comment here...
		:type default: str
		:param default2: Add a comment here...
		:type default2: str
		:return: None
		:rtype: NoneType
		"""

		self.default(default)
		self.default(default2)

	def default3(self, default: str, default2: str) -> str:
		"""
		Add a comment here...

		:param default: Add a comment here...
		:type default: str
		:param default2: Add a comment here...
		:type default2: str
		:return: (Add a comment here...)
		:rtype: (str)
		"""

		self.default2(default, default2)
		a = self._52_read()

		return a

