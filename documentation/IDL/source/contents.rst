**********
Change Log
**********

.. table:: Indentured Document List Current Release

    +-----------------+------------------+--------------+------------------------------+
    | Release Version | Internal Version | Last Updated | Approved By                  |
    +=================+==================+==============+==============================+
    | A               | 1                | 03/03/2020   | Nikhith Vankireddy           |
    +-----------------+------------------+--------------+------------------------------+

.. table:: Indentured Document List Change Log
    :widths: 5 40 23 8 12 12

    +-----+--------------------------------------------+--------------------------------------------+-------+-------------+------------+
    | No. | Change Description                         | Rationale                                  | Class | Approved By | Date       |
    +=====+============================================+============================================+=======+=============+============+
    | 1   |                                            |                                            |       |             |            |
    +-----+--------------------------------------------+--------------------------------------------+-------+-------------+------------+

**************************
Indentured Document List
**************************

:num:`Fig. #idl` shows a list of all documents and drawings in the iteration documentation package. The subsequent
sections give descriptions for each item in the indentured document list


.. _ConOpsFlow:

.. figure:: ../images/IDL.png
    :alt: Indentured Document List

    The indentured document list for the iteration documentation package.

1. System Report - Iteration Documentation Package
    Gives a full description of the delivered project including rationale and scope of delivery due to
    requirements, critical technology, and use cases. A description of the ConOps is also given as well as the System
    Verification Plan. The verification flow diagram details verifications complete with expected dates, date completed, and
    procedure to be used. The SRVM is also included and is complete with references to current test procedures, data sheets,
    inspection reports, etc. The SRVM includes all sub-system and sub-assembly requirements associated with current state of
    project. Evidence, including data sheet and inspection reports are captured referencing document by number and version,
    software configuration, result, expected result, and pass/fail.

2. Indentured Document List
    The current document which describes all documents in the System Report.

3. System Requirements Document
    Describes all requirements of the Facile system. It includes a simplified SRVM and
    test procedure descriptions as well as the system block diagram and architecture diagram.

4. Verification Documentation
    Contains all test procedures to perform to verify the Facile system. It also contains all
    associated data sheets and an inspection report for any requirement that if verified through inspection.

4.1 Acceptance Test Procedures
    Give a list of steps to follow to verify each requirement that can currently be verified.

4.2 Data Sheets
    The Data Sheets in this section are left blank, but they directly correspond to the verification procedure counterparts.
    While testing, a copy of the data sheets is to be printed and filled in manually and returned and pu in the models
    section.

4.3 Inspection Report
    Contains procedures to verify any requirements that are verified by inspection. Facile has no
    requirements that are verified through inspection, so the section is left intentionally blank.

5. Software Drawing Package
    The Software Drawing Package contains the software drawing for Facile.

5.1 Software Drawing
    Contains the drawing number, cage code, date, revision, notes, and a table of one or more Part
    Numbers (PN) assigned to the software executable files that comprise a SW release.

6. Software Description Document
    Provides a description of all versions of Facile and their capabilities. It also
    provides detailed descriptions about the underlying data structures and algorithms that Facile uses as well as
    documentation for all of Facile's source code to date.

6.1 Software Version Description
    Describes all Facile releases and the build process for each one as well as
    descriptions about functionality of each version.

6.2 Architectural/Design
    Describes the different components of Facile's structure and how various algorithms in Facile work.

6.2.1 Algorithms
    Primarily explains algorithms relating to Facile's token comparison and GUI exploring algorithms.

6.2.2 Data Structures
    Describes in depth, the target GUI model, the API model, and the compiler as well as some
    peripheral data structures important to Facile.

6.3 Source Code Documentation
    Breaks the source code down into modules, classes, and functions and shows the interface
    for each level. This documentation is created by the Facile developers as they code.

7. User Manual
    Shows someone how to use Facile to generate a Facile API.

