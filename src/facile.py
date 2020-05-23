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

sys.path.append(os.path.abspath("./gui/rc/"))

# These lines are needed to integrate Qt and pywinauto
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

from PySide2.QtWidgets import QApplication

import gui.frame.windows as windows

from gui.facileview import FacileView
from gui.splashscreen import FacileSplashScreen
import psutil


if __name__ == "__main__":

    # increases performance by hogging more processor time
    p = psutil.Process()
    p.nice(psutil.HIGH_PRIORITY_CLASS)
    
    app = QApplication([])

    splash = FacileSplashScreen()
    splash.show()
    view = FacileView()
    window = windows.ModernWindow(view, modal=False)
    splash.finish(window)
    window.showMaximized()
    
    sys.exit(app.exec_())
