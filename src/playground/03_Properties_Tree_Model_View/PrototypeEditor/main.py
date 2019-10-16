# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QLabel, QPushButton
from PySide2.QtCore import SIGNAL, QObject


def func():
    print("func has been called!")

if __name__ == "__main__":
    app = QApplication()

    #Create the tree structure
    label = QLabel("<font color=red size40>PropertyEditor</font>")
    label.show()

    button = QPushButton("Call func")
    QObject.connect(button, SIGNAL('clicked()'), func)
    button.show()
    sys.exit(app.exec_())


