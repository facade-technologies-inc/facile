:orphan:

------------
Introduction
------------

The customer needs a system that will produce custom Application Programming Interfaces
(APIs) that control existing Graphical User Interfaces (\*target GUIs) based on their behavior.
The APIs will be versatile and will be used for many purposes such as automated GUI testing,
task automation, or extending an application’s functionality.

------------
Stakeholders
------------

- The senior design team
- Facade Technologies Inc.
- Investors of Facade Technologies Inc.
- Customers of Facade Technologies Inc.

--------------------------
Product History/Background
--------------------------

There are many software products on the market focused on automating tasks through the
target GUI, but they require the user to choose very specific tasks that they want to perform. By
capturing the behavior of the GUI of interest, an API could be generated that provides more
robust, flexible, and fine-grained control of the target GUI.
Uses of an API with such capabilities may include, but are not limited to:

- Hiding the target GUI off the screen, but using the target software as an engine for other
  applications. (This is where the name “Facade” comes from).

- Creating a form of interprocess communication (IPC) where one application can easily
  use data from another application. (By creating multiple APIs and tying them together via
  python script).

- Extending functionality of the target software on the fly without requesting new features
  from developers or changing source code.

- Automating redundant GUI tasks.

-----------------
System Boundaries
-----------------

The system will be a Windows desktop application. The user will interact with the system
through a graphical user interface. For now, the system will interface and interact with the target
application GUI via pywinauto (a GUI automation library). Pywinauto is not in the scope of this
project, but it acts as the interface which allows the system to control GUIs on the Windows
operating system. In the future, the system may need to interface with target GUIs on different
operating systems which would require using an alternative to pywinauto. The system will be
modular in such a way that it will be easy to reconfigure it to interact with other GUI automation
libraries. The system will also be created in such a way that it will be possible to later add
functionality to generate the APIs in other languages. The generated API will also interface with
the target application via a GUI automation library.

------------------
System Environment
------------------

The system will operate on the Windows 10 operating system. Compatibility with other
operating systems is outside the scope of this project, but the system will be designed in such a
way adding compatibility later will minimize system re-work.

--------
Schedule
--------

.. tabularcolumns:: |p{100pt}|p{100pt}|p{200pt}|R|
.. table:: Project Schedule (Minimum Viable Product)

    +--------------------+--------------------+--------------------+--------------------+
    |       Level 1      |       Level 2      |       Level 3      |       Date         |
    +====================+====================+====================+====================+
    | Facade API         | GUI Component      | (View)             | 09/25/19           |
    | Builder            | Identifier         | Create             |                    |
    |                    |                    | functionality      |                    |
    |                    |                    | to show the target |                    |
    |                    |                    | GUI windows and    |                    |
    |                    |                    | components         |                    |
    |                    |                    | visually.          |                    |
    |                    |                    +--------------------+--------------------+
    |                    |                    | (Model)            | 10/03/19           |
    |                    |                    | Create the         |                    |
    |                    |                    | internal           |                    |
    |                    |                    | representation of  |                    |
    |                    |                    | GUI windows and    |                    |
    |                    |                    | components.        |                    |
    |                    |                    +--------------------+--------------------+
    |                    |                    | (Controller)       | 10/09/19           |
    |                    |                    | Connect view to    |                    |
    |                    |                    | model via          |                    |
    |                    |                    | interface          |                    |
    |                    |                    | that doesn't       |                    |
    |                    |                    | require            |                    |
    |                    |                    | view to care about |                    |
    |                    |                    | data structures    |                    |
    |                    |                    | used in the model. |                    |
    |                    +--------------------+--------------------+--------------------+
    |                    |                                           10/11/19           |
    |                    +--------------------+--------------------+--------------------+
    |                    | Visibilty          | (View)             | 10/17/19           |
    |                    | Behavior           | Create             |                    |
    |                    | Mapper             | functionality to   |                    |
    |                    |                    | show a visual      |                    |
    |                    |                    | representation of  |                    |
    |                    |                    | visibility         |                    |
    |                    |                    | behaviors of the   |                    |
    |                    |                    | target GUI.        |                    |
    |                    |                    +--------------------+--------------------+
    |                    |                    | (Model)            | 10/30/19           |
    |                    |                    | Create internal    |                    |
    |                    |                    | model for          |                    |
    |                    |                    | identifying        |                    |
    |                    |                    | visibility         |                    |
    |                    |                    | behaviors          |                    |
    |                    |                    +--------------------+--------------------+
    |                    |                    | (Controller)       | 11/04/19           |
    |                    |                    | Connect view to    |                    |
    |                    |                    | model via          |                    |
    |                    |                    | interface that     |                    |
    |                    |                    | doesn’t require    |                    |
    |                    |                    | view to care about |                    |
    |                    |                    | data structures    |                    |
    |                    |                    | used in the model. |                    |
    |                    +--------------------+--------------------+--------------------+
    |                    |                                           11/09/19           |
    |                    +--------------------+--------------------+--------------------+
    |                    | Action Pipeline    | (View)             | 11/20/19           |
    |                    | Builder            | Create             |                    |
    |                    |                    | functionality to   |                    |
    |                    |                    | view actions       |                    |
    |                    |                    | individually and   |                    |
    |                    |                    | connect actions to |                    |
    |                    |                    | build action       |                    |
    |                    |                    | pipelines.         |                    |
    |                    |                    +--------------------+--------------------+
    |                    |                    | (Model)            | 11/26/19           |
    |                    |                    | Create the         |                    |
    |                    |                    | internal           |                    |
    |                    |                    | representation of  |                    |
    |                    |                    | actions and action |                    |
    |                    |                    | pipelines.         |                    |
    |                    |                    +--------------------+--------------------+
    |                    |                    | (Controller)       | 11/30/19           |
    |                    |                    | Connect view to    |                    |
    |                    |                    | model via          |                    |
    |                    |                    | interface that     |                    |
    |                    |                    | doesn't require    |                    |
    |                    |                    | view to care about |                    |
    |                    |                    | data structures    |                    |
    |                    |                    | used in the model. |                    |
    |                    +--------------------+--------------------+--------------------+
    |                    |                                           12/03/19           |
    +--------------------+--------------------+--------------------+--------------------+
    |                                                                12/10/19           |
    +--------------------+--------------------+--------------------+--------------------+

