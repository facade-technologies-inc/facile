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

This module contains the ActionGraphics() Class.
"""
import sys

from PySide2.QtWidgets import QGraphicsItem, QApplication, QGraphicsView, QGraphicsScene, \
	QWidget, QStyleOptionGraphicsItem
from PySide2.QtGui import QPainter, QPainterPath
from PySide2.QtCore import QRectF

from data.apim.action import Action

class ActionGraphics(QGraphicsItem):
	"""
	This class defines the graphics for displaying a action in the ActionMenuItem view.
	"""
	
	PEN_WIDTH = 1.0
	#
	SPACE = 10
	def __init__(self, action: 'Action', parent=None) -> 'ActionGraphics':
		"""
		Constructs a Action Graphics object for the given action.
		
		:param action: The action for which this graphics item represents.
		:type action: Action
		:param parent: None
		:type parent: Nonetype
		:return: The graphics of an action.
		:rtype: ActionGraphics
		"""
		QGraphicsItem.__init__(self, parent)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		
		#TODO: What else do I need to add in constructor
	
	def boundingRect(self) -> QRectF:
		"""
		This function defines the outer bounds of the actions icon as a rectangle.
		
		:return: Creates the bounds for the graphics.
		:rtype: QRectF
		"""
		halfPenWidth = ActionGraphics.PEN_WIDTH/2
		#add PortGraphics.WIDTH & HEIGHT
		width = 100 + halfPenWidth
		height = 100 + halfPenWidth
		
		return QRectF(width, height, width, height)
	
	def shape(self) -> QPainterPath:
		"""
		
		:return:
		"""
		return QGraphicsItem.shape(self)
	
	def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, index: QWidget) -> None:
		"""
		Paint a checkbox without the label.

		:param painter: This draws the widget.
		:type painter: QStylePainter
		:param option: Option for the style of checkbox.
		:type option: QStyleOptionViewItem
		:param index: Index for the painted checkbox.
		:type index: QModelIndex
		:return: None
		:rtype: NoneType
		"""
		#painter.drawRect(self.boundingRect())
		painter.drawPath(self.shape())
		
	
if __name__ == "__main__":
	
	app = QApplication()
	v = QGraphicsView()
	s = QGraphicsScene()
	v.setScene(s)
	A = ActionGraphics(Action)
	s.addItem(A)
	v.show()
	sys.exit(app.exec_())