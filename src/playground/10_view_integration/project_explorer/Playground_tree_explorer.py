import sys
from PySide2.QtWidgets import QTreeView,QApplication
from PySide2.QtGui import QStandardItemModel
from model import MultipleProxyModel, pop_standard_model


if __name__ == "__main__":
    app = QApplication()
    
    # create dummy models and populate them with data
    model_1 = QStandardItemModel()
    model_2 = QStandardItemModel()
    model_3 = QStandardItemModel()
    pop_standard_model(model_1)
    pop_standard_model(model_2)
    pop_standard_model(model_3)

    # create a model that wraps around all 3 dummy models.
    myModel = MultipleProxyModel(model_1,model_2,model_3)
    
    # create a view to show the wrapper model in.
    view = QTreeView()
    view.setModel(myModel)
    view.show()
    
    sys.exit(app.exec_())

