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
This module contains the PortEditorWidget which allows the user to configure a single
port.
"""

from PySide2.QtWidgets import QWidget
from gui.ui.ui_porteditorwidget import Ui_Form as Ui_PortEditorWidget
from data.apim.port import Port

class PortEditorWidget(QWidget):
	"""
	The PortEditorWidget is used to edit a single port object.
	"""

	# pairs of selectable types. The first value will be shown in the port type dropdown menu, and the second
	# type will be the data value used.
	PORT_TYPES =[ ("String",         'str'),
				  ("Integer",        'int'),
				  ("Floating Point", 'float'),
				  ("Boolean",        'bool'),
				  ("List",           'list'),
				  ("Set",            'set'),
				  ("Tuple",          'tuple'),
				  ("Dictionary",     'dict'),
				]
	
	def __init__(self, port: 'Port' = None, allowOptional: bool = True) -> 'PortEditorWidget':
		"""
		Creates a port editor widget.
		
		:param port: The port to edit.
		:type port: Port
		:param allowOptional: if True, the optional checkbox will be shown.
		:type allowOptional: bool
		"""
		QWidget.__init__(self)
		self.ui = Ui_PortEditorWidget()
		self.ui.setupUi(self)

		for typeLabel, type in PortEditorWidget.PORT_TYPES:
			self.ui.typeEdit.addItem(typeLabel, type)
		self.ui.typeEdit.setCurrentText(PortEditorWidget.PORT_TYPES[0][0])

		if port is not None:
			self._port = port
		else:
			self._port = Port()
		self.updateEditor()

		if allowOptional:
			self.ui.optionalButton.clicked.connect(self.onOptionalButtonClicked)
		
		self.updateDefaultEditorState()
		
	def updateDefaultEditorState(self) -> None:
		"""
		If the port is required, set the default editor text to "None" and disable.
		Else, enable it and set it to the port's default value.
		
		:return: None
		:rtype: NoneType
		"""
		if self.ui.optionalButton.text() == "Optional":
			if self._port._default:
				self.ui.defaultEdit.setText(str(self._port._default))
			else:
				self.ui.defaultEdit.setText("")
				self.ui.defaultEdit.setPlaceholderText("Default Value")
			self.ui.defaultEdit.setEnabled(True)
		else:
			self.ui.defaultEdit.setText('None')
			self.ui.defaultEdit.setEnabled(False)
			
	def onOptionalButtonClicked(self) -> None:
		"""
		Switch the text on the button between "Required" and "Optional"
		
		:return: None
		:rtype: NoneType
		"""
		if self.ui.optionalButton.text() == "Required":
			self.ui.optionalButton.setText("Optional")
		else:
			self.ui.optionalButton.setText("Required")
		self.updateDefaultEditorState()
			
	def getPort(self) -> 'Port':
		"""
		Get's the port object associated with this port editor.
		
		:return: The Port being edited.
		:rtype:
		"""
		return self._port
	
	def updateEditor(self) -> None:
		"""
		Updates the editor widget to reflect the port values
		
		:return: None
		:rtype: NoneType
		"""
		self.ui.nameEdit.setText(self._port.getName())

		# get the pretty version of the type
		typeStr = str(self._port.getDataTypeStr())
		for typeLabel, type in PortEditorWidget.PORT_TYPES:
			if typeStr == type:
				typeStr = typeLabel
		if typeStr == 'NoneType':
			typeStr = 'String'
		self.ui.typeEdit.setCurrentText(typeStr)
		
		if self._port.isOptional():
			self.ui.optionalButton.setText("Optional")
			self.ui.defaultEdit.setText(str(self._port.getDefaultValue()))
		else:
			self.ui.optionalButton.setText("Required")
			self.ui.defaultEdit.setText("None")
			
	def updatePort(self) -> None:
		"""
		Sets all the values of the port values to the values of the editors
		
		.. note:: This function will update the underlying port. Don't call it unless you're
			absolutely certain that the values in the editors are good.
		
		:return: None
		:rtype: NoneType
		"""
		p = self.previewPort()
		self._port.mirror(p)
		
	def previewPort(self) -> 'Port':
		"""
		Returns a new port with all values from editors set.
		
		:return: The new port object
		:rtype: Port
		"""
		p = Port()
		p.setName(self.ui.nameEdit.text())
		
		if self.ui.optionalButton.text() == 'Optional':
			p.setOptional(True)
		else:
			p.setOptional(False)

		curText = self.ui.typeEdit.currentText()

		for text, type_ in PortEditorWidget.PORT_TYPES:
			if text == curText:
				curText = type_
				break

		try:
			dataType = eval(curText)
		except NameError:
			dataType = curText
		p.setDataType(dataType, enforceType=False)
		
		if p.isOptional():
			p.setDefaultValue(self.ui.defaultEdit.text())
			
		return p