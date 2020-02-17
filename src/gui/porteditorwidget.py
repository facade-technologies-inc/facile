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
		
		if port is not None:
			self._port = port
		else:
			self._port = Port()
		self.updateEditor()
		
		if not allowOptional:
			self.ui.checkBoxOptional.setChecked(False)
			self.ui.checkBoxOptional.hide()
		
			
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
		self.ui.typeEdit.setText(str(self._port.getDataType().__name__))
		self.ui.checkBoxOptional.setChecked(self._port.isOptional())
		
	
	def updatePort(self) -> None:
		"""
		Sets all the values of the port values to the values of the editors
		
		:return: None
		:rtype: NoneType
		"""
		self._port.setName(self.ui.nameEdit.text())
		self._port.setOptional(self.ui.checkBoxOptional.isChecked())
		
		try:
			dataType = eval(self.ui.typeEdit.text())
			assert (type(dataType) == type)
		except:
			# TODO: Figure out what to do in the case that we didn't recognize it as a type.
			pass
		else:
			self._port.setDataType(dataType)
