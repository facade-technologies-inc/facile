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

This is the main file that launches Facile. This module should only be run by the
user and never imported.

"""

import sys
import os
import warnings
import libs.env as env
env.CONTEXT = "Facile"

sys.path.append(os.path.abspath("./gui/rc/"))

# These lines are needed to integrate Qt and pywinauto
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

from PySide2.QtWidgets import QApplication

from gui.facileview import FacileView
from gui.splashscreen import FacileSplashScreen
import psutil

from libs.logging import archive_logs, root_logger

if __name__ == "__main__":
    archive_logs()
    root_logger.info("Initializing Application")

    # increases performance by hogging more processor time
    p = psutil.Process()
    p.nice(psutil.HIGH_PRIORITY_CLASS)
    
    app = QApplication([])

    splash = FacileSplashScreen()
    splash.show()

    view = FacileView()

    splash.finish(view)
    view.showMaximized()

    root_logger.info("Launching Facile")
    status = app.exec_()

    exit_msg = f"Facile has been terminated. Exiting with status: {status}"
    if status:
        root_logger.error(exit_msg)
    else:
        root_logger.info(exit_msg)
    sys.exit(status)
