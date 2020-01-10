
*************************
Acceptance Test Procedure
*************************


----------------------------------------------------------------------------------------------------
Operating System Acceptance Test
----------------------------------------------------------------------------------------------------

============
Introduction
============

This acceptance test document verifies that the software system, Facile is functional on 64 Bit Windows 10 Home Version 1903.  This acceptance test establishes the framework used by the acceptance test team to plan, execute, and document acceptance testing.  It describes the scope of the work performed and the approach taken to execute the tests created to validate that the system performs as required with the intended operating system. The details of this acceptance test are developed according to the requirements specifications and show traceability back to those specifications.

====================
Referenced Documents
====================

- System Requirements Document, Rev B, 10/27/2019

=======================
Required Test Equipment
=======================

- PC (Personal Computer)

=========================
Requirements Summary
=========================

To verify SR4.2.1 - Facile shall operate on 64-bit Windows 10 Home Version 1903.

===================
Pre-Test Conditions
===================

- PC (Personal Computer)

+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
| Steps | Action                                                                                | Expected Result                         |
+=======+=======================================================================================+=========================================+
|     1 | Right click on **Explorer**                                                           | A context menu of items open up         |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
|     2 | Select **System**                                                                     | **Settings** is open                    |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
|     3 | Scroll to **Device specifications,** and verify the System type, Edition, and Version | Refer to Figure 1.1                     |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
|     4 | Click on **Windows Search Bar**                                                       | Windows Search Bar comes into focus     |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
|     5 | Type cmd and press enter                                                              | A **Command Prompt** terminal opens     |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
|     6 | Click on the **Command Prompt**                                                       | The **Command Prompt** comes into focus |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
|     7 | Type "python facile.py" in the **Command Prompt**                                     | Facile should run. Test Case Completed. |
+-------+---------------------------------------------------------------------------------------+-----------------------------------------+
