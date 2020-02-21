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
"""

from PySide2.QtWidgets import QGraphicsItem

class WireGraphics(QGraphicsItem):
	"""

	"""
	def __init__(self, srcPortGraphics: 'portGraphics', dstPortGraphics: 'portGraphics',
				 actPipelineGFX: "ActionPipelineGraphics" = None):
		"""
		Constructs a WireGraphics object between the given port graphics. Also creates the underlying Wire in the APIM.

		:param srcPortGraphics: The PortGraphics for the source Port the wire is to be connected to.
		:type srcPortGraphics: portGraphics
		:param dstPortGraphics: The PortGraphics for the destination Port the wire is to be connected to.
		:type dstPortGraphics: portGraphics
		:param actPipelineGFX: This is the WireGraphics' parent QGraphicsItem used to instantiate the super class.
		Also used to get a reference to the ActionPipeline for adding newly created wires to the underlying data.
		:type actPipelineGFX: ActionPipelineGraphics
		"""

		QGraphicsItem.__init__(self, actPipelineGFX)
		self._srcPortGraphics: 'portGraphics' = srcPortGraphics
		self._dstPortGraphics: 'portGraphics' = dstPortGraphics

		# Get reference to the actionPipeline and add a wire to it.
		self._wire: 'Wire' = actPipelineGFX.getAction().connect()

		# TODO: render graphics.

