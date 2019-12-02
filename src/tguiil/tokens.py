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
from difflib import SequenceMatcher
from enum import Enum, unique

import numpy as np
from PIL import Image
from pywinauto.win32structures import RECT
from skimage.metrics import structural_similarity as ssim


class Token:
	"""
	Token class sets parameters of a token for each state that changes.
	"""
	
	class CreationException(Exception):
		def __init__(self, msg):
			Exception.__init__(self, msg)
	
	@unique
	class Match(Enum):
		EXACT = 1
		CLOSE = 2
		NO = 3
	
	Weight = {
		"TITLE": 10,
		"CHILDREN_TEXTS": 10,
		"CONTROL_ID": 10,
		"AUTO_ID": 10,
		"RECTANGLE": 10,
		"NUM_CONTROLS": 3,
		"EXPAND_STATE": 1,
		"SHOWN_STATE": 1,
		"IS_ENABLED": 1,
		"IS_VISIBLE": 1,
		"TEXTS": 3,
		"PIC": 1,
	}
	
	MAX_WEIGHTS = sum(Weight.values())
	THRESH_PERCENT = 50
	
	def __init__(self, appTimeStamp: int, identifier: int, isDialog: bool, isEnabled: bool,
	             isVisible: bool, processID: int, typeOf: str, rectangle: RECT, texts: list,
	             title: str, numControls: int, controlIDs: list, parentTitle: str,
	             parentType: str, topLevelParentTitle: str, topLevelParentType: str,
	             childrenTexts: list, picture: Image = None, autoID: int = None,
	             expandState: int = None, shownState: int = None):
		"""
		Checks if the tokens component state changed based on a random variable.
		
		:param appTimeStamp: The time that the application was started at.
		:type appTimeStamp: int
		:param identifier: stores the unique id number of the component
		:type identifier: int
		:param isDialog: stores if the component is a dialog
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
		:param controlIDs: stores the control identifiers. The four possible controls are title, typeOf, title + typeOf, and the closest text
		:type controlIDs: str
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
		self.appTimeStamp = appTimeStamp
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
		self.controlIDs = controlIDs
		self.autoid = autoID
		self.childrenTexts = childrenTexts
		self.expandState = expandState
		self.shownState = shownState
		
		if self.parentTitle is None:
			self.parentTitle = ""
		if self.topLevelParentTitle is None:
			self.topLevelParentTitle = ""
		if self.texts is None:
			self.texts = []
		if self.childrenTexts is None:
			self.childrenTexts = []
		
		self.childrenTexts.sort()
		self.controlIDs.sort()
	
	def isEqualTo(self, token2: 'Token'):
		"""
		The isEqualTo function gives a weight of importance to each attribute.
		This is based on the tokens when its state is changed.

		:param token2: returns how similar of a match the given token is to the current token
		:type token2: Token
		:return: None
		:rtype: NoneType
		"""
		
		#####################################################################
		# DECISION 1 - QUICK CHECK FOR NO MATCH
		#
		# If the following don't match, the tokens will automatically be
		# considered not matching.
		#   - Friendly Class Name
		#   - Control ID
		#   - Automation ID
		#   - Parent's Friendly Class Name
		#   - Top Level Parent's Friendly Class Name
		#   - Process ID
		#####################################################################
		
		if self.appTimeStamp == token2.appTimeStamp:
			if self.identifier != token2.identifier:
				return Token.Match.NO, 0
			
			elif self.processID != token2.processID:
				return Token.Match.NO, 0
		
		if self.type != token2.type:
			return Token.Match.NO, 0
		
		elif self.autoid != token2.autoid:
			return Token.Match.NO, 0
		
		elif self.parentType != token2.parentType:
			return Token.Match.NO, 0
		
		elif self.topLevelParentType != token2.topLevelParentType:
			return Token.Match.NO, 0
		
		#####################################################################
		# DECISION 2 - QUICK CHECK FOR EXACT MATCH
		#
		# If the following fields match exactly, we can determine that the
		# they are a perfect match.
		#   - Top Level Parent's Title
		#   - Parent's Title
		#   - Title
		#   - Rectangle
		#   - Number of Children
		#   - Text of Children
		#
		# NOTE: If execution reaches this point, all of the fields mentioned
		#       in DECISION 1 must have been the same
		#####################################################################
		elif self.topLevelParentTitle == token2.topLevelParentTitle and \
			self.parentTitle == token2.parentTitle and \
			self.title == token2.title and \
			self.rectangle == token2.rectangle and \
			self.numControls == token2.numControls and \
			self.childrenTexts == self.childrenTexts:
			return Token.Match.EXACT, 1
		
		#####################################################################
		# DECISION 3 - MORE IN DEPTH CHECK FOR CLOSE MATCH (WEIGHTING)
		#
		# If there has been no decision made about the tokens, we perform a
		# probabilistic match. The similarity of each of the following fields
		# are taken into consideration:
		#   - Control IDs
		#   - Picture (If Given)
		#   - Rectangle Dimensions and Position
		#   - Title
		#   - Parent Title
		#   - Top Level Parent Title
		#   - Children Texts
		#   - Enabled State
		#   - Visible State
		#   - Expand State
		#   - Shown State
		#   - rectangle size
		#
		# If the component is a dialog, we heavily much more heavily on these
		# fields:
		#   - Number Of Children
		#   - Children Text
		#   - Rectangle Size
		#####################################################################
		else:
			
			max = Token.MAX_WEIGHTS
			total = 0
			
			# compare control identifiers
			idSequence1 = ''.join(self.controlIDs)
			idSequence2 = ''.join(token2.controlIDs)
			controlSimilarity = SequenceMatcher(None, idSequence1, idSequence2).ratio()
			total += Token.Weight["CONTROL_ID"]
			
			# compare pictures
			if self.pic != None and token2.pic != None:
				if self.pic.size == token2.pic.size:
					try:
						picSimilarity = (ssim(np.array(self.pic), np.array(token2.pic)) + 1) / 2
						total += picSimilarity * Token.Weight["PIC"]
					except:
						total += 0
			else:
				max -= Token.Weight["PIC"]
			
			if self.autoid is not None and token2.autoid is not None and (
				self.autoid != "" or token2.autoid != ""):
				total += SequenceMatcher(None, self.autoid, token2.autoid).ratio() * Token.Weight[
					"AUTO_ID"]
			else:
				max -= Token.Weight["AUTO_ID"]
			
			# compare title, parent title, and top level parent title
			titleSequence1 = ' > '.join([self.title, self.parentTitle, self.topLevelParentTitle])
			titleSequence2 = ' > '.join(
				[token2.title, token2.parentTitle, token2.topLevelParentTitle])
			titleSimilarity = SequenceMatcher(None, titleSequence1, titleSequence2).ratio()
			total += titleSimilarity * Token.Weight["TITLE"]
			
			# compare texts
			texts1 = " ".join(self.texts)
			texts2 = " ".join(token2.texts)
			textsSimilarity = SequenceMatcher(None, texts1, texts2).ratio()
			total += textsSimilarity * Token.Weight["TEXTS"]
			
			# compare children texts
			childTexts1 = " ".join(self.childrenTexts)
			childTexts2 = " ".join(token2.childrenTexts)
			childTextsSimilarity = SequenceMatcher(None, childTexts1, childTexts2).ratio()
			if self.isDialog:
				max += 25
				total += childTextsSimilarity * (Token.Weight["CHILDREN_TEXTS"] + 25)
			else:
				total += childTextsSimilarity * Token.Weight["CHILDREN_TEXTS"]
			
			# compare number of children
			if self.numControls == token2.numControls:
				numChildrenDiff = 1
			elif self.numControls != 0 and token2.numControls != 0:
				numChildrenDiff = min(self.numControls / token2.numControls,
				                      token2.numControls / self.numControls)
			else:
				numChildrenDiff = 0
				# if self.isDialog:
				#     max += 15
				#     total += numChildrenDiff * (Token.Weight["NUM_CONTROLS"] + 15)
				# else:
				total += numChildrenDiff * Token.Weight["NUM_CONTROLS"]
			
			# compare rectangles
			# diffWidth = abs(self.rectangle.width() - token2.rectangle.width())
			# diffHeight = abs(self.rectangle.height() - token2.rectangle.height())
			# widthScore = diffWidth / token2.rectangle.width()
			# heightScore = diffHeight / token2.rectangle.height()
			# shapeScore = widthScore * heightScore
			# if self.isDialog:
			#     max += 5
			#     total += shapeScore * (Token.Weight["RECTANGLE"] + 5)
			# else:
			#     total += shapeScore * Token.Weight["RECTANGLE"]
			
			if token2.isEnabled == self.isEnabled:
				total += Token.Weight["IS_ENABLED"]
			
			if token2.isVisible == self.isVisible:
				total += Token.Weight["IS_VISIBLE"]
			
			if self.expandState is not None and token2.expandState is not None:
				if token2.expandState == self.expandState:
					total += Token.Weight["EXPAND_STATE"]
			else:
				max -= Token.Weight["EXPAND_STATE"]
			
			if self.shownState is not None and token2.shownState is not None:
				if token2.shownState == self.shownState:
					total += Token.Weight["SHOWN_STATE"]
			else:
				max -= Token.Weight["SHOWN_STATE"]
			
			score = total / max
			threshold = ((Token.THRESH_PERCENT * max) / 100) / max
			
			if score == 1:
				return Token.Match.EXACT, score
			
			elif score >= threshold:
				return Token.Match.CLOSE, score
			
			else:
				return Token.Match.NO, score
	
	def __str__(self):
		ret = "TOKEN:"
		for key, val in vars(self).items():
			ret += "\n\t{:20}:{}".format(key, val)
		return ret
	
	def __repr__(self):
		return self.__str__()
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the visibility behavior.

		.. note::
			This is not just a getter of the __dict__ attribute.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		d = self.__dict__.copy()
		d['rectangle'] = [self.rectangle.left, self.rectangle.top, self.rectangle.width(),
		                  self.rectangle.height()]
		if 'pic' in d and d['pic'] is not None:
			d['pic'] = np.array(self.picture).tolist()
		
		return d
	
	@staticmethod
	def fromDict(d: dict) -> 'Token':
		"""
		Creates a token from a dictionary.

		:param d: The dictionary that represents the Component.
		:type d: dict
		:return: The Token object that was constructed from the dictionary
		:rtype: Token
		"""
		
		if d is None:
			return None
		
		t = Token.__new__(Token)
		
		if d['pic']:
			d["pic"] = Image.fromarray(np.uint8(np.asarray(d["picture"])))
		
		if d['rectangle']:
			r = RECT()
			r.left = d['rectangle'][0]
			r.top = d['rectangle'][1]
			r.right = d['rectangle'][0] + d['rectangle'][2]
			r.bottom = d['rectangle'][1] + d['rectangle'][3]
			d['rectangle'] = r
		
		t.__dict__ = d
		return t
