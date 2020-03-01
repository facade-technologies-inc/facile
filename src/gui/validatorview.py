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
import threading

from PySide2.QtWidgets import QApplication

from gui.validatormessageview import ValidatorMessageView

sys.path.append(os.path.abspath("../"))

from PySide2.QtGui import QPalette
from PySide2.QtCore import Signal, Slot, QTimer, Qt, QCoreApplication
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel

from gui.ui.ui_validatorview import Ui_Form as Ui_ValidatorView

from data.validatormessage import ValidatorMessage
from data.validator import Validator
import data.statemachine as sm

class ValidatorView(QWidget):
	"""
	The ValidatorView class is the graphical view of the validator. It receives data from the Validator class.
	
	"""
	
	stopped = Signal()
	ran = Signal()
	refreshed = Signal()
	cleared = Signal()
	
	LABEL_STYLE = '<span style="font-weight:bold;color:{color};">{{}}</span> {label}'
	
	PROGRESSBAR_STYLE = """
		QProgressBar::chunk {{
			background-color: {color};
            border-bottom-right-radius: 7px;
            border-bottom-left-radius: 7px;
            border: 0px solid black;
        }}
	"""
	
	ERROR_LABEL = LABEL_STYLE.format(color="red", label="Errors")
	WARNING_LABEL = LABEL_STYLE.format(color="orange", label="Warnings")
	INFO_LABEL = LABEL_STYLE.format(color="green", label="Info")
	
	ERROR_PROGRESSBAR = PROGRESSBAR_STYLE.format(color='red')
	WARNING_PROGRESSBAR = PROGRESSBAR_STYLE.format(color='orange')
	SAFE_PROGRESSBAR = PROGRESSBAR_STYLE.format(color='green')
	
	def __init__(self, parent: QWidget = None):
		"""
		Construct the view for the validator.
		"""
		
		super(ValidatorView, self).__init__(parent)
		self.ui = Ui_ValidatorView()
		self.ui.setupUi(self)
		self.setWindowTitle("Validator View")
		
		self._counts = {
		}
		self._labelMapping = {
			ValidatorMessage.Level.Error: self.ui.errorLabel,
			ValidatorMessage.Level.Warning: self.ui.warningLabel,
			ValidatorMessage.Level.Info: self.ui.infoLabel
		}
		self._labelStyleMapping = {
			ValidatorMessage.Level.Error: ValidatorView.ERROR_LABEL,
			ValidatorMessage.Level.Warning: ValidatorView.WARNING_LABEL,
			ValidatorMessage.Level.Info: ValidatorView.INFO_LABEL,
		}
		self._mostSevere = 0
		self._visibleCount = 0
		self.allMessages = []
		self.showLevels = set()
		self.clear()
		self.sync()
		
		self.ui.checkBoxError.toggled.connect(lambda: self.refreshed.emit())
		self.ui.checkBoxWarning.toggled.connect(lambda: self.refreshed.emit())
		self.ui.checkBoxInfo.toggled.connect(lambda: self.refreshed.emit())
		self.ui.runButton.clicked.connect(lambda: self.ran.emit())
		self.ui.stopButton.clicked.connect(lambda: self.stopped.emit())
		self.ui.clearButton.clicked.connect(lambda: self.cleared.emit())
		
		self.refreshed.connect(self.refresh)
		self.cleared.connect(self.clear)
		
		self.dataValidator = Validator()
		
		# making this a blocking queued connection allows the view thread to stay responsive when
		# a lot of messages are being sent at the same time. If we just use a QueuedConnection,
		# the dataValidator's thread may generate messages much faster than the view can handle
		# them and the view will be too busy to respond to user interactions.
		self.dataValidator.sentMessage.connect(self.receiveMessage, type=Qt.BlockingQueuedConnection)
		self.dataValidator.updateProgress.connect(self.updateProgress, type=Qt.BlockingQueuedConnection)
		
		self.ran.connect(self.onRun)
		self.stopped.connect(self.onStop)
		
	@Slot()
	def onStop(self) -> None:
		"""
		Stop the validator and set buttons to correct state.
		
		:return:
		"""
		self.dataValidator.stop()
		self.ui.runButton.setEnabled(True)
		self.ui.stopButton.setEnabled(False)
		
	@Slot()
	def onRun(self) -> None:
		"""
		When the Validator is run, old messages are cleared and then the validator thread is
		started.
		
		:return: None
		:rtype: NoneType
		"""
		self.clear()
		self._mostSevere = 0
		self.ui.algorithmProgressBar.setStyleSheet(ValidatorView.SAFE_PROGRESSBAR)
		self.ui.algorithmProgressBar.setValue(0)
		self.dataValidator.start()
		self.ui.runButton.setEnabled(False)
		self.ui.stopButton.setEnabled(True)
		sm.StateMachine.instance.view.ui.actionValidate.setEnabled(False)
	
	@Slot()
	def clear(self) -> None:
		"""
		Clear all the information/messages in the view.
		
		:return: None
		:rtype: NoneType
		"""
		
		# clear messages and create new infrastructure for displaying messages.
		self.allMessages = []
		self.ui.centralWidget = QWidget()
		self.ui.messageLayout = QVBoxLayout()
		self.ui.messageLayout.addStretch()
		self.ui.centralWidget.setLayout(self.ui.messageLayout)
		self.ui.scrollArea.setWidget(self.ui.centralWidget)
		
		# Set color of the central widget to the application's base color
		color = QCoreApplication.instance().palette().color(QPalette.ColorRole.Base)
		palette = self.ui.centralWidget.palette()
		palette.setColor(QPalette.ColorRole.Background, color)
		self.ui.centralWidget.setAutoFillBackground(True)
		self.ui.centralWidget.setPalette(palette)
		
		# reset progress bar and hide it.
		if self.ui.algorithmProgressBar.value() == 100:
			self.ui.algorithmProgressBar.setValue(0)
		self.ui.algorithmProgressBar.hide()
		
		# reset individual counts
		self._counts = {
			ValidatorMessage.Level.Error: 0,
			ValidatorMessage.Level.Warning: 0,
			ValidatorMessage.Level.Info: 0
		}
		self.ui.errorLabel.setText("0 Errors")
		self.ui.warningLabel.setText("0 Warnings")
		self.ui.infoLabel.setText("0 Info")
		
		# set visible count to 0.
		self._visibleCount = 0
		self.ui.messageCountLabel.setText(str(self._visibleCount))
		
		# set worst level to 0
		self._mostSevere = 0
		
		self.ui.clearButton.setEnabled(False)

	@Slot()
	def refresh(self) -> None:
		"""
		Refresh the GUI to show the right widgets.
		
		:return: None
		:rtype: NoneType
		"""
		app = QCoreApplication.instance()
		
		self.sync()
		i=0
		for msg in self.allMessages:
			i+=1
			if msg.level in self.showLevels:
				if not msg.widget.isVisible():
					msg.widget.show()
					self._visibleCount += 1
				
			else:
				if msg.widget.isVisible():
					msg.widget.hide()
					self._visibleCount -= 1
				
			self.ui.messageCountLabel.setText(str(self._visibleCount))
			
			# process events every 10th iteration to not freeze GUI.
			if i % 10:
				app.processEvents()
	
	@Slot(dict)
	def receiveMessage(self, msg: ValidatorMessage) -> None:
		"""
		Receive message from the Validator class. Receive one message each time.
		
		:param msg: a customized validator message coming from the validator
		:type msg: ValidatorMessage
		:return: None
		:rtype: NoneType
		"""
		self.addWidgetToMessage(msg)
		self.allMessages.append(msg)
		self.ui.messageLayout.insertWidget(0, msg.widget)
		if msg.level in self.showLevels:
			msg.widget.show()
			self._visibleCount += 1
			self.ui.messageCountLabel.setText(str(self._visibleCount))
		else:
			msg.widget.hide()
			
		# update individual message level counts
		self._counts[msg.level] += 1
		
		# update appropriate message count label
		label = self._labelMapping[msg.level]
		style = self._labelStyleMapping[msg.level]
		count = self._counts[msg.level]
		label.setText(style.format(count))
		
		# update progress bar style if needed
		self._mostSevere = max(self._mostSevere, msg.level.value)
		if self._mostSevere < 2:
			self.ui.algorithmProgressBar.setStyleSheet(ValidatorView.SAFE_PROGRESSBAR)
		elif self._mostSevere < 3:
			self.ui.algorithmProgressBar.setStyleSheet(ValidatorView.WARNING_PROGRESSBAR)
		else:
			self.ui.algorithmProgressBar.setStyleSheet(ValidatorView.ERROR_PROGRESSBAR)
			
		self.ui.algorithmProgressBar.show()
		
		self.ui.clearButton.setEnabled(True)

	def addWidgetToMessage(self, msg: ValidatorMessage) -> None:
		"""
		Add a QLabel widget to each message received.
		
		:param msg: a customized validator message coming from the validator
		:type msg: ValidatorMessage
		:return: None
		:rtype: NoneType
		"""
		
		msg.widget = ValidatorMessageView(msg)
		
	def sync(self):
		"""
		determine what kind of messages should be shown.
		
		:return: None
		:rtype: NoneType
		"""
		self.showLevels = set()
		if self.ui.checkBoxError.isChecked():
			self.showLevels.add(ValidatorMessage.Level.Error)
		if self.ui.checkBoxWarning.isChecked():
			self.showLevels.add(ValidatorMessage.Level.Warning)
		if self.ui.checkBoxInfo.isChecked():
			self.showLevels.add(ValidatorMessage.Level.Info)
			
	@Slot()
	def updateProgress(self, progress: float) -> None:
		"""
		Updates the progress bar to the given value and show it.
		
		:param progress: the current algorithm progress.
		:type progress: float
		:return: None
		:rtype: NoneType
		"""
		
		self.ui.algorithmProgressBar.setValue(round(progress, 2))
		self.ui.algorithmProgressBar.show()
		
		if progress >= 100:
			self.ui.runButton.setEnabled(True)
			self.ui.stopButton.setEnabled(False)
			sm.StateMachine.instance.view.ui.actionValidate.setEnabled(True)
		

