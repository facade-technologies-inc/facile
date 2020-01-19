:orphan:

:mod:`properties`
=================

.. py:module:: properties

.. autoapi-nested-parse::

   ..
       /------------------------------------------------------------------------------    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
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



Module Contents
---------------


.. py:class:: Properties

   This class allows to create data of our properties.

   Constructs a Properties objects.

   :return: An ordered dictionary of properties.
   :rtype: Properties

   .. method:: newCategory(self, category: str)


      Adds a new category to the dict of categories.

      :param category: The category that will be added to the dict.
      :type category: str
      :return: None
      :rtype: NoneType


   .. method:: addProperty(self, category: str, name: str, value: object, type: object, readOnly: bool = False)


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


   .. method:: createPropertiesObject(predefinedCategories: list, customCategories: dict)
      :staticmethod:


      Property Factory, that is a static method, that createes properties objects for predefined and custom categories.

      :param predefinedCategories: Category that was already defined from a list.
      :type predefinedCategories: list
      :param customCategories: Categories that can be made from a list.
      :type customCategories: dict
      :return: Properties objects.
      :rtype: Properties


   .. method:: getModel(self)


      Gets the properties's objects model.

      :return: Model of properties object.
      :rtype: PropModel


   .. method:: getNumCategories(self)


      Gets the Number of Categories of the properties object.

      :return: Number of categories.
      :rtype: int


   .. method:: getCategories(self)


      Gets the categories from the list of categories.

      :return: The categories from the list.
      :rtype: list


   .. method:: getCategoryProperties(self, category: str)


      Gets the properties from the category.

      :param category: Category from list of categories.
      :type category: str
      :return: The properties from that category.
      :rtype: list


   .. method:: getPropertyCategory(self, property: Property)


      Gets the category of that property.

      :param property: Property of a particular category.
      :type property: Property
      :return: The category of a particular property.
      :rtype: str


   .. method:: getCategoryIndex(self, category: str)


      Gets the index of a category.

      :param category: Category from list of categories.
      :type category: str
      :return: Index of the category.
      :rtype: int


   .. method:: getNumPropertiesInCategory(self, category: str)


      Gets the number of properties within a category.

      :param category: Category from list of categories.
      :type category: str
      :return: Number of properties within a category.
      :rtype: int


   .. method:: getProperty(self, name: str)


      Gets a property by name if it exists in the properties object

      :param name: the name of the property to get
      :return: (A tuple containing the category name that the property is under and the property object) or None
      :rtype: tuple[str, Property] or NoneType


   .. method:: asDict(self)


      Get a dictionary representation of the visibility behavior.

      .. note::
              This is not just a getter of the __dict__ attribute.

      :return: The dictionary representation of the object.
      :rtype: dict


   .. method:: fromDict(d: dict)
      :staticmethod:


      Creates a Properties object from a dictionary.

      :param d: The dictionary that represents the Properties object.
      :type d: dict
      :return: The Properties object that was constructed from the dictionary
      :rtype: Properties



