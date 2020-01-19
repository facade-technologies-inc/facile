----------------------
Introduction and Scope
----------------------

Many software products have been designed to solely interact with the user through a graphical user
interface (GUI). This is convenient for the user, but it places an upper limit on the usefulness of
the software. The most significant limitations are speed of use (imposed by user) and functionality
(imposed by developers). There are products on the market which aim to mimic the user by recording a
sequence of actions and replaying them, but these solutions lack flexibility.

The goal of this project is to develop a system that can produce custom Python application
programming interfaces (APIs) to control existing GUIs (target GUIs) based on their behavior. This
GUI automation solution will provide a high degree of flexibility to the user by giving them the
ability to make decisions about what to automate at multiple levels of API development. An API that
controls a GUI would allow operations to be performed much faster within the GUI (opposed to user
interactions) and allow functionality not supported by the GUI to be developed in the program that
uses the API.

==============
Identification
==============

Façade Technologies Inc. needs a system that produces custom application programming interfaces that
control existing graphical user interfaces based on their behavior. The APIs will be versatile and
will be used for many purposes such as automated GUI testing, task automation, or extending an
application’s functionality.

============
Intended Use
============

The system should be able to be used by people with little-to-no programming experience. When the
user launches the system executable, there should be options to either create a new project or load
an existing one. Each project will hold the user’s work when developing a single API. Once the user
decides to work on a project, they are in the API design process. The user should be able to click a
button that generates an API that can perform all of the tasks specified in the API design process.

==========
Background
==========

There are many software products on the market focused on automating tasks through the target GUI,
but they require the user to choose very specific tasks that they want to perform. By capturing the
behavior of the GUI of interest, an API could be generated that provides more robust, flexible, and
fine-grained control of the target GUI.

Uses of an API with such capabilities may include, but are not limited to:

- Hiding the target GUI off the screen but using the target software as an engine for other
  applications. (This is where the name “Facade” comes from).

- Creating a form of inter-process communication (IPC) where one application can easily use data
  from another application (by creating multiple APIs and tying them together via python script).

- Extending functionality of the target software on the fly without requesting new features from
  developers or changing source code.

- Automating redundant GUI tasks.

=========================
Document Overview and Use
=========================

The intent of this document is to list and explain the requirements pertaining to the system known
as “Facile” in Facade Technologies Inc. The requirements described in this document are
preconditions for a successful completion of the Facile project.

============
StakeHolders
============

The stakeholders of this project are:
- Façade Technologies Inc.
- Façade Technologies Inc.’s shareholders.
- Façade Technologies Inc.’s customers.
- The senior design team.

--------------------
Referenced Documents
--------------------

There are no applicable or referenced documents for this project.

----------------------------------------
Definitions, Acronyms, and Abbreviations
----------------------------------------

Please see the glossary.

------------
Requirements
------------

==================
Speed Requirements
==================

SR4.1.1 Startup Speed
    Facile shall startup in less than 30 seconds after the Facile executable file is run.

SR4.1.2 API Documentation Generation Speed
    A single user-specified format (HTML, PDF, LaTeX, or TXT) of API documentation shall be
    generated in less than 5 minutes.

SR4.1.3 API Generation Speed
    The API Compiler shall produce a single custom Python API in less than 5 minutes after being
    initiated.

==========================
Environmental Requirements
==========================

SR4.2.1 Operating System
    Facile shall operate on 64bit Windows 10 Home version 1903

SR4.2.2 RAM Utilization
    Facile shall use less than or equal to 2 GB of RAM while operating.

SR4.2.3 Disk Utilization
    Facile shall require less than or equal to 5 GB of disk space to install.

SR4.2.4 Programming Language
    Facile source code shall be compatible with the Python 3.7.4 interpreter.

===========================
User Interface Requirements
===========================

SR4.3.1 Graphical User Interface (GUI)
    The Facade Builder shall contain a GUI that interacts with the user to produce custom APIs that
    control the target GUI.

SSR4.3.1.1 Target GUI Component Identifier
    The Facile GUI shall contain a view that allows users to identify components from the target
    GUI.

SSR4.3.1.2 Target GUI Behavior Mapper
    The Facile GUI shall contain a view that allows users to specify "Show/Hide" relations
    between two components.

SSR4.3.1.3 Project Overview Sidebar
    The Facile GUI shall contain a view that shows all model components of the API project.

SSR4.3.1.4 Property Editor Panel
    The Facile GUI shall contain a view that allows the user to edit specific properties for any
    model components in the project.

.. todo::
    Add the term "Model Component" to the glossary.

SSR4.3.1.5 Project Settings Dialog
    The Facile GUI shall contain a dialog that allows the user to edit project settings.

SSR4.3.1.6 API Model Creation
    The Facile GUI shall contain a view that allows the user to build a graphical model of the
    generated API.

SAR4.3.1.6.1 Action Pipeline Creation
    The Facile GUI shall allow the user to create action pipelines utilizing predefined actions.

