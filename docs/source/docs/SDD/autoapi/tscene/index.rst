:orphan:

:mod:`tscene`
=============

.. py:module:: tscene

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

   This module contains the TScene class.



Module Contents
---------------


.. py:class:: TScene(targetGUIModel: TargetGuiModel)

   Bases: :class:`PySide2.QtWidgets.QGraphicsScene`
   .. inheritance-diagram:: tscene.TScene

   Construct the TScene class

   :param targetGUIModel: get the TargetGuiModel of the project
   :type targetGUIModel: TargetGuiModel

   .. attribute:: itemSelected
      

      

   .. attribute:: itemBlink
      

      

   .. method:: getTargetGUIModel(self)


      Gets the target GUI Model.

      :return The target GUI model
      :rtype data.tguim.targetguimodel.TargetGuiModel


   .. method:: emitItemSelected(self, id: int)


      Emits a signal that carries the ID of the item that was selected

      :param id: The ID of the item that was selected.
      :type id: int
      :return: None
      :rtype: NoneType


   .. method:: blinkComponent(self, id: int)


      emits the itemBlink signal which means that an item should be shown in the
      target GUI.

      :param id: The ID of the component that should be blinked.
      :type id: int
      :return: None
      :rtype: NoneType



