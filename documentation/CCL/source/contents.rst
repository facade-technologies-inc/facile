------------
Introduction
------------

This document serves to record the history of changes for each document within the TDP. As the
contained documents are changed, the revisions must be approved and documented. The TDP will
remain up to date at all times by simply recompiling the documentation. This document also lays
out standards for naming and revision conventions to maintain uniformity.

==========================
Acronyms and Abbreviations
==========================

.. note::
    This section only contains acronyms and abbreviations that are relevant to the TDP wrapper
    document. All sub-documents will define their own acronyms and abbreviations.

+-------------------+----------------------------------------------------------+
| CCL               | Change Control Log                                       |
+-------------------+----------------------------------------------------------+
| ECR               | Engineering Change Request                               |
+-------------------+----------------------------------------------------------+
| API               | Application Programming Interface                        |
+-------------------+----------------------------------------------------------+
| TDP               | Technical Data Package                                   |
+-------------------+----------------------------------------------------------+

=========================
Classification of Changes
=========================

Depending on the severity of changes, they are classified as either Class I or Class II.
Published revisions must be dealt with differently depending on which class they are. Class I and
Class II changes are defined below.

Class I Change
    Affecting the system’s “form, fit, or function” such as the
    core functionality, performance or specifications like weight, interfaces or reliability. Project
    schedule, budget, and necessary resource availability are also considered class I changes.
    Increased severity requires heightened approval. In order to re-publish a document with a
    revised revision number that includes any Class I changes, an Engineering Change Request (ECR)
    must be performed. The ECR must be approved by the Team Lead, Sponsor, and Mentor before
    the revision change may be published and become part of the TDP.

Class II Change
    Least severe and refer to changes made to correct or alter
    documentation regarding typos, formatting, additional info., and things of that nature. Any
    change determined to not be a Class I change is defined as a Class II change. A document with
    Class II changes may be updated with a new revision number and published without ECR
    approval. These chases are often referred to as “redline” changes. As changes are made, the
    document revision must reflect the class type. Class I changes
    increase the revision number while Class II changes add a letter to the number, starting with A.
    Both would require a change to the date with the revised document reflecting the date it is
    published.

================
Document Summary
================

The following table gives a brief summary of all document revisions and lists the engineer
responsible for each document. For a comprehensive change log, see the next sections.

.. table:: Current Document Release Summary

    +--------+-------------------------+-----------------+------------------+-------------+
    | Doc #  | Document                | Release Version | Last Update Date | Responsible |
    |        |                         |                 |                  | Engineer    |
    +========+=========================+=================+==================+=============+
    | 1      | Technical Data Package  | A               | 01/19/2020       | Sam Badger  |
    |        |                         |                 |                  |             |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 2      | Security Classification | A               | 01/19/2020       | Sam Badger  |
    |        | Guide                   |                 |                  |             |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 3      | Concept of Operations   | B               | 01/19/2020       | Nikhith     |
    |        |                         |                 |                  | Vankireddy  |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 4      | Unsolicited Proposal    | A               | 01/19/2020       | Nikhith     |
    |        |                         |                 |                  | Vankireddy  |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 5      | System Requirements     | C               | 01/19/2020       | Nikhith     |
    |        | Document                |                 |                  | Vankireddy  |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 6      | Risk Analysis           | A               | 01/19/2020       | Philippe    |
    |        |                         |                 |                  | Cutillas    |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 7      | Acceptance Test         | A               | 01/19/2020       | Andrew      |
    |        | Procedures              |                 |                  | Kirima      |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 8      | Acceptance Test Data    | A               | 01/19/2020       | Andrew      |
    |        | Sheets                  |                 |                  | Kirima      |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 9      | Software Design         | A               | 01/19/2020       | Sean Farris |
    |        | Document                |                 |                  |             |
    +--------+-------------------------+-----------------+------------------+-------------+
    | 10     | User Manual             | A               | 01/19/2020       | Ramos Chen  |
    |        |                         |                 |                  |             |
    +--------+-------------------------+-----------------+------------------+-------------+


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Technical Data Package (Doc 1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Technical Data Package Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Security Classification Guide (Doc 2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Security Classification Guide Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Concept of Operations (Doc 3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Concept of Operations Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 9/1/2019       | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+
    | B        | Functionality that was built in the MVP was described  | 1/19/2020      | Sam Badger  |
    |          | in depth.                                              |                |             |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unsolicited Proposal (Doc 4)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Unsolicited Proposal Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 9/25/2019      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
System Requirements Document (Doc 5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: System Requirements Document Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 10/10/2019     | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+
    | B        | Changes to terminology and System Block Diagram.       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+
    | B        | Changes to terminology and System Block Diagram.       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~
Risk Analysis (Doc 6)
~~~~~~~~~~~~~~~~~~~~~

.. table:: Risk Analysis Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 9/16/2019      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Acceptance Test Procedures (Doc 7)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Acceptance Test Procedures Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Acceptance Test Data Sheets (Doc 8)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Acceptance Test Data Sheets Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Software Design Document (Doc 9)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Software Design Document Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+

~~~~~~~~~~~~~~~~~~~~
User Manual (Doc 10)
~~~~~~~~~~~~~~~~~~~~

.. table:: User Manual Change Log

    +----------+--------------------------------------------------------+----------------+-------------+
    | Revision | Reason for Change                                      | Date of change | Responsible |
    |          |                                                        |                | Engineer    |
    +==========+========================================================+================+=============+
    | A        | Document Created                                       | 1/19/2020      | Sam Badger  |
    +----------+--------------------------------------------------------+----------------+-------------+