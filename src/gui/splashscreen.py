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
from PySide2.QtCore import QTimer
from PySide2.QtGui import QPixmap

class FacileSplashScreen(QSplashScreen):
	"""
	FacileSplashScreen class sets the logo picture to display on the splash screen
	"""
	def __init__(self):
		QSplashScreen.__init__(self)
		height = QApplication.instance().primaryScreen().size().height() * .5
		self.setPixmap(QPixmap('../resources/facade_logo.png').scaledToHeight(height))
		


"""
		progress_bar = QProgressBar(splash)
		progress_bar.setMaximum(10)
		progress_bar.setGeometry(0,splash_pix.height() - 50, splash_pix.width(), 20)
		splash.show()
		splash.showMessage()

if __name__ == "__main__":
	app = QApplication([])
	FacileSplashScreen = fSS
	fSS.show()
	QTimer.singleShot(2500,fSS,SLOT(close()))
"""