SAR4.3.1.6.2 Show Relevant Actions
    The Facile GUI shall contain a view that shows all actions relevant to the target GUI model.

SSR4.3.1.7 Validator
    The Facile GUI shall contain a view that warns the user of potential errors in project models.

===========================
Custom Library Requirements
===========================

SR4.4.1 Target GUI Interface Library
    Facile shall utilize a custom library that interacts with the target GUI.

================
API Requirements
================

SR4.5.1 Target GUI Interface Library
    Facile shall produce a custom python API to control the target GUI.

=================
File Requirements
=================

SR4.6.1 API Documentation File Contents
    The system shall generate API documentation based on annotations in the API design process.

SR4.6.2 API Documentation File Formats
    Facile shall allow the user to decide the format(s) of documentation to generate for an API out of HTML, PDF, LaTeX, and text.

SR4.6.3 Project File Extension
    Facile project files shall be saved with a .fcl extension.

SR4.6.4 Project File Format
    Facile project files shall be in a human-readable format such as JSON.

--------------------
System Block Diagram
--------------------

Please refer to :num:`Fig. #sbd`

.. _SBD:

.. figure:: ../images/system_block_diagram.png
    :alt: System block diagram

    This is the system block diagram for Facile.

-------------------------
Verification Requirements
-------------------------

.. todo:: Update verification types - should be all TEST

===============================
Speed Requirements Verification
===============================

SR4.1.1 Startup Speed
    Test: The startup speed for facile shall be tested by running the Facile executable file and
    recording the time before any graphical user interface is shown. The test will show that the
    time required is under 30 seconds.

SR4.1.2 API Documentation Generation Speed
    Test: The API Documentation Generation speed for facile shall be tested by generating an API
    documentation based on user preference and recording the time required for the documentation to
    be created. The test will show that the time needed is under 5 mins.

SR4.1.3 API Generation Speed
    Test: The API Generation speed for facile shall be tested by generating a customized API and
    recording the time required for the API to be created. The test will show that the time
    needed is under 5 minutes.

=======================================
Environmental Requirements Verification
=======================================

SR4.2.1 Operating System
    Inspection: Operation system requirement shall be verified by inspecting if Facile can
    successfully run on 64bit Windows 10 Home version 1903.

SR4.2.2 RAM Utilization
    Inspection: RAM Utilization requirement shall be verified by inspecting the memory consumed
    by Facile on Windows 10 Task Manager.

SR4.2.3 Disk Utilization
    Inspection: Disk Utilization requirement shall be verified by installing Facile and
    inspecting the disk usage of it.

SR4.2.4 Programming Language
    Inspection: Programming Language requirement shall be verified by visually inspecting the
    programming language of any Facile file.

========================================
User Interface Requirements Verification
========================================

SR4.3.1 Graphical User Interface (GUI)
    Inspection: The Graphical User Interface requirement shall be verified by creating an API for
    Audacity using the Facile GUI.

SSR4.3.1.1 Target GUI Component Identifier
    .. todo:: add verification requirement

SSR4.3.1.2 Target GUI Behavior Mapper
    .. todo:: add verification requirement

SSR4.3.1.3 Project Overview Sidebar
    .. todo:: add verification requirement

SSR4.3.1.4 Property Editor Panel
    .. todo:: add verification requirement

SSR4.3.1.5 Project Settings Dialog
    .. todo:: add verification requirement

SSR4.3.1.6 API Model Creation
    .. todo:: add verification requirement

SAR4.3.1.6.1 Action Pipeline Creation
    .. todo:: add verification requirement

SAR4.3.1.6.2 Show Relevant Actions
    .. todo:: add verification requirement

SSR4.3.1.7 Validator
    .. todo:: add verification requirement

========================================
Custom Library Requirements Verification
========================================

SR4.4.1 Target GUI Interface Library
    Inspection: The Target GUI Interface Library requirement shall be verified by inspecting that
    all components in Notepad GUI can be identified.

=============================
API Requirements Verification
=============================

SR4.5.1 API Package
    Inspection: The API Package requirement shall be verified by using Facile to produce an API that
    controls the Audacity audio player.

==============================
File Requirements Verification
==============================

SR4.6.1 API Documentation File Contents
    Inspection: API Documentation File Contents requirement shall be verified by generating an API
    documentation and inspecting if it matches the annotations in the API design process.

SR4.6.2 API Documentation File Formats
    Inspection: API Documentation File Formats requirement shall be verified by generating an API
    documentation based on user preference and inspecting its format.

SR4.6.3 Project File Extension
    Inspection: Project File Extension requirement shall be verified by saving Facile project files
    and inspecting their extensions.

SR4.6.4 Project File Format
    Inspection: Project File Format requirement shall be inspected by reading through project files.

-------------------
Verification Matrix
-------------------

The following tables contain all of the requirements from the same level. They are separated due to
issues with long table rendering.

