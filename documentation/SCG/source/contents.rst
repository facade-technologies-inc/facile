----------
Change Log
----------

+-------------------------+-----------------+------------------+------------------+-------------+
| Document                | Release Version | Internal Version | Last Update Date | Approved By |
+=========================+=================+==================+==================+=============+
| Security Classification | A               | 1                | |today|          | Nikhith     |
| Guide                   |                 |                  |                  | Vankireddy  |
+-------------------------+-----------------+------------------+------------------+-------------+

+---------+---------+------+-------------+-----------+--------+---------+----------+------+
| Change  | Section | Page | Change      | Rationale | Change | Changed | Approved | Date |
| Log no. | no.     | no.  | Description |           | Class  | by      | by       |      |
+=========+=========+======+=============+===========+========+=========+==========+======+
|         |         |      |             |           |        |         |          |      |
+---------+---------+------+-------------+-----------+--------+---------+----------+------+


------------
Introduction
------------

This security classification guide is very important. It says what may be talked about and at
what level and with what restrictions.

As the project progresses, these classifications may change, so it's very important to read each
revision of this document thoroughly.

-------------
Trade Secrets
-------------

Do not speak of, show, or release this information in any manner without prior written consent
from an officer of Facade Technologies Inc. No promise of allowance for dissemination of any of
this information is given and restrictions will be determined on an as-needed basis.

1. Pictures of the Facile Software
#. Source code
#. Facile's architecture and inner workings
#. Limitations of Facile
#. GUI Libraries that we're using (pywinauto and pyautogui)
#. Current progress

-----------
Proprietary
-----------

This information may be talked about, but stay high level and mark as proprietary on any
documents. If any of this content is placed on a document, the document must be marked
conspicuously with the following text:

**Duplication and dissemination of these documents is prohibited without the prior written
consent of Facade Technologies Inc.**

1. The goal of the project: Generate custom APIs to control existing graphical user interfaces
#. Uses of a custom API
#. Advantages of Facile over existing solutions
#. The high level workings of Facile:

    - Build model of target GUI
    - Build model of API
    - Generate Python API

----
Open
----

1. The GUI framework that we're using - Qt for Python.
#. The programming language that we're using - Python.
#. Version control tools that we're using - Git/GitHub/TortoiseGit.
#. Team communication platform that we're using - Slack.
#. Jira
#. Agile methodology
#. When the project will be completed by (May 4th, 2020)

.. note::
    In the case that a piece of information falls under multiple categories, the tighter
    restrictions apply.