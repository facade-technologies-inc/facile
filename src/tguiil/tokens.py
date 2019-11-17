"""

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

This file contains the token class that weighs the importance of each attribute of a single token. 
"""
from enum import Enum, unique

class Token: 
	"""
	Token class sets parameters of a token for each state that changes. 
	"""
	@unique
	class Match(Enum):
		EXACT = 1
		CLOSE = 2
		NO = 3

	class Weight(Enum):
		IDENTIFIER = 10
		ISDIALOG = 1
		ISENABLED = 1
		ISVISIBLE = 1
		PARENTTITLE = 10
		PARENTTYPE = 10
		TOPPARENTTITLE = 1
		TOPPARENTTYPE = 1
		PROCESSID = 10
		TEXTS = 3
		NUMCONTROLS = 3
		PIC = 1
		TITLE = 10
		TYPE = 10
		RECTANGLE = 10
		CONTROLID = 10
		AUTOID = 10
		CHILDRENTEXTS = 1
		EXPANDSTATE = 1
		SHOWNSTATE = 1

	WEIGHT_SUM = sum(list(map(int,Weight)))
	THRESH_PERCENT = 90
	THRESHOLD = (WEIGHT_SUM * THRESH_PERCENT)/100
	PRIMARY_WEIGHT_SUM = 90
	SECONDARY_WEIGHT_SUM = 105

	def __init__(self,identifier: int, isDialog: bool, isEnabled: bool, isVisible: bool, parentTitle: str = None, parentType: str = None, topLevelParentTitle: str = None, topLevelParentType: str = None, processID: int, rectangle: win32structures.RECT, texts: list[str], title: str, numControls: int, picture: PIL.Image = None,typeOf: str, controlID: str, autoID: int = None, childrenTexts: list[str] = None, expandState: int = None, shownState: int = None):
		"""
		Checks if the tokens component state changed based on a random variable.
		
		:param identifier: stores the unique id number of the component
		:type identifier: int
		:param isDialog: stores if the component has dialog contained in it
		:type isDialog: bool
		:param isEnabled: stores if the component is enabled
		:type isEnabled: bool
		:param isVisible: stores if the component is visible
		:type isVisible: bool
		:param parentTitle: stores the components parents title
		:type parentTitle: str
		:param parentType: stores the components parents type
		:type parentType: str
		:param topLevelParentTitle: stores the components top level parents title
		:type topLevelParentTitle: str
		:param topLevelParentType: stores the components top level parents type
		:type topLevelParentType: str
		:param processID: stores the processing id of the component
		:type processID: int
		:param rectangle: stores the position of the component
		:type rectangle: win32structures.RECT
		:param texts: stores the text in the component
		:type texts: list[str]
		:param title: stores the title of the component
		:type title: str
		:param numControls: stores the number of controls of the component
		:type numControls: int
		:param picture: stores the image of the component
		:type picture: PIL.Image
		:param typeOf: stores the characteristics of the component
		:type typeOf: str
		:param controlID: stores the control identifiers. The four possible controls are title, typeOf, title + typeOf, and the closest text
		:type controlID: str
		:param autoID: stores the unique identifier of the component
		:type autoID: str
		:param childrenTexts: stores the text contained in the children of the component
		:type childrenTexts: list[str]
		:param expandState: stores if the components state is expanded
		:type expandState: int
		:param shownState: stores the state in which the component is in
		:type shownState: int
		
		:return: None
		:rtype: NoneType
		"""
		self.identifier = identifier
		self.isDialog = isDialog
		self.isEnabled = isEnabled
		self.isVisible = isVisible
		self.parentTitle = parentTitle
		self.parentType = parentType
		self.topLevelParentTitle = topLevelParentTitle
		self.topLevelParentType = topLevelParentType
		self.processID = processID
		self.rectangle = rectangle
		self.texts = texts
		self.title = title
		self.numControls = numControls
		self.pic = picture
		self.type = typeOf
		self.controlID = controlID
		self.autoid = autoID
		self.childrenTexts = childrenTexts
		self.expandState = expandState
		self.shownState = shownState

	def isEqualTo(self, token2):
		""" 
		The isEqualTo function gives a weight of importance to each attribute.
		This is based on the tokens when its state is changed.

		:param token2: returns how similar of a match the given token is to the current token
		:type token2: int
		:return: None
		:rtype: NoneType
		"""
		#####################################################################
		#	QUICK CHECK FOR EXACT MATCH
		#####################################################################
		# most important: id, autoID, typeOf, title, controlID, rectangle, parentTitle, parentType,processID
		# If all control identifiers and auto IDs match, return Token.Match.EXACT
		
		# make an important weight sum for what is most important
		#####################################################################
		#	MORE IN DEPTH CHECK FOR CLOSE MATCH (WEIGHTING)
		#####################################################################
		total = 0 

		if token2.identifier == self.identifier:
			total += Token.Weight.IDENTIFIER
	
		if token2.isDialog == self.isDialog:
			total += Token.Weight.ISDIALOG

		if token2.isEnabled == self.isEnabled:
			total += Token.Weight.ISENABLED

		if token2.isVisible == self.isVisible:
			total += Token.Weight.ISVISIBLE

		if token2.parentTitle == self.parentTitle:
			total += Token.Weight.PARENTTITLE

		if token2.parentType == self.parentType:
			total += Token.Weight.PARENTTYPE
	
		if token2.processID == self.processID:
			total += Token.Weight.PROCESSID

		if token2.rectangle == self.rectangle:
			total += Token.Weight.RECTANGLE

		if token2.texts == self.texts:
			total += Token.Weight.TEXTS

		if token2.title == self.title:
			total += Token.Weight.TITLE
	
		if token2.numControls == self.numControls:
			total += Token.Weight.NUMCONTROLS

		if token2.picture == self.picture:
			total += Token.Weight.PIC

		if token2.typeOf == self.typeOf:
			total += Token.Weight.RECT

		if token2.controlID == self.controlID:
			total += Token.Weight.CONTROLID

		if token2.autoid == self.autoid:
			total += Token.Weight.AUTOID

		if token2.childrenTexts == self.childrenTexts:
			total += Token.Weight.CHILDRENTEXTS
	
		if token2.expandState == self.expandState:
			total += Token.Weight.EXPANDSTATE

		if token2.shownState == self.shownState:
			total += Token.Weight.SHOWNSTATE

		if total == PRIMARY_WEIGHT_SUM:
			return Token.Match.EXACT

		if total == SECONDARY_WEIGHT_SUM:
			return Token.Match.CLOSE

		else: 
			return Token.Match.NO




	

