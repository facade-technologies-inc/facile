"""
..
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

This module contains the ScrollableGraphicsItem class.
"""

from PySide2.QtWidgets import QGraphicsItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide2.QtGui import QColor, QWheelEvent, Qt, QPen


class ScrollableGraphicsItem(QGraphicsRectItem):

    MARGIN = 60  # left and right margin for scrolling

    def __init__(self, parent=None):
        QGraphicsRectItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemClipsChildrenToShape)

        self._maxX = 0

        # create empty invisible child
        self._ghostContainer = QGraphicsRectItem(self)
        self._ghostContainer.setFlag(QGraphicsItem.ItemHasNoContents)
        self._ghostContainer.setPos(0, 0)

        self.contents = []  # all items that we can scroll between

    def addItemToContents(self, item):
        # assert(item not in self.contents)

        # add the item
        self.contents.append(item)
        item.setParentItem(self._ghostContainer)

        # set the position of the item
        cumulativeX = self.parentItem().scenePos().x() + self.parentItem().getWindowGraphics().width()
        y = self.parentItem().getWindowGraphics().scenePos().y() + self.boundingRect().height()/2 - item.height()/2

        if self.contents:
            item.prepareGeometryChange()
            for i, curItem in enumerate(self.contents):
                item.setPos(ScrollableGraphicsItem.MARGIN * (i+1) + cumulativeX, y)
                cumulativeX += curItem.width()
            self._maxX = cumulativeX + item.width() + ScrollableGraphicsItem.MARGIN*3
        else:
            self._ghostContainer.setPos(self.scenePos().x(), self.scenePos().y())
            item.setPos(ScrollableGraphicsItem.MARGIN, y)

    def removeItemFromContents(self, item):
        assert(item in self.contents)

        # permanently remove the item
        self.contents.remove(item)
        self.scene().removeItem(item)

        self.refreshContents()

    def refreshContents(self):
        """
        Updates the contents after a change
        """
        # remove all other items temporarily
        items = self.contents[:]
        self.contents = []
        for item in items:
            self.scene().removeItem(item)

        # Add items again to put them in the correct positions
        for item in items:
            self.addItemToContents(item)

    def getMaxX(self):
        """
        Gets the max X value
        """
        return self._maxX

    def getGhost(self):
        return self._ghostContainer

    def ghostCanGoLeft(self):
        br = self.boundingRect()
        cbr = self.childrenBoundingRect()  # because of clipping, this doesn't go beyond the bounding rect

        return cbr.x() + cbr.width() > br.x() + br.width() - ScrollableGraphicsItem.MARGIN

    def ghostCanGoRight(self):
        return self._ghostContainer.scenePos().x() <= self.scenePos().x()

    def wheelEvent(self, event: QWheelEvent) -> None:
        oldY = self._ghostContainer.pos().y()
        if event.delta() > 0:
            if self.ghostCanGoRight():
                for i in range(1, 17):
                    self._ghostContainer.setPos(self._ghostContainer.pos().x() + 1, oldY)
        else:
            if self.ghostCanGoLeft():
                for i in range(1, 17):
                    self._ghostContainer.setPos(self._ghostContainer.pos().x() - 1, oldY)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.transparent)
        painter.setPen(pen)

if __name__ == "__main__":
    app = QApplication()

    # create view and scene
    view = QGraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)

    # create scrollable item
    scrollableItem = ScrollableGraphicsItem()
    scene.addItem(scrollableItem)
    scrollableItem.setRect(-250, -50, 500, 100)
    # scrollableItem.setBrush(QColor(0, 255, 0))

    # create nested items
    width = 50
    height = 50
    buffer = 10
    for i in range(15):
        item = QGraphicsRectItem(0, 0, width, height)
        scrollableItem.addItemToContents(item)
        item.setBrush(QColor(255, 0, 0))

    view.show()

    app.exec_()


