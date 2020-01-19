:orphan:

:mod:`componentgraphics`
========================

.. py:module:: componentgraphics

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

   This module contains the ComponentGraphics class.



Module Contents
---------------


.. py:class:: ComponentGraphics(dataComponent: Component, rect: tuple = (), parent=None)

   ..
      Bases: :class:`PySide2.QtWidgets.QGraphicsItem`

   Inheritance Hierarchy:

   .. inheritance-diagram:: componentgraphics.ComponentGraphics

   This class displays an individual GUI component in the target gui,
   based on the component class.

   Constructs a ComponentGraphics object

   :param dataComponent: get the data of a Component
   :type dataComponent: Component
   :param parent: parent ComponentGraphics
   :type parent: ComponentGraphics

   .. attribute:: MIN_WIDTH
      :annotation: = 0

      

   .. attribute:: MIN_HEIGHT
      :annotation: = 0

      

   .. attribute:: MAX_MARGIN
      :annotation: = 30

      

   .. attribute:: MIN_MARGIN
      :annotation: = 10

      

   .. attribute:: MARGIN_PROP
      :annotation: = 0.05

      

   .. attribute:: PEN_WIDTH
      :annotation: = 1.0

      

   .. attribute:: TITLEBAR_H
      :annotation: = 40

      

   .. attribute:: TRIM
      :annotation: = 1

      

   .. method:: getNumMoves(self)


      Gets the number of times a component has moved

      :return: The number of times the component graphics have been moved.
      :rtype: int


   .. method:: getNumberOfTokens(self)


      Get the number of tokens.

      :return: the number of tokens
      :rtype: int


   .. method:: adjustPositioning(self)


      Places component using the following criteria:
              1. Place the component where it actually is in the GUI.
              2. If there is a collision with a sibling, the one that is on the bottom and/or right has to move.
              3. Once all sibling collisions are resolved, the parent may need to expand to fit all children inside.
              4. Once the parent is expanded, start at step 2 again, but his time with the parent.

      ..note::
              This is a recursive algorithm.

      :return: None
      :rtype: NoneType


   .. method:: checkForCollisions(self, siblings: list)


      Function that checks for collisions with self

      :param siblings: list of all components that are at the same level as self
      :type siblings: list[ComponentGraphics]
      :return: None


   .. method:: expandParent(self, parent: ComponentGraphics, siblings: list)


      This function expands the parent and is somewhat recursive, just for adaptability.

      :param siblings: list of all of self's siblings
      :type siblings: list[ComponentGraphics]
      :param parent: the parent component of self
      :type parent: ComponentGraphics or scene
      :return: None
      :rtype: NoneType


   .. method:: getX(self)


      Gets the original x value

      :return: The original x value of the component
      :rtype: int


   .. method:: getY(self)


      :return: the original y value of the component
      :rtype: int


   .. method:: resolveCollisions(self, collidingSiblings: list)


      This function will resolve collisions of a component with its siblings.

      :param collidingSiblings: siblings colliding with this component
      :type collidingSiblings: list
      :return: None
      :rtype: NoneType


   .. method:: getMargin(self)


      Returns the margin of this component

      :return: The margin around the component
      :rtype: float


   .. method:: itemChange(self, change: GraphicsItemChange, value)


      Overrides the default itemChange function by adding one extra conditional, otherwise normal behavior of the
      function is returned. This function is what prevents top-level components from colliding

      :param change: the type of state change
      :type change: GraphicsItemChange
      :param value: information about the change
      :return: None or Unknown (typeof(value))
      :rtype: NoneType


   .. method:: getCollidingComponents(self, components: list)


      Gets all of the components from a list that collide with this component.

      :param components: The components to detect collisions with
      :type components: list[ComponentGraphics]
      :return: All of the components that actually collide with this component
      :rtype: list[ComponentGraphics]


   .. method:: getLabel(self)


      Gets the label from this component.
      :return: The label for this component.
      :rtype: str


   .. method:: overlapsWith(self, sibling: ComponentGraphics)


      Determines if this ComponentGraphics is overlapping with another one.

      Components that share an edge are not necessarily considered to be overlapping.
      This method differs from collidesWithItem because of this.

      :param sibling: The other component to check collision with.
      :type sibling: ComponentGraphics
      :return: True if components overlap, False otherwise.
      :rtype: bool


   .. method:: contains(self, child: ComponentGraphics)


      Determines if one ComponentGraphics item completely contains another one visually.
      rectangles that match exactly are considered to be "containing" each other.

      This method is mostly used to determine if a parent component needs to be "grown" to fit its children
      inside.

      :param child: The component that we would like to determine if it's in the current component.
      :type child: ComponentGraphics
      :return: True if child is visually in the current component
      :rtype: bool


   .. method:: boundingRect(self, withMargins: bool = False)


      This pure virtual function defines the outer bounds of the item as a rectangle.
      :return: create the bounding of the item
      :rtype: QRectF


   .. method:: shape(self)


      Returns the shape of this item as a QPainterPath in local coordinates.
      The shape could be used for many things, like collision detection.

      :return: Returns the shape of this item as a QPainterPath in local coordinates.
      :rtype: QPainterPath


   .. method:: paint(self, painter, option, widget)


      Paints the contents of the component. Override the parent paint function

      :param painter: Use a Qpainter object.
      :type painter: QPainter
      :param option: It provides style options for the item.
      :type option: QStyleOptionGraphicsItem
      :param widget: QWidget
      :type widget: It points to the widget that is being painted on; or make it = None.
      :return: None
      :rtype: NoneType


   .. method:: mousePressEvent(self, event)


      This event handler is implemented to receive mouse press events for this item.

      :param event: a mouse press event
      :type event: QGraphicsSceneMouseEvent
      :return: None
      :rtype: NoneType


   .. method:: contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent)


      Opens a context menu (right click menu) for the component.

      :param event: The event that was generated when the user right-clicked on this item.
      :type event: QGraphicsSceneContextMenuEvent
      :return: None
      :rtype: NoneType


   .. method:: triggerSceneUpdate(self)


      Update the scene.


   .. method:: __repr__(self)


      Returns the componentView id as a string.

      :return: the componentView id as a string.
      :rtype: str



