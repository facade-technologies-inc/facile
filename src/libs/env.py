"""
..
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

This file contains information about the environment that Facile is running in.
"""

import os

TEMP_DIR = os.path.abspath("./temp/")
LOG_FILES_DIR = os.path.join(TEMP_DIR, "log_files/")

class NotAModuleException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ContextNotAvailableException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def getContext(modulepath: str):
    """
    Given the filepath of a python module in this project, we can determine the context of where it's located. This is
    important for determining where to import modules from. The possibe contexts are:

    - Facile: If we're running code as part of Facile.
    - Sphinx: If sphinx is importing our modules.
    - API:    If we're running code as part of a generated API.

    This function should be modified to obtain various context responses as needed. At the time of original creation,
    not all scenarios are known.

    :raises: NotAModuleException if the modulepath is not a path to a module.
    :raises: ContextNotAvailable if a decision about the context of the module could not be made for any reason.

    :param modulepath: The path to a specific module that we want to get the context for.
    :type modulepath: str
    :return: The appropriate context: "Facile", "Sphinx", or "API"
    :rtype: str
    """

    if not os.path.exists(modulepath):
        raise NotAModuleException(f"{modulepath} does not exist")

    elif not modulepath.endswith(".py"):
        raise NotAModuleException(f"{modulepath} is not a python module")

    context = None
    path, file = os.path.split(modulepath)

    facile_detector = f"{os.sep}facile{os.sep}src{os.sep}"
    if facile_detector in modulepath:
        context = "Facile"

    elif file in ["application.py", "baseapplication.py"]:
        sphinx_src = os.path.join(path, "Documentation", "src")
        if os.path.exists(sphinx_src):
            context = "Sphinx"

    if not context:
        context = "API"

    # Note: If there is a problem with detecting the context correctly, the following lines help with debugging:
    # print(f"\n{100*'='}")
    # print(f"Module Path: {modulepath}")
    # print(f"Context:     {context}")
    # print(f"{100 * '='}")

    if not context:
        raise ContextNotAvailableException(f"Can't detect context of module: {modulepath}")

    return context
