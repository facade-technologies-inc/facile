********************
Unsolicited Proposal
********************

--------
Abstract
--------

Many software products have been designed to solely interact with the user through a graphical user
interface (GUI). This is convenient for the user, but it places an upper limit on the usefulness of
the software. The most significant limitations are speed of use (imposed by user) and functionality
(imposed by developers). There are products on the market which aim to mimic the user by recording a
sequence of actions and replaying them, but these solutions lack flexibility.

The goal of this project is to develop a system that can produce custom Python Application
Programming Interfaces (APIs) to control existing GUIs (target GUIs) based on their behavior. This
GUI automation solution will provide a high degree of customization without compromising
flexibility. An API that controls a GUI would allow operations to be performed much faster within
the GUI and allow functionality not supported by the GUI to be developed in the program that uses
the API.

The system includes an environment that cooperates with the user to identify structural components
of the target GUI and define visibility behaviors. The user will be able to use the functionalities
of the target GUI components as building blocks of more complex actions - action pipelines. The
action pipelines are translated into python functions and included in the generated API with formal
documentation generated from user annotations. The user could then write a small python script to
import the API and run the action pipeline functions from their own Python programs.

-------------------------------
Significance of the Opportunity
-------------------------------

There are many software products on the market focused on automating tasks through the target GUI,
but they require the user to choose very specific tasks that they want to perform. By capturing the
behavior of the GUI of interest, an API could be generated that provides more robust, flexible, and
fine-grained control of the target GUI.

Uses of an API with such capabilities may include, but are not limited to:

- Hiding the target GUI off the screen and using the target software as an engine for other
  applications – hence the name Facade.

- Creating a form of inter-process communication (IPC) where one application can use data from
  another application by creating multiple APIs and tying them together via Python script.

- Extending functionality of the target software on the fly without requesting new features from
  developers or changing source code.

- Automating redundant GUI tasks.

--------------------
Technical Objectives
--------------------

The Facade API Builder will be a visually interactive application that will allow users to generate
custom APIs that will, in turn, allow more flexible and extensive control of existing user
interfaces. The builder itself will also be coded in Python, but through user interaction with the
builder’s GUI, no coding knowledge will be necessary in order to make use of the application. For
reasonable scope, the team has opted to exclusively support Python API generation in a Microsoft
Windows 10 environment, but a focus on modular development throughout the project will allow
additional compatibility to be incorporated in the future with little to no effort.

-----------------------
Functional Requirements
-----------------------

.. table:: Functional Requirements

    ===== ==========================================================================
      1    The system shall interact with the user through a GUI to dynamically
           Identify components of interest in the target GUI.

      2    The system shall contain a graphical display of the visual behaviors of
           the target GUI.

      3    The system shall allow users to save and load projects.

      4    The system shall allow the user to define sets of actions (action
           pipelines) to be performed in the target GUI.

      5    The system shall produce custom Python APIs that have the ability to
           control given GUIs within the Microsoft Windows operating system.

      6    The system shall require the user to annotate GUI components and action
           pipeline inputs/outputs.

      7    The system shall generate formal documentation for generated APIs based
           on annotations added by the user during the API development process.

      8    The system shall have a component that actively validates API structures
           during the API development process.
    ===== ==========================================================================

------------------------
Functional Block Diagram
------------------------

.. figure:: ../../images/functional_block_diagram.png
    :align: center
    :height: 300px
    :alt: Functional Block Diagram
    :figclass: align-center

    The functional block diagram is a high level picture describing the functions of the system.

---------------------------
Milestones and Deliverables
---------------------------

The team will build the system according to the senior design project milestones and will deliver
all according to this schedule:

.. tabularcolumns:: |p{50pt}|p{110pt}|p{180pt}|p{90pt}|
.. table:: Milestones and Deliverables

    ========== ========================= =========================================== ===================
     Date       Milestone                 Description                                 Deliverables
    ========== ========================= =========================================== ===================
    09/12/2019 Unsolicited Proposal      Sponsor approval to continue with rough     Document
                                         plan for project
    ---------- ------------------------- ------------------------------------------- -------------------
    10/01/2019 System Requirements       System Requirements for MVP are             Document
                                         documented

                                         Verification plan for system requirements
                                         is created.

                                         System Block diagram is created.
    ---------- ------------------------- ------------------------------------------- -------------------
    10/31/2019 Preliminary Design Review Development plan for MVP is presented.      Presentation
    ---------- ------------------------- ------------------------------------------- -------------------
    12/10/2019 Critical Design Review    MVP is presented                            Presentation

                                         Development plan for the next iteration
                                         is presented.
    ---------- ------------------------- ------------------------------------------- -------------------
    01/21/2019 Critical Design Report    Technical data package is released.         Source Code v0.2.0

                                                                                     Document
    ---------- ------------------------- ------------------------------------------- -------------------
    03/03/2020 Integration Status Review Second iteration work is presented.         Source Code v0.3.0

                                         Development plan for the final iteration    Presentation
                                         is presented.
    ---------- ------------------------- ------------------------------------------- -------------------
    04/23/2020 Final Acceptance Review   Final product is presented to the panel.    Presentation
    ---------- ------------------------- ------------------------------------------- -------------------
    05/04/2020 Design Day                Final product is presented to the public.   Poster

                                                                                     Demonstration

                                                                                     Source Code v1.0.0

                                                                                     Executable v1.0.0
    ---------- ------------------------- ------------------------------------------- -------------------
    05/13/2020 Final Report              Full technical data package is submitted.   Document
    ========== ========================= =========================================== ===================

