import sys
from PySide2.QtWidgets import QApplication, QTreeView
import data
from propertyeditordelegate import PropertyEditorDelegate

if __name__ == "__main__":
	
	app = QApplication()
	
	# Instantiate Properties Object
	prop = data.GUIComponentProperties()
	"""
	propFactory = PropertiesFactory()
	prop = propFactory.createPropertiesObject([Base])
	"""
	
	# Get model object associated with Properties object
	model = prop.getModel()

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
