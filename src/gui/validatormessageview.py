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

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from gui.ui.ui_validatormessageview import Ui_Form as Ui_ValidatorMessageView
from data.validatormessage import ValidatorMessage


class ValidatorMessageView(QWidget):
	"""
	The ValidatorMessageView class is the graphical view of the validator text message.

	"""
	
	def __init__(self, messageData: 'ValidatorMessage', parent: QWidget = None):
		"""
		Construct the view for the validator.
		"""
		
		super(ValidatorMessageView, self).__init__(parent)
		self.ui = Ui_ValidatorMessageView()
		self.ui.setupUi(self)
		
		self.ui.levelLabel.setText(messageData.level.name)
		self.ui.entityLabel.setText(str(messageData.entity))
		self.ui.messageLabel.setText(messageData.text)
		
		if messageData.level == ValidatorMessage.Level.Info:
			self.ui.levelLabel.setStyleSheet("color: green;")
		elif messageData.level == ValidatorMessage.Level.Warning:
			self.ui.levelLabel.setStyleSheet("color: orange;")
		else:
			self.ui.levelLabel.setStyleSheet("color: red;")
