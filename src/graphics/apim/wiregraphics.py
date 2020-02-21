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
	def __init__(self, srcPortGraphics: 'portGraphics', dstPortGraphics: 'portGraphics', parent: QGraphicsItem):
		"""

		:param srcPortGraphics:
		:param dstPortGraphics:
		"""
		QGraphicsItem.__init__(self, parent)
		self._srcPortGraphics: 'portGraphics' = srcPortGraphics
		self._dstPortGraphics: 'portGraphics' = dstPortGraphics
		# TODO construct and connect underlying wire.
		self._wire: '' = None