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

This module contains the Properties() class.
"""

from collections import OrderedDict
from propeditormodel import PropModel
from property import Property


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
        self._model = PropModel(self)


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
                    readOnly: object = False) -> None:
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
        :type readOnly: object
        :return: None
        :rtype: NoneType
        """
        if category not in self._categories.keys():
            raise Exception("{} does not exist".format(category))
        self._categories[category].append(Property(name, value, type, readOnly))

    @staticmethod
    def createPropertiesObject(predefinedCategories: list, customCategories: list) -> 'Properties':
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
                newProperties.addProperty("Base", "Name", "default", str)
                newProperties.addProperty("Base", "Type", "Push Button", str)
                newProperties.addProperty("Base", "Annotation", "", str)
                newProperties.addProperty("Base", "Read-Only", "", bool)
                newProperties.addProperty("Base", "Size", 3.45, float)
            elif predefinedCategories[i] == "Visual":
                newProperties.addProperty("Visual", "BoxColor", "black", str)
                newProperties.addProperty("Visual", "TextColor", "black", str)
                newProperties.addProperty("Visual", "BorderWidth", 1, int)
                newProperties.addProperty("Visual", "X", 0, int)
                newProperties.addProperty("Visual", "Y", 0, int)
                newProperties.addProperty("Visual", "Width", 100, int)
                newProperties.addProperty("Visual", "Height", 100, int)
            elif predefinedCategories[i] == "GUI Component":
                newProperties.addProperty("GUI Component", "Parent", 1, int, True)
                newProperties.addProperty("GUI Component", "Children", [], list, True)
            elif predefinedCategories[i] == "Visibility Behaviors":
                newProperties.addProperty("Visibility Behavior", "From", 1, int, True)
                newProperties.addProperty("Visibility Behavior", "To", 1, int, True)

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

    def getModel(self) -> PropModel:
        """
        Gets the properties's objects model.

        :return: Model of properties object.
        :rtype: QObject
        """
        return self._model

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

    def getPropertyCategory(self, property: 'property') -> str:
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
        :type category: object
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
