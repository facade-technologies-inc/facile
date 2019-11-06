# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QColor, Qt
from view.ui.ui_facileview import Ui_MainWindow as Ui_FacileView

from PrototypeEditor.data import GUIComponentProperties
from PrototypeEditor.model import PropModel
from PySide2.QtWidgets import QTreeView,QApplication
from PySide2.QtGui import QStandardItemModel
from project_explorer.model import MultipleProxyModel, pop_standard_model


class FacileView(QMainWindow):
    def __init__(self):
        super(FacileView, self).__init__()
        self.ui = Ui_FacileView()
        self.ui.setupUi(self)

        prop = GUIComponentProperties()
        self.ui.property_editor_view.setModel(prop.getModel())

        # create dummy models and populate them with data
        model_1 = QStandardItemModel()
        model_2 = QStandardItemModel()
        model_3 = QStandardItemModel()
        pop_standard_model(model_1)
        pop_standard_model(model_2)
        pop_standard_model(model_3)

        # create a model that wraps around all 3 dummy models.
        myModel = MultipleProxyModel(model_1, model_2, model_3)
        self.ui.project_explorer_view.setModel(myModel)



if __name__ == "__main__":
    
    def stylize(qApp):
        qApp.setStyle("Fusion")
    
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        qApp.setPalette(dark_palette)
        qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        
    app = QApplication([])
    stylize(app)
    window = FacileView()
    window.show()
    sys.exit(app.exec_())
