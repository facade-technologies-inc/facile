
.. raw:: latex

    \setcounter{page}{1}

------------------
Change Control Log
------------------

+-----------------+------------------+--------------+------------------------------+
| Release Version | Internal Version | Last Updated | Approved By                  |
+=================+==================+==============+==============================+
| B               | 1                | 03/02/2020   | Nikhith Vankireddy           |
+-----------------+------------------+--------------+------------------------------+

.. todo:: Fill out change log
+----------------+--------------------------------------------+--------------------------------------------+--------------+-------------+------------+
| Change Log No. | Change Description                         | Rationale                                  | Class Change | Approved By | Date       |
+================+============================================+============================================+==============+=============+============+
| 1              |                                            |                                            |              |             |            |
+----------------+--------------------------------------------+--------------------------------------------+--------------+-------------+------------+


.. todo:: Definitions
    - Action
    - Action Pipeline
    - API
    - Component Action
    - Facile
    - Facile API
    - GUI
    - Interferometer
    - IPC
    - Target Application

-----------------------
Deliverable Description
-----------------------

Due to the ambiguous nature of this project, a high-level overview of the entire Facile system may provide clarity and
insight into the work accomplished during iterations one and two. Detailed use-cases are also provided to give context
as to how Facile APIs can be used and why they're useful.

~~~~~~~~~~~~~~~
System Overview
~~~~~~~~~~~~~~~
The Facile system is used to create custom Python APIs (Facile APIs) that have the ability to control existing graphical
user interfaces. The generated APIs have a variety of uses, allowing users of the API to write programs that:

- Automate repetitive tasks.
- Automate the GUI testing process.
- Make multiple applications communicate that use Facile APIs as an ad hoc form of IPC.
- Create new user interfaces that are bound to the the old user interface via a Facile API.

Because Facile APIs have a variety of uses, they are more flexible than existing automation solutions that are either
focused on automating repetitive tasks, or automating the GUI testing process. Furthermore, existing automation
solutions are either code-less meaning they can't easily be integrated into other software products, or they involve so
much coding to use that someone without programming experience can't use them easily.

Facile APIs provide a happy medium; they're easy to for someone with little or no programming experience to create and
use, and they're flexible enough to be integrated into larger software products. The simplicity is achieved by producing
an API that is tailored both to the target application and to the user's needs.

So how do we allow the user to create a custom API that's tailored both to the target application and the user's needs?
We build two models; the first is called the **Target GUI Model** and the second it called the **API Model**.

The Target GUI Model describes what components make up the target GUI and how the target GUI behaves. This model is
built semi-automatically by analyzing the target GUI to identify its constituent components (such as windows, buttons,
editors, etc.), then allowing the user to describe how the GUI responds to specific actions (such as clicking a button).

The API Model describes actions that the user wants to perform in the target GUI. This is done by creating a set of
*action pipelines* which have inputs, outputs, and internal logic. The internal logic of the action pipelines can
directly link to components in the Target GUI Model, which in turn describe an actual component in the target GUI.
A more detailed description of this will be given later, but it's important to note that functions in most programming
languages also have this same structure - indeed the action pipelines will be translated directly to Python code in the
generated API.

Upon sufficient description of the API, the user may elect to generate the custom API by running the **API Compiler**.
Performing this action will generate the API in a specified directory and install the API as a Python package in a
local Python interpreter. The generated API code structure is merely a reflection of the API Model with enough generic
backbone structure to make the API work seamlessly. Data from the Target GUI Model is stored with the API and is used by
the API to interact with the correct components. The API also comes with complete documentation that's generated using
annotations given by the user.

From this description, the process to build a Facile API can be broken down into three steps:

1. Build the Target GUI Model (with annotations).
#. Build the API Model (with annotations).
#. Compile the Facile API.

.. todo:: Include image of three steps and link to it somewhere in the text above.

.. todo:: Show SBD and give description

~~~~~~~~~
Use Cases
~~~~~~~~~

Previously, it was claimed that Facile APIs have the following uses:

- Automate repetitive tasks.
- Automate the GUI testing process.
- Make multiple applications communicate that use Facile APIs as an ad hoc form of IPC.
- Create new user interfaces that are bound to the the old user interface via a Facile API.

*Mahr Metrology Inc.* (Mahr) will be used as the subject to demonstrate both the practicality and value of each of these
uses of Facile APIs. To understand why Mahr would use a Facile API, Mahr's background and current position must be
understood.

Mahr is a company based in Germany that has a small optics branch (Mahr Opto) located in Tucson. This branch came from
an acquisition of a small company called Engineering Synthesis Design Inc., which produced interferometers and software
called *IntelliWave* that was used to interface with their interferometers, but was also compatible with their
competitor's interferometers. IntelliWave was developed by just a handful of engineers who didn't have formal software
development training over the course of about 20 years. As such, IntelliWave has grown into an unintuitive product that
has many bugs - in fact, Mahr is unsure of IntelliWave's accuracy. This has caused many customers to leave Mahr and go
to their competitors such as Zygo that have products which perform better and have more trusted results. The customers
that stay with Mahr mostly stay because Mahr's pricing points are significantly lower than Mahr's competitors.

Because IntelliWave was created by a few engineers who didn't put the effort into documenting their code or verifying
the accuracy of its results, Mahr is having a hard time making fixes and has decided that continually making fixes to an
outdated technology is not sustainable and not worth the time in the long run. Doing so would be fighting an uphill
battle. This leaves Mahr with three possible options:

1. Mahr doesn’t change IntelliWave. They’ll continue to lose customers to their competitors and Mahr Opto will die
   slowly.

