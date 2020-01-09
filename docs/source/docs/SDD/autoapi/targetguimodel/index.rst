:orphan:

:mod:`targetguimodel`
=====================

.. py:module:: targetguimodel

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

   This module contains the TargetGuiModel class.



Module Contents
---------------


.. py:class:: TargetGuiModel

   Bases: :class:`PySide2.QtCore.QObject`
   .. inheritance-diagram:: targetguimodel.TargetGuiModel

   This class models the structure and behavior of the target gui.
   It contains Components organized in a tree structure, and stores the VisibilityBehaviors.
   New components are constructed and added to the tree when it receives new SuperTokens from
   the Observer.

   Constructs a TargetGuiModel object.

   :return: The constructed TargetGuiModel object
   :rtype: TargetGuiModel

   .. attribute:: dataChanged
      

      

   .. method:: getRoot(self)


      Gets the root component of the component tree.

      :return: The root component of the component tree.
      :rtype: Component


   .. method:: getScene(self)


      Gets the associated graphics scene

      :return: The GraphicsScene associated with the TargetGuiModel
      :rtype: TScene


   .. method:: getComponents(self)


      Gets the dictionary of components.

      :return: The dictionary of components.
      :rtype: dict


   .. method:: getComponent(self, iD: int)


      Gets the component with the specified id.

      :param iD: The component's unique identifier. See Entity class.
      :type iD: int
      :return: Component with the given id
      :rtype: Component


   .. method:: createComponent(self, newSuperToken: SuperToken, parentToken: SuperToken)


      The slot function which is called when the Observer emits the "newSuperToken" signal.
      Creates a new component using info from the SuperToken and adds it to the component tree.

      :param newSuperToken: The SuperToken associated with the component in the target GUI.
      :type newSuperToken: SuperToken
      :param parentToken: The parent SuperToken of the new SuperToken
      :type parentToken: SuperToken
      :return: The component that was created
      :rtype: 'Component'


   .. method:: getVisibilityBehaviors(self)


      Gets the dictionary of VisibilityBehaviors.

      :return: The dictionary of VisibilityBehaviors.
      :rtype: dict


   .. method:: getNthVisibilityBehavior(self, n: int)


      Gets the visibility behavior at a specific position.
      :param n: the index of the visiblity behavior to get
      :type n: int
      :return: The visiblity behavior at index n
      :rtype: VisiblityBehavior


   .. method:: getVisibilityBehavior(self, iD: int)


      Gets the VisibilityBehavior with the specified id.

      :param iD: The id of the desired VisibilityBehavior
      :type iD: int
      :return: The VisibilityBehavior with the specified id.
      :rtype: VisibilityBehavior


   .. method:: addVisibilityBehavior(self, newVisBehavior: VisibilityBehavior)


      Adds a given VisibilityBehavior to the dictionary of VisibilityBehaviors.

      :param newVisBehavior: The VisibilityBehavior object to be added.
      :type newVisBehavior: VisibilityBehavior
      :return: None
      :rtype: NoneType


   .. method:: asDict(self)


      Get a dictionary representation of the visibility behavior.

      .. note::
              This is not just a getter of the __dict__ attribute.

      :return: The dictionary representation of the object.
      :rtype: dict


   .. method:: fromDict(d: dict)
      :staticmethod:


      Creates a target GUI model from a dictionary.

      This method reconstructs the entire target GUI model in 2 "passes". First, all of the
      components and visibility behaviors are created, but they only store IDs of other
      components and visibility behaviors. Once all of the objects have been created,
      the references are finalized. Children of components are not stored until the 2nd pass

      :param d: The dictionary that represents the target GUI model.
      :type d: dict
      :return: The TargetGUIModel object that was constructed from the dictionary
      :rtype: TargetGuiModel



