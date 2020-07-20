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

This module contains the code for the manage project dialog.
"""

from PySide2.QtWidgets import QDialog, QWidget, QAbstractButton, QColorDialog, QInputDialog, QLineEdit
from PySide2.QtCore import Signal
from PySide2.QtGui import QPalette

from data.project import Project
from gui.ui.ui_manageprojectdialog import Ui_Dialog as Ui_ManageProjectDialog
import gui.facileview as fv
import data.statemachine as sm
from gui.theme import Theme
import QNotifications

# TODO: get rid of this once Project backend gets switched to enums.
backends = ["win32", "uia"]


class ManageProjectDialog(QDialog):
	"""
	This class is used to show settings for Facile and for the currently opened project, if available.
	"""

	projectUpdated = Signal()
	notify = Signal(str, str, int, bool, str)  # text to show, severity, duration, autohide, close button text

	# Possible message levels are: primary, success, info, warning, and danger
	NOTIF_LENGTH = 5000  # Time in ms to show a notification
	NOTIF_AUTOHIDE = False  # Automatically hide notifications on mouse hover
	NOTIF_BUTTON = ''  # Text for button to close the notification. Empty str is a good looking X
	
	def __init__(self, project: Project, mainWindow: 'FacileView', parent: QWidget = None):
		"""
		Constructs a ManageProjectDialog object.
		
		:param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
		:type parent: PySide2.QtWidgets.QWidget
		"""
		
		super(ManageProjectDialog, self).__init__(parent)
		self.ui = Ui_ManageProjectDialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Manage Project")

		self.mainWindow: fv.FacileView = mainWindow
		self._project = project

		self.notificationArea = self.setupNotificationArea()
		self.lastClickedTab = 0

		self.themeList = self.mainWindow.themeList
		self.theme = self.mainWindow.getCurrentTheme()
		self.initialTheme = self.theme
		self.listNameToTheme = {}

		self.initializeValues()  # Loads the theme, too
		self.connectSignals()

		if project:
			self.ui.project_tab.setEnabled(True)
			self.loadProjectSettings()

		self.ui.tabWidget.tabBarClicked.connect(self.checkNotifs)

	def checkNotifs(self, index: int):
		"""
		If the theme tab is selected, this allows certain messages to be shown.
		"""

		if index != 2 or index == self.lastClickedTab:
			self.lastClickedTab = index
			return

		self.lastClickedTab = index

		if not self._project:
			self.notify.emit("Custom theme colors can't be changed until a project is loaded.", 'primary',
							 ManageProjectDialog.NOTIF_LENGTH, ManageProjectDialog.NOTIF_AUTOHIDE,
							 ManageProjectDialog.NOTIF_BUTTON)
			return

		if not sm.StateMachine.instance.getCurrentActionPipeline():
			self.notify.emit("API Model colors can't be changed until you make an Action Pipeline.", 'primary',
							 ManageProjectDialog.NOTIF_LENGTH, ManageProjectDialog.NOTIF_AUTOHIDE,
							 ManageProjectDialog.NOTIF_BUTTON)

	def setupNotificationArea(self):
		"""
		Sets up the notification area for this dialog
		"""

		notificationArea = QNotifications.QNotificationArea(self.ui.tabWidget)
		notificationArea.setEntryEffect('fadeIn', 300)
		notificationArea.setExitEffect('fadeOut', 300)
		self.notify.connect(notificationArea.display)
		return notificationArea

	def loadProjectSettings(self):
		"""
		Loads project settings into the GUI
		"""
		project = self._project

		# Project settings
		self.ui.locationEdit.setText(project.getProjectDir())
		self.ui.nameEdit.setText(project.getName())
		self.ui.descriptionEdit.setText(project.getDescription())
		self.ui.appEdit.setText(project.getExecutableFile())

		# Backend
		self.ui.backendEdit.clear()
		self.ui.backendEdit.addItems(backends)
		if project.getBackend() in backends:
			idx = backends.index(project.getBackend())
		else:
			idx = 2
		self.ui.backendEdit.setCurrentIndex(idx)

		# Option to close app on exit
		if project.autoCloseAppOnExit:
			self.ui.closeAppConf.setChecked(project.autoCloseAppOnExit)

	def connectSignals(self):
		"""
		Connects any signals needed for proper behavior of the dialog
		"""

		self.ui.buttonBox.clicked.connect(self.applySettings)

		self.ui.t_baseColButton.clicked.connect(self.colorPicker_tguim)
		self.ui.a_baseColButton.clicked.connect(self.colorPicker_actionpipeline_base)
		self.ui.a_actionColButton.clicked.connect(self.colorPicker_actionpipeline_wrapper)
		self.ui.a_port_InsideColButton.clicked.connect(self.colorPicker_actionpipeline_inside_port)
		self.ui.a_port_OutsideColButton.clicked.connect(self.colorPicker_actionpipeline_outside_port)
		self.ui.a_sequence_ColButton.clicked.connect(self.colorPicker_actionpipeline_sequence_tag)

		self.ui.themeBox.currentTextChanged.connect(self.setCurrentTheme)
		self.ui.newThemeButton.clicked.connect(self.newThemePrompts)
		self.ui.deleteThemeButton.clicked.connect(self.deleteCurrentTheme)

	def deleteCurrentTheme(self):
		"""
		Deletes the currently selected theme and sets the theme back to classic dark
		"""

		curThemeName = self.ui.themeBox.currentText()

		tmpName = curThemeName
		if curThemeName.endswith(' - Default'):
			tmpName = curThemeName[:-10]

		if self.initialTheme.getName() != tmpName:
			newThemeName = self.initialTheme.getName()
		else:
			newThemeName = 'Classic (Dark)'

		self.ui.themeBox.blockSignals(True)
		self.ui.themeBox.setCurrentText(newThemeName)
		self.ui.themeBox.blockSignals(False)

		self.themeList.remove(self.listNameToTheme[curThemeName])
		self.listNameToTheme.pop(curThemeName)

		self.setCurrentTheme(newThemeName, refreshBox=True)

	def loadTheme(self, theme: Theme):
		"""
		Loads a theme into the GUI
		"""

		self.theme = theme

		# Enable tguim and apim color boxes (kept the names as target_gui/api_model_tab after gui restructure)

		if self.theme.isCustom():
			self.ui.deleteThemeButton.setEnabled(True)

			if self._project:
				self.ui.target_gui_model_tab.setEnabled(True)
				if sm.StateMachine.instance.getCurrentActionPipeline():
					self.ui.api_model_tab.setEnabled(True)
				else:
					self.ui.api_model_tab.setEnabled(False)
		else:
			self.ui.deleteThemeButton.setEnabled(False)

			if self._project:
				self.ui.target_gui_model_tab.setEnabled(False)
				self.ui.api_model_tab.setEnabled(False)

		# TGUIM settings
		self.ui.dynamicCol.setChecked(not self.theme.tguimColorSettings['Is Flat'])
		self.setTGUIMBaseCol(self.theme.tguimColorSettings['Base Color'])

		# APIM settings
		self.setActionPipelineBaseCol(self.theme.apimColors['Action Pipeline'])
		self.setActionPipelineWrapperCol(self.theme.apimColors['Action Wrapper'])
		self.setActionPipelineInsidePortCol(self.theme.apimColors['Inside Port'])
		self.setActionPipelineOutsidePortCol(self.theme.apimColors['Outside Port'])
		self.setActionPipelineSequenceTagCol(self.theme.apimColors['Sequence Tag'])

	def newThemePrompts(self):
		"""
		Gives the user prompts to make a new theme
		"""
		itemDict = {}
		items = []
		for theme in fv.FacileView.DEFAULT_THEMES:
			items.append(theme.getName())
			itemDict[theme.getName()] = theme

		while True:
			thmText, ok = QInputDialog.getItem(self, 'Choose base theme...',
											   'Which theme do you want your new theme to be based on?',
											   items, current=0, editable=False)

			if not ok:
				return

			theme = itemDict[thmText]
			name = ''
			forbiddenNames = list(self.listNameToTheme.keys()) + ['']

			while name in forbiddenNames:
				name, ok = QInputDialog.getText(self, 'Enter theme name...',
												"Enter your new theme's name. As a reminder,\nit can't have the "
												"same name as any of the other themes.", QLineEdit.EchoMode.Normal)

				if not ok:
					break

				if name not in forbiddenNames:
					# Make the new Theme
					newTheme = Theme(theme.base(), custom=True)
					newTheme.tguimColorSettings = theme.tguimColorSettings.copy()
					newTheme.apimColors = theme.apimColors.copy()
					newTheme.setName(name)

					self.themeList.append(newTheme)
					self.listNameToTheme[name] = newTheme
					self.setCurrentTheme(themeName=name, refreshBox=True)

					return

	def setTGUIMBaseCol(self, color):
		"""
		Opens the color picker, and once it is closed it shows a preview of the current color in a widget.
		Keeps an internal record of the accent color picked as well.

		:param color: The color to set
		:type color: QColor
		"""
		self.theme.tguimColorSettings['Base Color'] = color
		palette = QPalette()
		palette.setColor(QPalette.Background, color)
		self.ui.t_baseCol.setPalette(palette)
		
	def setActionPipelineBaseCol(self, color):
		"""
		Opens the color picker, and once it is closed it shows a preview of the current color in a widget.
		Keeps an internal record of the accent color picked as well.

		:param color: The color to set
		:type color: QColor
		"""
		self.theme.apimColors['Action Pipeline'] = color
		palette = QPalette()
		palette.setColor(QPalette.Background, color)
		self.ui.a_baseCol.setPalette(palette)

	def setActionPipelineWrapperCol(self, color):
		"""
		Opens the color picker, and once it is closed it shows a preview of the current color in a widget.
		Keeps an internal record of the accent color picked as well.

		:param color: The color to set
		:type color: QColor
		"""
		self.theme.apimColors['Action Wrapper'] = color
		palette = QPalette()
		palette.setColor(QPalette.Background, color)
		self.ui.a_actionCol.setPalette(palette)

	def setActionPipelineInsidePortCol(self, color):
		"""
		Opens the color picker, and once it is closed it shows a preview of the current color in a widget.
		Keeps an internal record of the accent color picked as well.

		:param color: The color to set
		:type color: QColor
		"""
		self.theme.apimColors['Inside Port'] = color
		palette = QPalette()
		palette.setColor(QPalette.Background, color)
		self.ui.a_port_InsideCol.setPalette(palette)

	def setActionPipelineOutsidePortCol(self, color):
		"""
		Opens the color picker, and once it is closed it shows a preview of the current color in a widget.
		Keeps an internal record of the accent color picked as well.

		:param color: The color to set
		:type color: QColor
		"""
		self.theme.apimColors['Outside Port'] = color
		palette = QPalette()
		palette.setColor(QPalette.Background, color)
		self.ui.a_port_OutsideCol.setPalette(palette)

	def setActionPipelineSequenceTagCol(self, color):
		"""
		Opens the color picker, and once it is closed it shows a preview of the current color in a widget.
		Keeps an internal record of the accent color picked as well.

		:param color: The color to set
		:type color: QColor
		"""
		self.theme.apimColors['Sequence Tag'] = color
		palette = QPalette()
		palette.setColor(QPalette.Background, color)
		self.ui.a_sequence_Col.setPalette(palette)
		
	def colorPicker_tguim(self):
		"""
		Opens a color picking dialog, then returns the color chosen
		"""
		colSelect = QColorDialog(self.theme.tguimColorSettings['Base Color'])
		colSelect.colorSelected.connect(self.setTGUIMBaseCol)
		colSelect.exec_()
	
	def colorPicker_actionpipeline_base(self):
		"""
		Opens a color picking dialog, then returns the color chosen
		"""
		colSelect = QColorDialog(self.theme.apimColors['Action Pipeline'])
		colSelect.colorSelected.connect(self.setActionPipelineBaseCol)
		colSelect.exec_()
		
	def colorPicker_actionpipeline_wrapper(self):
		"""
		Opens a color picking dialog, then returns the color chosen
		"""
		colSelect = QColorDialog(self.theme.apimColors['Action Wrapper'])
		colSelect.colorSelected.connect(self.setActionPipelineWrapperCol)
		colSelect.exec_()
		
	def colorPicker_actionpipeline_inside_port(self):
		"""
		Opens a color picking dialog, then returns the color chosen
		"""
		colSelect = QColorDialog(self.theme.apimColors['Inside Port'])
		colSelect.colorSelected.connect(self.setActionPipelineInsidePortCol)
		colSelect.exec_()
	
	def colorPicker_actionpipeline_outside_port(self):
		"""
		Opens a color picking dialog, then returns the color chosen
		"""
		colSelect = QColorDialog(self.theme.apimColors['Outside Port'])
		colSelect.colorSelected.connect(self.setActionPipelineOutsidePortCol)
		colSelect.exec_()
	
	def colorPicker_actionpipeline_sequence_tag(self):
		"""
		Opens a color picking dialog, then returns the color chosen
		"""
		colSelect = QColorDialog(self.theme.apimColors['Sequence Tag'])
		colSelect.colorSelected.connect(self.setActionPipelineSequenceTagCol)
		colSelect.exec_()
		
	def initializeValues(self):
		"""
		Initializes all the user settings to be visible/selected
		"""
		self.ui.enableSBs.setChecked(self.mainWindow.scrollBarsEnabled())

		self.setCurrentTheme(self.theme.getName(), refreshBox=True)
		self.setInitLayout()

	def setCurrentTheme(self, themeName, refreshBox: bool = False):
		"""
		Sets the theme box to have the current theme, and fills in the other entries too.

		:param themeName: the chosen theme's name
		:type themeName: str
		:param refreshBox: Whether or not to refresh the themebox
		:type refreshBox: bool
		"""

		if refreshBox:
			self.refreshThemeBox()

		if themeName is self.initialTheme.getName():
			themeName = themeName + ' - Default'

		newTheme = self.listNameToTheme[themeName]
		self.loadTheme(newTheme)

		self.ui.themeBox.setCurrentText(themeName)

	def refreshThemeBox(self):
		"""
		Fills in the theme drop down box with the most updated values
		"""
		self.ui.themeBox.blockSignals(True)

		self.listNameToTheme = {}
		self.ui.themeBox.clear()

		for theme in self.themeList:
			if theme.getName() == self.initialTheme.getName():
				name = theme.getName() + ' - Default'
			else:
				name = theme.getName()

			self.ui.themeBox.addItem(name)
			self.listNameToTheme[name] = theme

		self.ui.themeBox.blockSignals(False)

	def setInitLayout(self):
		"""
		Sets the layout box to have the current layout
		"""
		self.ui.layoutBox.addItems(["Models Only", "Essentials", "Classic", "All"])
		self.ui.layoutBox.setCurrentIndex(self.mainWindow.getLayout().value - 1)

	def applySettings(self, button: QAbstractButton = None, bypass=False):
		"""
		If apply is pressed, apply the settings without closing the window.
		Bypass variable is used for the OK button.

		:param button: The button being pressed
		:type button: QAbstractButton
		:param bypass: Whether to bypass the button criteria (only Apply works otherwise). Default is False.
		:type bypass: bool
		"""

		if bypass or button.text() == 'Apply':
			# First, save theme
			self.mainWindow.setTheme(self.theme)
			
			# Save project settings
			if self._project:
				self._project.setBackend(self.ui.backendEdit.currentText())
				self._project.setName(self.ui.nameEdit.text())
				self._project.setProjectDir(self.ui.locationEdit.text())
				self._project.setDescription(self.ui.descriptionEdit.toPlainText())
				self._project.setExecutableFile(self.ui.appEdit.text())

				if self._project.acaWarningShown:
					if self.ui.closeAppConf.isChecked():
						self._project.autoCloseAppOnExit = True
					else:
						self._project.autoCloseAppOnExit = False

			# Save selected layout
			if self.ui.layoutBox.currentIndex() < 4:
				self.mainWindow.setLayout(fv.FacileView.Layout(self.ui.layoutBox.currentIndex() + 1))
			else:
				self.mainWindow.setLayout(fv.FacileView.Layout.CLASSIC)
			self.mainWindow.enableScrollBars(self.ui.enableSBs.isChecked())

			self.theme.tguimColorSettings['Is Flat'] = not self.ui.dynamicCol.isChecked()
			self.mainWindow.setTheme(self.theme)
			self.setCurrentTheme(self.theme.getName())

			# Save settings once applied
			self.mainWindow.saveSettings()
	
	def accept(self) -> None:
		"""
		Called when the user clicks the "OK" button.
		
		:return: None
		:rtype: NoneType
		"""

		self.applySettings(bypass=True)

		QDialog.accept(self)
	
	def reject(self) -> None:
		"""
		Called when the user clicks the "close" button.

		:return: None
		:rtype: NoneType
		"""
		
		QDialog.reject(self)
