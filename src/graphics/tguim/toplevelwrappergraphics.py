
from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QStyleOptionGraphicsItem, QWidget
from PySide2.QtGui import QColor, QPainter, QPen

from graphics.tguim.scrollablegraphicsitem import ScrollableGraphicsItem

class TopLevelWrapperGraphics(QGraphicsRectItem):
    """
    A wrapper for the top-level graphics item and the scrollable extra items.
    """
    
    BUFFER = 2
    BUTTON_WIDTH = 50
    BACKGROUND_COLOR = QColor(0, 10, 255)
    
    EC_ABS_WIDTH = 1000  # Locks the right edge placement of the EC section relative to x=0 in the scene

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

            br = self.boundingRect()
            x = -br.width() / 2
            y = -br.height() / 2

            # calculate arrow points as if it were facing left, then flip if necessary.
            vertexX = br.x() + br.width() / 4
            vertexY = br.y() + br.height() / 2
            topX = br.x() + br.width() * 3 / 4
            topY = br.y() + br.height() / 4
            bottomX = topX
            bottomY = br.y() + br.height() * 3 / 4

            if not self._left: # if right
                vertexX = br.x() + br.width() * 3 / 4
                topX = br.x() + br.width() / 4
                bottomX = topX

            painter.drawLine(vertexX, vertexY, bottomX, bottomY)
            painter.drawLine(vertexX, vertexY, topX, topY)

        def mousePressEvent(self, event):
            event.accept()
            self._onClicked()

    def __init__(self, topLevelGraphics=None):
        QGraphicsRectItem.__init__(self)
        
        # Set the window
        self._topLevelGraphics = topLevelGraphics
        
        # Get its size and position
        x = self._topLevelGraphics.x()
        y = self._topLevelGraphics.y()
        width = self._topLevelGraphics.boundingRect().width()
        height = self._topLevelGraphics.boundingRect().height()
        
        # Add it to self and set its position to (0,0)
        self._topLevelGraphics.setParentItem(self)
        # self._topLevelGraphics.setPos(0, 0)
        
        # Set the unused parts to None for the moment.
        self._scrollableItem = None
        self._collapseButton = None
        self._expandButton = None

        # Set size and position to the top-level graphics's position and size
        self.setRect(x, y, width, height)
        
    def addECSection(self, ecs: 'ScrollableGraphicsItem'):
        """
        Adds the extra components section to this item, setting up the buttons with it.
        
        :param ecs: extra components section to add
        :type ecs: ScrollableGraphicsItem
        :return: None
        """

        ecs.setParentItem(self)
        self._scrollableItem = ecs
        
        # Set the section's position and size
        win = self._topLevelGraphics
        ecs.setRect(win.x() + win.width(), win.y(), TopLevelWrapperGraphics.EC_ABS_WIDTH - win.width(), win.height())

        # Define some variables
        bWidth = TopLevelWrapperGraphics.BUTTON_WIDTH
        height = self._topLevelGraphics.boundingRect().height()

        # Instantiate the Expand Button
        tlbr = self._topLevelGraphics.boundingRect()
        self._expandButton = TopLevelWrapperGraphics.Button(self, left=False, onClicked=self.onExpandClicked)
        self._expandButton.setRect(tlbr.x() + tlbr.width(), tlbr.y(), bWidth, height)
        self._expandButton.hide()
        
        # Instantiate the Collapse Button
        sibr = self._scrollableItem.boundingRect()
        self._collapseButton = TopLevelWrapperGraphics.Button(self, left=True, onClicked=self.onCollapseClicked)
        self._collapseButton.setRect(sibr.x() + sibr.width(), sibr.y(), bWidth, height)
        self._collapseButton.hide()

        # Adjust the size once we know how big things are
        ebbr = self._expandButton.boundingRect()
        width = tlbr.width() + ebbr.width() + TopLevelWrapperGraphics.BUFFER
        self.setRect(self.x(), self.y(), width, height)
    
    def onCollapseClicked(self):
        """
        Collapses the extra component section
        
        :return: None
        """
        self._scrollableItem.hide()
        self._collapseButton.hide()
        self._expandButton.show()
        width = self._topLevelGraphics.rect().width() + \
                self._expandButton.rect().width() + \
                TopLevelWrapperGraphics.BUFFER
        self.setRect(self.rect().x(), self.rect().y(), width, self.rect().height())

    def onExpandClicked(self):
        """
        Expands the extra component section
        
        :return: None
        """
        self._scrollableItem.show()
        self._collapseButton.show()
        self._expandButton.hide()
        width = self._topLevelGraphics.rect().width() + \
                self._scrollableItem.rect().width() + \
                self._collapseButton.rect().width() + \
                TopLevelWrapperGraphics.BUFFER * 2
        self.setRect(self.rect().x(), self.rect().y(), width, self.rect().height())

    def getLabel(self) -> str:
        """
        Gets the label from this TLW graphics item.
        
        :return: The label for this component.
        :rtype: str
        """
    
        return "Wrapper for " + self._topLevelGraphics.getLabel()

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
