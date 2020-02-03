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
	
This module contains the BlackBoxEditorDialog class which is used for managing the
outward-facing aspects of an Action.
"""
import sys
import os
sys.path.append(os.path.abspath("./rc"))


from PySide2.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QApplication
from PySide2.QtGui import QPalette, QColor, Qt, QCloseEvent
from gui.ui.ui_blackboxeditordialog import Ui_Dialog as Ui_BlackBoxEditorDialog
from gui.porteditorwidget import PortEditorWidget

class BlackBoxEditorDialog(QDialog):
	"""
	This is a dialog for managing the outward-facing aspect of an Action.
	"""
	
	def __init__(self, action: 'Action'):
		"""
		Constructs an instance of the BlackBoxEditorDialog.
		
		:param action: The action instance that we would like to edit.
		:type action: Action
		:return: the dialog for editing the outward-facing aspects of the Action.
		:rtype: BlackBoxEditorDialog
		"""
		QDialog.__init__(self)
		self.ui = Ui_BlackBoxEditorDialog()
		self.ui.setupUi(self)
		
		self.ui.inputCentralWidget = QWidget()
		self.ui.inputLayout = QVBoxLayout()
		self.ui.inputLayout.addStretch()
		self.ui.inputLayout.setContentsMargins(0,0,0,0)
		self.ui.inputLayout.setSpacing(0)
		self.ui.inputCentralWidget.setLayout(self.ui.inputLayout)
		self.ui.inputScrollArea.setWidget(self.ui.inputCentralWidget)
		
		self.ui.outputCentralWidget = QWidget()
		self.ui.outputLayout = QVBoxLayout()
		self.ui.outputLayout.addStretch()
		self.ui.outputLayout.setContentsMargins(0, 0, 0, 0)
		self.ui.outputLayout.setSpacing(0)
		self.ui.outputCentralWidget.setLayout(self.ui.outputLayout)
		self.ui.outputScrollArea.setWidget(self.ui.outputCentralWidget)
		
		self.ui.addInputPortButton.clicked.connect(lambda: self.addPort(self.ui.inputLayout))
		self.ui.addOutputPortButton.clicked.connect(lambda: self.addPort(self.ui.outputLayout))
		
		#TODO:
		# Set name field &
		# Add existing ports.
		
	def addPort(self, layout: QVBoxLayout):
		layout.insertWidget(0, PortEditorWidget())
		
	def accept(self) -> None:
		"""
		When the user clicks "OK", the ports and name are set on the Action.
		
		:return: None
		:rtype: NoneType
		"""
		#TODO: Set the ports and name
		return QDialog.accept(self)
		
		
	
	
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
	
	d = BlackBoxEditorDialog(None)
	d.show()
	
	sys.exit(app.exec_())