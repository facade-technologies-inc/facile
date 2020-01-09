:orphan:

:mod:`bitness`
==============

.. py:module:: bitness

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

   This module contains functions to get the bitness of an executable file, python, and
   the system.



Module Contents
---------------


.. function:: isExecutable(filename: str) -> bool

   Determines if a file is executable or not. NOTE: Windows only

   Adapted from this source:
   http://timgolden.me.uk/python/win32_how_do_i/tell-if-a-file-is-executable.html

   :param filename: the name of the file in question.
   :return: True if file is executable. False otherwise.


.. function:: getExeBitness(exeFile: str) -> int

   NOTE: For windows only

   Solution found at
   https://stackoverflow.com/questions/1345632/determine-if-an-executable-or-library-is-32-or-64-bits-on-windows


.. function:: getPythonBitness() -> int

   Solution found at:
   https://stackoverflow.com/questions/1405913/how-do-i-determine-if-my-python-shell-is-executing-in-32bit-or-64bit-mode-on-os


.. function:: getSystemBitness() -> int

   Solution adapted from
   https://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python


.. function:: appBitnessMatches(exeFile: str) -> bool

   Returns True if the executable and the currently running version of python are teh same bitness.


