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

This file contains the FacileSplashScreen class which creates a loading window before the application
is started up.

"""
from PySide2.QtWidgets import QSplashScreen, QApplication
from PySide2.QtGui import QPixmap, Qt

class FacileSplashScreen(QSplashScreen):
	"""
	FacileSplashScreen class sets the logo picture to display on the splash screen
	"""
	def __init__(self):
		QSplashScreen.__init__(self)
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		height = QApplication.instance().primaryScreen().size().height() * .25
		width = QApplication.instance().primaryScreen().size().width() * .25
		
		logo = QPixmap('../resources/splash_screen_02.png').scaledToHeight(height)
		
		self.setPixmap(logo)