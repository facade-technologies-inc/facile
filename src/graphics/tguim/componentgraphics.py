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

This module contains the ComponentGraphics class.
"""

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt, QFont, QFontMetricsF
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneContextMenuEvent, QMenu, QGraphicsWidget
import data.statemachine as sm
from graphics.tguim.scrollablegraphicsitem import ScrollableGraphicsItem
from graphics.tguim.toplevelwrappergraphics import TopLevelWrapperGraphics

from qt_models.componentmenu import ComponentMenu


class ComponentGraphics(QGraphicsItem):
    """
    This class displays an individual GUI component in the target gui,
    based on the component class.
    """
    
    # Individual Components
    PEN_WIDTH = 1.5  # Width of component borders
    TITLEBAR_H = 0  # Titlebar height
    TRIM = 1
    
    # Variable Settings
    # TODO: Should let user change these ones, and also warn them of extra processing power for smaller increment size.
    SCALE_INCR = 0.05  # Increment to use when trying to scale components. Smaller increments lead to
                       #   more realistic model, but require more processing power/time.
    MIN_SIDE_LENGTH = 3  # Prevents components from getting any smaller when a side reaches this size.
    
    # Top-Level Windows
    WINDOW_SPACING = 100  # Vertical spacing between windows in TGUIM
    MIN_AREA_THRESH_P = 0.25  # Qualifies a component to go to extra components section. Percent as proportion.
    WINDOW_LEFT_OFFSET = 30  # Offset from left side of scene to show all windows.
    WINDOW_HEIGHT = 600  # The fixed height for all top-level windows
    
    # Extra Components Sections
    EC_X_PADDING = 0  # Padding between top level windows and the EC section
    EC_MARGINS = 3  # *Half* of the spacing between components in the extra components section
    EC_ABS_WIDTH = 1000  # Locks the right edge placement of the EC section relative to x=0 in the scene
    MIN_TIME_DIFF = .05  # Time difference from the overlapping component
                         #   to qualify moving self to extra components section
    
    def __init__(self, dataComponent: 'Component', rect: tuple = (), parent=None):
        """
        Constructs a ComponentGraphics object

        :param dataComponent: get the data of a Component
        :type dataComponent: Component
        :param parent: parent ComponentGraphics
        :type parent: ComponentGraphics
        """
        
        QGraphicsItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
        if parent is None:
            self.isRoot = True  # TODO: Have to resize scene to smallest possible
        else:
            self.isRoot = False
        
        self._dataComponent = dataComponent
        
        # force components to have at least the minimum size
        self._x = rect[0]
        self._y = rect[1]
        
        # variables related to extra components algorithm
        self._extraComponents = []
        self.isExtraComponent = False
        self._ecSection = None  # reassigned later only if top-level window
        
        # --- This is where components get their initial positions set. ---
        
        # Root
        if self._dataComponent.getParent() is None:
            self._width = max(ComponentGraphics.MIN_SIDE_LENGTH, rect[2])
            self._height = max(ComponentGraphics.MIN_SIDE_LENGTH, rect[3])
            self.setPos(max(0, rect[0]), max(0, rect[1]))
            self._parentGraphics = None
            self._parentIsScene = False
            self._absScale = 1
        
        # Top-Level Window
        elif self._dataComponent.getParent().getParent() is None:
            # Set initial width, height, and scale
            self._width = max(ComponentGraphics.MIN_SIDE_LENGTH, rect[2])
            self._height = max(ComponentGraphics.MIN_SIDE_LENGTH, rect[3])
            self._absScale = 1
            
            # Scale to uniform height
            scale = ComponentGraphics.WINDOW_HEIGHT/self._height
            self.setScale(scale)

            # Forces windows to snap to top-left, aligned vertically.
            self.setPos(ComponentGraphics.WINDOW_LEFT_OFFSET, 0)
            self._parentGraphics = self.scene()
            self._parentIsScene = True
        
        # All other components
        else:
            self._width = max(ComponentGraphics.MIN_SIDE_LENGTH, rect[2])
            self._height = max(ComponentGraphics.MIN_SIDE_LENGTH,
                               rect[3] + ComponentGraphics.TITLEBAR_H)
            self.setPos(max(0, rect[0]),
                        max(0, rect[1] + ComponentGraphics.TITLEBAR_H))
            
            self._parentGraphics = self.scene().getGraphics(self._dataComponent.getParent())
            
            # Gets the absolute scale of the data parent and scales self accordingly
            self._absScale = self._parentGraphics.getAbsScale()
            self.setScale(self._absScale)
            
            self._parentIsScene = False
        
        self.adjustPositioning()

        # Creates the top-level wrapper, places self in it.
        # Important that this is after adjustPositioning
        if self._parentIsScene:
            self.scene().addItem(TopLevelWrapperGraphics(self))
        
        self.menu = ComponentMenu()
        self.menu.onBlink(lambda: self.scene().blinkComponent(self._dataComponent.getId()))
        
        try:
            self.triggerSceneUpdate()
        except:
            pass
    
    def getDataComponent(self) -> 'Component':
        """
        Returns self's datacomponent, ie the Component object this componentGraphics is representing

        :return: This ComponentGraphic's dataComponent
        :rtype: Component
        """
        
        return self._dataComponent
    
    def getGraphicalParent(self) -> 'ComponentGraphics':
        """
        Returns graphics for the parent of this componentgraphics item. Not always the same as the component's parent,
        specifically because of extra components section and the toplevel wrapper.
        
        :return: graphics for the parent of this componentgraphics item
        :rtype: ComponentGraphics
        """
        
        return self.parentItem()

    def getDataParentGraphics(self) -> 'ComponentGraphics':
        """
        Returns graphics for the parent of this componentgraphics's data item.

        :return: graphics for the parent of this componentgraphics's data item
        :rtype: ComponentGraphics
        """
    
        return self._parentGraphics
    
    def getNumberOfTokens(self) -> int:
        """
        Get the number of tokens.

        :return: the number of tokens
        :rtype: int
        """
        tokensCount = len(self._dataComponent.getSuperToken().tokens)
        
        return tokensCount
    
    def adjustPositioning(self) -> None:
        """
        Places windows in a vertical list

        :return: None
        :rtype: NoneType
        """
        
        if self._parent is None:
            # We're dealing with the root that should never be drawn.
            return
        
        siblings = self.getSiblings()
        
        if self._parentIsScene:
            newYPos = 0
            sib = None
            for sibling in siblings:
                tmpPos = sibling.y() + sibling.height()
                if tmpPos >= newYPos:
                    newYPos = tmpPos
                    sib = sibling
            
            if sib:
                newYPos += ComponentGraphics.WINDOW_SPACING
            else:
                newYPos = 0
            
            self.setPos(ComponentGraphics.WINDOW_LEFT_OFFSET, newYPos)
        
        # A window's 1st level of components
        elif self._dataComponent.getParent().getParent().getParent() is None:
            self.chkExtraComponent()
            # self.resolveCollisions()
        
        # All other components
        else:
            # self.resolveCollisions()
            pass
    
    def chkExtraComponents(self) -> None:
        """
        Moves any 1st-level/depth components of parent (a window) that overlap existing siblings, to the
        extra components section on the right of parent.

        :return: None
        :rtype: NoneType
        """

        if self._dataComponent.getParent().getParent() is None:
            collidingSibs = self.getCollidingSiblings()
            for sib in collidingSibs:
                if self.wasFoundMuchLaterThan(sib) and self.overlapsALotWith(sib):
                    if self._dataComponent.timestamp < sib.getDataComponent().timestamp:
                        self._parent.addToExtraComponents(sib)
                    else:  # timestamps are never going to be equal
                        self._parent.addToExtraComponents(self)
                else:
                    continue
                    
    def addToExtraComponents(self, component: 'ComponentGraphics'):
        """
        Adds a component to the extra components section.
        
        :param component: component to add to extra components section
        :type component: 'ComponentGraphics'
        :return: None
        """
        
        if self._dataComponent.getParent().getParent() is None:
            if not self._ecSection:
                # TODO: Work on integrating with wrapper.
                self._ecSection = ScrollableGraphicsItem()
                self._ecSection.setParentItem(self.parentItem())
                self._ecSection.setRect(self.x() + self.width() + ComponentGraphics.EC_X_PADDING,
                                        self.y(), ComponentGraphics.EC_ABS_WIDTH - self.width(),
                                        self.height())
            
            self._ecSection.addItemToContents(component)
            self._extraComponents.append(component)
            
    def getScrollableItem(self) -> 'ScrollableGraphicsItem':
        """
        Returns the scrollable item, i.e. the extra components section, tied to this item.
        Only works for top-level components.
        
        :return: The extra components section tied to this item
        :rtype: ScrollableGraphicsItem
        """

        if self._dataComponent.getParent().getParent() is None:
            return self._ecSection
    
    def getCollidingSiblings(self) -> list:
        """
        Returns all siblings that collide with self.

        :return: list of colliding siblings
        :rtype: list
        """
        
        collidingSiblings = []
        for sibling in self.getSiblings():
            if sibling is None:
                continue
            
            if self.overlapsWith(sibling):
                collidingSiblings.append(sibling)
        return collidingSiblings
    
    def setScale(self, scale: float) -> None:
        """
        Scales self to percentage of original size, by scaling its height and width. Scales towards top left corner.
        Always relative to current size, not to original size.

        :param scale: scale to scale component by
        :return: None
        :rtype: NoneType
        """
        
        self.prepareGeometryChange()
        
        self._absScale = scale * self._absScale
        self._width = scale * self._width
        self._height = scale * self._height
    
    def scaleChildren(self, scale: float) -> None:
        """
        Scales all of self's children to percentage of original size, also scaling their position relative to self.
        Scales towards top left corner of self. Always relative to current size, not to original size.

        :param scale: scale to scale component by
        :return: None
        :rtype: NoneType
        """
        
        for childData in self._dataComponent.getChildren():
            self.scene().getGraphics(childData).hardScale(scale)
    
    def scaleSiblings(self, scale: float) -> None:
        """
        Scales all of self's siblings to percentage of original size, also scaling their position relative to parent.
        Scales towards top left corner of self. Always relative to current size, not to original size.

        :param scale: scale to scale component by
        :return: None
        :rtype: NoneType
        """
        
        for sib in self.getSiblings():
            sib.hardScale(scale)
    
    def hardScale(self, scale: float) -> None:
        """
        Scales self and all children to percentage of original size, and also scales self and all components' positions
        relative to their parents as well. Always relative to current size, not to original size.

        :param scale: scale to scale component by
        :return: None
        :rtype: NoneType
        """
        
        self.setPos(self.x() * scale, self.y() * scale)
        self.scaleChildren(scale)
        self.setScale(scale)
        
    def getAbsScale(self) -> float:
        """
        Gets the absolute scale of this component.
        
        :return: absolute scale of this component
        :rtype: float
        """
        
        return self._absScale
    
    def wasFoundMuchLaterThan(self, sib: 'ComponentGraphics') -> bool:
        """
        Contrary to name, determines if *either self or sib* were found much later than the other,
        with "much later" being defined by ComponentGraphics.MIN_TIME_DIFF.

        :param sib: sibling of this ComponentGraphic's _dataComponent
        :type sib: ComponentGraphics
        :return: whether or not self was found much later than sib
        :rtype: bool
        """
        
        if abs(self._dataComponent.timestamp - sib.getDataComponent().timestamp) > ComponentGraphics.MIN_TIME_DIFF:
            return True
        else:
            return False
        
    def overlapsALotWith(self, sib: 'ComponentGraphics') -> bool:
        """
        Whether or not self overlaps a large area of sib
        
        :param sib: Sibling component that overlaps with self
        :type sib: ComponentGraphics
        :return: Whether or not self overlaps a large area of sib
        :rtype: bool
        """
        
        # TODO: Figure this out
        if self.x() + self.width() > sib.x():
            xoverlap = self.x() + self.width() - sib.x()
        elif self.x() < sib.x() + sib.width():
            pass
    
    def getSiblings(self) -> list:
        """
        Returns a list of all of the component's siblings.

        :return: self's siblings
        :rtype: list
        """
        
        siblings = [self.scene().getGraphics(sibling) for sibling in self._dataComponent.getSiblings() if
                    sibling is not self._dataComponent]
        siblings = list(filter(None, siblings))
        
        # Should never run, but here as failsafe
        if self._dataComponent in siblings:
            siblings.remove(self._dataComponent)
        
        return siblings
    
    def width(self) -> float:
        """
        Shortcut to get the boundingRect's width.
        
        :return: componentGraphic's width
        :rtype: float
        """
        
        return self.boundingRect().width()
    
    def height(self) -> float:
        """
        Shortcut to get the boundingRect's height.
        
        :return: componentGraphic's height
        :rtype: float
        """
        
        return self.boundingRect().height()
    
    def getX(self) -> int:
        """
        Gets the original x value
        
        :return: The original x value of the component
        :rtype: int
        """
        return self._x
    
    def getY(self):
        """
        
        :return: the original y value of the component
        :rtype: int
        """
        return self._y
        
    def getLabel(self) -> str:
        """
        Gets the label from this component.
        :return: The label for this component.
        :rtype: str
        """
        
        if self._dataComponent.getParent() is None:
            return ""
        try:
            category, name = self._dataComponent.getProperties().getProperty("Name")
            return name.getValue()
        except:
            return "No Label"
    
    def overlapsWith(self, sibling: 'ComponentGraphics') -> bool:
        """
        Determines if this ComponentGraphics is overlapping with another one.

        Components that share an edge are not necessarily considered to be overlapping.
        This method differs from collidesWithItem because of this.

        :param sibling: The other component to check collision with.
        :type sibling: ComponentGraphics
        :return: True if components overlap, False otherwise.
        :rtype: bool
        """
        
        selfBound = self.boundingRect(False)
        selfx = self.scenePos().x() + selfBound.x()
        selfy = self.scenePos().y() + selfBound.y()
        
        sibBound = sibling.boundingRect(False)
        sibx = sibling.scenePos().x() + sibBound.x()
        siby = sibling.scenePos().y() + sibBound.y()
        
        if (sibx < selfx + selfBound.width() and
                sibx + sibBound.width() > selfx and
                siby < selfy + selfBound.height() and
                siby + sibBound.height() > selfy):
            return True
        return False
    
    def contains(self, child: 'ComponentGraphics') -> bool:
        """
        Determines if one ComponentGraphics item completely contains another one visually.
        rectangles that match exactly are considered to be "containing" each other.

        This method is mostly used to determine if a parent component needs to be "grown" to fit its children
        inside.

        :param child: The component that we would like to determine if it's in the current component.
        :type child: ComponentGraphics
        :return: True if child is visually in the current component
        :rtype: bool
        """
        pBound = self.boundingRect(False)
        px = self.scenePos().x() + pBound.x()
        py = self.scenePos().y() + pBound.y()
        
        cBound = child.boundingRect(False)
        cx = child.scenePos().x() + cBound.x()
        cy = child.scenePos().y() + cBound.y()
        
        if (px <= cx and
                py <= cy and
                px + pBound.width() >= cx + cBound.width() and
                py + pBound.height() >= cy + cBound.height()):
            return True
        return False
    
    def boundingRect(self):
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.
        :return: create the bounding of the item
        :rtype: QRectF
        """
        halfWidth = ComponentGraphics.PEN_WIDTH / 2
        adjustment = -ComponentGraphics.TRIM + ComponentGraphics.PEN_WIDTH
        return QRectF(-halfWidth,
                      -halfWidth,
                      self._width + adjustment,
                      self._height + adjustment)
    
    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        The shape could be used for many things, like collision detection.

        :return: Returns the shape of this item as a QPainterPath in local coordinates.
        :rtype: QPainterPath
        """
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
    
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
        
        if self.isRoot or boundingRect.width() == 0 and boundingRect.height() == 0:
            painter.setPen(QPen(QColor(Qt.transparent)))
            painter.setBrush(QColor(Qt.transparent))
            return
        
        pen = QPen(QColor(100, 200, 255))
        if self.isSelected():
            pen.setStyle(Qt.DashDotLine)
            pen.setColor(QColor(255, 0, 0))
        else:
            pen.setStyle(Qt.SolidLine)
            pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        
        painter.setBrush(QColor(88, 183, 255))
        
        id = self._dataComponent.getId()
        
        painter.drawRoundedRect(boundingRect, 5, 5)
        br = self.boundingRect()
        
        # draw name label
        name = self.getLabel()
        # TODO: make a better algorithm on font size in the future
        # 44 width -> only cover 12 words with 5 -> 5Fonts one is 3.6 (added 5)
        # 48 width -> only cover 18 words with 4 -> 4Fonts one is 2.6 (added 5)
        if len(name) * 3.5 > self.boundingRect().width():
            if len(name) * 2.5 > self.boundingRect().width():
                nameFont = QFont("Times", 2)
            else:
                nameFont = QFont("Times", 4)
        else:
            nameFont = QFont("Times", 5)
        painter.setFont(nameFont)
        fm = QFontMetricsF(nameFont)
        name = fm.elidedText(name, Qt.ElideRight, br.width() - ComponentGraphics.TITLEBAR_H)
        
        painter.setBrush(QColor(100, 200, 255))
        painter.drawText(self.boundingRect().x() + 5, 13, name)
        
        if sm.StateMachine.instance.configVars.showTokenTags:
            self.drawTokenTag(br, painter)
    
    def drawTokenTag(self, br: QRectF, painter: 'QPainter'):
        """
        This is a helper function for the paint function.
        It renders "Token Tags" in the corners of the GUI Components displayed in the TGUIM View.
        Token Tags show how many Tokens are associated with the associated component.

        :param br: The bounding rectangle of the component.
        :type br: QRectF
        :param painter: A QPainter object.
        :type painter: QPainter
        :return: None
        :rtype: NoneType
        """
        
        # TODO: May want to rename TITLEBAR_H since titlebars are no longer used
        if br.width() >= ComponentGraphics.TITLEBAR_H:
            token_count = str(self.getNumberOfTokens())
            
            ttX = br.x() + br.width() - ComponentGraphics.TITLEBAR_H
            ttY = br.y()
            ttWidth = ComponentGraphics.TITLEBAR_H
            ttHeight = ComponentGraphics.TITLEBAR_H
            
            rectBox = QRectF(ttX, ttY, ttWidth, ttHeight)
            tokenTagFont = QFont("Times", 10)
            painter.setFont(tokenTagFont)
            painter.setBrush(QColor(255, 0, 0, 127))
            # painter.drawRect(rectBox)
            painter.drawEllipse(rectBox.center(), ttWidth / 2 - 1, ttHeight / 2 - 1)
            painter.setBrush(QColor(100, 200, 255))
            fm = QFontMetricsF(tokenTagFont)
            pixelsWide = fm.width(token_count)
            pixelsHigh = fm.height()
            painter.drawText(ttX + ttWidth / 2 - pixelsWide / 2, ttY + ttHeight / 2 + pixelsHigh / 4, token_count)
    
    def mousePressEvent(self, event):
        """
        This event handler is implemented to receive mouse press events for this item.

        :param event: a mouse press event
        :type event: QGraphicsSceneMouseEvent
        :return: None
        :rtype: NoneType
        """
        self.setSelected(True)
        self.scene().emitItemSelected(self._dataComponent.getId())
    
    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        """
        Opens a context menu (right click menu) for the component.

        :param event: The event that was generated when the user right-clicked on this item.
        :type event: QGraphicsSceneContextMenuEvent
        :return: None
        :rtype: NoneType
        """
        self.setSelected(True)
        self.menu.prerequest()
        selectedAction = self.menu.exec_(event.screenPos())
    
    def triggerSceneUpdate(self):
        """
        Update the scene.
        """
        self.scene().invalidate(self.scene().sceneRect(), QGraphicsScene.ItemLayer)
    
    def onDataUpdated(self):
        self.triggerSceneUpdate()
    
    def __repr__(self):
        """
        Returns the componentView id as a string.

        :return: the componentView id as a string.
        :rtype: str
        """
        return "Component: {}".format(self._dataComponent.getId())
