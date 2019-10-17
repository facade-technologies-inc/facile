import data

if __name__ == "__main__":
	
	app = QApplication()
	
	# 1. instantiate Properties Object
	prop = data.GUIComponentProperties()
	
	# 2. Get model object associated with Properties object
	model = prop.getModel()
	
	# 3. Instantiate QTreeView object
	view = QTreeView()
	
	# 4. load model into view.
	
	
	sys.exit(app.exec_())
