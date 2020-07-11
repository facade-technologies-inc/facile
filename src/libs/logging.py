"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2020] Facade Technologies Inc.                                 |
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

This module contains all logging-related code.

Important: This module should only be loaded a single time. If a reload is forced, logging will be split into multiple
files.
"""

import os
import shutil
import logging.config
from datetime import datetime
import benedict

from libs.env import TEMP_DIR, LOG_FILES_DIR

initial_timestamp = datetime.now().strftime("%Y-%m-%d~%Hh-%Mm-%Ss")

def archive_logs():
    """
    Moves all log files into their own directory with a unique timestamp. The idea is that we're cleaning up any
    lingering log files.
    """
    # make sure all necessary directories exist.
    for directory in [TEMP_DIR, LOG_FILES_DIR]:
        if not os.path.exists(directory):
            os.mkdir(directory)

    # move all loose files into directories.
    for file in os.listdir(LOG_FILES_DIR):

        if initial_timestamp in file:
            continue

        full_file = os.path.join(LOG_FILES_DIR, file)
        if os.path.isfile(full_file):
            prefix = file.split("_")[0]
            curFile = os.path.join(LOG_FILES_DIR, file)
            newLogDir = os.path.join(LOG_FILES_DIR, f"{prefix}_logs")
            newFile = os.path.join(newLogDir, file)

            if not os.path.exists(newLogDir):
                os.mkdir(newLogDir)

            shutil.move(curFile, newFile)

archive_logs()

########################################################################################################################
# LOGGING CONFIGURATION:                                                                                               #
#   The logging_config_YAML variable dictates how logging will be performed and which loggers are available. More can  #
#   be read here: https://docs.python.org/3/library/logging.html                                                       #
########################################################################################################################

logging_config_YAML = f"""

version: 1

formatters:
  short:
    format: '%(name)s - %(levelname)s - %(message)s'
  medium:
    format: '%H:%M:%S - %(name)s - %(levelname)s - %(message)s'
  long:
    format: '%Y-%m-%d %H:%M:%S - %(name)s - %(levelname)s - %(message)s'
  precise:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers:
  null_handler:
    class: logging.NullHandler
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: short
    stream: ext://sys.stdout
  main:
    class: logging.FileHandler
    level: DEBUG
    formatter: precise
    filename: {os.path.join(LOG_FILES_DIR, f"{initial_timestamp}_facile.log")}
  compilerFile:
    class: logging.FileHandler
    level: DEBUG
    formatter: precise
    filename: {os.path.join(LOG_FILES_DIR, f"{initial_timestamp}_facile_compiler.log")}
  explorerFile:
    class: logging.FileHandler
    level: DEBUG
    formatter: precise
    filename: {os.path.join(LOG_FILES_DIR, f"{initial_timestamp}_facile_explorer.log")}

loggers:
  facile:
    level: DEBUG
    handlers: [main]
    propagate: no
  facile.compiler:
    level: DEBUG
    handlers: [compilerFile]
    propagate: yes
  facile.explorer:
    level: DEBUG
    handlers: [explorerFile]
    propagate: yes

root:
  level: DEBUG
  handlers: [main]
"""

logging.config.dictConfig(benedict.load_yaml_str(logging_config_YAML))

########################################################################################################################
# LOGGERS:                                                                                                             #
#   A variety of loggers can be used to separate logging information in logical ways. As new loggers are added, they   #
#   also need to be added to the YAML config string above. For more information, see:                                  #
#                                    https://docs.python.org/3/library/logging.html                                    #
# - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -#
# USE:                                                                                                                 #
#   Using the loggers is simple. First, you need to import the proper one from the list below. For example:            #
#                                                                                                                      #
#   >>> from libs.logging import main_logger as logger                                                                 #
#                                                                                                                      #
#   Then, you can output whatever information you want using the following functions:                                  #
#                                                                                                                      #
#   >>> logger.debug("Some debug info")                                                                                #
#   >>> logger.info("Your information message")                                                                        #
#   >>> logger.warning("A warning message")                                                                            #
#   >>> logger.error("a non-fatal error message")                                                                      #
#   >>> logger.critical("You really fucked up.")                                                                       #
#   >>> try:                                                                                                           #
#   >>>     a = 1 + "a"                                                                                                #
#   >>> except Exception as e:                                                                                         #
#   >>>     logger.exception(e)                                                                                        #
########################################################################################################################

root_logger     = logging.getLogger("root")                     # PURPOSE: Prolog/Epilog information
main_logger     = logging.getLogger("facile")                   # PURPOSE: General application information
explorer_logger = logging.getLogger("facile.explorer")          # PURPOSE: Explorer/Observer related information
compiler_logger = logging.getLogger("facile.compiler")          # PURPOSE: Compiler/Doc Generator related information


def log_exceptions(logger: logging.Logger = main_logger, suppress: bool = False):
    """
    A decorator to automatically log any unhandled exceptions that occur within a function.

    The exceptions are raised again after logging if suppress is set to False.

    .. seealso::
        If you don't know about decorators, they're really useful! You can read about them here:
        https://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html

    :param logger: The logger to use to do the logging.
    :type logger: logging.Logger
    :param suppress: If True, the caught exceptions will not be raised again after logging.
    :type suppress: bool
    """
    def wrapper(f):
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                if not suppress:
                    raise e
        return wrapped
    return wrapper