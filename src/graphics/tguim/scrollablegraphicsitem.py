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
from PySide2.QtGui import QColor, QWheelEvent

class ScrollableGraphicsItem(QGraphicsRectItem):

    MARGIN = 60  # left and right margin for scrolling

    def __init__(self, parent=None):
        QGraphicsRectItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemClipsChildrenToShape)

        # create empty invisible child
        self._ghostContainer = QGraphicsRectItem(self)
        self._ghostContainer.setFlag(QGraphicsItem.ItemHasNoContents)

        self.contents = []  # all items that we can scroll between

    def addItemToContents(self, item):
        assert(item not in self.contents)

        # add the item
        self.contents.append(item)
        item.setParentItem(self._ghostContainer)

        # set the position of the item
        cumulativeX = 0
        for i, item in enumerate(self.contents):
            item.setPos(ScrollableGraphicsItem.MARGIN * (i+1) + cumulativeX - self.boundingRect().width()/2,
                        -item.boundingRect().height()/2)
            cumulativeX += item.boundingRect().width()

    def removeItemFromContents(self, item):
        assert(item in self.contents)

        # permanently remove the item
        self.contents.remove(item)
        self.scene().removeItem(item)

        # remove all other items temporarily
        items = self.contents[:]
        self.contents = []
        for item in items:
            self.scene().removeItem(item)

        # Add items again to put them in the correct positions
        for item in items:
            self.addItemToContents(item)

    def getGhost(self):
        return self._ghostContainer

    def wheelEvent(self, event: QWheelEvent) -> None:
        br = self.boundingRect()
        cbr = self.childrenBoundingRect() # because of clipping, this doesn't go beyond the bounding rect

        canGoLeft = cbr.x() + cbr.width() > br.x() + br.width() - ScrollableGraphicsItem.MARGIN
        canGoRight = cbr.x() < br.x() + ScrollableGraphicsItem.MARGIN

        oldPos = self._ghostContainer.pos()
        if event.delta() > 0:
            if canGoRight:
                self._ghostContainer.setPos(oldPos.x() + 6, oldPos.y())
        else:
            if canGoLeft:
                self._ghostContainer.setPos(oldPos.x() - 6, oldPos.y())

    def paint(self, painter, option, widget):
        """
        Paints the contents of the component. Override the parent paint function

        :param painter: Use a Qpainter object.
        :type painter: QPainter
        :param option: It provides style options for the item.
        :type option: QStyleOptionGraphicsItem
        :param widget: QWidget
        :type widget: It points to the widget that is being painted on; or make it = None.
        :return: None
        :rtype: NoneType
        """
        
        boundingRect = self.boundingRect()
        
        painter.setBrush(QColor(10,10,10, 50))
    
        painter.drawRoundedRect(boundingRect, 5, 5)
        

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

        

