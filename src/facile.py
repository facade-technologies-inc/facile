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

This is the main file that launches Facile. This module should only be run by the
user and never imported.

"""
import sys
import warnings

# These lines are needed to integrate Qt and pywinauto
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QPalette, QColor, Qt

from gui.facileview import FacileView

if __name__ == "__main__":
	def stylize(qApp):
		qApp.setStyle("Fusion")
		
		dark_palette = QPalette()
		dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.WindowText, Qt.white)
		dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Text, Qt.white)
		dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ButtonText, Qt.white)
		dark_palette.setColor(QPalette.BrightText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.HighlightedText, Qt.black)
		dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
		dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
		qApp.setPalette(dark_palette)
		qApp.setStyleSheet(
			"QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
	
	
	app = QApplication([])
	stylize(app)
	window = FacileView()
	window.show()
	window.showMaximized()
	sys.exit(app.exec_())
