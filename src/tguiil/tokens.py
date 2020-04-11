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

This file contains the token class that weighs the importance of each attribute of a single token. 
"""
from difflib import SequenceMatcher
from enum import Enum, unique
from datetime import datetime
from functools import cmp_to_key

import numpy as np
from PIL import Image
from pywinauto.win32structures import RECT
import pywinauto
from skimage.metrics import structural_similarity as ssim

import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
# Can support more languages in future


class Token:
    """
    Token class sets parameters of a token for each state that changes.
    """
    control_ID_count = {}
    
    class CreationException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)
    
    @unique
    class Match(Enum):
        EXACT = 1
        CLOSE = 2
        NO = 3
    
    # These are the MAXIMUM weights, only if the info is identical between 2 tokens. Otherwise it's often scaled.
    Weight = {
        "TITLE": 13,
        "CHILDREN_TEXTS": 15,
        "CONTROL_ID": 8,
        "AUTO_ID": 9,
        "RECTANGLE": 5,
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
    
    # ---- Per-Type Constants ---- #
    # Windows
    WCTEXTS_THRESH_L = 0.6  # if only WCTEXTS_THRESH_L of children texts are the same btwn tokens for wins, diff wins.
    TLWINDOW_THRESH = 0.6  # Threshold for similarity % between two windows' names
                            # and children texts (otherwise no match)
    # Menus
    MENU_TITLE_SIMILARITY_THRESH = 0.8  # Threshold for similarity % between menu names (otherwise no match)
    MENU_TEXTS_THRESH_L = 0.8  # Threshold for similarity % between menu children texts (otherwise no match)
    MENU_TOT_EX_THRESH = 0.8  # Threshold for similarity % between two Menus' names & children texts
                                # for them to be *EXACT* matches (otherwise probabilistic approach)
    # -----------------------------#
    
    # For handling strings not having any significant meaning
    STR1_NOT_SIG = -1.0
    STR2_NOT_SIG = -2.0
    BOTH_NOT_SIG = -3.0
    
    def __init__(self, appTimeStamp: int, identifier: int, isDialog: bool, isEnabled: bool,
                 isVisible: bool, processID: int, typeOf: str, rectangle: RECT, texts: list,
                 title: str, numControls: int, controlIDs: list, parentTitle: str,
                 parentType: str, topLevelParentControlIDs: list, topLevelParentTitle: str, topLevelParentType: str,
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
        :param topLevelParentControlIDs: A list of control identifiers for the dialog that contains (or is) this component.
        :type topLevelParentControlIDs: List[str]
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
        self.topLevelParentControlIDs = topLevelParentControlIDs
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
        
        # self.childrenTexts.sort()  # ChildrenTexts is now a list of lists so this doesn't work
        self.controlIDs.sort()
    
    @staticmethod
    def createToken(timeStamp: datetime, component: pywinauto.base_wrapper.BaseWrapper, captureImage:bool=True) -> 'Token':
        """
        Create a token from a pywinauto control.

        :raises: Token.CreationException

        :param timeStamp: The time that the application instance was created.
        :type timeStamp: datetime
        :param component: A pywinauto control from the target GUI.
        :type component: pywinauto.base_wrapper
        :return: The token that was created from the pywinauto control.
        :rtype: Token
        """
        
        try:
            parent = component.parent()
            if parent:
                parentTitle = parent.window_text()
                parentType = parent.friendly_class_name()
            else:
                parentTitle = ""
                parentType = ""
            
            topLevelParent = component.top_level_parent()
            topLevelParentTitle = topLevelParent.window_text()
            topLevelParentType = topLevelParent.friendly_class_name()
            
            # Information we can get about any element
            id = component.control_id()
            isDialog = component.is_dialog()
            isEnabled = component.is_enabled()
            isVisible = component.is_visible()
            processID = component.process_id()
            rectangle = component.rectangle()
            texts = component.texts()[1:]
            title = component.window_text()
            numControls = component.control_count()
            typeOf = component.friendly_class_name()

            image = None
            if captureImage:
                image = component.capture_as_image()

                # size of dialogs is a bit off, so we trim to adjust.
                if isDialog:
                    width, height = image.size

                    # Setting the points for cropped image
                    left = 15
                    top = 0
                    right = width - 17
                    bottom = height - 17

                    # Cropped image of above dimension
                    # (It will not change orginal image)
                    image = image.crop((left, top, right, bottom))
            
            # get text of all children that are not editable.
            childrenTexts = []
            for child in component.children():
                if type(child) != pywinauto.controls.win32_controls.EditWrapper and type(child) != \
                        pywinauto.controls.uia_controls.EditWrapper:
                    text = child.texts()
                    if text is None:
                        text = child.window_text()
                    if text is None:
                        text = ""
                    childrenTexts.append(text)
            
            # additional information we can get about uia elements
            try:
                autoID = component.automation_id()
                shownState = component.get_show_state()
                expandState = component.get_expand_state()
            except:
                autoID = None
                expandState = None
                shownState = None
            
            # construct control identifiers
            # There are 4 possible control identifiers:
            #   - title
            #   - friendly class
            #   - title + friendly class
            #   - closest text + friendly class (only if the title is empty)
            
            if title is None:
                title = ""

            controlIDs = [title, typeOf, title + typeOf]
            topLevelControlIDs = [topLevelParentTitle, topLevelParentType, topLevelParentTitle + topLevelParentType]
        except Exception as e:
            raise Token.CreationException("Could not build token: {}".format(str(e)))
        
        # create a new token
        token = Token(timeStamp, id, isDialog, isEnabled, isVisible, processID, typeOf,
                      rectangle, texts, title, numControls, controlIDs, parentTitle,
                      parentType, topLevelControlIDs, topLevelParentTitle, topLevelParentType, childrenTexts, image,
                      autoID, expandState, shownState)
        
        return token
    
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
                self.childrenTexts == token2.childrenTexts and \
                ((self.pic is None) == (token2.pic is None)):
            return Token.Match.EXACT, 1
        
        #####################################################################
        # DECISION 3 - COMPONENT-TYPE-EXCLUSIVE DECISIONS
        #
        # Some conditions may still qualify tokens for an exact match, close
        # match, or no match, but are only valid for certain component types.
        # This section handles these cases, and they are often probabilistic
        # in nature.
        #
        # TODO: Fill these out. Try to stick only to no or exact matches,
        #  and leave close matching for the in-depth check.
        #####################################################################
        
        #
        #                    -------------------------
        #                        Top-level Windows
        #                    -------------------------
        #
        #    *Only checks for NO MATCH, otherwise does probabilistic approach*
        #
        elif self.isDialog:
            total = 0
            # --- Title --- #
            titleSim = stringSimilarity(self.title, token2.title)
            
            if titleSim > 0:
                total += titleSim * Token.Weight['TITLE']
            
            # Not handling -1 or -2 since those already mean there's a v big difference in the titles
            
            elif titleSim == Token.BOTH_NOT_SIG:
                if self.title == token2.title:
                    total += Token.Weight['TITLE']
            
            # --- Children Texts --- #
            if self.childrenTexts and token2.childrenTexts:
                try:
                    t1 = [text for sublist in self.childrenTexts for text in sublist]
                    t2 = [text for sublist in token2.childrenTexts for text in sublist]
                except Exception as e:
                    print('childrenTexts for window is deeper than 2, find another way to do this.')
                    raise e
                
                t1Str = ' '.join(t1)
                t2Str = ' '.join(t2)
                
                textsSim = stringSimilarity(t1Str, t2Str)
                
                if textsSim < Token.WCTEXTS_THRESH_L:  # This is the line that fixes multiple windows in one in tguim.
                    return Token.Match.NO, 0
                else:
                    total += textsSim * Token.Weight['CHILDREN_TEXTS']
            
            if total < Token.TLWINDOW_THRESH * (Token.Weight['TITLE'] + Token.Weight['CHILDREN_TEXTS']):
                return Token.Match.NO, 0

            return self.inDepthMatchCheck(token2)
        
        #
        #                    -------------------------
        #                              Menus
        #                    -------------------------
        #
        #    *Only checks for NO MATCH or EXACT match, otherwise does probabilistic approach*
        #
        elif self.type is 'Menu':
            total = 0
            
            titleSim = stringSimilarity(self.title, token2.title)
            
            if titleSim <= Token.MENU_TITLE_SIMILARITY_THRESH:  # For menus, the name is extremely important.
                return Token.Match.NO, 0
            else:
                total += titleSim * Token.Weight['TITLE']

            if self.childrenTexts and token2.childrenTexts:
                try:
                    t1 = [text for sublist in self.childrenTexts for text in sublist]
                    t2 = [text for sublist in token2.childrenTexts for text in sublist]
                except Exception as e:
                    print('childrenTexts for menu is deeper than 2, find another way to do this.')
                    raise e
    
                t1Str = ' '.join(t1)
                t2Str = ' '.join(t2)
    
                textsSim = stringSimilarity(t1Str, t2Str)
    
                if textsSim < Token.MENU_TEXTS_THRESH_L:
                    return Token.Match.NO, 0
                else:
                    total += textsSim * Token.Weight['CHILDREN_TEXTS']
            else:
                # Not the same menu if one doesnt have children texts
                return Token.Match.NO, 0
            
            if total > Token.MENU_TOT_EX_THRESH * (Token.Weight['TITLE'] + Token.Weight['CHILDREN_TEXTS']):
                return Token.Match.EXACT, 0

            return self.inDepthMatchCheck(token2)
        
        ###------------------- EXAMPLE ---------------------###
        # Just an example one that would need to be filled out
        
        elif self.type == 'Button':
            # Some cool stuff, after which
            return self.inDepthMatchCheck(token2)
        # executes if none of it is satisfied
        
        ###-------------------------------------------------###
        
        #####################################################################
        # DECISION 4 - MORE IN DEPTH CHECK FOR CLOSE MATCH (WEIGHTING)
        #
        # (Description of approach in inDepthMatchCheck's DocString)
        #####################################################################
        else:
            return self.inDepthMatchCheck(token2)
    
    def inDepthMatchCheck(self, token2: 'Token'):
        """
        If there has been no decision made about the tokens, we perform a
        probabilistic match. The similarity of each of the following fields
        are taken into consideration:
          - Control IDs
          - Picture (If Given)
          - Rectangle Dimensions and Position
          - Title
          - Parent Title
          - Top Level Parent Title
          - Children Texts
          - Enabled State
          - Visible State
          - Expand State
          - Shown State
          - rectangle size

        If the component is a dialog, we rely much more heavily on these
        fields:
          - Number Of Children
          - Children Text
          - Rectangle Size

        :param token2:
        :return:
        """
        
        max = Token.MAX_WEIGHTS
        total = 0
        
        # compare control identifiers
        idSequence1 = ''.join(self.controlIDs)
        idSequence2 = ''.join(token2.controlIDs)
        controlSimilarity = SequenceMatcher(None, idSequence1, idSequence2).ratio()
        total += Token.Weight["CONTROL_ID"] * controlSimilarity
        
        # compare pictures
        if self.pic is not None and token2.pic is not None:
            if self.pic.size == token2.pic.size:
                try:
                    picSimilarity = (ssim(np.array(self.pic), np.array(token2.pic)) + 1) / 2
                    total += picSimilarity * Token.Weight["PIC"]
                except:
                    total += 0
        elif self.pic is not None or token2.pic is not None:
            total += 0
        else:
            max -= Token.Weight["PIC"]
        
        if self.autoid is not None and token2.autoid is not None and (
                self.autoid != "" or token2.autoid != ""):
            total += SequenceMatcher(None, self.autoid, token2.autoid).ratio() * Token.Weight["AUTO_ID"]
        else:
            max -= Token.Weight["AUTO_ID"]
        
        # compare title, parent title, and top level parent title
        titleSequence1 = ' > '.join([self.title, self.parentTitle, self.topLevelParentTitle])
        titleSequence2 = ' > '.join([token2.title, token2.parentTitle, token2.topLevelParentTitle])
        titleSimilarity = SequenceMatcher(None, titleSequence1, titleSequence2).ratio()
        total += titleSimilarity * Token.Weight["TITLE"]
        
        # compare texts
        texts1 = " ".join(self.texts)
        texts2 = " ".join(token2.texts)
        textsSimilarity = SequenceMatcher(None, texts1, texts2).ratio()
        total += textsSimilarity * Token.Weight["TEXTS"]
        
        # compare children texts
        # TODO: flatten nested lists first using methods as link below...
        #  https://symbiosisacademy.org/tutorial-index/python-flatten-nested-lists-tuples-sets/
        try:
            t1 = [text for sublist in self.childrenTexts for text in sublist]
            t2 = [text for sublist in token2.childrenTexts for text in sublist]
        except Exception as e:
            print('childrenTexts is deeper than 2, find another way to do this.')
            raise e
        
        childTexts1 = ' '.join(t1)
        childTexts2 = ' '.join(t2)
        childTextsSimilarity = SequenceMatcher(None, childTexts1, childTexts2).ratio()
        # if self.isDialog:
        #     max += 25
        #     total += childTextsSimilarity * (Token.Weight["CHILDREN_TEXTS"] + 25)
        # else:
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

    def registerAsAccepted(self):
        """
        This method should only be called on components that are stored in the TGUIM.
        .. warning:: This method should only be called once on each token that is stored permanently.
        :return: None
        :rtype: NoneType
        """
        for controlID in self.controlIDs:
            if self.type == controlID or controlID.strip() == "":
                newVal = 10000000
            else:
                newVal = Token.control_ID_count.get(controlID, 0) + 1
            Token.control_ID_count[controlID] = newVal

    def getControlIDs(self):
        """
        Get the control IDs in order of uniqueness.
        :return: The list of control identifiers in order of uniqueness. In case of a tie, the longer control ID will come first.
        :rtype: List[str]
        """
        return list(filter(len, sorted(self.controlIDs, key=cmp_to_key(Token.control_ID_comparator))))

    def getTopLevelParentControlIDs(self):
        """
        Get the top-level parent control IDs in order of uniqueness.
        :return: The list of control identifiers in order of uniqueness. In case of a tie, the longer control ID will come first.
        :rtype: List[str]
        """
        return list(filter(len, sorted(self.topLevelParentControlIDs, key=cmp_to_key(Token.control_ID_comparator))))

    @staticmethod
    def control_ID_comparator(controlID1: str, controlID2: str) -> int:
        """
        Allows us to compare 2 control IDs based on their uniqueness.

        :param controlID1: The first controlID to compare.
        :type controlID1: str
        :param controlID2: The second controlID to compare.
        :type controlID2: str
        :return: negative int if controlID1 is more unique than controlID2,
                 positive int if controlID2 is more unique than controlID1,
                 If 2 control IDs have same uniqueness, the longer one is considered more unique.
        :rtype: int
        """
        count1 = Token.control_ID_count.get(controlID1, 100000000)
        count2 = Token.control_ID_count.get(controlID2, 100000000)
    
        if count1 < count2:
            return -1
        elif count1 > count2:
            return 1
        else:
            return len(controlID2) - len(controlID1)
    
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
            d['pic'] = np.array(self.pic).tolist()
        
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
            d["pic"] = Image.fromarray(np.uint8(np.asarray(d["pic"])))
        
        if d['rectangle']:
            r = RECT()
            r.left = d['rectangle'][0]
            r.top = d['rectangle'][1]
            r.right = d['rectangle'][0] + d['rectangle'][2]
            r.bottom = d['rectangle'][1] + d['rectangle'][3]
            d['rectangle'] = r
        
        t.__dict__ = d
        return t

def cleanString(myStr: str, sws: bool = True):
    """
    Removes punctuation, puts myStr in lowercase, and removes stopwords
    Stopwords are meaningless: I, you, your, this, a, the, etc.

    :param myStr: String to clean
    :type myStr: str
    :param sws: Whether or not to remove stopwords. Defaults to True.
    :return: Cleaned string
    :rtype: str
    """
    
    myStr = ''.join([word for word in myStr if word not in string.punctuation])
    myStr = myStr.lower()
    if sws:
        myStr = ' '.join([word for word in myStr.split() if word not in stopwords])
    return myStr

def stringSimilarity(str1: str, str2: str) -> float:
    """
    Returns the similarity of two strings using cosine similarity.

    :param str1: First string
    :param str2: Second string
    :return: Similarity strength between 0 (none) and 1 (exact). *Not* a probability.
    :rtype: float
    """
    
    cleaned = list(map(cleanString, [str1, str2]))
    
    if not cleaned[0]:
        cleaned[0] = cleanString(str1, False)
    if not cleaned[1]:
        cleaned[1] = cleanString(str2, False)
    
    # These mean the strings were plain spaces, punctuation, or just empty.
    # In those cases, we return a negative value to let Facile know what happened.
    ### -1: str1 is meaningless, -2: str2 is meaningless, -3: both are meaningless ###
    if not cleaned[0] and not cleaned[1]:
        return Token.BOTH_NOT_SIG
    elif not cleaned[0]:
        return Token.STR1_NOT_SIG
    elif not cleaned[1]:
        return Token.STR2_NOT_SIG
    
    vectors = CountVectorizer().fit_transform(cleaned).toarray()
    
    v1 = vectors[0].reshape(1, -1)
    v2 = vectors[1].reshape(1, -1)
    
    return cosine_similarity(v1, v2)[0][0]