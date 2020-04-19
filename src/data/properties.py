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

This module contains the Properties() class.
"""

from collections import OrderedDict
from enum import Enum

try: # Facile imports
	from data.property import Property
	from qt_models.propeditormodel import PropModel
except ImportError: # API imports
	from .property import Property


class Properties:
	"""
	This class allows to create data of our properties.
	"""
	
	def __init__(self):
		"""
		Constructs a Properties objects.

		:return: An ordered dictionary of properties.
		:rtype: Properties
		"""
		self._categories = OrderedDict()
	
	def newCategory(self, category: str) -> None:
		"""
		Adds a new category to the dict of categories.

		:param category: The category that will be added to the dict.
		:type category: str
		:return: None
		:rtype: NoneType
		"""
		self._categories[category] = []
	
	def addProperty(self, category: str, name: str, value: object, type: object,
	                readOnly: bool = False) -> None:
		"""
		To add a property to a certain category.

		:param category: Specific category for that property.
		:type category: str
		:param name: Name of property.
		:type name: str
		:param value: Value of property.
		:type value: object
		:param type: Type of property.
		:type type: object
		:param readOnly: Data structure of property.
		:type readOnly: bool
		:return: None
		:rtype: NoneType
		"""
		if category not in self._categories.keys():
			raise Exception("{} does not exist".format(category))
		self._categories[category].append(Property(name, value, type, readOnly))
	
	@staticmethod
	def createPropertiesObject(predefinedCategories: list, customCategories: dict) -> 'Properties':
		"""
		Property Factory, that is a static method, that createes properties objects for predefined and custom categories.

		:param predefinedCategories: Category that was already defined from a list.
		:type predefinedCategories: list
		:param customCategories: Categories that can be made from a list.
		:type customCategories: dict
		:return: Properties objects.
		:rtype: Properties
		"""
		newProperties = Properties()
		
		for i in range(len(predefinedCategories)):
			newProperties.newCategory(predefinedCategories[i])
			if predefinedCategories[i] == "Base":
				newProperties.addProperty("Base", "ID", 0, int, True)
				newProperties.addProperty("Base", "Name", "default", str)
				newProperties.addProperty("Base", "Type", "Push Button", str, True)
				newProperties.addProperty("Base", "Annotation", "Add a comment here...", str)
			elif predefinedCategories[i] == "Visual":
				newProperties.addProperty("Visual", "X", 0, int, True)
				newProperties.addProperty("Visual", "Y", 0, int, True)
				newProperties.addProperty("Visual", "Width", 100, int, True)
				newProperties.addProperty("Visual", "Height", 100, int, True)
				#newProperties.addProperty("Visual", "Has Moved", False, bool, True)
			elif predefinedCategories[i] == "GUI Component":
				newProperties.addProperty("GUI Component", "Title", "default", str, True)
				newProperties.addProperty("GUI Component", "Parent Title", "default", str, True)
				newProperties.addProperty("GUI Component", "Class Name", "default", str, True)
				newProperties.addProperty("GUI Component", "Is Dialog", True, bool, True)
			elif predefinedCategories[i] == "Visibility Behavior":
				newProperties.addProperty("Visibility Behavior", "Reaction Type", None, Enum)
				newProperties.addProperty("Visibility Behavior", "Source ID", 1, int, True)
				newProperties.addProperty("Visibility Behavior", "Destination ID", 1, int, True)
				newProperties.addProperty("Visibility Behavior", "Trigger Action", "None", str)
			elif predefinedCategories[i] == "Action":
				pass
			elif predefinedCategories[i] == "Port":
				pass
			elif predefinedCategories[i] == "Wire":
				pass
		
		for category in customCategories.keys():
			newProperties.newCategory(category)
			properties = customCategories[category]
			for property in properties:
				name = property["name"]
				type = property["type"]
				default = property["default"]
				readOnly = property["readOnly"]
				newProperties.addProperty(category, name, default, type, readOnly)
		
		return newProperties
	
	def getModel(self) -> 'PropModel':
		"""
		Gets a new PropModel object for this properties object.

		:return: Model of properties object.
		:rtype: PropModel
		"""

		try: # FACILE
			return PropModel(self)
		except: # API
			return None
	
	def getNumCategories(self) -> int:
		"""
		Gets the Number of Categories of the properties object.

		:return: Number of categories.
		:rtype: int
		"""
		return len(self._categories)
	
	def getCategories(self) -> list:
		"""
		Gets the categories from the list of categories.

		:return: The categories from the list.
		:rtype: list
		"""
		return list(self._categories.keys())
	
	def getCategoryProperties(self, category: str) -> list:
		"""
		Gets the properties from the category.

		:param category: Category from list of categories.
		:type category: str
		:return: The properties from that category.
		:rtype: list
		"""
		return self._categories[category]
	
	def getPropertyCategory(self, property: 'Property') -> str:
		"""
		Gets the category of that property.

		:param property: Property of a particular category.
		:type property: Property
		:return: The category of a particular property.
		:rtype: str
		"""
		for category in self.getCategories():
			props = self.getCategoryProperties(category)
			if property in props:
				return category
	
	def getCategoryIndex(self, category: str) -> int:
		"""
		Gets the index of a category.

		:param category: Category from list of categories.
		:type category: str
		:return: Index of the category.
		:rtype: int
		"""
		categories = self.getCategories()
		return categories.index(category)
	
	def getNumPropertiesInCategory(self, category: str) -> int:
		"""
		Gets the number of properties within a category.

		:param category: Category from list of categories.
		:type category: str
		:return: Number of properties within a category.
		:rtype: int
		"""
		properties = self.getCategoryProperties(category)
		return len(properties)
	
	def getProperty(self, name: str) -> tuple:
		"""
		Gets a property by name if it exists in the properties object
		
		:param name: the name of the property to get
		:return: (A tuple containing the category name that the property is under and the property object) or None
		:rtype: tuple[str, Property] or NoneType
		"""
		for category in self._categories:
			for property in self._categories[category]:
				if property.getName() == name:
					return category, property
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the visibility behavior.

		.. note::
			This is not just a getter of the __dict__ attribute.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		d = {}
		for cat, props in self._categories.items():
			d[cat] = [prop.asDict() for prop in props]
		return d
	
	@staticmethod
	def fromDict(d: dict) -> 'Properties':
		"""
		Creates a Properties object from a dictionary.

		:param d: The dictionary that represents the Properties object.
		:type d: dict
		:return: The Properties object that was constructed from the dictionary
		:rtype: Properties
		"""
		
		if d is None:
			return None
		
		props = Properties()
		
		for cat in d:
			props.newCategory(cat)
			for prop in d[cat]:
				props._categories[cat].append(Property.fromDict(prop))
		
		return props
