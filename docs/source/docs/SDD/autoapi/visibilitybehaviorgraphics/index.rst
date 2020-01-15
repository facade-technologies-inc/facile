:orphan:

:mod:`visibilitybehaviorgraphics`
=================================

.. py:module:: visibilitybehaviorgraphics

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

   This module contains the VBGraphics class.



Module Contents
---------------


.. py:class:: VBGraphics(dataVisibilityBehavior: VisibilityBehavior, parent: TScene)

   ..
      Bases: :class:`PySide2.QtWidgets.QGraphicsItem`

   Inheritance Hierarchy:

   .. inheritance-diagram:: visibilitybehaviorgraphics.VBGraphics

   Construct the VBGraphics class.
   'src' means the source component, the one triggering the vb.
   'dest' means the destination component, the one receiving and affected by the vb.

   :param dataVisibilityBehavior: get the data of a VisibilityBehavior
   :type dataVisibilityBehavior: VisibilityBehavior
   :param parent: The parent of the visibility behavior (This will always be the scene)
   :type parent: TScene
   :return: None
   :rtype: NoneType

   .. method:: boundingRect(self)


      This pure virtual function defines the outer bounds of the item as a rectangle.

      :return: create the bounding of the item
      :rtype: QRectF


   .. method:: paint(self, painter: QPainter, option, widget)


      Paints the contents of the visibilitybehavior. Override the parent paint function

      :param painter: Use a Qpainter object.
      :type painter: QPainter
      :param option: It provides style options for the item.
      :type option: QStyleOptionGraphicsItem
      :param widget: QWidget
      :type widget: It points to the widget that is being painted on; or make it = None.
      :return: None
      :rtype: NoneType


   .. method:: buildPath(self, x1, x2, y1, y2)


      This function is used to build the path for the visibility behavior.
      It has some basic arrow routing algorithm:

      1. src is at right, dest is at left, just cubic to it
      #. src is at left, dest is at right

              a. y is almost the same, cubic to it
              #. distance is bigger than 1/3 * root.width, go around the root component
              
                              i. src is higher than dest, go around from the top
                              #. bb src is lower than dest, go around from the bottom
                              
              #. horizontal distance is smaller than 1/3 * root.width, zigzag to it
              
      .. todo::
              Improve on the algorithm (add collision detector)

      :param x1: the x coordinate for the src component
      :type x1: float
      :param x2: the x coordinate for the dest component
      :type x2: float
      :param y1: the y coordinate for the src component
      :type y1: float
      :param y2: the x coordinate for the dest component
      :type y2: float
      :return path: return the path of the visibility behavior
      :rtype path: QPainterPath


   .. method:: getOneComponentDownRoot(self)


      This function is used to locate the base component of the program.

      :return: the component with id = 2; the base component for the program; the component that is one step down of the root component
      :rtype: Component



