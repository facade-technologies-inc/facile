
***********************
Risk Analysis
***********************

.. todo::
	Insert Risk Analysis introduction
	
.. csv-table:: Risk summary
	:widths: 30 100 150 50
	:header: "Risk #", "Name", "Statement", "Category"
	:file: C:/Users/smalb/facade-technologies-inc/facile/documentation/Risk/source/auto_generated_risk_summary.csv
	
.. csv-table:: Risk Severities
	:widths: 30 70 70 70 50
	:header: "Risk #", "Likelihood (0-1)", "Consequence (0-1)", "Criticality (0-1)", "Action"
	:file: C:/Users/smalb/facade-technologies-inc/facile/documentation/Risk/source/auto_generated_risk_severity.csv
	
.. figure:: C:/Users/smalb/facade-technologies-inc/facile/documentation/Risk/source/auto_generated_risk_matrix.png
	:alt: A visual representation of risk severity
	
	A visual representation of risk severity

---------------------
Risk Descriptions
---------------------

An in-depth description of all documented risks is given below. The risks are sorted by
criticality in descending order.


================================================================================
Risk 1 - Old project incompatibility
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 1

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               1.0 |                0.6   |                0.6   |
	+-------------------+----------------------+----------------------+
	

Changes to the source code may result in old projects being incompatible with newer versions of Facile.

If data is serialized (written to disk as binary files) there may be problems with deserializing data (constructing objects from binary files) because the newer classes don't match the older classes.

We plan to **Mitigate** this risk by following this plan:

Look into other project formats that are not dependent on source code remaining unchanged.


================================================================================
Risk 2 - GUI Component Reidentification
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 2

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.6 |                0.8   |               0.48   |
	+-------------------+----------------------+----------------------+
	

We may not be able to reidentify GUI components consistently.

Component reidentification relies heavily on the functionality and reliability of the component token generation and comparison processes. Since tokens will rarely be 100% similar, there is always a risk of misidentifying a component or vice versa, and it is difficult to estimate at this time the average success rate that will come from the component reidentification

We plan to **Mitigate** this risk by following this plan:

Find as many unique identifiers as possible to store in tokens, and develop an algorithm/statistical method to compare two tokens with a certain probability of certainty


================================================================================
Risk 3 - Index Organization
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 3

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.4 |                1.0   |                0.4   |
	+-------------------+----------------------+----------------------+
	

We may fail to make sure the index that has been deleted is actually the index that was supposed to be deleted.

If the wrong index gets deleted it could crash the program.

We plan to **Mitigate** this risk by following this plan:

Provide a unique identifier to each data item and be sure to save the latest item if each have the same data.


================================================================================
Risk 4 - Reconstructing project structure
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 4

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.4 |                0.8   |               0.32   |
	+-------------------+----------------------+----------------------+
	

It is possible that not all internal data can be easily reconstructed when a project is loaded by simply using the pickle module.

There may be a specific order required to rebuild internal data structures that were created before a project was saved and closed.

We plan to **Watch** this risk by following this plan:

Determine which data structures are pickleable and which ones will need to be recreated by calling constructors.


================================================================================
Risk 5 - Visibility Behavior Conditionals
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 5

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.4 |                0.4   |               0.16   |
	+-------------------+----------------------+----------------------+
	

We may fail to come up with a system for allowing the user to define logical conditions determining if visibility behaviors are followed.

A visibility behavior may be dependant on whether user input in the target GUI is valid. Therefore visibility behaviors should be configurable to reflect this reality. This will require that a visibilty behavior contain information about how to get data from the target GUI. How to implement this functionality is unclear.

We plan to **Watch** this risk by following this plan:

Develop the VisibilityBehavior class so it contains a Conditional class. The Conditional class will have references to the target GUI components which contain the data that will be used in the conditional statement.


================================================================================
Risk 6 - Restoring graphics upon load
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 6

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.4 |                0.3   |               0.12   |
	+-------------------+----------------------+----------------------+
	

When a project is loaded, it may be difficult to restore the graphics to their original state.

The Graphics will rely on the underlying data structure for the target GUI AND manual positioning.

We plan to **Mitigate** this risk by following this plan:

Make sure to store coordinates, sizes, colors, line weight, etc. of each item that is in the graphics view so that the objects can be serialized/deserialized easily.


================================================================================
Risk 7 - Target GUI Incompatability
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 7

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.6 |                0.2   |               0.12   |
	+-------------------+----------------------+----------------------+
	

