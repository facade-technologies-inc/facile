# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QColor, Qt
from ui.ui_facileview import Ui_MainWindow as Ui_FacileView


class FacileView(QMainWindow):
    def __init__(self):
        super(FacileView, self).__init__()
        self.ui = Ui_FacileView()
        self.ui.setupUi(self)

