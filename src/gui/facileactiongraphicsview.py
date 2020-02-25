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
	
This module contains the FacileGraphicsView class which is just like a normal graphics
view, but can be zoomed.
"""


from PySide2.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem

import data.statemachine as sm
from gui.facilegraphicsview import FacileGraphicsView
import graphics.apim.actionpipelinegraphics as apg
from graphics.apim.portgraphics import PortGraphics


class FacileActionGraphicsView(FacileGraphicsView):
	"""
	This class adds functionality to the QGraphicsView to zoom in and out.
	
	This is primarily used as the view that shows the target GUI model and API model
	"""
	
	def showAction(self, action: 'Action') -> None:
		newScene = QGraphicsScene()
		
		# Add the action pipeline graphics
		ap = apg.ActionPipelineGraphics(action)
		br = ap.boundingRect()
		newScene.addItem(ap)
		
		# Add the action pipeline name
		nameItem = QGraphicsTextItem(action.getName())
		nameItem.setPos(-br.width()/2, -br.height()/2 - PortGraphics.TOTAL_HEIGHT/2)
		newScene.addItem(nameItem)
		
		self.setScene(newScene)
	

	def refresh(self) -> None:
		"""
		Clears the scene and re-creates it.
		
		:return: None
		:rtype: NoneType
		"""
		cap = sm.StateMachine.instance.getCurrentActionPipeline()
		self.showAction(cap)
