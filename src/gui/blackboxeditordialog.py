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


from PySide2.QtWidgets import QDialog, QWidget, QVBoxLayout
from gui.ui.ui_blackboxeditordialog import Ui_Dialog as Ui_BlackBoxEditorDialog
from gui.porteditorwidget import PortEditorWidget
import data.statemachine as sm

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
		self.setModal(True)
		self.ui.errorLabel.hide()
		
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
		
		self.ui.addInputPortButton.clicked.connect(lambda: self.addPortWidget(None, self.ui.inputLayout))
		self.ui.addOutputPortButton.clicked.connect(lambda: self.addPortWidget(None, self.ui.outputLayout))
		
		self._action = action
		
		self.ui.actionName.setText(self._action.getName())
		
		self.addExistingPorts()
	
	def addExistingPorts(self) -> None:
		"""
		Adds port editors for all of the existing ports in the action.
		
		:return: None
		:rtype: NoneType
		"""
		for port in self._action.getInputPorts():
			self.addPortWidget(port, self.ui.inputLayout)
		for port in self._action.getOutputPorts():
			self.addPortWidget(port, self.ui.outputLayout)
		
	def addPortWidget(self, port: 'Port', layout: QVBoxLayout):
		"""
		Add a single port editor to a specified layout. The layout provided should
		be the layout for either the input or output port editors.
		
		:param port: The port to create the editor widget for.
		:type port: Port
		:param layout: The layout to place the editor widget in.
		:type layout: QVBoxLayout
		:return: None
		:rtype: NoneType
		"""
		
		if layout == self.ui.outputLayout:
			pew = PortEditorWidget(port, allowOptional=False)
		else:
			pew = PortEditorWidget(port, allowOptional=True)
		layout.insertWidget(0, pew)
		
	def accept(self) -> None:
		"""
		When the user clicks "OK", the ports and name are set on the Action.
		
		:return: None
		:rtype: NoneType
		"""
		apim = sm.StateMachine.instance._project.getAPIModel()
		
		# get copies of input and output ports for validation.
		inputPorts = []
		il = self.ui.inputLayout
		for i in range(il.count() - 1):
			pew = il.itemAt(i).widget()
			inputPorts.append(pew.previewPort())
		
		outputPorts = []
		il = self.ui.outputLayout
		for i in range(il.count() - 1):
			pew = il.itemAt(i).widget()
			outputPorts.append(pew.previewPort())
			
		# clear error message
		self.ui.errorLabel.setText("")
		errors = []
		#################################
		# VALIDATE ACTION NAME AND PORTS
		#################################
		name = self.ui.actionName.text().strip()
		
		# Make sure name of action pipeline is unique
		if name in [ap.getName() for ap in apim.getActionPipelines()]:
			errors.append("An action pipeline with the name '%s' already exists." % name)
			
		# Make sure name is a valid identifier
		if not name.isidentifier():
			errors.append("The name of the action pipeline must be a valid Python identifier.")
			
		# Name must start with a lower-case character
		if name[0].isupper():
			errors.append("The action name must start with a lower-case letter.")
		
		# Make sure all inputs have unique names.
		inputNames = set()
		for port in inputPorts:
			if port.getName() in inputNames:
				errors.append("Duplicate name '{}' in input ports is not allowed".format(port.getName()))
			inputNames.add(port.getName())
		
		# Make sure all outputs have unique names.
		outputNames = set()
		for port in outputPorts:
			if port.getName() in outputNames:
				errors.append("Duplicate name '{}' in output ports is not allowed.".format(port.getName()))
			outputNames.add(port.getName())
			
		# Make sure that optional inputs come after required inputs
		optionalFound = False
		for port in inputPorts:
			if port.isOptional():
				optionalFound = True
			if optionalFound and not port.isOptional():
				errors.append("Optional inputs must come after required inputs.")
				break
				
		# Make sure that optional inputs have a default value
		for port in inputPorts:
			if port.isOptional():
				if port.getDefaultValue() == "":
					errors.append("All optional ports must have default values.")
				
		# Make sure the type of the port is not NoneType
		for port in inputPorts + outputPorts:
			if port.getDataType() == type(None):
				errors.append("Data type of port cannot be NoneType.")
				break
				
		# If type is simple, and port is optional, check the type of the default value.
		checkable_types = [int, float, str, bool]
		for port in inputPorts:
			if port.isOptional() and port.getDataType() != type(None):
				default = port.getDefaultValue()
				t = port.getDataType()
				bad=False
				try:
					result = t(default)
				except ValueError:
					bad = True
				else:
					if t == bool and result == False:
						bad = True
						
				if t == str:
					validEnds = default.startswith('"') and default.endswith('"') or default.startswith("'") and default.endswith("'")
					if not validEnds:
						errors.append("String values must be enclosed by quotes.")
					else:
						if default[0] in default[1:-1]:
							errors.append("Avoid using the same quote character in the default "
							              "value as the one that encloses the default value.")
						
				if bad:
					errors.append("The default value is not the correct type for port '{}'.".format(port.getName()))
		
		if len(errors) != 0:
			errMsg = "Errors:\n"
			for err in errors:
				errMsg += "\t" + err + "\n"
			self.ui.errorLabel.setText(errMsg)
			self.ui.errorLabel.show()
			return
		else:
			self.ui.errorLabel.hide()
		
		#################################
		# EDIT ACTION NAME AND PORTS
		#################################
		self._action.setName(name)
		
		# add new input ports to the action
		il = self.ui.inputLayout
		newPorts = []
		for i in range(il.count() - 1):
			pew = il.itemAt(i).widget()
			pew.updatePort()
			port = pew.getPort()
			newPorts.append(port)
			if port.getAction() is None:
				self._action.addInputPort(port)
		
		# remove old input ports from the action.
		for port in self._action.getInputPorts():
			if port not in newPorts:
				self._action.removePort(port)
		
		# add new output ports to the action.
		ol = self.ui.outputLayout
		newPorts = []
		for i in range(ol.count() - 1):
			pew = ol.itemAt(i).widget()
			pew.updatePort()
			port = pew.getPort()
			newPorts.append(port)
			if port.getAction() is None:
				self._action.addOutputPort(port)
		
		# remove old output ports from the action.
		for port in self._action.getOutputPorts():
			if port not in newPorts:
				self._action.removePort(port)
			
		return QDialog.accept(self)
