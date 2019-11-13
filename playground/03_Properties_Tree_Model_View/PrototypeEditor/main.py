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
"""

import sys
from PySide2.QtWidgets import QApplication, QTreeView
from properties import Properties
from propeditordelegate import PropertyEditorDelegate

if __name__ == "__main__":
	
	app = QApplication()

	# Instantiate Properties Object
	customCategories = {"NewCategory": [{"name": "someProperty", "default": False, "type": bool,  "readOnly": False}]}
	predefinedCategories = ["Base", "Visual", "GUI Component"]
	properties = Properties.createPropertiesObject(predefinedCategories, customCategories)

	
	# Get model object associated with Properties object
	model = properties.getModel()

	# Instantiate custom delegate
	delegate = PropertyEditorDelegate()

	# Instantiate QTreeView object
	view = QTreeView()
	
	# load model into view.
	view.setModel(model)

	#load delegate into view
	view.setItemDelegate(delegate)

	view.show()
	sys.exit(app.exec_())
