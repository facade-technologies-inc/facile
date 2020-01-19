:orphan:

:mod:`visibilitybehavior`
=========================

.. py:module:: visibilitybehavior

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

   This module contains the VisibilityBehavior class.



Module Contents
---------------


.. py:class:: VisibilityBehavior(tguim: TargetGuiModel, srcComp: Component = None, destComp: Component = None, reactionType: ReactionType = ReactionType.Show)

   ..
      Bases: :class:`data.entity.Entity`

   Inheritance Hierarchy:

   .. inheritance-diagram:: visibilitybehavior.VisibilityBehavior

   This class describes a visibility behavior in the target gui - how a component becomes visible
    or invisible to the user. E.g. clicking a button (the "from" component) causes a window (the "to" component)
    to be shown.

   Constructs a VisibilityBehavior object.

   :param tguim: The one and only target GUI model
   :type tguim: TargetGuiModel
   :param srcComp: The "source" component. The one triggering the vis behavior.
   :type srcComp: Component
   :param destComp: The "destination" component. The one whose visibility is affected by the vis behavior.
   :type destComp: Component
   :param reactionType: Show or Hide
   :type reactionType: ReactionType
   :return: A constructed VisibilityBehavior
   :rtype: VisibilityBehavior

   .. py:class:: ReactionType

      ..
         Bases: :class:`enum.Enum`

      .. attribute:: Show
         

         

      .. attribute:: Hide
         

         


   .. method:: createGraphics(self)


      Creates the graphics for the visibility component.

      :return: None
      :rtype: NoneType


   .. method:: getDestComponent(self)


      Gets the "Destination" component of the visibility behavior - the component whose visibility is affected.

      :return: The "Destination" component of the visibility behavior.
      :rtype: Component


   .. method:: getSrcComponent(self)


      Gets the "source" component of the visibility behavior - the component that triggers the vis behavior.

      :return: The "source" component of the visibility behavior
      :rtype: Component


   .. method:: getCondition(self)


      Gets the Condition object associated with this visibility behavior.

      :return: The Condition object associated with this visibility behavior.
      :rtype: Condition


   .. method:: getReactionType(self)


      Gets the reaction type of the visibility behavior.

      :return: The reaction type of the visibility behavior.
      :rtype: ReactionType


   .. method:: getGraphicsItem(self)


      Gets the graphics item associated with the visibility behavior.

      :return: return the visibilitybehavior graphics item
      :rtype: VBGraphics


   .. method:: setDestComponent(self, destComp: Component)


      Sets the "Destination" component of the visibility behavior - the component whose visibility is affected.

      :param destComp: The desired "to/destination" component of the visibility behavior
      :type destComp: Component
      :return: None
      :rtype: NoneType


   .. method:: setSrcComponent(self, srcComp: Component)


      Sets the "from" component of the visibility behavior - the component that triggers the vis behavior.

      :param srcComp: The desired "from/source" component of the visibility behavior
      :type srcComp: Component
      :return: None
      :rtype: NoneType


   .. method:: setReactionType(self, reactType: ReactionType)


      Sets the reaction type of the visibility behavior. Input param must be in the set of valid reaction types.

      :param reactType: The reaction of the visibility behavior
      :type reactType: ReactionType
      :return:


   .. method:: asDict(self)


      Get a dictionary representation of the visibility behavior.

      .. note::
              This is not just a getter of the __dict__ attribute.

      .. todo::
              save the condition

      :return: The dictionary representation of the object.
      :rtype: dict


   .. method:: fromDict(d: dict, tguim: TargetGuiModel)
      :staticmethod:


      Creates a visibility behavior from a dictionary.

      The created visibility behavior isn't "complete" because it only holds the IDs of other
      components and visibility behaviors. Outside of this function, the references are completed.

      .. note::
              The graphics item will not be created here. It must be created later.

      :param d: The dictionary that represents the VisibilityBehavior.
      :type d: dict
      :param tguim: The target GUI model to add the component to
      :type tguim: TargetGuiModel
      :return: The VisibilityBehavior object that was constructed from the dictionary
      :rtype: VisibilityBehavior