---------------------------
Related Work and Experience
---------------------------

The team includes five software engineers, one project manager and one systems engineer. Aside from
the relevant subject matter learned at the University of Arizona, the team has the following
experience:

- Sean Farris, a software engineer, has interned at Realize51, a sub-contractor for Raytheon,
  working with one of Raytheon’s Algorithm teams where he wrote Python scripts and developed
  technical documentation.

- Brandi Diesso, a software engineer, interns with Microsoft TEALS philanthropies. She is
  responsible for teaching about 20 high-school students Python and Block code.

- Sam Badger, a software engineer, has interned with Mahr Metrology where he developed GUI
  automation tools and has interned with Raytheon where he developed a custom continuous
  integration system implemented in Python.

- Philippe Cutillas, a software engineer, has experience working for IT at the University of
  Arizona’s College of Nursing.

- Ramos Chen, a software engineer, has interned with a few of start-up companies where he worked on
  platform development and web development as a test engineering.

- Andrew Kirima, a systems engineer with software background, has some experience with Python
  programming and has implemented a Smart Park Insight system on an SCRD.

-------------
Key Personnel
-------------

.. tabularcolumns:: |p{80pt}|p{80pt}|p{150pt}|p{70pt}|
.. table:: Key Personnel Roles and Contact

    ================== ======================= =============================== ================
     Name               Role/Position           E-Mail                          Phone
    ================== ======================= =============================== ================
    Nikhith Vankireddy Project Manager         nvankireddy@email.arizona.edu   (480) 469 - 5996

    Sam Badger         Team Lead               smalbadger@email.arizona.edu    (520) 275 - 9786

                       Software Engineer

    Philippe Cutillas  Software Engineer       pcutillas@email.arizona.edu     (520) 302 - 8730

    Ramos Chen         Software Engineer       jiuruchen@email.arizona.edu     (469) 954 - 2872

    Sean Farris        Software Engineer       sfarris@email.arizona.edu       (520) 591 - 0345

    Andrew Kirima      Software Engineer       andrewkirima@email.arizona.edu  (509) 619 - 3496

                       Systems Engineer

    Brandi Diesso      Information Scientist   bdiesso@email.arizona.edu       (516) 330 - 4944

    Claude Merrill     Mentor                  claudemerrill@email.arizona.edu (520) 444 - 3000

    Catherine Merrill  Mentor                  cdmerrill@email.arizona.edu     (520) 445 - 9902

    Sharon ONeal       Reviewer                sharononeal@email.arizona.edu   (520) 822 - 4040
    ================== ======================= =============================== ================

----------------------------
Foreign Citizen Restrictions
----------------------------

ITAR (International Traffic and Arms Regulation) restrictions do not apply to this project.

Foreign citizens may work on this project with no further restrictions than what is placed on
citizens of the U.S.

-------------------------------
Non-Disclosure Agreements (NDA)
-------------------------------

Personnel working on this project or anyone who is privileged with technical information regarding
this project must first sign an NDA with Facade Technologies Inc.

If you believe a breach of contract has been or is being made, please contact the team lead.

----------------------------
Intellectual Property Rights
----------------------------

All artifacts and information related to and produced as a result of this project are legally
protected under the non-disclosure agreements signed by key personnel. Said artifacts are solely
the property of Facade Technologies Inc.

------------------------
Facilities and Equipment
------------------------

.. table:: Facilities

    =================================== ================================================================
    Name                                Description
    =================================== ================================================================
    University of Arizona Libraries     The team will reserve private rooms in the libraries for team
                                        meetings.
    =================================== ================================================================

.. table:: Equipment

    =================================== ================================================================
    Name                                Description
    =================================== ================================================================
    Jira                                Used for planning and tracking work among the team.
    GitHub                              Used for maintaining and developing software with a team.
    Slack                               Used for communicating with all members of the team.
    PC (Personal Computers)             Team members provide their own computers that run Windows 10.
    =================================== ================================================================

----------------------------
Customer Furnished Equipment
----------------------------
Façade Technologies Inc. will provide company polo shirts containing the Façade Logo. Façade
Techonologies Inc. will also provide food for the design team during some review meetings.

--------------
Estimated Cost
--------------

The senior design team has a $4,000 budget that may only be used to complete this project. The
team estimates the actual cost will be under $2,000.

.. todo::
    Fill in cost tables for proposal (Do we need to update these?)

---------------------------
Sub-Contractors/Consultants
---------------------------

Facade Technologies Inc. and the design team will not be sub-contracting any part of this project.

----------
Signatures
----------

.. image:: ../../images/proposal_signatures.png
    :align: center
    :alt: Signatures of approval from all team members, mentor, and sponsor
