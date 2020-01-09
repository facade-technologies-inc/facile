:orphan:

:mod:`facilegraphicsview`
=========================

.. py:module:: facilegraphicsview

.. autoapi-nested-parse::

   ..
           /------------------------------------------------------------------------------ |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
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
           
   This module contains the FacileGraphicsView class which is just like a normal graphics
   view, but can be zoomed.

   TODO: make this view draggable



Module Contents
---------------


.. py:class:: FacileGraphicsView(parent: QWidget = None)

   Bases: :class:`PySide2.QtWidgets.QGraphicsView`
   .. inheritance-diagram:: facilegraphicsview.FacileGraphicsView

   This class adds functionality to the QGraphicsView to zoom in and out.

   This is primarily used as the view that shows the target GUI model and API model

   Create a GraphicsView for Facile.
   :param parent: The widget to embed the graphics view into
   :type parent: QWidget
   :return: None
   :rtype: NoneType

   .. attribute:: ZOOM_FACTOR
      :annotation: = 1.25

      

   .. method:: wheelEvent(self, event: QWheelEvent)


      Handle wheel scroll events. This will zoom in or out depending on the

      :param event: the wheel scroll event
      :type event: QWheelEvent
      :return: None
      :rtype: NoneType


   .. method:: zoomIn(self, pos: QPoint)


      Zoom in one ZOOM_FACTOR

      :param pos: The position to zoom into
      :type pos: QPoint
      :return: None
      :rtype: NoneType


   .. method:: zoomOut(self, pos: QPoint)


      Zoom out one ZOOM_FACTOR

      :param pos: The position to zoom out from
      :type pos: QPoint
      :return: None
      :rtype: NoneType



