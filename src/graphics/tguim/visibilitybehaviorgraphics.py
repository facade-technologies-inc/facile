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

This module contains the VBGraphics class.
"""

from copy import copy

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QPainter, QPen, Qt, QColor, QBrush, QPainterPathStroker, QContextMenuEvent, \
    QMouseEvent
from PySide2.QtWidgets import QGraphicsItem, QAbstractGraphicsShapeItem

import data.statemachine as sm
from qt_models.visibilitybehaviormenu import VisibilityBehaviorMenu
from gui.settriggeractiondialog import SetTriggerActionDialog


class VBGraphics(QAbstractGraphicsShapeItem):
    MAX_LEFT_DIST = 140
    MIN_LEFT_DIST = 20
    ARROW_COL = QColor(230, 230, 230)
    SEL_ARROW_COL = QColor(255, 200, 50)
    HIDDEN_ARROW_COL = copy(ARROW_COL)
    HIDDEN_ARROW_COL.setAlpha(round(ARROW_COL.alpha()/2))

    def __init__(self, dataVisibilityBehavior: 'VisibilityBehavior', parent: 'TGUIMScene'):
        """
        Construct the VBGraphics class.
        'src' means the source component, the one triggering the vb.
        'dest' means the destination component, the one receiving and affected by the vb.

        :param dataVisibilityBehavior: get the data of a VisibilityBehavior
        :type dataVisibilityBehavior: VisibilityBehavior
        :param parent: The parent of the visibility behavior (This will always be the scene)
        :type parent: TGUIMScene
        :return: None
        :rtype: NoneType
        """
        QAbstractGraphicsShapeItem.__init__(self)
        parent.addItem(self)
        self._dataVB = dataVisibilityBehavior
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self._srcComp = self.scene().getGraphics(self._dataVB.getSrcComponent())
        self._dstComp = self.scene().getGraphics(self._dataVB.getDestComponent())
        self._boundingRect = None
        self._path = None

        self._compIsHidden = False # When path is built, if a connected component is hidden, this will be True

        def onRemove():
            tguim = sm.StateMachine.instance._project.getTargetGUIModel()
            tguim.removeVisibilityBehavior(self._dataVB)
            self.scene().removeItem(self)
            sm.StateMachine.instance.view.ui.propertyEditorView.setModel(None)

        def onSetTriggerAction():
            dlg = SetTriggerActionDialog(self._dataVB)
            dlg.exec_()

        def focus():
            self._zoomable = True
            self.scene().views()[0].smoothFocus(self)

        self.menu = VisibilityBehaviorMenu()
        self.menu.onRemove(onRemove)
        self.menu.onSetTrigger(onSetTriggerAction)
        self.menu.onFocus(focus)

    def boundingRect(self):
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.

        :return: create the bounding of the item
        :rtype: QRectF
        """
        if self._boundingRect:
            return self._boundingRect

        srcPos = self._srcComp.scenePos()
        dstPos = self._dstComp.scenePos()

        leftCornerX = min(srcPos.x(), dstPos.x())
        leftCornerY = min(srcPos.y(), dstPos.y())
        width = abs(srcPos.x() - dstPos.x())
        height = abs(srcPos.y() - dstPos.y())
        return QRectF(leftCornerX, leftCornerY, width, height)

    def paint(self, painter: QPainter, option, widget):
        """
        Paints the contents of the visibilitybehavior. Override the parent paint function.
        Only renders the visibility behavior if the configuration variable, showBehaviors, is true.

        :param painter: Use a Qpainter object.
        :type painter: QPainter
        :param option: It provides style options for the item.
        :type option: QStyleOptionGraphicsItem
        :param widget: QWidget
        :type widget: It points to the widget that is being painted on; or make it = None.
        :return: None
        :rtype: NoneType
        """
        # Only draw visibility behaviors if "Show Visibility Behaviors" action is checked in the View drop down.
        if sm.StateMachine.instance.configVars.showBehaviors:
            pen = QPen()
            if self.isSelected():
                arrowColor = VBGraphics.SEL_ARROW_COL
                pen.setStyle(Qt.DashDotLine)
            else:
                arrowColor = VBGraphics.ARROW_COL
                if self._compIsHidden:
                    arrowColor = VBGraphics.HIDDEN_ARROW_COL
                pen.setStyle(Qt.SolidLine)

            pen.setColor(arrowColor)

            pen.setJoinStyle(Qt.RoundJoin)
            pen.setCapStyle(Qt.RoundCap)
            pen.setWidth(3)
            painter.setPen(pen)

            # Path and Arrowhead
            path, arrival, direction, pathBoundingRect = self.buildPath()
            arrowHead, arrowHeadBoundingRect = self.buildArrowHead(arrival, direction)

            brTLx = min(pathBoundingRect.topLeft().x(), arrowHeadBoundingRect.topLeft().x())
            brTLy = min(pathBoundingRect.topLeft().y(), arrowHeadBoundingRect.topLeft().y())
            brBLy = max(pathBoundingRect.bottomLeft().y(), arrowHeadBoundingRect.bottomLeft().y())
            brTRx = max(pathBoundingRect.topRight().x(), arrowHeadBoundingRect.topRight().x())
            brHeight = brBLy - brTLy
            brWidth = brTRx - brTLx

            margin = 100

            self._boundingRect = QRectF(brTLx - margin, brTLy - margin, brWidth + margin * 2, brHeight + margin * 2)

            # Either of these lines will fix the drawing issue
            self.prepareGeometryChange()
            # self.scene().setSceneRect(self.scene().itemsBoundingRect())

            # Draw path
            painter.drawPath(path)

            # Draw Arrowhead
            pen.setStyle(Qt.SolidLine)
            painter.setPen(pen)
            painter.drawPath(arrowHead)
            painter.fillPath(arrowHead, QBrush(arrowColor))

    def buildArrowHead(self, arrival, direction):
        """
        Draws the path for the arrowhead.

        :param arrival: x,y coordinate tuple of arrival point
        :type arrival: tuple
        :param direction: Direction of arrival - from top:0, left:1, right:2, bottom:3
        :type direction: int
        """
        x = arrival[0]
        y = arrival[1]

        # draw the arrow head
        aSize = 4
        if direction == 0:  # Top
            arrowHead = QPainterPath()
            arrowHead.moveTo(x, y)
            arrowHead.lineTo(x - aSize, y - aSize * 2)
            arrowHead.lineTo(x + aSize, y - aSize * 2)
            arrowHead.lineTo(x, y)
        elif direction == 1:  # Left
            arrowHead = QPainterPath()
            arrowHead.moveTo(x, y)
            arrowHead.lineTo(x - aSize * 2, y - aSize)
            arrowHead.lineTo(x - aSize * 2, y + aSize)
            arrowHead.lineTo(x, y)
        elif direction == 2:  # Right
            arrowHead = QPainterPath()
            arrowHead.moveTo(x, y)
            arrowHead.lineTo(x + aSize * 2, y - aSize)
            arrowHead.lineTo(x + aSize * 2, y + aSize)
            arrowHead.lineTo(x, y)
        else:  # Bottom
            arrowHead = QPainterPath()
            arrowHead.moveTo(x, y)
            arrowHead.lineTo(x - aSize, y + aSize * 2)
            arrowHead.lineTo(x + aSize, y + aSize * 2)
            arrowHead.lineTo(x, y)

        boundingRect = arrowHead.boundingRect()

        return arrowHead, boundingRect

    def buildPath(self) -> tuple:
        """
        Makes a path from the source component to the destination component.
        Follows the following general pattern, both for src and dst behavior, which are then connected by a line:
            - If not in extra components section:
                - If in same window, just follow rectangular path from one component to other.
                - If center is in left 6th of window route arrow directly out left.
                - Otherwise, if center is in top half of window, route out top of window, then parallel to window
                until on left side of scene.
                - Otherwise, out bottom of window, then parallel to window until on left of scene.
            - If in extra components section:
                - If hidden on the left, then the arrow is routed past a certain point, after which it turns to go
                into EC section, then turns again going until the top-level window's end, seeming like it goes under.
                - If hidden on right, same situation, mirrored.
                - If in the middle, arrow follows parallel to left side of component, with a buffer

        Note: When using points, the first index is what point on the component: top:0, left:1, right:2, bottom:3
            and the second index is the coordinate: x:0, y:1.

        :return: the path, arrival coordinates, direction of arrival, and path boundingrect
        :rtype: (QPainterPath, tuple(int, int), int, rect)
        """

        # --- INITIALIZATION --- #
        # Instantiate path
        path = QPainterPath()

        # Get the components
        srcComp = self._srcComp
        dstComp = self._dstComp

        # Get the components' containing windows, their positional attributes as [x, y, width, height] list,
        # and the EC Section width
        srcWin = srcComp.getWindowGraphics()
        dstWin = dstComp.getWindowGraphics()
        srcWinRect = [srcWin.scenePos().x(), srcWin.scenePos().y(), srcWin.width(), srcWin.height()]
        dstWinRect = [dstWin.scenePos().x(), dstWin.scenePos().y(), dstWin.width(), dstWin.height()]
        if srcWin.getScrollableItem():
            srcECSWidth = srcWin.getScrollableItem().rect().width()
        else:
            srcECSWidth = 0
        if dstWin.getScrollableItem():
            dstECSWidth = dstWin.getScrollableItem().rect().width()
        else:
            dstECSWidth = 0

        # Find points to stem from/arrive to as [top, left, right, bottom] list of x,y coordinate tuples
        srcPoints = [(srcComp.scenePos().x() + srcComp.width() / 2, srcComp.scenePos().y()),
                     (srcComp.scenePos().x(), srcComp.scenePos().y() + srcComp.height() / 2),
                     (srcComp.scenePos().x() + srcComp.width(), srcComp.scenePos().y() + srcComp.height() / 2),
                     (srcComp.scenePos().x() + srcComp.width() / 2, srcComp.scenePos().y() + srcComp.height())]
        dstPoints = [(dstComp.scenePos().x() + dstComp.width() / 2, dstComp.scenePos().y()),
                     (dstComp.scenePos().x(), dstComp.scenePos().y() + dstComp.height() / 2),
                     (dstComp.scenePos().x() + dstComp.width(), dstComp.scenePos().y() + dstComp.height() / 2),
                     (dstComp.scenePos().x() + dstComp.width() / 2, dstComp.scenePos().y() + dstComp.height())]

        # Get both of their center points
        # NOTE: If src/dstPoints is changed, this needs to be changed
        srcCompCenter = (srcPoints[0][0], srcPoints[1][1])
        dstCompCenter = (dstPoints[0][0], dstPoints[1][1])
        # ---------------------- #

        # Catch if in EC Section, along with the Extra Comp itself
        srcInECSection, srcEC = srcComp.isInECSection()
        dstInECSection, dstEC = dstComp.isInECSection()

        # --- Calculate Distances --- #
        numWin = round(abs(srcWinRect[1] - dstWinRect[1]) / 700 - 1)  # Number of windows between the two windows

        srcDistProp = (srcCompCenter[0] - srcWinRect[0]) / srcWinRect[2]  # distance from left of window as prop
        dstDistProp = (dstCompCenter[0] - dstWinRect[0]) / dstWinRect[2]

        vDistSrc = 10 + max(0, srcDistProp * 20)  # Distance from top or bottom edges to make a turn to go to the left
        vDistDst = 10 + max(0, dstDistProp * 20)  # Distance from top or bottom edges to make a turn to go to the left

        echDist = 20  # The x distance to pass before turning to go into EC Section
        ecvDist = 50  # The height the VB goes to before going to hidden component

        # sign = lambda a: (a > 0) - (a < 0)  # gets the sign of a number
        srcPadding = 20
        dstPadding = 20
        if srcInECSection:  # The x distance from the side of an extra component to turn towards/away from it
            prop = (srcPoints[2][1] - srcEC.scenePos().y()) / srcEC.height()
            srcPadding = 10 + 20 * prop  # min 10, max 30
            vDistSrc *= (1 + prop / 4)
            vDistSrc = min(vDistSrc, 49)
        if dstInECSection:  # The x distance from the side of an extra component to turn towards/away from it
            prop = (dstPoints[2][1] - dstEC.scenePos().y()) / dstEC.height()
            dstPadding = 10 + 20 * prop  # min 10, max 30
            vDistDst *= (1 + prop / 4)
            vDistDst = min(vDistDst, 49)

        # Distance from left of window (its x pos) to make a right-angle turn
        if dstWinRect[1] != srcWinRect[1]:  # Dst is below src
            hDist = min(numWin * 15 + (srcDistProp + dstDistProp) * 10 + VBGraphics.MIN_LEFT_DIST,
                        VBGraphics.MAX_LEFT_DIST)
        else:  # Same window
            hDist = VBGraphics.MIN_LEFT_DIST  # Still assigned, but used in a different way

        # --------------------------- #

        # --- IN SAME WINDOW --- #
        if srcWin is dstWin:
            if not (srcInECSection or dstInECSection):  # same window
                # Destination is on left
                if dstCompCenter[0] + hDist <= srcPoints[1][0] and dstPoints[2][0] < srcPoints[1][0] - hDist:
                    xDist = srcPoints[1][0] - dstPoints[2][0]
                    path.moveTo(srcPoints[1][0], srcPoints[1][1])
                    path.lineTo(srcPoints[1][0] - xDist / 2, srcPoints[1][1])
                    path.lineTo(srcPoints[1][0] - xDist / 2, dstPoints[2][1])
                    path.lineTo(dstPoints[2][0], dstPoints[2][1])
                    arrival = (dstPoints[2][0], dstPoints[2][1])
                    direction = 2

                # Destination is generally to the left but closer than last condition
                elif dstCompCenter[0] + hDist <= srcCompCenter[0]:
                    path.moveTo(srcPoints[1][0], srcPoints[1][1])
                    if dstCompCenter[1] < srcCompCenter[1]:  # Dst above Src
                        if dstPoints[2][0] >= srcPoints[1][0] - hDist:
                            path.lineTo(dstPoints[3][0], srcPoints[1][1])
                            path.lineTo(dstPoints[3][0], dstPoints[3][1])
                        else:
                            path.lineTo(srcPoints[1][0] - hDist / 2, srcPoints[1][1])
                            path.lineTo(srcPoints[1][0] - hDist / 2, dstPoints[3][1] + hDist)
                            path.lineTo(dstPoints[3][0], dstPoints[3][1] + hDist)
                            path.lineTo(dstPoints[3][0], dstPoints[3][1])
                        arrival = (dstPoints[3][0], dstPoints[3][1])
                        direction = 3
                    else:
                        if dstPoints[2][0] >= srcPoints[1][0] - hDist:
                            path.lineTo(dstPoints[0][0], srcPoints[1][1])
                            path.lineTo(dstPoints[0][0], dstPoints[0][1])
                        else:
                            path.lineTo(srcPoints[1][0] - hDist / 2, srcPoints[1][1])
                            path.lineTo(srcPoints[1][0] - hDist / 2, dstPoints[0][1] - hDist)
                            path.lineTo(dstPoints[0][0], dstPoints[0][1] - hDist)
                            path.lineTo(dstPoints[0][0], dstPoints[0][1])
                        arrival = (dstPoints[0][0], dstPoints[0][1])
                        direction = 0

                # Destination is pretty much vertically aligned
                elif dstCompCenter[0] + hDist > srcCompCenter[0] > dstCompCenter[0] - hDist:
                    if dstCompCenter[1] < srcCompCenter[1]:  # Dst above Src
                        yDist = srcPoints[0][1] - dstPoints[3][1]
                        path.moveTo(srcPoints[0][0], srcPoints[0][1])
                        path.lineTo(srcPoints[0][0], srcPoints[0][1] - yDist / 2)
                        path.lineTo(dstPoints[3][0], srcPoints[0][1] - yDist / 2)
                        path.lineTo(dstPoints[3][0], dstPoints[3][1])
                        arrival = (dstPoints[3][0], dstPoints[3][1])
                        direction = 3
                    else:
                        yDist = dstPoints[0][1] - srcPoints[3][1]
                        path.moveTo(srcPoints[3][0], srcPoints[3][1])
                        path.lineTo(srcPoints[3][0], srcPoints[3][1] + yDist / 2)
                        path.lineTo(dstPoints[0][0], srcPoints[3][1] + yDist / 2)
                        path.lineTo(dstPoints[0][0], dstPoints[0][1])
                        arrival = (dstPoints[0][0], dstPoints[0][1])
                        direction = 0

                # Destination is generally to the right but closer than next condition
                elif srcCompCenter[0] <= dstCompCenter[0] - hDist <= srcPoints[2][0] or \
                        dstPoints[1][0] < srcPoints[2][0] + hDist:
                    path.moveTo(srcPoints[2][0], srcPoints[2][1])
                    if dstCompCenter[1] < srcCompCenter[1]:  # Dst above Src
                        if dstPoints[1][0] < srcPoints[2][0] + hDist:
                            path.lineTo(dstPoints[3][0], srcPoints[2][1])
                            path.lineTo(dstPoints[3][0], dstPoints[3][1])
                        else:
                            path.lineTo(srcPoints[2][0] + hDist / 2, srcPoints[2][1])
                            path.lineTo(srcPoints[2][0] + hDist / 2, dstPoints[3][1] + hDist)
                            path.lineTo(dstPoints[3][0], dstPoints[3][1] + hDist)
                            path.lineTo(dstPoints[3][0], dstPoints[3][1])
                        arrival = (dstPoints[3][0], dstPoints[3][1])
                        direction = 3
                    else:
                        if dstPoints[1][0] < srcPoints[2][0] + hDist:
                            path.lineTo(dstPoints[0][0], srcPoints[2][1])
                            path.lineTo(dstPoints[0][0], dstPoints[0][1])
                        else:
                            path.lineTo(srcPoints[2][0] + hDist / 2, srcPoints[2][1])
                            path.lineTo(srcPoints[2][0] + hDist / 2, dstPoints[0][1] - hDist)
                            path.lineTo(dstPoints[0][0], dstPoints[0][1] - hDist)
                            path.lineTo(dstPoints[0][0], dstPoints[0][1])
                        arrival = (dstPoints[0][0], dstPoints[0][1])
                        direction = 0

                # Destination is on right
                else:
                    xDist = dstPoints[1][0] - srcPoints[2][0]
                    path.moveTo(srcPoints[2][0], srcPoints[2][1])
                    path.lineTo(srcPoints[2][0] + xDist / 2, srcPoints[2][1])
                    path.lineTo(srcPoints[2][0] + xDist / 2, dstPoints[1][1])
                    path.lineTo(dstPoints[1][0], dstPoints[1][1])
                    arrival = (dstPoints[1][0], dstPoints[1][1])
                    direction = 1

            elif srcInECSection and not dstInECSection:
                vDist = max(vDistDst, vDistSrc)
                ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                leftPausePoint = srcWinRect[0] + srcWinRect[2] + ecEnterDist + 30 - srcPadding  # 30 is max pad
                compHiddenOnLeft = srcPoints[1][0] - srcPadding < leftPausePoint
                compHiddenOnRight = srcPoints[1][0] - srcPadding > srcWinRect[0] + srcWinRect[2] + \
                                    srcECSWidth - ecEnterDist

                self._compIsHidden = compHiddenOnLeft or compHiddenOnRight

                if compHiddenOnLeft:
                    if srcPoints[2][0] + srcPadding >= srcWinRect[0] + srcWinRect[2]:
                        # For smoother animation. Not hidden yet
                        bottom = srcPoints[3]
                        right = srcPoints[2]
                        left = srcPoints[1]

                        if left[0] > leftPausePoint:
                            path.moveTo(left[0], left[1])
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] > leftPausePoint:
                            path.moveTo(leftPausePoint, bottom[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] + srcPadding > leftPausePoint:
                            path.moveTo(right[0], right[1])
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] + srcPadding > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] + vDist)

                        else:
                            path.moveTo(srcWinRect[0] + srcWinRect[2], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] + vDist)

                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2],
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                    srcWinRect[1] + srcWinRect[3] + vDist)
                elif compHiddenOnRight:
                    if srcPoints[1][0] < srcWinRect[0] + srcWinRect[2] + srcECSWidth:  # Not hidden yet but close
                        left = srcPoints[1]
                        path.moveTo(left[0], left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    elif srcPoints[1][0] - srcPadding < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                        left = srcPoints[1]
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth,
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + srcWinRect[3] + vDist)
                else:
                    left = srcPoints[1]
                    path.moveTo(left[0], left[1])
                    path.lineTo(left[0] - srcPadding, left[1])
                    path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] + vDist)

                path.lineTo(dstPoints[3][0], srcWinRect[1] + srcWinRect[3] + vDist)
                path.lineTo(dstPoints[3][0], dstPoints[3][1])
                arrival, direction = (dstPoints[3][0], dstPoints[3][1]), 3

            elif dstInECSection and not srcInECSection:
                vDist = max(vDistDst, vDistSrc)
                path.moveTo(srcPoints[3][0], srcPoints[3][1])
                path.lineTo(srcPoints[3][0], srcWinRect[1] + srcWinRect[3] + vDist)

                ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                leftPausePoint = dstWinRect[0] + dstWinRect[2] + ecEnterDist + 30 - dstPadding  # 30 is max pad
                compHiddenOnLeft = dstPoints[1][0] - dstPadding < leftPausePoint
                compHiddenOnRight = dstPoints[1][0] - dstPadding > dstWinRect[0] + dstWinRect[2] + \
                                    dstECSWidth - ecEnterDist

                if compHiddenOnLeft:
                    if dstPoints[2][0] + dstPadding > dstWinRect[0] + dstWinRect[2]:
                        # For smoother animation. Not hidden yet
                        bottom = dstPoints[3]
                        right = dstPoints[2]
                        left = dstPoints[1]

                        if left[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(left[0], left[1])
                            arrival = (left[0], left[1])
                            direction = 1

                        elif right[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(leftPausePoint, bottom[1])
                            arrival = (leftPausePoint, bottom[1])
                            direction = 3

                        elif right[0] + dstPadding > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] + dstPadding > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        else:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(dstWinRect[0] + dstWinRect[2], right[1])
                            arrival = (dstWinRect[0] + dstWinRect[2], right[1])
                            direction = 2

                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + dstWinRect[3] + vDist)
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(dstWinRect[0] + dstWinRect[2],
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2], dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        direction = 2

                elif compHiddenOnRight:
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + dstWinRect[3] + vDist)
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                    if dstPoints[1][0] < dstWinRect[0] + dstWinRect[2] + dstECSWidth:  # Not hidden yet but close
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(left[0], left[1])
                        arrival = (left[0], left[1])
                        direction = 1
                    elif dstPoints[1][0] - dstPadding < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        direction = 1
                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                   dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        direction = 1
                else:
                    left = dstPoints[1]
                    path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] + vDist)
                    path.lineTo(left[0] - dstPadding, left[1])
                    path.lineTo(left[0], left[1])
                    arrival = (left[0], left[1])
                    direction = 1

            else:  # both in EC Section
                vDist = max(vDistDst, vDistSrc)

                ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                leftPausePoint = srcWinRect[0] + srcWinRect[2] + ecEnterDist + 30 - srcPadding  # 30 is max pad
                compHiddenOnLeft = srcPoints[1][0] - srcPadding < leftPausePoint
                compHiddenOnRight = srcPoints[1][0] - srcPadding > srcWinRect[0] + srcWinRect[2] + \
                                    srcECSWidth - ecEnterDist

                if compHiddenOnLeft:
                    if srcPoints[2][0] + srcPadding > srcWinRect[0] + srcWinRect[2]:
                        # For smoother animation. Not hidden yet
                        bottom = srcPoints[3]
                        right = srcPoints[2]
                        left = srcPoints[1]

                        if left[0] > leftPausePoint:
                            path.moveTo(left[0], left[1])
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] > leftPausePoint:
                            path.moveTo(leftPausePoint, bottom[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] + srcPadding > leftPausePoint:
                            path.moveTo(right[0], right[1])
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] + srcPadding > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] + vDist)

                        elif right[0] > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] + vDist)

                        else:
                            path.moveTo(srcWinRect[0] + srcWinRect[2], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] + vDist)

                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2],
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                    srcWinRect[1] + srcWinRect[3] + vDist)
                elif compHiddenOnRight:
                    if srcPoints[1][0] < srcWinRect[0] + srcWinRect[2] + srcECSWidth:  # Not hidden yet but close
                        left = srcPoints[1]
                        path.moveTo(left[0], left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    elif srcPoints[1][0] - srcPadding < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                        left = srcPoints[1]
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth,
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + srcWinRect[3] + vDist)
                else:
                    left = srcPoints[1]
                    path.moveTo(left[0], left[1])
                    path.lineTo(left[0] - srcPadding, left[1])
                    path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] + vDist)

                # Destination
                ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                leftPausePoint = dstWinRect[0] + dstWinRect[2] + ecEnterDist + 30 - dstPadding  # 30 is max pad
                compHiddenOnLeft = dstPoints[1][0] - dstPadding < leftPausePoint
                compHiddenOnRight = dstPoints[1][0] - dstPadding > dstWinRect[0] + dstWinRect[2] + \
                                    dstECSWidth - ecEnterDist

                if compHiddenOnLeft:
                    if dstPoints[2][0] + dstPadding > dstWinRect[0] + dstWinRect[2]:
                        # For smoother animation. Not hidden yet
                        bottom = dstPoints[3]
                        right = dstPoints[2]
                        left = dstPoints[1]

                        if left[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(left[0], left[1])
                            arrival = (left[0], left[1])
                            direction = 1

                        elif right[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(leftPausePoint, bottom[1])
                            arrival = (leftPausePoint, bottom[1])
                            direction = 3

                        elif right[0] + dstPadding > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] + dstPadding > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        else:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDist)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(dstWinRect[0] + dstWinRect[2], right[1])
                            arrival = (dstWinRect[0] + dstWinRect[2], right[1])
                            direction = 2

                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + dstWinRect[3] + vDist)
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(dstWinRect[0] + dstWinRect[2],
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2], dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        direction = 2

                elif compHiddenOnRight:
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + dstWinRect[3] + vDist)
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                    if dstPoints[1][0] < dstWinRect[0] + dstWinRect[2] + dstECSWidth:  # Not hidden yet but close
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(left[0], left[1])
                        arrival = (left[0], left[1])
                        direction = 1
                    elif dstPoints[1][0] - dstPadding < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        direction = 1
                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                   dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        direction = 1
                else:
                    left = dstPoints[1]
                    path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] + vDist)
                    path.lineTo(left[0] - dstPadding, left[1])
                    path.lineTo(left[0], left[1])
                    arrival = (left[0], left[1])
                    direction = 1

            boundingRect = path.boundingRect()
            return path, arrival, direction, boundingRect
        # ---------------------- #

        # --- NEIGHBORING WINDOWS --- #
        # We only have special cases when the components are on the inside halves of the neighboring windows
        # or if they are extra components
        elif numWin is 0:
            if dstPoints[0][1] > srcPoints[0][1]:  # Dst is below src
                if ((srcInECSection or srcCompCenter[1] > srcWinRect[1] + srcWinRect[3] / 2)
                        and (dstInECSection or dstCompCenter[1] < dstWinRect[1] + dstWinRect[3] / 2)):

                    if srcInECSection:
                        ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                        ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                        leftPausePoint = srcWinRect[0] + srcWinRect[2] + ecEnterDist + 30 - srcPadding  # 30 is max pad
                        compHiddenOnLeft = srcPoints[1][0] - srcPadding < leftPausePoint
                        compHiddenOnRight = srcPoints[1][0] - srcPadding > srcWinRect[0] + srcWinRect[2] + \
                                            srcECSWidth - ecEnterDist

                        if compHiddenOnLeft:
                            if srcPoints[2][0] + srcPadding > srcWinRect[0] + srcWinRect[2]:
                                bottom = srcPoints[3]
                                right = srcPoints[2]
                                left = srcPoints[1]

                                if left[0] > leftPausePoint:
                                    path.moveTo(left[0], left[1])
                                    path.lineTo(leftPausePoint, left[1])
                                    path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)

                                elif right[0] > leftPausePoint:
                                    path.moveTo(leftPausePoint, bottom[1])
                                    path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)

                                elif right[0] + srcPadding > leftPausePoint:
                                    path.moveTo(right[0], right[1])
                                    path.lineTo(leftPausePoint, right[1])
                                    path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)

                                elif right[0] + srcPadding > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                                    path.moveTo(right[0], right[1])
                                    path.lineTo(right[0] + srcPadding, right[1])
                                    path.lineTo(right[0] + srcPadding, dstWinRect[1] - vDistDst)

                                elif right[0] > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                                    path.moveTo(right[0], right[1])
                                    path.lineTo(right[0] + srcPadding, right[1])
                                    path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                dstWinRect[1] - vDistDst)

                                else:
                                    path.moveTo(srcWinRect[0] + srcWinRect[2], right[1])
                                    path.lineTo(right[0] + srcPadding, right[1])
                                    path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                dstWinRect[1] - vDistDst)
                            else:
                                path.moveTo(srcWinRect[0] + srcWinRect[2],
                                            srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                            srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                            dstWinRect[1] - vDistDst)
                        elif compHiddenOnRight:
                            if srcPoints[1][0] < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                                # Not hidden yet but close
                                left = srcPoints[1]
                                path.moveTo(left[0], left[1])
                                path.lineTo(left[0] - srcPadding, left[1])
                                path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            elif srcPoints[1][0] - srcPadding < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                                left = srcPoints[1]
                                path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, left[1])
                                path.lineTo(left[0] - srcPadding, left[1])
                                path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            else:
                                path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth,
                                            srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                        dstWinRect[1] - vDistDst)
                        else:
                            left = srcPoints[1]
                            path.moveTo(left[0], left[1])
                            path.lineTo(left[0] - srcPadding, left[1])
                            path.lineTo(left[0] - srcPadding, dstWinRect[1] - vDistDst)

                    else:  # Src Comp in bottom half of its win
                        path.moveTo(srcPoints[3][0], srcPoints[3][1])
                        path.lineTo(srcPoints[3][0], dstWinRect[1] - vDistDst)

                    # Destination
                    if dstInECSection:
                        ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                        ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                        leftPausePoint = dstWinRect[0] + dstWinRect[2] + ecEnterDist + 30 - dstPadding  # 30 is max pad
                        compHiddenOnLeft = dstPoints[1][0] - dstPadding < leftPausePoint
                        compHiddenOnRight = dstPoints[1][0] - dstPadding > dstWinRect[0] + dstWinRect[2] + \
                                            dstECSWidth - ecEnterDist

                        if compHiddenOnLeft:
                            if dstPoints[2][0] + dstPadding > dstWinRect[0] + dstWinRect[2]:
                                # For smoother animation. Not hidden yet
                                top = dstPoints[0]
                                right = dstPoints[2]
                                left = dstPoints[1]

                                if left[0] > leftPausePoint:
                                    path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)
                                    path.lineTo(leftPausePoint, left[1])
                                    path.lineTo(left[0], left[1])
                                    arrival = (left[0], left[1])
                                    direction = 1

                                elif right[0] > leftPausePoint:
                                    path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)
                                    path.lineTo(leftPausePoint, top[1])
                                    arrival = (leftPausePoint, top[1])
                                    direction = 0

                                elif right[0] + dstPadding > leftPausePoint:
                                    path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)
                                    path.lineTo(leftPausePoint, right[1])
                                    path.lineTo(right[0], right[1])
                                    arrival = (right[0], right[1])
                                    direction = 2

                                elif right[0] + dstPadding > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                                    path.lineTo(right[0] + dstPadding, dstWinRect[1] - vDistDst)
                                    path.lineTo(right[0] + dstPadding, right[1])
                                    path.lineTo(right[0], right[1])
                                    arrival = (right[0], right[1])
                                    direction = 2

                                elif right[0] > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] - vDistDst)
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, dstWinRect[1] + ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, right[1])
                                    path.lineTo(right[0], right[1])
                                    arrival = (right[0], right[1])
                                    direction = 2

                                else:
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] - vDistDst)
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, dstWinRect[1] + ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, right[1])
                                    path.lineTo(dstWinRect[0] + dstWinRect[2], right[1])
                                    arrival = (dstWinRect[0] + dstWinRect[2], right[1])
                                    direction = 2

                            else:
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                            dstWinRect[1] - vDistDst)
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                            dstWinRect[1] + ecHiddenHeight)
                                path.lineTo(dstWinRect[0] + dstWinRect[2],
                                            dstWinRect[1] + ecHiddenHeight)
                                arrival = (dstWinRect[0] + dstWinRect[2],
                                           dstWinRect[1] + ecHiddenHeight)
                                direction = 2

                        elif compHiddenOnRight:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                        dstWinRect[1] - vDistDst)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                        dstWinRect[1] + ecHiddenHeight)
                            if dstPoints[1][0] < dstWinRect[0] + dstWinRect[
                                2] + dstECSWidth:  # Not hidden yet but close
                                left = dstPoints[1]
                                path.lineTo(left[0] - dstPadding, dstWinRect[1] + ecHiddenHeight)
                                path.lineTo(left[0] - dstPadding, left[1])
                                path.lineTo(left[0], left[1])
                                arrival = (left[0], left[1])
                                direction = 1
                            elif dstPoints[1][0] - dstPadding < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                                left = dstPoints[1]
                                path.lineTo(left[0] - dstPadding, dstWinRect[1] + ecHiddenHeight)
                                path.lineTo(left[0] - dstPadding, left[1])
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                                arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                                direction = 1
                            else:
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                            dstWinRect[1] + ecHiddenHeight)
                                arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                           dstWinRect[1] + ecHiddenHeight)
                                direction = 1
                        else:
                            left = dstPoints[1]
                            path.lineTo(left[0] - dstPadding, dstWinRect[1] - vDistDst)
                            path.lineTo(left[0] - dstPadding, left[1])
                            path.lineTo(left[0], left[1])
                            arrival = (left[0], left[1])
                            direction = 1

                    else:  # Dst Comp in top half of its win
                        path.lineTo(dstPoints[0][0], dstWinRect[1] - vDistDst)
                        path.lineTo(dstPoints[0][0], dstPoints[0][1])
                        arrival = (dstPoints[0][0], dstPoints[0][1])
                        direction = 0

                    boundingRect = path.boundingRect()
                    return path, arrival, direction, boundingRect

            # Dst above src
            else:
                if ((srcInECSection or srcCompCenter[1] <= srcWinRect[1] + srcWinRect[3] / 2)
                        and (dstInECSection or dstCompCenter[1] >= dstWinRect[1] + dstWinRect[3] / 2)):

                    if srcInECSection:
                        ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                        ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                        leftPausePoint = srcWinRect[0] + srcWinRect[2] + ecEnterDist + 30 - srcPadding  # 30 is max pad
                        compHiddenOnLeft = srcPoints[1][0] - srcPadding < leftPausePoint
                        compHiddenOnRight = srcPoints[1][0] - srcPadding > srcWinRect[0] + srcWinRect[2] + \
                                            srcECSWidth - ecEnterDist

                        if compHiddenOnLeft:
                            if srcPoints[2][0] + srcPadding >= srcWinRect[0] + srcWinRect[2]:
                                bottom = srcPoints[3]
                                right = srcPoints[2]
                                left = srcPoints[1]

                                if left[0] > leftPausePoint:
                                    path.moveTo(left[0], left[1])
                                    path.lineTo(leftPausePoint, left[1])
                                    path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)

                                elif right[0] > leftPausePoint:
                                    path.moveTo(leftPausePoint, bottom[1])
                                    path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)

                                elif right[0] + srcPadding > leftPausePoint:
                                    path.moveTo(right[0], right[1])
                                    path.lineTo(leftPausePoint, right[1])
                                    path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)

                                elif right[0] + srcPadding > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                                    path.moveTo(right[0], right[1])
                                    path.lineTo(right[0] + srcPadding, right[1])
                                    path.lineTo(right[0] + srcPadding, dstWinRect[1] + dstWinRect[3] + vDistDst)

                                elif right[0] > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                                    path.moveTo(right[0], right[1])
                                    path.lineTo(right[0] + srcPadding, right[1])
                                    path.lineTo(right[0] + srcPadding, srcWinRect[1] + ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                srcWinRect[1] + ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + dstWinRect[3] + vDistDst)

                                else:
                                    path.moveTo(srcWinRect[0] + srcWinRect[2], right[1])
                                    path.lineTo(right[0] + srcPadding, right[1])
                                    path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                srcWinRect[1] + ecHiddenHeight)
                                    path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + dstWinRect[3] + vDistDst)

                            else:
                                path.moveTo(srcWinRect[0] + srcWinRect[2], srcWinRect[1] + ecHiddenHeight)
                                path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist, srcWinRect[1] + ecHiddenHeight)
                                path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                            dstWinRect[1] + dstWinRect[3] + vDistDst)
                        elif compHiddenOnRight:
                            if srcPoints[1][0] < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                                # Not hidden yet but close
                                left = srcPoints[1]
                                path.moveTo(left[0], left[1])
                                path.lineTo(left[0] - srcPadding, left[1])
                                path.lineTo(left[0] - srcPadding, srcWinRect[1] + ecHiddenHeight)
                            elif srcPoints[1][0] - srcPadding < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                                left = srcPoints[1]
                                path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, left[1])
                                path.lineTo(left[0] - srcPadding, left[1])
                                path.lineTo(left[0] - srcPadding, srcWinRect[1] + ecHiddenHeight)
                            else:
                                path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, srcWinRect[1] + ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                        srcWinRect[1] + ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDistDst)
                        else:
                            left = srcPoints[1]
                            path.moveTo(left[0], left[1])
                            path.lineTo(left[0] - srcPadding, left[1])
                            path.lineTo(left[0] - srcPadding, dstWinRect[1] + dstWinRect[3] + vDistDst)

                    else:  # Src Comp in top half of its win
                        path.moveTo(srcPoints[0][0], srcPoints[0][1])
                        path.lineTo(srcPoints[0][0], dstWinRect[1] + dstWinRect[3] + vDistDst)

                    # Destination
                    if dstInECSection:
                        ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
                        ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
                        leftPausePoint = dstWinRect[0] + dstWinRect[2] + ecEnterDist + 30 - dstPadding  # 30 is max pad
                        compHiddenOnLeft = dstPoints[1][0] - dstPadding < leftPausePoint
                        compHiddenOnRight = dstPoints[1][0] - dstPadding > dstWinRect[0] + dstWinRect[2] + \
                                            dstECSWidth - ecEnterDist

                        if compHiddenOnLeft:
                            if dstPoints[2][0] + dstPadding > dstWinRect[0] + dstWinRect[2]:
                                # For smoother animation. Not hidden yet
                                bottom = dstPoints[3]
                                right = dstPoints[2]
                                left = dstPoints[1]

                                if left[0] > leftPausePoint:
                                    path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)
                                    path.lineTo(leftPausePoint, left[1])
                                    path.lineTo(left[0], left[1])
                                    arrival = (left[0], left[1])
                                    direction = 1

                                elif right[0] > leftPausePoint:
                                    path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)
                                    path.lineTo(leftPausePoint, bottom[1])
                                    arrival = (leftPausePoint, bottom[1])
                                    direction = 3

                                elif right[0] + dstPadding > leftPausePoint:
                                    path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)
                                    path.lineTo(leftPausePoint, right[1])
                                    path.lineTo(right[0], right[1])
                                    arrival = (right[0], right[1])
                                    direction = 2

                                elif right[0] + dstPadding > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                                    path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] + vDistDst)
                                    path.lineTo(right[0] + dstPadding, right[1])
                                    path.lineTo(right[0], right[1])
                                    arrival = (right[0], right[1])
                                    direction = 2

                                elif right[0] > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + dstWinRect[3] + vDistDst)
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, right[1])
                                    path.lineTo(right[0], right[1])
                                    arrival = (right[0], right[1])
                                    direction = 2

                                else:
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + dstWinRect[3] + vDistDst)
                                    path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                                dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                    path.lineTo(right[0] + dstPadding, right[1])
                                    path.lineTo(dstWinRect[0] + dstWinRect[2], right[1])
                                    arrival = (dstWinRect[0] + dstWinRect[2], right[1])
                                    direction = 2

                            else:
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                            dstWinRect[1] + dstWinRect[3] + vDistDst)
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                            dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                path.lineTo(dstWinRect[0] + dstWinRect[2],
                                            dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                arrival = (
                                dstWinRect[0] + dstWinRect[2], dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                direction = 2

                        elif compHiddenOnRight:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            if dstPoints[1][0] < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                                # Not hidden yet but close
                                left = dstPoints[1]
                                path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                path.lineTo(left[0] - dstPadding, left[1])
                                path.lineTo(left[0], left[1])
                                arrival = (left[0], left[1])
                                direction = 1
                            elif dstPoints[1][0] - dstPadding < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                                left = dstPoints[1]
                                path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                path.lineTo(left[0] - dstPadding, left[1])
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                                arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                                direction = 1
                            else:
                                path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                            dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                           dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                                direction = 1
                        else:
                            left = dstPoints[1]
                            path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(left[0] - dstPadding, left[1])
                            path.lineTo(left[0], left[1])
                            arrival = (left[0], left[1])
                            direction = 1

                    else:  # Dst Comp in bottom half of its win
                        path.lineTo(dstPoints[3][0], dstWinRect[1] + dstWinRect[3] + vDistDst)
                        path.lineTo(dstPoints[3][0], dstPoints[3][1])
                        arrival = (dstPoints[3][0], dstPoints[3][1])
                        direction = 3

                    boundingRect = path.boundingRect()
                    return path, arrival, direction, boundingRect

        # ------------------------ #

        # --- LEAVING SOURCE --- #
        if not srcInECSection:
            # If in left 6th of containing window, exit through left
            if srcCompCenter[0] <= srcWinRect[0] + srcWinRect[2] / 6:
                left = srcPoints[1]  # x, y coordinate tuple
                path.moveTo(left[0], left[1])
                path.lineTo(srcWinRect[0] - hDist, left[1])

            # Else if in top half of window, exit through top, and go left
            elif srcCompCenter[1] <= srcWinRect[1] + srcWinRect[3] / 2:
                top = srcPoints[0]
                path.moveTo(top[0], top[1])
                path.lineTo(top[0], srcWinRect[1] - vDistSrc)
                path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] - vDistSrc)

            # Else in bottom half of window, exit through bottom, and go left
            elif srcCompCenter[1] > srcWinRect[1] + srcWinRect[3] / 2:
                bottom = srcPoints[3]
                path.moveTo(bottom[0], bottom[1])
                path.lineTo(bottom[0], srcWinRect[1] + srcWinRect[3] + vDistSrc)
                path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] + srcWinRect[3] + vDistSrc)

            else:
                raise Exception("Src: This shouldn't happen.")

        # In Extra Components Section
        else:
            ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
            ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
            leftPausePoint = srcWinRect[0] + srcWinRect[2] + ecEnterDist + 30 - srcPadding  # 30 is max pad
            compHiddenOnLeft = srcPoints[1][0] - srcPadding < leftPausePoint
            compHiddenOnRight = srcPoints[1][0] - srcPadding > srcWinRect[0] + srcWinRect[2] + \
                                srcECSWidth - ecEnterDist

            if dstPoints[0][1] > srcPoints[0][1]:  # If destination is below source
                if compHiddenOnLeft:
                    if srcPoints[2][0] + srcPadding > srcWinRect[0] + srcWinRect[2]:
                        bottom = srcPoints[3]
                        right = srcPoints[2]
                        left = srcPoints[1]

                        if left[0] > leftPausePoint:
                            path.moveTo(left[0], left[1])
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDistSrc)

                        elif right[0] > leftPausePoint:
                            path.moveTo(leftPausePoint, bottom[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDistSrc)

                        elif right[0] + srcPadding > leftPausePoint:
                            path.moveTo(right[0], right[1])
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] + srcWinRect[3] + vDistSrc)

                        elif right[0] + srcPadding > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] + vDistSrc)

                        elif right[0] > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] + vDistSrc)

                        else:
                            path.moveTo(srcWinRect[0] + srcWinRect[2], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] + vDistSrc)
                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2], srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                    srcWinRect[1] + srcWinRect[3] + vDistSrc)

                    path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] + srcWinRect[3] + vDistSrc)

                elif compHiddenOnRight:
                    if srcPoints[1][0] < srcWinRect[0] + srcWinRect[2] + srcECSWidth:  # Not hidden yet but close
                        left = srcPoints[1]
                        path.moveTo(left[0], left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    elif srcPoints[1][0] - srcPadding < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                        left = srcPoints[1]
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth,
                                    srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + srcWinRect[3] + vDistSrc)
                    path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] + srcWinRect[3] + vDistSrc)
                else:
                    left = srcPoints[1]
                    path.moveTo(left[0], left[1])
                    path.lineTo(left[0] - srcPadding, left[1])
                    path.lineTo(left[0] - srcPadding, srcWinRect[1] + srcWinRect[3] + vDistSrc)
                    path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] + srcWinRect[3] + vDistSrc)

            else:  # Destination is above source
                if compHiddenOnLeft:
                    if srcPoints[2][0] + srcPadding > srcWinRect[0] + srcWinRect[2]:
                        bottom = srcPoints[3]
                        right = srcPoints[2]
                        left = srcPoints[1]

                        if left[0] > leftPausePoint:
                            path.moveTo(left[0], left[1])
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] - vDistSrc)

                        elif right[0] > leftPausePoint:
                            path.moveTo(leftPausePoint, bottom[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] - vDistSrc)

                        elif right[0] + srcPadding > leftPausePoint:
                            path.moveTo(right[0], right[1])
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(leftPausePoint, srcWinRect[1] - vDistSrc)

                        elif right[0] + srcPadding > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] - vDistSrc)

                        elif right[0] > srcWinRect[0] + srcWinRect[2] + ecEnterDist:
                            path.moveTo(right[0], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] - vDistSrc)

                        else:
                            path.moveTo(srcWinRect[0] + srcWinRect[2], right[1])
                            path.lineTo(right[0] + srcPadding, right[1])
                            path.lineTo(right[0] + srcPadding, srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        srcWinRect[1] + srcWinRect[3] - ecHiddenHeight)
                            path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist,
                                        dstWinRect[1] - vDistDst)

                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2], srcWinRect[1] + ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist, srcWinRect[1] + ecHiddenHeight)
                        path.lineTo(srcWinRect[0] + srcWinRect[2] + ecEnterDist, srcWinRect[1] - vDistSrc)

                    path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] - vDistSrc)

                elif compHiddenOnRight:
                    if srcPoints[1][0] < srcWinRect[0] + srcWinRect[2] + srcECSWidth:  # Not hidden yet but close
                        left = srcPoints[1]
                        path.moveTo(left[0], left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + ecHiddenHeight)
                    elif srcPoints[1][0] - srcPadding < srcWinRect[0] + srcWinRect[2] + srcECSWidth:
                        left = srcPoints[1]
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, left[1])
                        path.lineTo(left[0] - srcPadding, left[1])
                        path.lineTo(left[0] - srcPadding, srcWinRect[1] + ecHiddenHeight)
                    else:
                        path.moveTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth, srcWinRect[1] + ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] + ecHiddenHeight)
                    path.lineTo(srcWinRect[0] + srcWinRect[2] + srcECSWidth - ecEnterDist,
                                srcWinRect[1] - vDistSrc)
                    path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] - vDistSrc)
                else:
                    left = srcPoints[1]
                    path.moveTo(left[0], left[1])
                    path.lineTo(left[0] - srcPadding, left[1])
                    path.lineTo(left[0] - srcPadding, srcWinRect[1] - vDistSrc)
                    path.lineTo(srcWinRect[0] - hDist, srcWinRect[1] - vDistSrc)
        # ---------------------- #

        # --- TO DESTINATION --- #
        # Basically the same algorithm as leaving src, except all steps are reversed
        if not dstInECSection:
            # If in left 6th of containing window, enter through left
            if dstCompCenter[0] <= dstWinRect[0] + dstWinRect[2] / 6:
                direction = 1
                left = dstPoints[direction]  # x, y coordinate tuple
                path.lineTo(srcWinRect[0] - hDist, left[1])
                path.lineTo(left[0], left[1])
                arrival = (left[0], left[1])

            # Else if in top half of window, enter through top, coming from the left
            elif dstCompCenter[1] <= dstWinRect[1] + dstWinRect[3] / 2:
                direction = 0
                top = dstPoints[direction]
                path.lineTo(srcWinRect[0] - hDist, dstWinRect[1] - vDistDst)
                path.lineTo(top[0], dstWinRect[1] - vDistDst)
                path.lineTo(top[0], top[1])
                arrival = (top[0], top[1])

            # Else in bottom half of window, enter through bottom, coming from the left
            elif dstCompCenter[1] > dstWinRect[1] + dstWinRect[3] / 2:
                direction = 3
                bottom = dstPoints[direction]
                path.lineTo(srcWinRect[0] - hDist, dstWinRect[1] + dstWinRect[3] + vDistDst)
                path.lineTo(bottom[0], dstWinRect[1] + dstWinRect[3] + vDistDst)
                path.lineTo(bottom[0], bottom[1])
                arrival = (bottom[0], bottom[1])

            else:
                raise Exception("Dst: This shouldn't happen.")

        # In Extra Components Section
        else:
            ecEnterDist = echDist  # The x distance to pass before turning to go into EC Section
            ecHiddenHeight = ecvDist  # The height the VB goes to before going to hidden component
            leftPausePoint = dstWinRect[0] + dstWinRect[2] + ecEnterDist + 30 - dstPadding  # 30 is max pad
            compHiddenOnLeft = dstPoints[1][0] - dstPadding < leftPausePoint
            compHiddenOnRight = dstPoints[1][0] - dstPadding > dstWinRect[0] + dstWinRect[2] + \
                                dstECSWidth - ecEnterDist

            if srcPoints[0][1] > dstPoints[0][1]:  # If destination is above source
                if compHiddenOnLeft:
                    if dstPoints[2][0] + dstPadding > dstWinRect[0] + dstWinRect[2]:
                        # For smoother animation. Not hidden yet
                        bottom = dstPoints[3]
                        right = dstPoints[2]
                        left = dstPoints[1]

                        if left[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(left[0], left[1])
                            arrival = (left[0], left[1])
                            direction = 1

                        elif right[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(leftPausePoint, bottom[1])
                            arrival = (leftPausePoint, bottom[1])
                            direction = 3

                        elif right[0] + dstPadding > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] + dstPadding > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        else:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] + vDistDst)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(dstWinRect[0] + dstWinRect[2], right[1])
                            arrival = (dstWinRect[0] + dstWinRect[2], right[1])
                            direction = 2

                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + dstWinRect[3] + vDistDst)
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(dstWinRect[0] + dstWinRect[2],
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        arrival = (
                            dstWinRect[0] + dstWinRect[2], dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        direction = 2

                elif compHiddenOnRight:
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + dstWinRect[3] + vDistDst)
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                    if dstPoints[1][0] < dstWinRect[0] + dstWinRect[
                        2] + dstECSWidth:  # Not hidden yet but close
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(left[0], left[1])
                        arrival = (left[0], left[1])
                        direction = 1
                    elif dstPoints[1][0] - dstPadding < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        direction = 1
                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                    dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                   dstWinRect[1] + dstWinRect[3] - ecHiddenHeight)
                        direction = 1
                else:
                    left = dstPoints[1]
                    path.lineTo(left[0] - dstPadding, dstWinRect[1] + dstWinRect[3] + vDistDst)
                    path.lineTo(left[0] - dstPadding, left[1])
                    path.lineTo(left[0], left[1])
                    arrival = (left[0], left[1])
                    direction = 1

            else:  # Destination is below source
                path.lineTo(srcWinRect[0] - hDist, dstWinRect[1] - vDistDst)
                if compHiddenOnLeft:
                    if dstPoints[2][0] + dstPadding > dstWinRect[0] + dstWinRect[2]:
                        # For smoother animation. Not hidden yet
                        top = dstPoints[0]
                        right = dstPoints[2]
                        left = dstPoints[1]

                        if left[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)
                            path.lineTo(leftPausePoint, left[1])
                            path.lineTo(left[0], left[1])
                            arrival = (left[0], left[1])
                            direction = 1

                        elif right[0] > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)
                            path.lineTo(leftPausePoint, top[1])
                            arrival = (leftPausePoint, top[1])
                            direction = 0

                        elif right[0] + dstPadding > leftPausePoint:
                            path.lineTo(leftPausePoint, dstWinRect[1] - vDistDst)
                            path.lineTo(leftPausePoint, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] + dstPadding > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] - vDistDst)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        elif right[0] > dstWinRect[0] + dstWinRect[2] + ecEnterDist:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] - vDistDst)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(right[0], right[1])
                            arrival = (right[0], right[1])
                            direction = 2

                        else:
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] - vDistDst)
                            path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                        dstWinRect[1] + ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, dstWinRect[1] + ecHiddenHeight)
                            path.lineTo(right[0] + dstPadding, right[1])
                            path.lineTo(dstWinRect[0] + dstWinRect[2], right[1])
                            arrival = (dstWinRect[0] + dstWinRect[2], right[1])
                            direction = 2

                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] - vDistDst)
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + ecEnterDist,
                                    dstWinRect[1] + ecHiddenHeight)
                        path.lineTo(dstWinRect[0] + dstWinRect[2],
                                    dstWinRect[1] + ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2],
                                   dstWinRect[1] + ecHiddenHeight)
                        direction = 2

                elif compHiddenOnRight:
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] - vDistDst)
                    path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth - ecEnterDist,
                                dstWinRect[1] + ecHiddenHeight)
                    if dstPoints[1][0] < dstWinRect[0] + dstWinRect[
                        2] + dstECSWidth:  # Not hidden yet but close
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(left[0], left[1])
                        arrival = (left[0], left[1])
                        direction = 1
                    elif dstPoints[1][0] - dstPadding < dstWinRect[0] + dstWinRect[2] + dstECSWidth:
                        left = dstPoints[1]
                        path.lineTo(left[0] - dstPadding, dstWinRect[1] + ecHiddenHeight)
                        path.lineTo(left[0] - dstPadding, left[1])
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth, left[1])
                        direction = 1
                    else:
                        path.lineTo(dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                    dstWinRect[1] + ecHiddenHeight)
                        arrival = (dstWinRect[0] + dstWinRect[2] + dstECSWidth,
                                   dstWinRect[1] + ecHiddenHeight)
                        direction = 1
                else:
                    left = dstPoints[1]
                    path.lineTo(left[0] - dstPadding, dstWinRect[1] - vDistDst)
                    path.lineTo(left[0] - dstPadding, left[1])
                    path.lineTo(left[0], left[1])
                    arrival = (left[0], left[1])
                    direction = 1

        boundingRect = path.boundingRect()
        return path, arrival, direction, boundingRect

    def getOneComponentDownRoot(self):
        """
        This function is used to locate the base component of the program.

        :return: the component with id = 2; the base component for the program; the component that is one step down of the root component
        :rtype: Component
        """
        possibleRoot = self._dataVB.getSrcComponent()

        while possibleRoot.getParent().getParent() is not None:
            possibleRoot = possibleRoot.getParent()

        return possibleRoot

    def shape(self):
        """
        Stroke the shape of the line.

        :return: the arrow path
        :rtype: QPainterPathStroker
        """
        path, tmp, tmp1, tmp2 = self.buildPath()

        stroker = QPainterPathStroker()
        stroker.setWidth(50)

        return stroker.createStroke(path).simplified()

    def mousePressEvent(self, event: QMouseEvent):
        """
        This event handler is implemented to receive mouse press events for this item.

        :param event: a mouse press event
        :type event: QGraphicsSceneMouseEvent
        :return: None
        :rtype: NoneType
        """
        self._zoomable = False
        self.setSelected(True)
        self.scene().emitItemSelected(self._dataVB.getId())

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        """
        Opens a context menu (right click menu) for the component.

        :param event: The event that was generated when the user right-clicked on this item.
        :type event: QGraphicsSceneContextMenuEvent
        :return: None
        :rtype: NoneType
        """

        self.menu.exec_(event.screenPos())
