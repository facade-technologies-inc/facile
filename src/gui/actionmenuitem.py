from PySide2.QtWidgets import QWidget
from gui.ui.ui_actionmenuitem import Ui_Form as Ui_ActionMenuItem

class ActionMenuItem(QWidget):
	"""
	ActionMenuItem is a widget for Facile's Action Menu View.
	"""
	
	def __init__(self, action: 'Action') -> 'ActionMenuItem':
		"""
		Constructs a ActionMenuItem object.

		:return: The new ActionMenuItem object.
		:rtype: ActionMenuItem
		"""
		super(ActionMenuItem, self).__init__()
		
		# UI Initialization
		self.ui = Ui_ActionMenuItem()
		self.ui.setupUi(self)
		
		#Set text for the action menu item
		self._action = action
		self.setText(self.getName())
	
	def getName(self) -> str:
		"""
		
		:return:
		"""
		return self._action.getProperties().getProperty("Name")[1].getValue()
		
	def setText(self, text: str) -> None:
		"""
		Sets the name of the action item.
		
		:param text: Name of action item.
		:type text: str
		:return: None
		:rtype: Nonetype
		"""
		self.ui.actionLabel.setText(text)
	
#TODO: Action graphics in reference to Port Graphics in seperate class
#TODO: Make a method to paint the graphics
#TODO: Make a method to draw the custom graphic
#TODO: Make a method to set the graphic