------------------
System Constraints
------------------

The system must be built within the following specifications.

====
Cost
====

The budget supplied to the team for development of the project is $4000. About $150 will
be reserved for the Design Day poster, and an unknown amount will also be reserved for
a Jira subscription. Due to the nature of the project being solely software, it is unlikely
that we will use any additional funds. Other costs such as Design Day clothing, a GitHub
subscription, and occasional meals will be furnished by the company.

========
Schedule
========

The minimum viable product will be completed by 12/10/2019. See the “schedule”
section for a more detailed schedule.

============
Technologies
============

The system shall be compatible with Windows 10. Qt5 and Pyside2 will be used to
create the GUI. Github and Jira will be used for version control, process monitoring and
team collaboration. The software shall be exclusively programmed in Python 3. The
pywinauto library will be used to interface with the target GUI. Sphinx will be used to
generate documentation for the generated API from header comments within the API.

===============
Life Expectancy
===============

The software product is expected to run with full functionality, until the Windows 10
operating system becomes obsolete.

=======================
Size, Weight, and Power
=======================

This system constraint does not apply to our system since it is purely a software.

----------
System Use
----------

The system will be used by people with little-to-no programming experience. When the user
launches the system executable, there will be options to either create a new project or load an
existing one. If the user chooses to load an existing project, they will be prompted to select a
project file to continue where the project was left off at.

If the user selects to create a new project, a dialog will prompt the user to select the executable
file of the target application. Once the executable is selected, the system will launch the target
application and attach to it with a GUI automation tool (pywinauto) that allows a python program
to discover and interact with elements of the graphical user interface. Once the target
application is launched, the user can toggle between the following tools.

At any time during development of the API, the user is able to save their progress to a project
file(s) and load it into the development area to resume.

Once the user is satisfied with the state of their API project, they can click a “Generate API”
button which will invoke the Python API Compiler which generates the API which is a valid
python package.

Once the python package is created, another tool called Sphinx will be run to generate
documentation for the package.

When a developer decides to use the generated python package, the most simple program they
could write would look like the following:

.. code-block:: python

    from MyGeneratedAPI import *
    output1, output2, output3 = my_action_pipeline(input1, input2, input3)

========================
GUI Component Identifier
========================

This tool has 2 modes; autonomous and controlled. In autonomous mode, the system
will probe the target GUI by clicking buttons and watching for new windows and GUI
components to be shown or hidden. In manual mode, the system watches while the user
interacts with the target GUI. As new windows and GUI components are discovered,
they will be drawn in the Facade API Builder’s development area.

==========================
Visibility Behavior Mapper
==========================

As target GUI components are identified, the internal representation of the target GUI
needs to know how specific elements behave. The behaviors of interest that we care
about are windows opening/closing and widgets being shown/hidden. These behaviors
are important because to interact with a GUI component, it must be visible not to the
human, but to the computer. For instance, A button can be shown in a window, but the
window is moved out of the area of visibility (behind another application or off the screen
entirely.)

=======================
Action Pipeline Builder
=======================

Once a portion of the target GUI is sufficiently described behaviorally and structurally,
the user will be able to describe specific actions that they would like to perform with the
target GUI in a graphical manner. The user will be able to develop “modules” that are
described by their input, output, and functionality. Modules can be chained together to
build more complex functionality. The combination of modules results in another (parent)
module being created. Any unconnected inputs/outputs of the internal (child) modules
will be inputs/outputs of the parent module. The parent modules are referred to as
“action pipelines” and each of the leaf modules (modules without children) are referred to
as “actions”.

=========
Annotator
=========

The user will be able to annotate windows and components of the GUI as they see fit.
There will also be opportunities for the user to leave comments on certain portions of the
GUI representation. While the user is creating action pipelines, the annotator will require
that the user provides names and types for all of the inputs and outputs of the module
being created. The user will also be prompted to write a description about what the
module does. These annotations are important for 2 reasons:

- They allow future users who open the project to know what is going on.

- The annotations will be directly injected into the generated python library in the
  form of Python Docstrings. After generating the Python package, a tool called
  Sphinx will be run that collects docstrings and puts them into formal library
  documentation that properly describes the interfaces available to the user of the
  package.

=========
Validator
=========

As the user works to build their API, they will have the opportunity to run a validator that
will analyze the user’s work and point out any errors with the user’s API design. For
instance, if the user develops an action pipeline that contains an action loop where the
output of a module eventually feeds into the input of the same module (either directly or
indirectly), the verifier would warn the user of the design flaw. If possible, the verifier will
run in the background as the user builds the API.

---------------
Expected Output
---------------

The output includes a Python package that interacts with the target GUI specified by the user.
Once the API is generated a developer can then use the API as a component in another Python
program.