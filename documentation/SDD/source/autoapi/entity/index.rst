:orphan:

:mod:`entity`
=============

.. py:module:: entity

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

   This module contains the Entity class.



Module Contents
---------------


.. py:class:: Entity

   This class is the abstract super class for the Component and VisibilityBehavior classes.
   It defines a unique id for entities that are created, and has a properties object.

   Constructs an Entity object.  Note: This is an abstract class, so this constructor is used
   only by the constructors of Entity's sub-classes.

   :return: The constructed Entity
   :rtype: Entity

   .. attribute:: count
      :annotation: :int = 0

      

   .. method:: getId(self)


      Gets the unique id for the entity.

      :return: The id for entity.
      :rtype: int


   .. method:: getProperties(self)


      Gets the entity's Properties object.

      :return: The entity's Properties object.
      :rtype: Properties


   .. method:: setProperties(self, propertiesObj: Properties)


      Sets the Properties object for the entity.

      :param propertiesObj: The properties object to be associated with the entity.
      :type propertiesObj: Properties
      :return: None
      :rtype: NoneType



