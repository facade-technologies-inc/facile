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
"""


from PySide2.QtWidgets import QMenu
import data.statemachine as sm

class ComponentMenu(QMenu):
	
	def __init__(self):
		QMenu.__init__(self)
		
		self.blinkAction = self.addAction("Show in target GUI")
		
	def onBlink(self, func):
		self.blinkAction.triggered.connect(func)
		
	def prerequest(self):
		if sm.StateMachine.instance._project.getProcess():
			self.blinkAction.setEnabled(True)
		else:
			self.blinkAction.setEnabled(False)