#. Mahr can rebuild IntelliWave. This will cost millions of dollars and many years to complete given their small
   software engineering team. They also run the risk of making another product that can’t keep up with competitors and
   won’t put them in a better position. If successful, they'll have a new product to add to their product line, but at a
   high cost.

#. Mahr can get creative with 3rd party solutions to hide IntelliWave’s flaws, test its results, and provide new
   functionality.

Option #3 is where Facile comes into play. Using a Facile API, Mahr can do quite a bit:

1. **Automate Repetitive Tasks**: IntelliWave already has a builtin automation feature that allows the user to write
   scripts in a custom environment and then replay those same actions. For instance, the user could write a script to
   read in a file containing fringe data for a lens that was measured previously, fetch the aberration data, export the
   data, then repeat with a different lens profile. This feature is incredibly buggy in IntelliWave, but it does allow
   users to
   automate simple actions. The major drawbacks of this feature are:

   a. It requires the user to become familiar with IntelliWave's automation platform - it's like learning a new
      language, and it doesn't always behave as expected.

   #. It doesn't allow other programs to automate actions in IntelliWave very easily. To get around this, IntelliWave
      has a built-in server that will accept commands, but this feature has countless bugs as well!

   A user of IntelliWave would benefit from having a Python API to control IntelliWave. This would let the user program
   in a widely-used language with much more support and bypass the bugs in the automation platform. Mahr is currently
   working on their own Python API that controls the user interface of IntelliWave, but the single API has been in the
   making for over a year and has some performance drawbacks. Mahr is deciding whether to release the API to its
   customers, or keep it for internal use. This will be discussed more in point 4 (Creating New User Interfaces).

   The drawbacks of Mahr's Python API is that it has to be maintained by developers since it's been manually crafted.
   This is expensive and could be mostly automated through Facile. Although a Facile API could replace Mahr's current
   API and would only take a few days to create, Mahr may not want to get rid of all their hard work. For this reason,
   Facile APIs are designed to work in cooperation with APIs like Mahr's.

   An example of an operation that could be performed automatically is measuring the radius of curvature of a lens. To
   do this manually, has to place the lens, then click a series of buttons to open a dialog that shows the radius of
   curvature along with some other statistics. A Facile API could be used to perform all of the button clicks and obtain
   the desired data from the GUI. This would allow the user to simply position a lens and run a script. If they're
   measuring lenses all the time, this could save a lot of time.

#. **Automated GUI Testing**: With an application as large as IntelliWave, testing can be very costly and take a long
   time to perform thoroughly. Ideally, IntelliWave should be tested thoroughly after any changes, but it's too
   expensive for Mahr to do. Facile APIs could greatly help in this matter. By writing testing scripts that use a Facile
   API to perform user interactions, Mahr could more easily identify whether IntelliWave is behaving correctly which
   would allow them to deliver better products to their customers more confidently.

   Mahr is very interested in performing automated tests. This was one of the factors that led them to build their own
   API for IntelliWave. Mahr is considering doing a complete rebuild of IntelliWave, but they want to know which
   calculations IntelliWave performs correctly so that they can figure out which algorithms can be copied and which ones
   need to be reworked. Of course, this requires someone with a lot of knowledge of optics to build the testing scripts,
   but any testing method requires this.

.. todo:: resume here
#. **Making Multiple Applications Communicate**: IntelliWave generates a lot of statistics about lenses being measured,
   but listing out what all of the statistics are is beyond the scope of this project. These statistics are useful to
   many of Mahr's clients, but often the clients wish to have the data exported into specific formats to they can be
   loaded into various programs


1.	They can perform automated tests easier by using the Facile API to perform user interactions, get results, and compare them to results that are known to be true. A single round of testing can cost tens of thousands of dollars when done manually on an application as large as IntelliWave and even then, complete testing is unlikely. Automating the testing procedure could save Mahr hundreds of thousands, possibly millions of dollars in the long run, and allow better products to be developed faster.

Mahr can even create Facile APIs for competitor products to compare results. This would give them a competitive edge by effectively letting their competitors check for bugs in their product.

2.	A Facile API could be a partial remedy for IntelliWave’s unintuitive user interface. Not by changing it directly, but by acting as the glue between it and a different user interface. Mahr can satisfy their customers’ needs more directly by providing custom graphical user interfaces that simply use IntelliWave as a backend. These custom graphical user interfaces can be developed extremely quickly (in a matter of days possibly) using tools such as Qt Creator.


-------------------------------
System Verification Plan / SRVM
-------------------------------

-----------------------------
Configuration Management Plan
-----------------------------

-----------------------------
Indentured Document List
-----------------------------

.. raw:: latex

    INSERT_DOC=IDL

-----------------------------
System Requirements Document
-----------------------------

.. raw:: latex

    INSERT_DOC=SRD

--------------------------
Verification Documentation
--------------------------

.. raw:: latex

    INSERT_DOC=Verification

------------------------
Hardware Drawing Package
------------------------

.. raw:: latex

    INSERT_DOC=HDP

----------------------------
Software Drawing Package
----------------------------

.. raw:: latex

    INSERT_DOC=SDP

-------------------------------------
Software Version Description Document
-------------------------------------

.. raw:: latex

    INSERT_DOC=SVDD

--------------------------
Software Design Document
--------------------------

.. raw:: latex

    INSERT_DOC=SDD

-----------
Models
-----------

.. raw:: latex

    INSERT_DOC=Models


-----------
User Manual
-----------

.. raw:: latex

    INSERT_DOC=UserManual

------------------------
Client Feedback Document
------------------------

.. raw:: latex
    INSERT_DOC=CFD
