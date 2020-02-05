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

This module contains the portGraphics class, which is responsible for rendering ports in the APIM View.
"""

from PySide2.QtCore import QRectF, QPoint
from PySide2.QtGui import QPainterPath, QPainter, QPolygon
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QApplication, QGraphicsView, QStyleOptionGraphicsItem, QWidget
from data.apim.port import Port

class portGraphics(QGraphicsItem):
    """
    This class defines the graphics for displaying a port in the APIM View.
    """

    PEN_WIDTH = 1.0
    WIDTH = 50
    SIDE_HEIGHT = 2 * WIDTH
    TAPER_HEIGHT = 0.5 * SIDE_HEIGHT
    TOTAL_HEIGHT = SIDE_HEIGHT + TAPER_HEIGHT
    # Center the shape about the origin of its coordinate system.
    LEFT_X_POS = -0.5 * WIDTH
    UPPER_Y_POS = -0.5 * TOTAL_HEIGHT

    def __init__(self, port: 'Port', parent=None):
        """
        Constructs a portGraphics object for the given Port object.
        :param port: The port for which this graphics item represents.
        :type port: Port
        """
        QGraphicsItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        #TODO: What else should be in the constructor ?...

    def boundingRect(self) -> QRectF:
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.
        :return: create the bounding of the item
        :rtype: QRectF
        """
        halfPenWidth = portGraphics.PEN_WIDTH / 2

    def shape(self) -> QPainterPath:
        """

        :return:
        """
        # Create the polygon (pentagon-like shape)
        poly = QPolygon()
        poly << QPoint(portGraphics.LEFT_X_POS, portGraphics.UPPER_Y_POS)  # Upper Left Corner
        poly << QPoint(10, 10)  # Upper Right Corner
        poly << QPoint(10, 10)  # Lower Right Corner
        poly << QPoint(10, 10)  # Bottom Vertex
        poly << QPoint(10, 10)  # Lower Left Corner



        path = QPainterPath()
        path.addPolygon()


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        """

        :param painter:
        :param option:
        :param widget:
        :return:
        """

