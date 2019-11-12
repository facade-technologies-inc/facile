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
from PySide2.QtCore import QThread, Signal

from tguiil.application import Application
from tguiil.token import Token
from tguiil.supertoken import SuperToken

class Observer(QThread):
    """
    The observer continually traverses the target GUI and notifies when new components are found.
    It maintains a tree of super tokens to determine whether a component has already been found or not.
    
    To use:
        process = psutil.Popen(["C:\\Program Files\\Notepad++\\notepad++.exe"])
        observer = Observer(process.pid)
        observer.newSuperToken.connect(targetGUIModel.addSuperToken)
        observer.start()
    """
    
    # This signal is emitted when a new component is detected.
    newSuperToken = Signal(SuperToken, SuperToken)  # (new SuperToken, new SuperToken's parent SuperToken)

    def __init__(self, processID: int, backend: str = "uia") -> 'Observer':
        """
        Constructs an Observer. The target application must already be started before constructing the Observer.
        
        :raises: NoSuchProcess
        :raises: AccessDenied
        :param processID: The ID of the process to watch.
        :type processID: int
        """
        self._process = psutil.Process(processID)
        self._backend = backend

        # We'll create a tree of super tokens by using a dictionary rather than keeping children and parent references
        # inside of the super tokens. The benefit of this is that the Target GUI Model is the only true tree structure.
        # That way, we don't have to make sure 2 trees are synced all the time.
        root = SuperToken()
        self._childMapping = {root: []}  # maps each super token to its list of children.
        self._parentMapping = {root: None}   # maps each super token to its parent.
        
    def run(self) -> int:
        """
        The starting point for the thread after calling start()
        
        :return: the exit code
        :rtype: int
        """
        app = Application(backend=self._backend)
        app.setProcess(self._process)
        while self._process.is_running():
            work = app.windows()[:]
            while len(work) > 0:
                curComponent = work.pop()
                
                #TODO:
                # 1. create token
                # 2. find the new token in super token tree
                #       a. if exact match is found, move on
                #       b. if close match is found, add the token to the close super token
                #       c. if no match is found, create a new super token and emit the newSuperToken signal
                
                children = curComponent.children()
                for child in children:
                    work.push(child)
