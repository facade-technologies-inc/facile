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


from PySide2.QtWidgets import QGraphicsScene
from gui.facilegraphicsview import FacileGraphicsView
from graphics.apim.actionpipelinegraphics import ActionPipelineGraphics


class FacileActionGraphicsView(FacileGraphicsView):
	"""
	This class adds functionality to the QGraphicsView to zoom in and out.
	
	This is primarily used as the view that shows the target GUI model and API model
	"""
	
	def showAction(self, action: 'Action') -> None:
		newScene = QGraphicsScene()
		newScene.addItem(ActionPipelineGraphics(action))
		self.setScene(newScene)
	

