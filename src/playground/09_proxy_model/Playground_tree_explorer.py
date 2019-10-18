import sys
from PySide2.QtWidgets import QTreeView,QApplication
from PySide2.QtGui import QStandardItemModel
import model

if __name__ == "__main__":
    app = QApplication()
    model_1 = QStandardItemModel()
    model_2 = QStandardItemModel()
    model_3 = QStandardItemModel()
    model.pop_standard_model(model_1)
    model.pop_standard_model(model_2)
    model.pop_standard_model(model_3)


    view = QTreeView()
    

    view.setModel(model_1)
   

    view.show()
    sys.exit(app.exec_())

