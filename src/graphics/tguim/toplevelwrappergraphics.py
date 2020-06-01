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

This file contains the TopLevelWrapperGraphics class, which wraps around windows
and their extra components section.
"""

import os
from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QStyleOptionGraphicsItem, QWidget
from PySide2.QtGui import QColor, QPainter, QPen, QImageReader

from graphics.tguim.scrollablegraphicsitem import ScrollableGraphicsItem

class TopLevelWrapperGraphics(QGraphicsRectItem):
    """
    A wrapper for the top-level graphics item and the scrollable extra items.
    """
    
    BUFFER = 1
    BUTTON_WIDTH = 60
    BACKGROUND_COLOR = QColor(255, 0, 0)  # 100, 100, 100, 60)
    # Scrollable Item
    SGI_MIN_WIDTH = 1000
    SGI_MAX_WIDTH = 2000

    class Button(QGraphicsRectItem):
        """
        Expand/Collapse button to show/hide the scrollable extras

        This class is only to be used within the TopLevelWrapperGraphics class
        """
        ARROW_COLOR = QColor(30, 30, 30)
        BACKGROUND_COLOR = QColor(56, 56, 56)

        def __init__(self, *args, left=True, onClicked=None):
            QGraphicsRectItem.__init__(self,*args)
            self._left = left
            self._onClicked = onClicked
            self.setBrush(TopLevelWrapperGraphics.Button.BACKGROUND_COLOR)

        def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
            QGraphicsRectItem.paint(self, painter, option, widget)
            pen = QPen()
            pen.setWidth(5)
            pen.setColor(TopLevelWrapperGraphics.Button.ARROW_COLOR)
            painter.setPen(pen)
            
            if self._left:
                filename = 'button_col.jpg'
            else:  # if right
                filename = 'button_exp.jpg'
                
            ir = QImageReader()
            filename = ":/icon/resources/EC_Buttons/" + filename
            ir.setFileName(filename)
            
            painter.drawImage(self.boundingRect(), ir.read())

        def mousePressEvent(self, event):
            event.accept()
            self._onClicked()

    def __init__(self, topLevelGraphics=None):
        QGraphicsRectItem.__init__(self)
        self.setBrush(TopLevelWrapperGraphics.BACKGROUND_COLOR)
        self.setFlag(QGraphicsRectItem.ItemClipsChildrenToShape)
        
        # Set the window
        self._topLevelGraphics = topLevelGraphics
        b = TopLevelWrapperGraphics.BUFFER
        
        # Get its size and position
        self._x = self._topLevelGraphics.x() - b
        self._yG = self._topLevelGraphics.y()
        width = self._topLevelGraphics.boundingRect().width()
        self._heightG = self._topLevelGraphics.boundingRect().height()
        
        # Add it to self and set its position to (0,0)
        self._topLevelGraphics.setParentItem(self)
        # self._topLevelGraphics.setPos(0, 0)
        
        # Set the unused parts to None for the moment.
        self._scrollableItem = None
        self._collapseButton = None
        self._expandButton = None

        # Set size and position to the top-level graphics's position and size
        self.setRect(self._x, self._yG - b, width + b*2, self._heightG + b*2)

    def getWindowGraphics(self):
        """
        Gets the top-level component that is stored in this item.
        
        :return: Top-level window component being stored in this wrapper
        :rtype: ComponentGraphics
        """
        
        return self._topLevelGraphics

    def addECSection(self, ecs: 'ScrollableGraphicsItem'):
        """
        Adds the extra components section to this item, setting up the buttons with it.
        
        :param ecs: extra components section to add
        :type ecs: ScrollableGraphicsItem
        :return: None
        """

        ecs.setParentItem(self)
        self._scrollableItem = ecs
        ecs.prepareGeometryChange()

        # Define some variables
        b = TopLevelWrapperGraphics.BUFFER
        bWidth = TopLevelWrapperGraphics.BUTTON_WIDTH
        
        # Set the section's position and size. It'll be the exact same size (width) as the window.
        win = self._topLevelGraphics
        ecsWidth = min(TopLevelWrapperGraphics.SGI_MAX_WIDTH, max(TopLevelWrapperGraphics.SGI_MIN_WIDTH, win.width()))
        ecs.setRect(win.scenePos().x() + win.width(), self._yG, ecsWidth, self._heightG)

        # Instantiate the Expand Button
        tlg = self._topLevelGraphics
        self._expandButton = TopLevelWrapperGraphics.Button(self, left=False, onClicked=self.onExpandClicked)
        self._expandButton.setRect(tlg.scenePos().x() + tlg.width() + b, self._yG, bWidth, self._heightG)
        self._expandButton.hide()
        
        # Instantiate the Collapse Button
        sig = self._scrollableItem
        self._collapseButton = TopLevelWrapperGraphics.Button(self, left=True, onClicked=self.onCollapseClicked)
        self._collapseButton.setRect(tlg.scenePos().x() + tlg.width() + ecsWidth + b, self._yG, bWidth, self._heightG)

        # Adjust the size once we know how big things are
        cbbr = self._collapseButton.boundingRect()
        width = tlg.width() + sig.boundingRect().width() + cbbr.width() + b*3
        self.setRect(self._x, self._yG - b, width, self._heightG + b*2)
    
    def onCollapseClicked(self):
        """
        Collapses the extra component section
        
        :return: None
        """
        self._scrollableItem.hide()
        self._collapseButton.hide()
        self._expandButton.show()
        width = self._topLevelGraphics.width() + \
                TopLevelWrapperGraphics.BUTTON_WIDTH + \
                TopLevelWrapperGraphics.BUFFER * 3
        self.setRect(self._x, self._yG - TopLevelWrapperGraphics.BUFFER,
                     width, self._heightG + TopLevelWrapperGraphics.BUFFER*2)
        # self.boundingRect().setWidth(width)

    def onExpandClicked(self):
        """
        Expands the extra component section
        
        :return: None
        """
        self._scrollableItem.show()
        self._collapseButton.show()
        self._expandButton.hide()
        width = self._topLevelGraphics.width() + \
                self._scrollableItem.boundingRect().width() + \
                TopLevelWrapperGraphics.BUTTON_WIDTH + \
                TopLevelWrapperGraphics.BUFFER * 3
        self.setRect(self._x, self._yG - TopLevelWrapperGraphics.BUFFER,
                     width, self._heightG + TopLevelWrapperGraphics.BUFFER*2)
        # self.boundingRect().setWidth(width)

    def getLabel(self) -> str:
        """
        Gets the label from this TLW graphics item.
        
        :return: The label for this component.
        :rtype: str
        """
    
        return "Wrapper for " + self._topLevelGraphics.getLabel()

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
        painter.setBrush(QColor(100, 100, 100, 80))
        painter.drawRoundedRect(boundingRect, 5, 5)

if __name__ == "__main__":
    app = QApplication()

    # create view and scene
    view = QGraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)

    # create top level item
    topLevelItem = QGraphicsRectItem()
    topLevelItem.setRect(0, 0, 500, 300)
    topLevelItem.setBrush(QColor(255,255,255))

    tlwg = TopLevelWrapperGraphics(topLevelItem)
    scene.addItem(tlwg)

    view.show()
    app.exec_()
