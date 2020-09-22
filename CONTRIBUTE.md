# Contributor's Guide (Team #19033)
This guide describes how to properly contribute to the facile project. Before developing, please read this document thoroughly.

## Copyright Banner
The following banner __must__ be the first thing to appear in every module's Docstring:
```
/------------------------------------------------------------------------------\
|                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
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
```


## Developer Tools
The following tools will be used by the development team while working on this project. Developers will be expected to use these tools throughout the duration of this project.

| Tool      | Version  | purpose |
|------     |---------:|---------|
|Python     |3.7.4     |[Tutorial](https://github.com/facade-technologies-inc/facile/blob/master/tutorials/Python.md) - This entire project will be programmed in Python.|
|PyCharm    |2019.1.3  |[Tutorial](https://github.com/facade-technologies-inc/facile/blob/master/tutorials/PyCharm.md) - Used for Python development. Includes great linters to help developers keep to style guidelines and includes debugger as well as many other tools. |
|Qt Creator |4.10.0    |[Tutorial](https://github.com/facade-technologies-inc/facile/blob/master/tutorials/Qt5.md) - GUI development toolset. We'll be using PySide2 (a Python Qt wrapper) to create the GUI.|
|Git        |2.23.0    |[Tutorial](https://github.com/facade-technologies-inc/facile/blob/master/tutorials/Git.md) - Used for version control|

Note: We highly recommend you configure a virtual environment using PyCharm. Refer to this link: https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

## Git Branching Scheme
This repository uses the [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branching scheme with the following caveats:

  1. Click on the upper green "Code" button and copy our SSH key.
  1. On your PC's File Explorer, go to the destination you want to store Facile and clone the repository. 
  1. Create a new branch to work on. Make sure the name of the branch is detailed on the feature/issue that you are working on. 
  1. Once you are done with you're work, committ the changes (Please add an insightful description of what you completed for every commit).
  1. The `git flow <subcommand> finish <branch>` commands are never used. Instead, when you would like a branch to be merged, simply push the branch to GitHub and submit a pull request.
  Refer to this link for Pull Request: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews#about-pull-request-reviews

## Coding Standards
By default, this project will be developed to the [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) standards. Any preferred deviations from these styles are specified below:
  1. All Docstrings will use the [reST format](http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html).
  1. Every module, class, and function must have a Docstring that sufficiently describes the purpose of it.
  1. For methods and functions, Docstrings must specify parameters, parameter types, exceptions that can be thrown, and return types as well as a description of what the function or method does.
