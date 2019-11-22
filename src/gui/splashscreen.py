"""

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

This file contains the 
"""
from PySide2 import QSplashScreen
import time

class FacileSplashScreen(QSplashScreen):

	def __init__(self):
		self.setWindowTitle('Facile')

	def setPixmap(QPixmap):
		splash_pix = QPixmap('facade_logo.png'')
		splash = QSplashScreen(splash_pix)
		progress_bar = QProgressBar(splash)
		progress_bar.setMaximum(10)
		progress_bar.setGeometry(0,splash_pix.height() - 50, splash_pix.width(), 20)
		splash.show()
		splash.showMessage()




