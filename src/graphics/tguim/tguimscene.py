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

This module contains the TGUIMScene class.
"""

from PySide2.QtCore import Signal, QTimer
from PySide2.QtWidgets import QGraphicsScene

from graphics.tguim.componentgraphics import ComponentGraphics
import graphics.tguim.visibilitybehaviorgraphics as vbg

class TGUIMScene(QGraphicsScene):
	itemSelected = Signal(int)
	itemBlink = Signal(int)
	
	def __init__(self, targetGUIModel: 'TargetGuiModel'):
		"""
		Construct the TGUIMScene class

		:param targetGUIModel: get the TargetGuiModel of the project
		:type targetGUIModel: TargetGuiModel
		"""
		QGraphicsScene.__init__(self)
		self._targetGuiModel = targetGUIModel
		self._dataToGraphicsMapping = {}

		# Create all component graphics
		work = [(self._targetGuiModel.getRoot(), ComponentGraphics(self._targetGuiModel.getRoot(), (0,0,0,0), None))]
		while len(work) > 0:
			data, parentGraphics = work.pop()

			# add the root's component to the scene.
			if data is self._targetGuiModel.getRoot():
				self.addItem(parentGraphics)

			for child in data.getChildren():
				graphics = self.createComponentGraphics(child, parentGraphics)
				work.append((child, graphics))

		# Create all visibility behavior graphics
		for vb in targetGUIModel.getVisibilityBehaviors():
			graphics = self.createVisibilityBehaviorGraphics(vb)
			self.addItem(graphics)

		def onNewComponent(newComponent):
			parentGraphics = self.getGraphics(newComponent.getParent())
			self.createComponentGraphics(newComponent, parentGraphics)

		def onNewBehavior(newBehavior):
			self.createVisibilityBehaviorGraphics(newBehavior)

		self._targetGuiModel.newComponent.connect(onNewComponent)
		self._targetGuiModel.newBehavior.connect(onNewBehavior)

	def createComponentGraphics(self, dataItem: 'Component', parent: 'ComponentGraphics') -> 'ComponentGraphics':
		"""
		Create the graphics for a component

		:param dataItem: The component to make a graphics item for
		:type dataItem: Component
		:param parent: The parent to the new graphics item.
		:type parent: ComponentGraphics
		:return: None
		:rtype: NoneType
		"""
		graphics = ComponentGraphics(dataItem, dataItem.getSuperToken().posRelativeToParent, parent)
		self._dataToGraphicsMapping[dataItem] = graphics
		return graphics

	def createVisibilityBehaviorGraphics(self, dataItem: 'VisibilityBehavior') -> 'VisibilityBehaviorGraphics':
		"""
		Create the graphics for a visibility behavior

		:param dataItem: The visibility behavior to create the graphics for.
		:type dataItem: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		graphics = vbg.VBGraphics(dataItem, self)
		self._dataToGraphicsMapping[dataItem] = graphics
		return graphics

	def getGraphics(self, dataItem):
		"""
		Gets the graphics associated with either a component or a visibility behavior.

		.. note:: alternatively, this method can take in the id of a component or visibility behavior.

		:param dataItem: The component or visibility behavior to get the graphics for.
		:type dataItem: Component or VisibilityBehavior
		:return: The graphics associated with dataItem.
		:rtype: ComponentGraphics or VBGraphics
		"""
		if type(dataItem) is int:
			dataItem = self._targetGuiModel.getComponent(dataItem)

		return self._dataToGraphicsMapping.get(dataItem, None)
	
	def getTargetGUIModel(self) -> 'TargetGuiModel':
		"""
		Gets the target GUI Model.

		:return The target GUI model
		:rtype data.tguim.targetguimodel.TargetGuiModel
		"""
		return self._targetGuiModel
	
	def emitItemSelected(self, id: int) -> None:
		"""
		Emits a signal that carries the ID of the item that was selected

		:param id: The ID of the item that was selected.
		:type id: int
		:return: None
		:rtype: NoneType
		"""
		self.itemSelected.emit(id)
	
	def blinkComponent(self, id: int) -> None:
		"""
		emits the itemBlink signal which means that an item should be shown in the
		target GUI.
		
		:param id: The ID of the component that should be blinked.
		:type id: int
		:return: None
		:rtype: NoneType
		"""
		self.itemBlink.emit(id)
