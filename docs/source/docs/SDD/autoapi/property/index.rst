:orphan:

:mod:`property`
===============

.. py:module:: property

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

   The module contains the Property() class.



Module Contents
---------------


.. py:class:: Property(name: str, value: object, type: object, readOnly: bool = False)

   This class allows us to establish the data of our properties.

   Constructs a Property Object

   :param name: The name of the property.
   :type name: str
   :param value: The value of the property.
   :type value: object
   :param type: The type of the property.
   :type type: object
   :param readOnly: The type of data structure.
   :type readOnly: bool
   :return: The constructed property.
   :rtype: Property

   .. method:: isReadOnly(self)


      Shows the property's data structure.

      :return: The property's data structure.
      :rtype: bool


   .. method:: getName(self)


      Gets the property's name.

      :return: The property's name.
      :rtype: str


   .. method:: getValue(self)


      Gets the property's value.

      :return: The property's value.
      :rtype: object


   .. method:: getType(self)


      Gets the property's type.

      :return: The property's type.
      :rtype: object


   .. method:: setValue(self, newValue: object)


      Sets the value if there is a new value.

      :param newValue: New value that needs to be set.
      :type newValue: object
      :return: The property's value.
      :rtype: bool


   .. method:: __str__(self)



   .. method:: __repr__(self)



   .. method:: asDict(self)


      Get a dictionary representation of the visibility behavior.

      .. note::
              This is not just a getter of the __dict__ attribute.

      :return: The dictionary representation of the object.
      :rtype: dict


   .. method:: fromDict(d: dict)
      :staticmethod:


      Creates a Property object from a dictionary.

      :param d: The dictionary that represents the Property object.
      :type d: dict
      :return: The Property object that was constructed from the dictionary
      :rtype: Property



