:orphan:

:mod:`component`
================

.. py:module:: component

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

   This module contains the Component class.



Module Contents
---------------


.. py:class:: Component(tguim: TargetGuiModel, parent: Component = None, superToken: SuperToken = None, createGraphics: ComponentGraphics = True)

   ..
      Bases: :class:`data.entity.Entity`

   Inheritance Hierarchy:

   .. inheritance-diagram:: component.Component

   This class models an individual GUI component in the target gui.
   Components are organized in a tree in the TargetGuiModel class.

   Constructs a Component object.

   :param tguim: The TargetGuiModel that the component belongs to.
   :type tguim: TargetGuiModel
   :param parent: The parent component in the component tree.
   :type parent: Component
   :param superToken: The SuperToken associated with the new Component
   :type superToken: SuperToken
   :param createGraphics: if True, graphics will be created. If not, they won't
   :type createGraphics: bool

   .. method:: createGraphics(self)


      Create the graphics for the component

      :return: None
      :rtype: NoneType


   .. method:: getSuperToken(self)


      Gets the component's SuperToken

      :return: The component's SuperToken
      :rtype: SuperToken


   .. method:: getSrcVisibilityBehaviors(self)


      Gets all the visibility behaviors coming out from this component

      :return: The list of all the visibility behaviors coming out from this component
      :rtype: List of VisibilityBehavior


   .. method:: getDestVisibilityBehaviors(self)


      Gets all the visibility behaviors coming into this component

      :return: The list of all the visibility behaviors coming into this component
      :rtype: List of VisibilityBehavior


   .. method:: getModel(self)


      Gets the target GUI model that this component belongs to.

      :return: the target GUI model that this component belongs to.
      :rtype: TargetGuiModel


   .. method:: getChildren(self)


      Gets a list of the component's children components.

      :return: A list of the component's children components.
      :rtype: list


   .. method:: getSiblings(self)


      Gets a list of the component's sibling components, including itself.

      :return: A list of the component's sibling components, including itself.
      :rtype: list


   .. method:: childCount(self)


      Gets the number of child components the component has.

      :return: The number of child components the component has.
      :rtype: int


   .. method:: getParent(self)


      Gets the component's parent component.

      :return: The component's parent component.
      :rtype: Component


   .. method:: getParentGraphicsItem(self)


      Gets the parent component's graphics item if it exists.

      :return: The parent component's graphics item or None
      :rtype: ComponentGraphics or None


   .. method:: getPathFromRoot(self)


      Gets the path in the tree to the component from the root.
      The path is a list of 2-element tuples where the first element is a component,
      and the second element is the position of that component amongst its siblings.

      :return: The path to the component from the root.
      :rtype: list


   .. method:: getGraphicsItem(self)


      Gets the associated graphics item used to display the component.

      :return: The graphics item used to display the component.
      :rtype: ComponentGraphics


   .. method:: getNthChild(self, n: int)


      Gets the Nth child component of the component.

      :param n: The nth index into the component's list of children
      :type n: int
      :return: The nth child of the component. None if index out of range
      :rtype: Component


   .. method:: getNumDescendants(self)


      Gets the number of components descended from this component in the tree.

      :return: The number of descendant components.
      :rtype: int


   .. method:: getMaxDepth(self, curDepth: int = 1)


      Gets How many levels deep the tree goes below the component.

      :param curDepth: The level in the tree the component is at. (Root=1)
      :type: curDepth: int
      :return: How many levels deep the tree goes below the component.
      :rtype: int


   .. method:: getPositionInSiblings(self)


      Gets the index of itself in its parent's children list.

      :return: the index of itself in its parent's children list.
      :rtype: int


   .. method:: addChild(self, child, pos=0)


      Adds a given component to the list of children components.

      :param child: A component object to be added to the children list.
      :type child: Component
      :param pos: Optionally position the child in children list. default=0
      :type pos: int
      :return: None
      :rtype: NoneType


   .. method:: remove(self)



   .. method:: addDestVisibilityBehavior(self, newVisBehavior: VisibilityBehavior)


      Adds a given visibility behavior (VB) to the list of "Destination" visibility behaviors.
      This component is the destination for the VB.

      :param newVisBehavior: The VisibilityBehavior that affects the visibility of this component.
      :type newVisBehavior: VisibilityBehavior
      :return: None
      :rtype: NoneType


   .. method:: removeDestVisibilityBehavior(self, visBehavior: VisibilityBehavior)


      Removes a given visibility behavior (VB) from the list of "Destination" visibility behaviors.
      This component is the destination for the VB.

      :param visBehavior: The VisibilityBehavior that affects the visibility of this component.
      :type visBehavior: VisibilityBehavior
      :return: None
      :rtype: NoneType


   .. method:: addSrcVisibilityBehavior(self, newVisBehavior: VisibilityBehavior)


      Adds a given visibility behavior (VB) to the list of "Source" visibility behaviors.
      "Source" VBs are VBs coming out from this component.

      :param newVisBehavior: The VisibilityBehavior that is triggered by ('coming out from') this component.
      :type newVisBehavior: VisibilityBehavior
      :return: None
      :rtype: NoneType


   .. method:: removeSrcVisibilityBehavior(self, visBehavior: VisibilityBehavior)


      removes a given visibility behavior (VB) from the list of "Source" visibility behaviors.
      "Source" VBs are VBs coming out from this component.

      :param visBehavior: The VisibilityBehavior that is triggered by ('coming out from') this component.
      :type visBehavior: VisibilityBehavior
      :return: None
      :rtype: NoneType


   .. method:: __repr__(self)


      Returns the component's id as a string.

      :return: The component's id as a string.
      :rtype: str


   .. method:: asDict(self)


      Get a dictionary representation of the component.

      NOTE: this is not just a getter of the __dict__ attribute.

      :return: The dictionary representation of the object.
      :rtype: dict


   .. method:: fromDict(d: dict, tguim: TargetGuiModel)
      :staticmethod:


      Creates a Component from a dictionary.

      The created component isn't "complete" because it only holds the IDs of other components
      and visibility behaviors. Outside of this function, the references are completed. The
      children references are not set here because they need to be set one at a time while the
      graphics items are being created.

      :param d: The dictionary that represents the Component.
      :type d: dict
      :param tguim: The target GUI model to add the component to
      :type tguim: TargetGuiModel
      :return: The Component object that was constructed from the dictionary
      :rtype: Component