We may fail to detect that a target GUI is incompatible.

If the user chooses an application that was not developed with one of the compatible frameworks (MFC, VB6, VCL, WinForms, WPF, Store apps, and Qt5) then we won't be able to detect GUI components correctly.

We plan to **Mitigate** this risk by following this plan:

When application is started, probe for components. If None were found inside the main window, raise an exception.


================================================================================
Risk 8 - GUI Mapping Incompatability
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 8

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.2 |                0.6   |               0.12   |
	+-------------------+----------------------+----------------------+
	

We may fail to map one or more components and behaviors in the target GUI.

If the GUI contains component or behavior that is not included in one of the compatible frameworks (MFC, VB6, VCL, WinForms, WPF, Store apps, and Qt5), Facile may not be able to map the component or behavior.

We plan to **Mitigate** this risk by following this plan:

If an exception arises, rise a flagg in the software.


================================================================================
Risk 9 - Speed Requirement
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 9

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.4 |                0.2   |               0.08   |
	+-------------------+----------------------+----------------------+
	

We may fail to map the GUI under 1 min.

If the GUI contains a large number of components, Facile may not be able to display in the entire GUI in a relatively short time.

We plan to **Mitigate** this risk by following this plan:

Improve the algorithm. Save time on traversing.


================================================================================
Risk 10 - Bad User-defined Visibility Conditionals
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 10

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.2 |                0.2   |               0.04   |
	+-------------------+----------------------+----------------------+
	

A user may define illogical visibility behavior conditionals.

Illogical visibility behavior conditionals may affect how the "API Modules" are defined.

We plan to **Mitigate** this risk by following this plan:

We will catch these invalid behaviors with the validator to make the user change them before compilation.


================================================================================
Risk 11 - Overuse of RAM
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 11

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.2 |                0.2   |               0.04   |
	+-------------------+----------------------+----------------------+
	

We may fail to use less than or equal to 2 GB of RAM while operating.

If the user has big projects or projects that have been open for a while, the indexes could go out of scope and get deleted.

We plan to **Mitigate** this risk by following this plan:

Use a custom data structure that removes irrelevant persistent indexes.


================================================================================
Risk 12 - Input of Properties
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 12

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.2 |                0.2   |               0.04   |
	+-------------------+----------------------+----------------------+
	

We may fail to compact what a user can input into the property editor.

If the editor is to flexible then improper data could be added.

We plan to **Mitigate** this risk by following this plan:

Implement a function to constrict the kind of properties that will be accepeted.


================================================================================
Risk 13 - Property Values
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 13

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.2 |                0.2   |               0.04   |
	+-------------------+----------------------+----------------------+
	

We may fail to display values of a property as a drop down menu.

If the values aren't found as a drop down menu then it would be just inefficient for the user.

We plan to **Mitigate** this risk by following this plan:

Implement a function to have the model displayed as a drop down menu.


================================================================================
Risk 14 - Size the component
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 14

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.0 |                0.4   |                0.0   |
	+-------------------+----------------------+----------------------+
	

The size of the parent node may not be able to hold the children nodes.

If the user adds a extensive amount of components under one window, the window may not have enough space to hold all the widgets.

We plan to **Mitigate** this risk by following this plan:

Design the window in a way that it could automatically re-size itself to hold all the new widgets.


================================================================================
Risk 15 - Arrow routing
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 15

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.0 |                0.2   |                0.0   |
	+-------------------+----------------------+----------------------+
	

The arrow may be directed to the target component in a straight line.

One arrow may need to go around different components to go to the tartget widegt.

We plan to **Mitigate** this risk by following this plan:

Design an alogorithm to allow the arrow to go through the entire mapped GUI to find the target component.


================================================================================
Risk 16 - Visibility Behavior QtModel interface
================================================================================

.. table:: Likelihood, Consequence, and Criticality of risk 16

	+-------------------+----------------------+----------------------+
	| Likelihood (0-1)  | Consequence (0-1)    | Criticality (0-1)    |
	+===================+======================+======================+
	|               0.0 |                0.8   |                0.0   |
	+-------------------+----------------------+----------------------+
	

We may fail to implement the QtModel for visibility behaviors.

The QtModel is the part of Qt's model/view framework which will interface views to the underlying model data. The developer has yet to prototype this.

We plan to **Mitigate** this risk by following this plan:

Prototype the QtModel using example code as a guide.


