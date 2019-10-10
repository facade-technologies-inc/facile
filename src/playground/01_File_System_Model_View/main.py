import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFileSystemModel, QTreeView
from view import MyView                                                  
#from model import MyModel

if __name__ == "__main__":
	app = QApplication([])
	model = QFileSystemModel()
	window = MyView(model)
	window.show()
	sys.exit(app.exec_())
	