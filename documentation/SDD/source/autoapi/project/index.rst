:orphan:

:mod:`project`
==============

.. py:module:: project

.. autoapi-nested-parse::

   ..
       /------------------------------------------------------------------------------    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
       |------------------------------------------------------------------------------|
       |                                                                              |
       |    Copyright [2019] Facade Technologies Inc.                                 |
       |    All Rights Reserved.                                                      |
       |                                                                              |
       | NOTICE:  All information contained herein is, and remains the property of    |
       | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
       | and technical concepts contained herein are proprietary to Facade            |
       | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
       | Patents, patents in process, and are protected by trade secret or copyright  |
       | law.  Dissemination of this information or reproduction of this material is  |
       | strictly forbidden unless prior written permission is obtained from Facade   |
       | Technologies Inc.                                                            |
       |                                                                              |
       \------------------------------------------------------------------------------/

   This module contains the Project class.



Module Contents
---------------


.. py:class:: Project(name: str, description: str, exe: str, backend: str, projectDir: str = '~/', startupTimeout: int = 10)

   This class is the top level to a Facile Project.
   It stores information about the target application, the target GUI model, the API model, compilation profiles, etc.

   .. note::
           Only one project can be stored in each directory.
           
   .. todo::
           Create custom exceptions and check input in setters
           
   .. todo::
           Store backend as enum instead of string

   Constructs a Project object.

   :param name: The name of the project.
   :type name: str
   :param description: The project description.
   :type description: str
   :param exe: The executable file of the target application.
   :type exe: str
   :param backend: The accessibility technology used to control the target application.
   :type backend: str
   :param projectDir: The directory that the project is stored in.
   :type projectDir: str
   :param startupTimeout: The number of seconds to wait for the target application to startup.
   :type startupTimeout: int
   :return: The constructed project
   :rtype: Project

   .. method:: getObserver(self)


      Gets the project's observer

      :return: The project's observer
      :rtype: Observer


   .. method:: getExplorer(self)


      Gets the project's explorer

      :return: The project's explorer
      :rtype: Explorer


   .. method:: getTargetGUIModel(self)


      Gets the the project's target GUI model.

      :return: The project's target GUI model.
      :rtype: TargetGuiModel


   .. method:: setProjectDir(self, url: str)


      Sets the project's directory.

      :param url: The path to the directory where the project should be saved.
      :type url: str
      :return: None
      :rtype: NoneType


   .. method:: setDescription(self, description: str)


      Sets the project's description

      :param description: The project's description.
      :type description: str
      :return: None
      :rtype: NoneType


   .. method:: setName(self, name: str)


      Sets the name of the project

      :param name: The name of the project
      :type name: str
      :return: None
      :rtype: NoneType


   .. method:: setExecutableFile(self, exe: str)


      Sets the target application of the project.

      :param exe: The executable of the target application
      :type exe: str
      :return: None
      :rtype: NoneType


   .. method:: setBackend(self, backend: str = 'uia')


      Sets the accessibility technology (backend) used to control the target application.

      Defaults to uia.

      :param backend: The accessibility technology used to control the target application
      :type backend: str
      :return: None
      :rtype: NoneType


   .. method:: setStartupTimeout(self, timeout: int)


      Sets the timeout for the target application startup time.

      :param timeout: the timeour for starting up the target application.
      :type timeout: int
      :return: None
      :rtype: NoneType


   .. method:: getName(self)


      Gets the project's name.

      :return: The project's name.
      :rtype: str


   .. method:: getExecutableFile(self)


      Gets the path to the executable file used to startup the target application.

      :return: The target application's executable file.
      :rtype: str


   .. method:: getDescription(self)


      Gets the project's description.

      :return: The project's description.
      :rtype: str


   .. method:: getBackend(self)


      Gets the project's accessibility technology (backend).

      :return: The project's accessibility technology (backend)
      :rtype: str


   .. method:: getStartupTimeout(self)


      Gets the target application's startup timeout.

      :return: the target app's startup timeout
      :rtype: int


   .. method:: getProjectDir(self)


      Gets the directory that the project is located in.

      :return: The project's directory
      :rtype: str


   .. method:: getMainProjectFile(self)


      Gets the project's main file path (the .fcl file)

      :return: The path to the project's .fcl file
      :rtype: str


   .. method:: getTargetGUIModelFile(self)


      Gets the project's target GUI model file path (.tguim)

      :return: The path to the project's .tguim file
      :rtype: str


   .. method:: getAPIModelFile(self)


      Gets the project's API model file path (.apim)

      :return: The path to the project's .apim file
      :rtype: str


   .. method:: startTargetApplication(self)


      Starts the target application

      :return: None
      :rtype: NoneType


   .. method:: stopTargetApplication(self)


      Kills the target application.

      :return: None
      :rtype: NoneType


   .. method:: getProcess(self)


      Gets the process of the target application iff it is running.

      :return: The process object if the target application is running. None if it is not running.
      :rtype: psutil.Process or NoneType


   .. method:: getProjectExplorerModel(self, view: QTreeView)


      Gets a model that allows a Qt tree view to access the data in a limited manner.

      :param view: The view to place the model into
      :type view: QTreeView
      :return: The project explorer model
      :rtype: ProjectExplorerModel


   .. method:: load(mainFile: str)
      :staticmethod:


      Creates a Project object from a .fcl file.

      :param mainFile: The project's .fcl file
      :type mainFile: str
      :return: The project object reconstructed from a .fcl file.
      :rtype: Project


   .. method:: save(self)


      Writes a project out to disk as a set of files. (.fcl, .tguim, .apim)

      :return: None
      :rtype: NoneType


   .. method:: addToRecents(self)


      Adds the project to the recents file.

      :return: None
      :rtype: NoneType


   .. method:: getRecents(limit: int = 0)
      :staticmethod:


      Gets a list of project files that have recently been opened. The number of returned project locations will be
      limited iff the limit is set to an integer greater than 0.

      :param limit: The maximum number of recent projects to return. If limit is less than or equal to zero, the list will not be limited.
      :type limit: int
      :return: a list of all recent project file names
      :rtype: list[str]



