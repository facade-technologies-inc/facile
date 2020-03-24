*****************************
Software Version Desctription
*****************************

Purpose
~~~~~~~

The SVDD is used for defining a specific release of a software. The SVDD provides a description of the contents for a
specific software release, the methods to re-create the software, the known problems and changes from the previous
release. This document is especially important in agile because the team builds multiple MVPs, each of the MVP released
during a design review is marked as a new software release (version) of Facile. The SVDD release contents conform to the
configuration standards established in Facile Iteration Documentation Package Release B1.

Scope
~~~~~

The current release of Facile is 0.3.0, the primary goal of this iteration was to build on the previous release- Facile
0.2.0 by adding extra features and functionalities designed to satisfy the established system requirements of the
project. In Facile 0.3.0 the main feature addition was the ability to let the user build an action pipeline.

Version Description
~~~~~~~~~~~~~~~~~~~

Compatibility
#############

The current release version Facile 0.3.0 is compatible with Windows 10 Home Version 1903.
The current release version Facile 0.3.0 is compatible with Python 3.7.4 and all its associated packages.
The current release version Facile 0.3.0 is compatible with IntelliWave Release 6.7.1.1007.
The current release version Facile 0.3.0 is compatible with Notepad Version 1903.

New Features
############
Facile 0.3.0 introduces the ability to create an API Model (action pipelines) and then generate a simple API.

Known Problems
##############
There are no known problems in the current release version- Facile 0.3.0. However, configuration process has been
established for when a certain bug is found in the current release. As of 03/03/2020 no known bugs exist in Facile
0.3.0.

Build Procedure
###############
Facile 0.3.0 does not include tools to generate an executable file from the source code. Instead, there are scripts that
are run that auto-generate more source code. To run Facile, these scripts must be run first. They are:

- 01_build_icon_resource.py (writes a file that lists all icon files used)
- 02_build_rc.py (generates python code that uses the icons from 01_build_icon_resource.py)
- 03_build_ui.py (generates python code from a set of *.ui files which describe the user interface of Facile)

These scripts must be run in order.

Run Procedure
#############
Because Facile does not yet have an executable file, the python interpreter must be run with facile as an input. To
achieve this, open a command prompt window and type "python facile.py" in Facile's directory.

Installation
############
The current release version Facile 0.3.0 does not support installation. Facile 0.3.0 needs to be downloaded as a Python
package, and the user needs to run the source code to operate the software. The next iteration- FAR is when a Facile
executable file (Facile 1.0.0) shall be released, this file can be installed.

Previous Version
################
The version prior to the current release was Facile 0.2.0. This version was implemented during the first iteration and
was released at Critical Design Review. Facile 0.2.0 allowed the user to create a Target GUI Model, but did not allow
the user to create an API Model or generate an API.




