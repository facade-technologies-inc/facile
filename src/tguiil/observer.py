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

This module contains the Observer class, which watches the target GUI for changes.

"""

import psutil

import pywinauto

from PySide2.QtCore import QThread, Signal

from tguiil.application import Application
from tguiil.tokens import Token
from tguiil.supertokens import SuperToken

#TODO: Create play/pause methods

class Observer(QThread):
    """
    The observer continually traverses the target GUI and notifies when new components are found.
    It maintains a tree of super tokens to determine whether a component has already been found or not.
    
    To use:
        process = psutil.Popen(["C:\\Program Files\\Notepad++\\notepad++.exe"])
        observer = Observer(process.pid, 'uia')
        observer.newSuperToken.connect(targetGUIModel.addSuperToken)
        observer.start()
    """
    
    # This signal is emitted when a new component is detected.
    newSuperToken = Signal(SuperToken, SuperToken)  # (new SuperToken, new SuperToken's parent SuperToken)

    def __init__(self, processID: int, backend: str = "uia"):
        """
        Constructs an Observer. The target application must already be started before constructing the Observer.
        
        :raises: NoSuchProcess
        :raises: AccessDenied
        :param processID: The ID of the process to watch.
        :type processID: int
        :return: None
        :rtype: NoneType
        """
        self._process = psutil.Process(processID)
        self._backend = backend
        self._childMapping = {None: []}  # maps each super token to its list of children.
        
    def run(self) -> int:
        """
        DO NOT CALL THIS METHOD. This method is run in a new thread when the start() method is called.
        
        :return: the exit code of the thread which should be 0.
        :rtype: int
        """
        app = Application(backend=self._backend)
        app.setProcess(self._process)
        while self._process.is_running():
            
            # work acts as a stack. Each element is a 2-tuple where the first element
            # is a GUI component and the second element is the parent super token.
            work = [(win, None) for win in app.windows()]
            while len(work) > 0:
                curComponent, parentSuperToken = work.pop()
                token = self.createToken(curComponent)
                matchedSuperToken = self.matchToSuperToken(token)

                children = curComponent.children()
                for child in children:
                    work.append((child, matchedSuperToken))
    
    def createToken(self, component: pywinauto.base_wrapper) -> Token:
        """
        Create a token from a pywinauto control.
        
        :param component: A pywinauto control from the target GUI.
        :type component: pywinauto.base_wrapper
        :return: The token that was created from the pywinauto control.
        :rtype: Token
        """

        parent = component.parent()
        topLevelParent = component.top_level_parent()
        
        # Information we can get about any element
        id = component.control_id()  ####store this, required, int
        isDialog = component.is_dialog()  ####store this, required, bool
        isEnabled = component.is_enabled()  ####store this, required, bool
        isVisible = component.is_visible()  ####store this, required, bool
        parentTitle = parent.window_text()  ####store this, optional, str
        parentType = parent.friendly_class_name()  ####store this, optional, str
        topLevelParentTitle = topLevelParent.window_text()  ####store this, optional, str
        topLevelParentType = topLevelParent.friendly_class_name()  ####store this, optional, str
        processID = component.process_id()  ####store this, required, int
        rectangle = component.rectangle()  ####store this, required, win32structures.RECT
        texts = component.texts()[1:]  ####store this, required, list[str]
        title = component.window_text()  ####store this, required, str
        numControls = component.control_count()  ####store this, required, int
        image = component.capture_as_image()  ####store this, optional, PIL.Image
        typeOf = component.friendly_class_name()  ####store this, required, str
    
        # construct control identifiers
        # There are 4 possible control identifiers:
        #   - title
        #   - friendly class
        #   - title + friendly class
        #   - closest text + friendly class (only if the title is empty)
        controlIdentifiers = [title, typeOf, title + typeOf]  # TODO: Get last control identifier
    
        # additional information we can get about uia elements
        if isinstance(component, pywinauto.controls.uiawrapper):
            autoID = component.automation_id()  ####store this, optional, int
            childrenTexts = component.children_texts()  ####store this, optional, list[str]
            expandState = component.get_expand_state()  ####store this, optional, int
            shownState = component.get_show_state()  ####store this, optional, int
    
        # create a new token
        # TODO: Reorder parameters to fit Token constructor
        token = Token(controlIdentifiers, id, isDialog, isEnabled, isVisible, processID, rectangle,
                      texts, title, numControls, typeOf, autoID, childrenTexts,
                      expandState, shownState, image, parentTitle, parentType,
                      topLevelParentTitle, topLevelParentType)
        
        return token

    def matchToSuperToken(self, token: Token, parentSuperToken: SuperToken) -> SuperToken:
        """
        Gets the SuperToken that best matches the given token.
        
        The parentSuperToken is necessary in the case that a new SuperToken is created. In this
        case, both the new SuperToken and its parent will be carried in the newSuperToken signal
        which will be emitted.
        
        Having the parent super token also allows us to reduce the search space when finding the
        matched SuperToken.
        
        :param token: The token to find a SuperToken match with.
        :type token: Token
        :param parentSuperToken: The parent of the SuperToken that will be matched with the token.
        :type parentSuperToken: SuperToken
        :return: The SuperToken that gets matched to the provided token.
        :rtype: SuperToken
        """
        # determine if the new token matches any super tokens and how well it matches if it does.
        bestMatch = 0
        bestDecision = Token.Match.NO
        selectedSuperToken = None
        for superToken in self._childMapping[parentSuperToken]:
            decision, matchVal = superToken.shouldContain(token)
            bestDecision = min(bestDecision, decision)
        
            if decision == Token.Match.NO:
                continue
        
            elif decision == Token.Match.EXACT:
                return superToken
        
            elif decision == Token.Match.CLOSE:
                # in the case that multiple SuperTokens closely match the token,
                # we'll use the SuperToken that has the higher match.
                if matchVal > bestMatch:
                    bestMatch = matchVal
                    selectedSuperToken = superToken
    
        # No match was found
        if selectedSuperToken == None and bestMatch != 1:
            newSuperToken = SuperToken(token)
            self._childMapping[parentSuperToken].append(newSuperToken)
            self._childMapping[newSuperToken] = []
            self.newSuperToken.emit(newSuperToken, parentSuperToken)
            return newSuperToken
    
        # a close match was found
        else:
            selectedSuperToken.addToken(token)
    
        return selectedSuperToken
    
    def play(self):
        """
        Runs the Observer.
        
        :return: True if the observer is running, False otherwise.
        :rtype: bool
        """
        if not self._process.is_running():
            return False
        
        if self.isRunning():
            return True
        
        self.start()
        return self.isRunning()
    
    def pause(self):
        """
        Stops the Observer.

        :return: True if the observer is running, False otherwise.
        :rtype: bool
        """
        if self.isRunning():
            self.quit()
            return True
        return False
