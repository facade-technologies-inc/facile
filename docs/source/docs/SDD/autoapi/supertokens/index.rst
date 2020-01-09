:orphan:

:mod:`supertokens`
==================

.. py:module:: supertokens

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

   This file contains the super tokens class that initializes tokens as a list and a function that
   iterates through the tokens in the token list.



Module Contents
---------------


.. py:class:: SuperToken(token, parent: SuperToken)

   A super token is used to identify a component in multiple states. They can be ignored if the user
   does not care about specific components.

   Constructs a unique identifier and a way to hide certain components

   :param token: The first token to be added to the SuperToken that's being created.
   :type token: Token
   :param parent: The parent of the SuperToken being created.
   :type parent: SuperToken or NoneType
   :return: None
   :rtype: NoneType

   .. attribute:: id_counter
      :annotation: = 1

      

   .. method:: addToken(self, tokenA)


      The addToken function adds a token to the supertoken.

      :param tokenA: Returns the super token of the token to which the component belongs to
      :type tokenA: Token
      :return: None
      :rtype: SuperToken


   .. method:: getTokens(self)


      Gets a copy of the token list. It's important that this is a copy because 2 threads may access token
      data at a time.

      This function shares a common mutex with the addToken function.

      :return: list of tokens
      :rtype: list[Token]


   .. method:: shouldContain(self, token2)


      determines if this SuperToken should contain the token provided

      :param token2: The token that we would like to add to the super token
      :type token2: Token
      :return: The decision about whether it should be contained or not and the certainty
      :rtype: Token.Match, float


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


      Creates a super token from a dictionary.

      :param d: The dictionary that represents the Component.
      :type d: dict
      :return: The SuperToken object that was constructed from the dictionary
      :rtype: SuperToken



