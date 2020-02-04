import sys
import os

sys.path.append(os.path.abspath("../"))

from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
from gui.ui.ui_actionmenu import Ui_Form as Ui_ActionMenu
from gui.actionmenuitem import ActionMenuItem


class ActionMenu(QWidget):
	"""
	ActionMenu is a widget for Facile's API modules.
	"""
	
	def __init__(self) -> 'ActionMenu':
		"""
		Constructs a ActionMenu object.

		:return: The new ActionMenu object
		:rtype: ActionMenu
		"""
		super(ActionMenu, self).__init__()
		
		# UI Initialization
		self.ui = Ui_ActionMenu()
		self.ui.setupUi(self)
		
		#Widget Initialization
		self.ui._centralWidget = QWidget()
		self.ui._itemLayout = QVBoxLayout()
		
		self.ui._centralWidget.setLayout(self.ui._itemLayout)
		
		self.ui.menuItemScrollArea.setWidget(self.ui._centralWidget)

		for i in range(5):
			self.addAction(None)
			
		self.ui._itemLayout.addStretch()
	
	def addAction(self, action: "Action") -> None:
		menuItem = ActionMenuItem()
		menuItem.setText("Andrew ")

		self.ui._itemLayout.addWidget(menuItem)
	
	def setLabelText(self, text: str) -> None:
		self.ui.menuLabel.setText(text)
	
			
		
		
		
if __name__ == "__main__":
	app = QApplication([])
	
	window = ActionMenu()
	window.setLabelText("Andrews Menu")
	window.show()
	sys.exit(app.exec_())