.. tabularcolumns:: |J|p{10pt}|p{10pt}|p{10pt}|p{10pt}|
.. table:: System Requirement Verification Matrix

    +-----------------------------------------------------------+---------------+
    |                                                           | Verification  |
    |                                                           | Method        |
    |                                                           +---+---+---+---+
    |                                                           | T | A | D | I |
    +-----------------------------------------------------------+---+---+---+---+
    | ``Speed Requirements``                                                    |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.1.1 Startup Speed``                           | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.1.2 API Documentation Generation Speed``      | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.1.3 API Generation Speed``                    | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``Environmental Requirements``                                            |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.2.1 Operating System``                        | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.2.2 Ram Utilization``                         | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.2.3 Disk Utilization``                        | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.2.4 Programming Language``                    | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``User Interface Requirements``                                           |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.3.1 Graphical User Interface``                | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``Custom Library Requirements``                                           |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.4.1 Target GUI Interface Library``            | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``API Requirements``                                                      |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.5.1 API Package``                             | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``File Requirements``                                                     |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.6.1 API Documentation File Contents``         | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.6.2 API Documentation File Formats``          | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.6.3 Project File Contents``                   | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SR4.6.4 Project File Format``                     | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+

.. tabularcolumns:: |J|p{10pt}|p{10pt}|p{10pt}|p{10pt}|
.. table:: Sub-system Requirement Verification Matrix

    +-----------------------------------------------------------+---------------+
    |                                                           | Verification  |
    |                                                           | Method        |
    |                                                           +---+---+---+---+
    |                                                           | T | A | D | I |
    +-----------------------------------------------------------+---+---+---+---+
    | ``User Interface Requirements``                                           |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.1 Target GUI Component Identifier``      | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.2 Target GUI Behavior Mapper``           | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.3 Project Overview Sidebar``             | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.4 Property Editor Panel``                | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.5 Project Settings Dialog``              | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.6 API Model Creation``                   | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SSR4.3.1.7 Validator``                            | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+

.. tabularcolumns:: |J|p{10pt}|p{10pt}|p{10pt}|p{10pt}|
.. table:: Sub-assembly Requirement Verification Matrix

    +-----------------------------------------------------------+---------------+
    |                                                           | Verification  |
    |                                                           | Method        |
    |                                                           +---+---+---+---+
    |                                                           | T | A | D | I |
    +-----------------------------------------------------------+---+---+---+---+
    | ``User Interface Requirements``                                           |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SAR4.3.1.6.1 Action Pipeline Creation``           | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+
    | ``..... SAR4.3.1.6.2 Show Relevant Actions``              | X |   |   |   |
    +-----------------------------------------------------------+---+---+---+---+

-----
Notes
-----

=====================
Design Considerations
=====================

The following components should exist in the Facile application to aid in the design process of an
API:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Target GUI Component Identifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Facade Builder should contain a view that allows the user to identify GUI components in the
target GUI.

~~~~~~~~~~~~~~~~~~~~~~~~~~
Target GUI Behavior Mapper
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Facade Builder should contain a view that allows the user to map out visibility behaviors of the
target GUI.

~~~~~~~~~~~
API Builder
~~~~~~~~~~~

The Facade Builder should contain a view that allows the user to declare sequences of actions to be
performed by the generated API.

~~~~~~~~~
Annotator
~~~~~~~~~

The Facade Builder should allow the user to annotate inputs and outputs of the generated API entry
points.

~~~~~~~~~
Validator
~~~~~~~~~

The Facade Builder should contain a view that validates the user’s work by showing error/warning
messages when an invalid structure is created anywhere in the design process.

~~~~~~~~~~~~~~~
API Compilation
~~~~~~~~~~~~~~~

The Facade Builder should contain a mechanism that runs the API Compiler using the internal data
structures produced by the Facade Builder that were created by the user in the design process.

=======================
Security Considerations
=======================

Facile should be designed with the following security considerations in mind:

~~~~~~~~~~~~~~~~
Builder Autonomy
~~~~~~~~~~~~~~~~

Facile should only explore the target GUI autonomously with explicit user
consent.

~~~~~~~~~~~~~~~~
API Restrictions
~~~~~~~~~~~~~~~~

Generated APIs should only have the capability to perform actions on the target GUI that have been
specified by the creator of the API (i.e. the person who designed the API using Facile).

~~~~~~~~~~~~
Data Storage
~~~~~~~~~~~~

Facile should only store data from the target application locally in RAM (i.e. the data disappears
when Facile stops running).

~~~~~~~~~~~~~~~~~~~
Unexpected Behavior
~~~~~~~~~~~~~~~~~~~

During execution of the generated API, in the event that a specified action cannot be performed, an
exception should be raised.

======================
Software Block Diagram
======================

.. figure:: ../images/software_block_diagram.png
    :alt: A simple diagram showing progression of user actions.

    Depicts a high level work flow that the user would take to create a custom API.



