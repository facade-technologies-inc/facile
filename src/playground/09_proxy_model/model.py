from PySide2.QtGui import QStandardItem
from PySide2.QtGui import QAbstractProxyModel

def pop_standard_model(model):

    for i in range(3):
        parent1 = QStandardItem('Family {}. Some long status text for sp'.format(i))
        for j in range(3):
            child1 = QStandardItem('Child {}'.format(i*3+j))
            child2 = QStandardItem('row: {}, col: {}'.format(i, j+1))
            child3 = QStandardItem('row: {}, col: {}'.format(i, j+2))
            parent1.appendRow([child1, child2, child3])
        model.appendRow(parent1)

class MultipleProxyModel(QAbstractProxyModel):
    def __init__(self):



   
        