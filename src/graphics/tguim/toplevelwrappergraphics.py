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
from PySide2.QtGui import QColor, QPainter, QPen, QImageReader, QCursor
from PySide2.QtCore import Qt

from graphics.tguim.scrollablegraphicsitem import ScrollableGraphicsItem


class TopLevelWrapperGraphics(QGraphicsRectItem):
    """
    A wrapper for the top-level graphics item and the scrollable extra items.
    """
    
    BUFFER = 1
    BUTTON_WIDTH = 60
    BACKGROUND_COLOR = QColor(120, 120, 120, 80)
    RESIZE_AREA_WIDTH = 8
    # Scrollable Item
    SGI_MIN_WIDTH = 500
    SGI_MIN_ASSGND_WIDTH = 1000
    SGI_MAX_ASSGND_WIDTH = 2000

    class Button(QGraphicsRectItem):
        """
        Expand/Collapse button to show/hide the scrollable extras

        This class is only to be used within the TopLevelWrapperGraphics class
        """
        ARROW_COLOR = QColor(30, 30, 30)
        BACKGROUND_COLOR = QColor(56, 56, 56)

        def __init__(self, *args, left=True, onClicked=None, resizer=False):
            QGraphicsRectItem.__init__(self,*args)
            self._left = left
            self._onClicked = onClicked
            self._resizer = resizer
            self.setBrush(TopLevelWrapperGraphics.Button.BACKGROUND_COLOR)
            self.setAcceptHoverEvents(True)
            if not resizer:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.SizeHorCursor))

        def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
            # QGraphicsRectItem.paint(self, painter, option, widget)
            if not self._resizer:
                if self._left:
                    filename = 'button_col.jpg'
                else:  # if right
                    filename = 'button_exp.jpg'

                ir = QImageReader()
                filename = ":/icon/resources/EC_Buttons/" + filename
                ir.setFileName(filename)

                painter.drawImage(self.boundingRect(), ir.read())
            else:
                painter.setPen(Qt.transparent)
                painter.setBrush(QColor(200, 200, 200))
                painter.drawRoundedRect(self.boundingRect(), 5, 5)

        def mousePressEvent(self, event):
            """
            Overloads the default mouse press event. Implemented to enable manual resizing.

            :param event: The mouse event
            :type event: QtWidgets.QGraphicsSceneMouseEvent
            """
            if not self._resizer:
                event.accept()
                self._onClicked()
            else:
                tlw: TopLevelWrapperGraphics = self.parentItem()
                if tlw._scrollableItem:
                    tlw.mouseDragStartPos = event.pos()
                    tlw.prevWidth = tlw._width
                # QGraphicsRectItem.mousePressEvent(self, event)

        def mouseMoveEvent(self, event):
            """
            Overloads the default mouse move event. Implemented to enable manual resizing.

            :param event: The mouse event
            :type event: QtWidgets.QGraphicsSceneMouseEvent
            """
            if self._resizer:
                tlw: TopLevelWrapperGraphics = self.parentItem()
                if tlw._scrollableItem:
                    if event.button() in (Qt.LeftButton, Qt.NoButton) and not tlw.mouseDragging:
                        tlw.mouseDragging = True

                    if tlw.mouseDragging:
                        tlw.mouseDragEndPos = event.pos()

                        # Calculate the difference in position
                        diff = tlw.mouseDragEndPos.x() - tlw.mouseDragStartPos.x()

                        # Calculate the new sgi width
                        sgi = tlw._scrollableItem
                        sgiRect = sgi.rect()
                        newSGIWidth = sgiRect.width() + diff
                        if newSGIWidth >= TopLevelWrapperGraphics.SGI_MIN_WIDTH:
                            # Move Ghost container logically
                            canGoLeft = sgi.ghostCanGoLeft()
                            canGoRight = sgi.ghostCanGoRight()
                            curMaxX = tlw.scenePos().x() + tlw.rect().width() - self.rect().width() - \
                                TopLevelWrapperGraphics.BUTTON_WIDTH - TopLevelWrapperGraphics.BUFFER
                            print(sgi.getGhost().x())
                            if diff > 0:  # Expanding self
                                # We should move the ghost container with the expansion
                                if canGoRight and not canGoLeft and sgi.getGhost().scenePos().x() < sgi.scenePos().x():
                                    sgi.getGhost().moveBy(diff, 0)

                                # Prevent the expansion from going far past last item
                                elif curMaxX >= sgi.getMaxX():
                                    return

                                # Otherwise keep the container on the left
                                elif not canGoRight:
                                    sgi.getGhost().setPos(sgi.scenePos().x(), sgi.scenePos().y())

                            # Resize SGI
                            sgiRect.setWidth(newSGIWidth)
                            tlw._scrollableItem.setRect(sgiRect)

                            # Move collapse button and resizer (self)
                            tlw._collapseButton.moveBy(diff, 0)
                            self.moveBy(diff, 0)

                            # Resize TLWGI
                            tlwRect = tlw.rect()
                            tlwRect.setWidth(tlwRect.width() + diff)
                            tlw.setRect(tlwRect)

                        tlw.prepareGeometryChange()
                        tlw.update()
                    else:
                        # Allows the user to still move the scene w click & drag
                        QGraphicsRectItem.mouseMoveEvent(self, event)
                        return
                else:
                    QGraphicsRectItem.mouseMoveEvent(self, event)
            else:
                QGraphicsRectItem.mouseMoveEvent(self, event)

        def mouseReleaseEvent(self, event):
            """
            Overloads the default mouse release event. Implemented to enable manual resizing.

            :param event: The mouse event
            :type event: QtWidgets.QGraphicsSceneMouseEvent
            """
            if self._resizer:
                tlw: TopLevelWrapperGraphics = self.parentItem()
                if tlw.mouseDragging:
                    tlw.prepareGeometryChange()
                    tlw._width = tlw.rect().width()
                    tlw.mouseDragging = False
                    tlw.update()
            QGraphicsRectItem.mouseReleaseEvent(self, event)

    def __init__(self, topLevelGraphics=None):
        QGraphicsRectItem.__init__(self)
        self.setBrush(TopLevelWrapperGraphics.BACKGROUND_COLOR)
        self.setFlag(QGraphicsRectItem.ItemClipsChildrenToShape)
        self.setAcceptDrops(True)
        
        # Set the window
        self._topLevelGraphics = topLevelGraphics
        b = TopLevelWrapperGraphics.BUFFER
        
        # Get its size and position
        self._x = self._topLevelGraphics.x() - b
        self._yG = self._topLevelGraphics.y()
        self._width = self._topLevelGraphics.boundingRect().width()
        self._heightG = self._topLevelGraphics.boundingRect().height()
        
        # Add it to self and set its position to (0,0)
        self._topLevelGraphics.setParentItem(self)
        # self._topLevelGraphics.setPos(0, 0)
        
        # Set the unused parts to None for the moment.
        self._scrollableItem = None
        self._collapseButton = None
        self._expandButton = None
        self._resizer = None

        # Set size and position to the top-level graphics's position and size
        self.setRect(self._x, self._yG - b, self._width + b*2, self._heightG + b*2)

        # All things related to resizing
        self.mouseDragStartPos = None
        self.mouseDragEndPos = None
        self.mouseDragging = False
        self.prevWidth = self.rect().width()

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

        # Define some variables
        b = TopLevelWrapperGraphics.BUFFER
        bWidth = TopLevelWrapperGraphics.BUTTON_WIDTH
        
        # Set the section's position and size. It'll be the exact same size (width) as the window.
        win = self._topLevelGraphics
        ecsWidth = min(TopLevelWrapperGraphics.SGI_MAX_ASSGND_WIDTH, max(TopLevelWrapperGraphics.SGI_MIN_ASSGND_WIDTH,
                                                                         win.width()))
        ecs.setRect(win.scenePos().x() + win.width(), self._yG, ecsWidth, self._heightG)

        # Instantiate the Expand Button
        tlg = self._topLevelGraphics
        self._expandButton = TopLevelWrapperGraphics.Button(self, left=False, onClicked=self.onExpandClicked)
        self._expandButton.setRect(tlg.scenePos().x() + tlg.width() + b, self._yG+2, bWidth-4, self._heightG-4)
        self._expandButton.hide()
        
        # Instantiate the Collapse Button
        sig = self._scrollableItem
        self._collapseButton = TopLevelWrapperGraphics.Button(self, left=True, onClicked=self.onCollapseClicked)
        self._collapseButton.setRect(tlg.scenePos().x() + tlg.width() + ecsWidth + b, self._yG+2, bWidth-4,
                                     self._heightG-4)

        # Instantiate the resizing button
        resizeWidth = TopLevelWrapperGraphics.RESIZE_AREA_WIDTH
        self._resizer = TopLevelWrapperGraphics.Button(self, resizer=True)
        self._resizer.setRect(tlg.scenePos().x() + tlg.width() + ecsWidth + bWidth + b*2,
                                     self._yG + 2, resizeWidth, self._heightG - 4)

        # Adjust the size once we know how big things are
        cbbr = self._collapseButton.boundingRect()
        self._width = tlg.width() + sig.boundingRect().width() + cbbr.width() + b*4 + resizeWidth
        self.setRect(self._x, self._yG - b, self._width, self._heightG + b*2)
    
    def onCollapseClicked(self):
        """
        Collapses the extra component section
        
        :return: None
        """
        self._scrollableItem.hide()
        self._collapseButton.hide()
        self._resizer.hide()
        self._expandButton.show()
        self._width = self._topLevelGraphics.width() + \
                TopLevelWrapperGraphics.BUTTON_WIDTH + \
                TopLevelWrapperGraphics.BUFFER * 3
        self.setRect(self._x, self._yG - TopLevelWrapperGraphics.BUFFER,
                     self._width, self._heightG + TopLevelWrapperGraphics.BUFFER*2)
        # self.boundingRect().setWidth(width)

    def onExpandClicked(self):
        """
        Expands the extra component section
        
        :return: None
        """
        self._scrollableItem.show()
        self._collapseButton.show()
        self._expandButton.hide()
        self._resizer.show()
        self._width = self._topLevelGraphics.width() + \
                self._scrollableItem.boundingRect().width() + \
                TopLevelWrapperGraphics.BUTTON_WIDTH + \
                TopLevelWrapperGraphics.RESIZE_AREA_WIDTH + \
                TopLevelWrapperGraphics.BUFFER * 4
        self.setRect(self._x, self._yG - TopLevelWrapperGraphics.BUFFER,
                     self._width, self._heightG + TopLevelWrapperGraphics.BUFFER*2)

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
        painter.setBrush(TopLevelWrapperGraphics.BACKGROUND_COLOR)
        painter.drawRoundedRect(boundingRect, 5, 5)
