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
from pathlib import Path

CONTEXT = "API"                         # "Facile", "Sphinx", or "API" depending on where the process was started from.

####################################
# Only set when CONTEXT is "Facile"
####################################
FACILE_ENTRY_MODE = ""                  # "EXE" or "PY" depending on how facile was run.
FACILE_DIR = ""                         # Working directory when Facile was started
FACILE_SRC_DIR = ""                     # <FACILE_DIR>/src if running from python. <FACILE_DIR>/ if running exe.
FACILE_SPHINX_DIR = ""                  # Location of the sphinx_src/ directory
TEMP_DIR = ""                           # <TEMP_DIR>/ directory
LOG_FILES_DIR = ""                      # <TEMP_DIR>/log_files/ directory
COMTYPES_CLIENT_GEN_DIR = ""            # <TEMP_DIR>/comptypes/client/gen/ directory

class InvalidContextException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def update_context(newContext:str):
    """
    Updates the context to "Facile", "Sphinx", or "API".

    This function should only be called from facile.py or conf.py

    .. warning::
        Calling this function from the wrong spot will undoubtedly fuck things up.

    :param newContext: One of the possible values mentioned above.
    :type newContext: str
    :return: None
    """
    global CONTEXT, \
        TEMP_DIR, \
        LOG_FILES_DIR, \
        FACILE_ENTRY_MODE, \
        FACILE_DIR, \
        FACILE_SRC_DIR, \
        FACILE_SPHINX_DIR, \
        COMTYPES_CLIENT_GEN_DIR

    def norm_abs_path(*args, **kwargs):
        path = os.path.normpath(os.path.abspath(os.path.join(*args, **kwargs)))
        return path

    if newContext not in {"Facile", "Sphinx", "API"}:
        raise InvalidContextException(newContext)

    CONTEXT = newContext

    # Clear other global variables - some will be set and some may not.
    FACILE_ENTRY_MODE = ""
    FACILE_DIR = ""
    TEMP_DIR = ""
    LOG_FILES_DIR = ""

    # -- Update other global environment variables ---------------------------------
    if CONTEXT in {"Facile"}:
        if sys.executable.endswith("facile.exe"):
            active_file = sys.executable
            FACILE_ENTRY_MODE = "EXE"
            FACILE_DIR = norm_abs_path(os.path.dirname(active_file))
            FACILE_SRC_DIR = FACILE_DIR
            FACILE_SPHINX_DIR = norm_abs_path(FACILE_DIR, "sphinx_src")
            TEMP_DIR = norm_abs_path(os.environ['USERPROFILE'], "AppData", "LocalLow", "Facile", "temp")
        else:
            active_file = sys.argv[0]  # the python file
            FACILE_ENTRY_MODE = "PY"
            FACILE_DIR = norm_abs_path(os.path.dirname(active_file))
            FACILE_SRC_DIR = FACILE_DIR
            FACILE_SPHINX_DIR = norm_abs_path(FACILE_SRC_DIR, "tools", "doc_generator", "sphinx_src")
            TEMP_DIR = norm_abs_path(FACILE_DIR, "temp")

        LOG_FILES_DIR = norm_abs_path(TEMP_DIR, "log_files")
        COMTYPES_CLIENT_GEN_DIR = norm_abs_path(TEMP_DIR, "comptypes", "client", "gen")

        # other Facile-related environment setup.
        import comtypes.client
        comtypes.client.gen_dir = COMTYPES_CLIENT_GEN_DIR

    # -- Make sure necessary directories exist -------------------------------------
    if TEMP_DIR:
        Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)

    if COMTYPES_CLIENT_GEN_DIR:
        Path(COMTYPES_CLIENT_GEN_DIR).mkdir(parents=True, exist_ok=True)


def dump_vars(logger=None):
    """
    Prints all env variables to stdout (or a logger if provided)

    :param logger: The logger to log the env vars to.
    :type logger: logging.Logger
    """

    if logger:
        pFunc = logger.info
    else:
        pFunc = print

    dump_var_str = f"""
    /==================================================================================================================
    | ENV VARIABLES                                                                                                    
    ===================================================================================================================
    |
    |    CONTEXT:                   {CONTEXT}
    |    FACILE_ENTRY_MODE:         {FACILE_ENTRY_MODE}
    |    FACILE_DIR:                {FACILE_DIR}
    |    FACILE_SRC_DIR:            {FACILE_SRC_DIR}
    |    FACILE_SPHINX_DIR:         {FACILE_SPHINX_DIR}
    |    TEMP_DIR:                  {TEMP_DIR}
    |    LOG_FILES_DIR:             {LOG_FILES_DIR}
    |    COMTYPES_CLIENT_GEN_DIR:   {COMTYPES_CLIENT_GEN_DIR}
    |
    \\==================================================================================================================
    """

    pFunc(dump_var_str)

updateContext = update_context
dumpVars = dump_vars
