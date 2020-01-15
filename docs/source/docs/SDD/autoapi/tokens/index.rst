:orphan:

:mod:`tokens`
=============

.. py:module:: tokens

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

   This file contains the token class that weighs the importance of each attribute of a single token. 



Module Contents
---------------


.. py:class:: Token(appTimeStamp: int, identifier: int, isDialog: bool, isEnabled: bool, isVisible: bool, processID: int, typeOf: str, rectangle: RECT, texts: list, title: str, numControls: int, controlIDs: list, parentTitle: str, parentType: str, topLevelParentTitle: str, topLevelParentType: str, childrenTexts: list, picture: Image = None, autoID: int = None, expandState: int = None, shownState: int = None)

   Token class sets parameters of a token for each state that changes.

   Checks if the tokens component state changed based on a random variable.

   :param appTimeStamp: The time that the application was started at.
   :type appTimeStamp: int
   :param identifier: stores the unique id number of the component
   :type identifier: int
   :param isDialog: stores if the component is a dialog
   :type isDialog: bool
   :param isEnabled: stores if the component is enabled
   :type isEnabled: bool
   :param isVisible: stores if the component is visible
   :type isVisible: bool
   :param parentTitle: stores the components parents title
   :type parentTitle: str
   :param parentType: stores the components parents type
   :type parentType: str
   :param topLevelParentTitle: stores the components top level parents title
   :type topLevelParentTitle: str
   :param topLevelParentType: stores the components top level parents type
   :type topLevelParentType: str
   :param processID: stores the processing id of the component
   :type processID: int
   :param rectangle: stores the position of the component
   :type rectangle: win32structures.RECT
   :param texts: stores the text in the component
   :type texts: list[str]
   :param title: stores the title of the component
   :type title: str
   :param numControls: stores the number of controls of the component
   :type numControls: int
   :param picture: stores the image of the component
   :type picture: PIL.Image
   :param typeOf: stores the characteristics of the component
   :type typeOf: str
   :param controlIDs: stores the control identifiers. The four possible controls are title, typeOf, title + typeOf, and the closest text
   :type controlIDs: str
   :param autoID: stores the unique identifier of the component
   :type autoID: str
   :param childrenTexts: stores the text contained in the children of the component
   :type childrenTexts: list[str]
   :param expandState: stores if the components state is expanded
   :type expandState: int
   :param shownState: stores the state in which the component is in
   :type shownState: int

   :return: None
   :rtype: NoneType

   .. py:class:: Match

      ..
         Bases: :class:`enum.Enum`

      .. attribute:: EXACT
         :annotation: = 1

         

      .. attribute:: CLOSE
         :annotation: = 2

         

      .. attribute:: NO
         :annotation: = 3

         


   .. attribute:: Weight
      

      

   .. attribute:: MAX_WEIGHTS
      

      

   .. attribute:: THRESH_PERCENT
      :annotation: = 50

      

   .. method:: isEqualTo(self, token2: Token)


      The isEqualTo function gives a weight of importance to each attribute.
      This is based on the tokens when its state is changed.

      :param token2: returns how similar of a match the given token is to the current token
      :type token2: Token
      :return: None
      :rtype: NoneType


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


      Creates a token from a dictionary.

      :param d: The dictionary that represents the Component.
      :type d: dict
      :return: The Token object that was constructed from the dictionary
      :rtype: Token



