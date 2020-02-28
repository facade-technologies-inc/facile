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

This module contains the code for the copy project dialog.
"""
import sys
import os
import data.statemachine as sm

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QWidget, QFileDialog
from data.compilationprofile import CompilationProfile
from gui.ui.ui_apicompilerdialog import Ui_Dialog as Ui_ApiCompilerDialog
from tguiil.matchoption import MatchOption
from libs.bitness import getPythonBitness, isExecutable, appBitnessMatches, getExeBitness


class ApiCompilerDialog(QDialog):
	"""
	This class is used when user runs the api compiler. If the information is valid, all the information will be
	stored in a CompilationProfile object and sent in a signal. If not, the ApiCompilerDialog will not accept the
	input and give error messages accordingly.
	"""
	
	setApiCompiler = Signal(CompilationProfile)
	
	def __init__(self, parent: QWidget = None):
		"""
		Constructs a ApiCompilerDialog object.

		:param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
		:type parent: PySide2.QtWidgets.QWidget
		:return: The constructed new Api Compiler dialog object.
		:rtype: ApiCompilerDialog
		"""
		
		super(ApiCompilerDialog, self).__init__(parent)
		self.ui = Ui_ApiCompilerDialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Setup API Compiler")
		
		# disable file path editors
		self.ui.apiLocation.setEnabled(False)
		self.ui.interpreterLocation.setEnabled(False)
		self.ui.apiLocation.setText(sm.StateMachine.instance._project.getProjectDir())
		self.ui.interpreterLocation.setText(sys.executable)
		
		self.ui.browseFilesButton_folder.clicked.connect(self.browseForAPILocation)
		self.ui.browseFilesButton_folder_2.clicked.connect(self.browseForInterpreterLocation)
		
		self.ui.dialogButtons.accepted.connect(self.accept)
		self.ui.dialogButtons.rejected.connect(self.reject)
		
		self.ui.error_label.setText("")
	
	# TODO: make it un-selectable before a project is open
	
	@Slot()
	def browseForAPILocation(self) -> None:
		"""
		Opens a file dialog when the user clicks on the "..." button to choose a project directory.

		The user will only be able to select folders, and when a folder is selected, the value will
		be placed into the read-only text editor to the left.
		
		The default location is the current project location.

		:return: None
		:rtype: NoneType
		"""
		
		if getPythonBitness() == 32:
			openDir = "C:/Program Files (x86)"
		else:
			openDir = "C:/Program Files"
		openDir = os.path.abspath(openDir)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.apiLocation.setText(url))
		fileDialog.exec_()
	
	@Slot()
	def browseForInterpreterLocation(self) -> None:
		"""
		Opens a file dialog when the user clicks on the "..." button to choose a target application.

		The dialog that pops up doesn't restrict what file the user selects, but before creating the
		project, the file will be checked for correct bitness, and to make sure that it's an executable file.
		The path to the file will be placed into the read-only text editor to the left.
		
		The default location is the default python location on user's end.

		:return: None
		:rtype: NoneType
		"""
		
		if getPythonBitness() == 32:
			openDir = "C:/Program Files (x86)"
		else:
			openDir = "C:/Program Files"
		openDir = os.path.abspath(openDir)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.interpreterLocation.setText(url))
		fileDialog.exec_()
		
	@Slot()
	def accept(self):
		"""
		This method is called when the user clicks the "OK" button.

		It will validate all of the user's input and show error messages if
		any information is invalid.

		:emits: setApiCompiler if the api compiler setting was successfully accpeted
		:return: None
		:rtype: NoneType
		"""

		self.ui.error_label.setText("")
		errors = []
		interpExe = self.ui.interpreterLocation.text()
		
		# Check for valid target application executable
		if not interpExe:
			errors.append("Need to select target application executable")
		else:
			if not isExecutable(interpExe):
				errors.append("Target application must be an executable file.")
			elif not appBitnessMatches(interpExe):
				pyBit = getPythonBitness()
				appBit = getExeBitness(interpExe)
				errors.append(
					"{} bit Python cannot control {} bit application".format(pyBit, appBit))
		
		# Construct a set for documentation type
		setDocType = set()
		if self.ui.checkBoxDocx.isChecked():
			setDocType.add(CompilationProfile.DocType.Doc)
		if self.ui.checkBoxHtml.isChecked():
			setDocType.add(CompilationProfile.DocType.Html)
		if self.ui.checkBoxPdf.isChecked():
			setDocType.add(CompilationProfile.DocType.Pdf)
		if self.ui.checkBoxEPub.isChecked():
			setDocType.add(CompilationProfile.DocType.EPub)
		
		if len(setDocType) == 0:
			errors.append("You must select at least one documentation type.")
			
		# Construct a set for component resolution type
		setcompResOpts = set()
		# TODO: change option1 and option2 here, CompilationProfile, ui
		if self.ui.checkBox1.isChecked():
			setcompResOpts.add(MatchOption.ExactToken)
		if self.ui.checkBox2.isChecked():
			setcompResOpts.add(MatchOption.CloseToken)
		if self.ui.checkBoxPyw.isChecked():
			setcompResOpts.add(MatchOption.PWABestMatch)
			
		if len(setcompResOpts) == 0:
			errors.append("You must select at least one component resolution type.")
		
		apiFolderDir = self.ui.apiLocation.text()
		interpExeDir = self.ui.interpreterLocation.text()
		
		theCompilationProfile = CompilationProfile(setDocType, setcompResOpts, apiFolderDir, interpExeDir)
		
		
		
		# if there are any errors, show them, then return.
		if len(errors) != 0:
			errMsg = "Errors:\n"
			for err in errors:
				errMsg += "\t" + err + "\n"
			self.ui.error_label.setText(errMsg)
			return

		# TODO: figure out why FindExecutable: There is no association for the file get printed
		print("apicompilerdialog accepted")
		self.setApiCompiler.emit(theCompilationProfile)
		return QDialog.accept(self)