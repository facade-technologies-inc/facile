"""
/------------------------------------------------------------------------------\
|                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
|------------------------------------------------------------------------------|
|                                                                              |
|    Copyright [2019] Facade Technologies Inc.                                 |
|    All Rights Reserved.                                                      |
|                                                                              |
| NOTICE:  All information contained herein is, and remains the property of    |
| Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
| and technical concepts contained herein are proprietary to Facade            |
| Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
| Patents, patents in process, and are protected by trade secret or copyright  |
| law.  Dissemination of this information or reproduction of this material is  |
| strictly forbidden unless prior written permission is obtained from Facade   |
| Technologies Inc.                                                            |
|                                                                              |
\------------------------------------------------------------------------------/

This module contains the PropModel() class.
"""

from PySide2.QtGui import QColor
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from enum import Enum


class PropModel(QAbstractItemModel):
    """
    A subclass that allows us to show the Data through QTreeView.
    """
    def __init__(self, propData: object):
        """
        Constructs a model for the Property Editor.

        :param propData: The data from the properties.
        :type propData: object
        :return: The constructed model.
        :rtype: QObject
        """
        QAbstractItemModel.__init__(self)
        self._propData = propData

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        """
        Purpose of this function is to return a QModelIndex that maps to the appropriate data

        :param row: Row of the index.
        :type row: int
        :param column: Column of the index.
        :type column: int
        :param parent: Parent of that row or column.
        :type parent: QModelIndex
        :return: The index for the data.
        :rtype: QModelIndex
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        # referencing category
        if not parent.isValid():
            internalData = self._propData.getCategories()[row]
        else:
            parentData = parent.internalPointer()
            if parentData in self._propData.getCategories():
                internalData = self._propData.getCategoryProperties(parentData)[row]

            else:
                return QModelIndex()

        return self.createIndex(row, column, internalData)

    def parent(self, index: QModelIndex) -> QModelIndex:
        """
        Purpose of this function is to return the parent index of the index that is provided

        :param index: Index that is provided.
        :type index: QModelIndex
        :return: Returns the parent index of the index provided.
        :rtype: QModelIndex
        """
        if not index.isValid():
            return QModelIndex()

        data = index.internalPointer()

        if data in self._propData.getCategories():
            return QModelIndex()

        category = self._propData.getPropertyCategory(data)

        return self.createIndex(self._propData.getCategoryIndex(category), 0, category)

    def columnCount(self, parent: QModelIndex) -> int:
        """
        Purpose of this function is to return the number of columns for the children of a given parent

        :param parent: Parent will tell us our column count.
        :type parent: QModelIndex
        :return: Number of columns.
        :rtype: int
        """
        return 2

    def rowCount(self, parent: QModelIndex) -> int:
        """
        Purpose of this function is to return the number of children of a given parent

        :param parent: Parent will tell us our column count.
        :type parent: QModelIndex
        :return: Number of rows.
        :rtype: int
        """
        if not parent.isValid():
            numCategories = self._propData.getNumCategories()
            return numCategories

        parentData = parent.internalPointer()

        if parentData in self._propData.getCategories():
            return self._propData.getNumPropertiesInCategory(parentData)
        else:
            return 0

    def data(self, index: QModelIndex, role: int) -> object:
        """
        Purpose of this function is to retrieve data stored under the given role for the item referred to by the
        index

        :param index: Index that is provided.
        :type index: QModelIndex
        :param role: The given role for item referred.
        :type role: int
        :return: Data of the given role from index.
        :rtype: object
        """
        if not index.isValid():
            return QModelIndex()

        row = index.row()
        col = index.column()
        data = index.internalPointer()

        if role == Qt.DisplayRole:
            if data in self._propData.getCategories():
                if col == 0:
                    return data
                else:
                    return None
            else:
                col = index.column()
                if col == 0:
                    return data.getName()
                elif col == 1:
                    t = data.getType()
                    if issubclass(t, Enum):
                        return data.getValue().name
                    return str(data.getValue())
                else:
                    return None

        elif role == Qt.BackgroundRole:
            if data in self._propData.getCategories():
                return QColor(Qt.yellow)
            else:
                shade = row % 2 * 25
                return QColor(100 + shade, 150 + shade, 200 + shade)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> object:
        """
        This method is used for displaying the header data for 'the given role
        and orientation of that specific section.

        :param section: Specific section for the header data.
        :type section: int
        :param orientation: Given orientation for the header data.
        :type orientation: Qt.Orientation
        :param role: The given role for the header data.
        :type role: int
        :return: Model of header data.
        :rtype: object
        """

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ["Name", "Value"][section]
        return None

    def traverse(self) -> None:
        """
        This method is used for debugging by mimicking how a view might query the model for data.

        :return: None
        :rtype: NoneType
        """
        parent = QModelIndex()
        work = [parent]

        while len(work) > 0:
            cur = work.pop()

            curRow = cur.row()
            curCol = cur.column()
            curData = self.data(cur, Qt.DisplayRole)
            if cur.isValid():
                print(curRow, curCol, curData)
                pass

            rows = self.rowCount(cur)
            cols = self.columnCount(cur)
            for r in range(rows):
                for c in range(cols):
                    work.append(self.index(r, c, cur))

    def setData(self, index: QModelIndex, value: object, role: int) -> bool:
        """
        Purpose of this function is to set the role data for the index to value

        :param index: Index that is provided.
        :type index: QModelIndex
        :param value: Value that is set.
        :type value: object
        :param role: The given role data.
        :type role: int
        :return: Set data for index to a value.
        :rtype: bool
        """
        if role != Qt.EditRole:
            return False

        if not index.isValid():
            return False

        if not value:
            return False

        data = index.internalPointer()

        if data in self._propData.getCategories():
            return False
        else:
            if index.column() != 1:
                return False
            else:
                valueWasSet = data.setValue(value)
                return valueWasSet

    def flags(self, index: QModelIndex) -> object:
        """
        Purpose of this function is to determine what can be done with a given index

        :param index: Index that is provided.
        :type index: QModelIndex
        :return: Returns the item flags for the given index.
        :rtype: ItemFlags
        """
        if not index.isValid():
            return Qt.NoItemFlags

        data = index.internalPointer()

        if data in self._propData.getCategories():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            if index.column() == 1:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable