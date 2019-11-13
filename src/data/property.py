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

The module contains the Property() class.
"""

class Property:
	"""
	This class allows us to establish the data of our properties.
	"""
	def __init__(self, name:str, value:object, type:object, readOnly: object=False):
		"""
		Constructs a Property Object

		:param name: The name of the property.
		:type name: str
		:param value: The value of the property.
		:type value: object
		:param type: The type of the property.
		:type type: object
		:param readOnly: The type of data structure.
		:type readOnly: object
		:return: The constructed property.
		:rtype: Property
		"""
		self._name = name
		self._value = value
		self._type = type
		self._readOnly = readOnly

	def isReadOnly(self) -> object:
		"""
		Shows the property's data structure.

		:return: The property's data structure.
		:rtype: object
		"""
		return self._readOnly

	def getName(self) -> str:
		"""
		Gets the property's name.

		:return: The property's name.
		:rtype: str
		"""
		return self._name

	def getValue(self) -> object:
		"""
		Gets the property's value.

		:return: The property's value.
		:rtype: object
		"""
		return self._value

	def getType(self) -> object:
		"""
		Gets the property's type.

		:return: The property's type.
		:rtype: object
		"""
		return self._type

	def setValue(self, newValue: object) -> bool:
		"""
		Sets the value if there is a new value.

		:param newValue: New value that needs to be set.
		:type newValue: object
		:return: The property's value.
		:rtype: bool
		"""
		if self.isReadOnly():
			return False
		else:
			self._value = newValue
			return True


	def __str__(self):
		return "{}:{}".format(self._name, self._value)

	def __repr__(self):
		return str(self)