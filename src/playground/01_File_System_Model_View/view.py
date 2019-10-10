from PySide2.QtCore import QDir
from PySide2.QtWidgets import QSplitter, QTreeView, QListView, QTableView

class MyView(QSplitter):
	def __init__(self, model):
		QSplitter.__init__(self)
		model.setRootPath("C:/")
		self._model = model
		self._treeView = QTreeView(self)
		self._listView = QListView(self)
		
		self._treeView.setModel(model)
		self._listView.setModel(model)
		
		self._treeView.setRootIndex(model.index("C:/"))
		self._listView.setRootIndex(model.index(QDir.currentPath()))
		
		self.setWindowTitle("Two views onto the same file system")