from PySide2.QtWidgets import QWidget
from gui.ui.ui_actionmenuitem import Ui_Form as Ui_ActionMenuItem

class ActionMenuItem(QWidget):
	"""
	ActionMenuItem is a widget for Facile's Action Menu View.
	"""
	
	def __init__(self) -> 'ActionMenuItem':
		"""
		Constructs a ActionMenuItem object.

		:return: The new ActionMenuItem object
		:rtype: ActionMenuItem
		"""
		super(ActionMenuItem, self).__init__()
		
		# UI Initialization
		self.ui = Ui_ActionMenuItem()
		self.ui.setupUi(self)
		
	def setText(self, text: str) -> None:
		
		self.ui.actionLabel.setText(text)

