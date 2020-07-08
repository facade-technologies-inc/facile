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

.. note::
    This file makes extensive use of global variables because they're meant to be almost read-only.
"""

import os
import sys

CONTEXT = "API"                         # "Facile", "Sphinx", or "API" depending on where the process was started from.

####################################
# Only set when CONTEXT is "Facile"
####################################
FACILE_ENTRY_MODE = ""                  # "EXE" or "PY" depending on how facile was run.
FACILE_DIR = ""                         # Working directory when Facile was started
TEMP_DIR = ""                           # temp/ directory
LOG_FILES_DIR = ""                      # temp/log_files/ directory

class InvalidContextException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def updateContext(newContext:str):
    """
    Updates the context to "Facile", "Sphinx", or "API".

    This function should only be called from facile.py or conf.py

    .. warning::
        Calling this function from the wrong spot will undoubtedly fuck things up.

    :param newContext: One of the possible values mentioned above.
    :type newContext: str
    :return: None
    """
    if newContext not in {"Facile", "Sphinx", "API"}:
        raise InvalidContextException(newContext)

    global CONTEXT, TEMP_DIR, LOG_FILES_DIR, FACILE_ENTRY_MODE, FACILE_DIR
    CONTEXT = newContext

    # Clear other global variables - some will be set and some may not.
    FACILE_ENTRY_MODE = ""
    FACILE_DIR = ""
    TEMP_DIR = ""
    LOG_FILES_DIR = ""

    # -- Update other global environment variables ---------------------------------
    if CONTEXT in {"Facile"}:
        if sys.executable.endswith("facile.exe"):
            FACILE_ENTRY_MODE = "EXE"
            active_file = sys.executable
        else:
            FACILE_ENTRY_MODE = "PY"
            active_file = sys.argv[0] # the python file

        FACILE_DIR = os.path.dirname(active_file)
        TEMP_DIR = os.path.abspath(os.path.join(FACILE_DIR,"temp"))
        LOG_FILES_DIR = os.path.abspath(os.path.join(TEMP_DIR, "log_files"))
