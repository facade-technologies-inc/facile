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
from qt_models.propeditormodel import PropModel
from data.property import Property

# TODO: Don't use object in type hints when there is a more specific type you could put


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

    def getCategories(self) -> object:
        """
        Gets the categories of the properties object.

        :return: The categories of the properties object.
        :rtype: object
        """
        return self._categories

    def newCategory(self, category: object) -> None:
        """
        Adds a new category to the list of categories.

        :return: None
        :rtype: NoneType
        """
        self._categories[category] = []

    def addProperty(self, category: object, name: str, value: object, type: object,
                    readOnly: object = False) -> None:
        """
        To add a property to a certain category.

        :param category: Specific category for that property.
        :type category: object
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
    def createPropertiesObject(predefinedCategories: object, customCategories: object) -> object:
        """
        Property Factory, that is a static method, that createes properties objects for predefined and custom categories.

        :param predefinedCategories: Category that was already defined.
        :type predefinedCategories: object
        :param customCategories: Categories that can be made.
        :type customCategories: object
        :return: Properties objects.
        :rtype: object
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

        # TODO: Fix this.
        for i in range(len(customCategories)):
            newProperties.newCategory(customCategories[i])
            if customCategories[i] == "Custom":
                newProperties.addProperty("Custom", "Name", "Value", "Type", str)
                newProperties.addProperty("Custom", "Name", "Value", "Type", int)
                newProperties.addProperty("Custom", "Name", "Value", "Type", float)
                newProperties.addProperty("Custom", "Name", "Value", "Type", bool)

        return newProperties

    def getModel(self) -> PropModel:
        """
        Gets the properties's objects model.

        :return: Model of properties object.
        :rtype: PropModel
        """
        return self._model

    def getNumCategories(self) -> int:
        """
        Gets the Number of Categories of the properties object.

        :return: Number of categories.
        :rtype: int
        """
        return len(self._categories)

    def getCategories(self) -> object:
        """
        Gets the categories from the list of categories.

        :return: The categories from the list.
        :rtype: object
        """
        return list(self._categories.keys())

    def getCategoryProperties(self, category: object) -> object:
        """
        Gets the properties from the category.

        :param category: Category from list of categories.
        :type category: object
        :return: The properties from that category.
        :rtype: object
        """
        return self._categories[category]

    def getPropertyCategory(self, property: object) -> object:
        """
        Gets the category of that property.

        :param property: Property of a particular category.
        :type property: object
        :return: The category of a particular property.
        :rtype: object
        """
        for category in self.getCategories():
            props = self.getCategoryProperties(category)
            if property in props:
                return category

    def getCategoryIndex(self, category:object) -> object:
        """
        Gets the index of a category.

        :param category: Category from list of categories.
        :type category: object
        :return: Index of the category.
        :rtype: object
        """
        categories = self.getCategories()
        return categories.index(category)

    def getNumPropertiesInCategory(self, category:object) -> int:
        """
        Gets the number of properties within a category.

        :param category: Category from list of categories.
        :type category: object
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
                    return tuple(category, property)
