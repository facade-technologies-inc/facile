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

    This document contains the BaseApplication class
"""

import sys
import os
import time as t
import json
import psutil
import pywinauto
import pyautogui
import traceback
from datetime import datetime
from typing import Set

try: # API
    from .tguiil.tokens import Token
    from .tguiil.application import Application
    from .tguiil.matchoption import MatchOption
    from .tguiil.componentfinder import ComponentFinder
    from .data.tguim.targetguimodel import TargetGuiModel
    from .data.tguim.visibilitybehavior import VisibilityBehavior
except: # SPHINX
    from tguiil.tokens import Token
    from tguiil.application import Application
    from tguiil.matchoption import MatchOption
    from tguiil.componentfinder import ComponentFinder
    from data.tguim.targetguimodel import TargetGuiModel
    from data.tguim.visibilitybehavior import VisibilityBehavior

pathToThisFile, thisFile = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, pathToThisFile)


class WaitException(Exception):
    def __init__(self, msg: str):
        Exception.__init__(self, msg)


class BaseApplication:
    """
    The core of all Facile APIs: contains functions that are necessary for any API. The
    custom generated Application class inherits from this.
    """
    
    def __init__(self, exeLoc: str, options: Set['MatchOption'], name: str, reqCompIds: list, backend: str = 'uia'):
        """
        Initializes a BaseApplication instance.

        :param exeLoc: filepath to executable for target application
        :type exeLoc: str
        :param options: options to use when searching for a component
        :type options: set
        :param name: project name (necessary for opening tguim file)
        :type name: str
        :param reqCompIds: a list of required components' IDs
        :type reqCompIds: list
        :param backend: backend type
        :type backend: str
        """
        
        # Note that app is a custom Desktop instance from pywinauto, not an application instance.
        self.app = Application(backend=backend)
        self._isRunning = False
        self._options = options
        self._exeLoc = exeLoc
        self._name = name
        self._compFinder = ComponentFinder(self.app, self._options)
        self._pathMap = {}
        self._compIDs = reqCompIds
        
        try:
            with open(os.path.join(pathToThisFile, self._name + ".tguim"), 'r') as tguimFile:
                d = json.loads(tguimFile.read())
                self._tgm = TargetGuiModel.fromDict(d)
        except Exception as e:
            print("Couldn't load from {}".format('./' + self._name + '.tguim'))
            self._tgm = None
            traceback.print_exc()

        self._generatePathMap()
    
    def startApp(self):
        """
        Starts the target application, then waits for all processes' active window to be ready.
        """
        if not self._isRunning:
            self.app.start(self._exeLoc)
            self._isRunning = True
        else:
            print('Your app is already running. If you want more instances, '
                  'import the API again under a different name and start it.\n(i.e. from myAPI import myApp as myApp2)')
    
    def stop(self):
        """
        Stops the target application and the processes spawned by it
        """
        if self._isRunning:
            self.app.kill()
        else:
            print('Your app should not be running. If it is, please report this as a bug on our website.')
            
    def pause(self):
        """
        Pauses execution while the user interacts with their app.
        """
        
        pyautogui.alert('Execution paused. Press "OK" when ready to continue.')
    
    def wait(self, state: str, timeout: int = 10):
        """
        Pauses until state is reached for each process's active window, timing out in timeout seconds.
        Useful when waiting for target app to complete execution of a task, or when starting up.
        Wraps around pywinauto's wait function.

        :param state: state to wait for ('visible', 'ready', 'exists', 'enabled', 'active'), or time to wait in s or m
        :type state: str
        :param timeout: Maximum number of seconds to wait for state to be reached. Defaults to a minute, should be longer for apps with more windows.
        :type timeout: float
        """
        
        try:
            if ' s' in state:
                t.sleep(float(state[:-2]))
            elif ' m' in state:
                t.sleep(60 * float(state[:-2]))
            else:
                self.app.wait(state, timeout)
        except Exception as e:
            raise WaitException('Not a valid wait time or state. Please use "x s" or "x m" for x seconds/minutes \
            respectively, or use one of "visible", "ready", "exists", "enabled", "active" as state to wait for.')

    def _generatePathMap(self):
        """
        Creates a map of component ID to (supertoken path, handle) tuples, where handle is initialized to None
        """

        for id in self._compIDs:
            tmpComp = self._getComponentObject(id)
            path = [comp.getSuperToken() for comp, pos in tmpComp.getPathFromRoot()][:-1]  # The last item is the root
            print(path)
            path.reverse()  # 1st component is window, second is 1-level deep child, etc.
            self._pathMap[id] = (path, None)
    
    def _findComponent(self, compID: int) -> 'pywinauto.base_wrapper.BaseWrapper':
        """
        Finds the component with ID compID forcing its appearance if not visible.

        :param compID: ID of component to find.
        :type compID: int
        :return: handle to component
        :rtype: pywinauto.base_wrapper.BaseWrapper
        """

        path, tmpHandle = self._pathMap[compID]

        if tmpHandle:
            if tmpHandle.visible:
                return tmpHandle

        comp = self._getComponentObject(compID)
        self._forceShow(comp)

        handle = self._compFinder.find(comp.getSuperToken(), path)

        self._pathMap[compID] = (path, handle)
        return handle
    
    def _getComponentObject(self, compID: int) -> 'Component':
        """
        Gets the Component object for an item with ID compID. Handles possible errors with getting it.

        :param compID: ID of component to get the Component object for
        :type compID: int
        :return: The component item for an item with ID compID
        :rtype: Component
        """
        
        try:
            comp = self._tgm.getComponent(compID)
            if comp:
                return comp
            else:
                raise Exception("Could not get component " + str(compID) + " from TGUIM.")
        except Exception as e:
            raise Exception(str(e))
        
    def _getWindowObjectIDFromHandle(self, winHandle: pywinauto.base_wrapper.BaseWrapper) -> 'Component':
        """
        Gets the Component object for a component with handle compHandle.
        ** ONLY WORKS FOR WINDOWS ** (Can be modified for more, but implemented this way to save processing power/time.

        :param winHandle: handle of window to get Component object for
        :type winHandle: pywinauto.base_wrapper.BaseWrapper
        :return: The Component object for an item with handle compHandle
        :rtype: Component
        """
        
        # Create Token for handle
        timeStamp = datetime.now()
        token = Token.createToken(timeStamp, winHandle, captureImage=False)
    
        # determine if the new token matches any super tokens and how well it matches if it does.
        bestMatch = 0
        bestDecision = Token.Match.NO.value
        selectedComponent = None
        potentialMatches = []
        comps = self._tgm.getComponents()
        for id in comps:
            comp = comps[id]
            st = comp.getSuperToken()
            if st.tokens[0].isDialog:
                potentialMatches.append((st, comp))
        
        for superToken, comp in potentialMatches:
            decision, matchVal = superToken.shouldContain(token)
            bestDecision = min(bestDecision, decision.value)
            
            if decision.value == Token.Match.NO.value:
                continue
        
            elif decision.value == Token.Match.EXACT.value:
                return comp.getId()
        
            elif decision.value == Token.Match.CLOSE.value:
                # in the case that multiple SuperTokens closely match the token,
                # we'll use the SuperToken that has the higher match.
                if matchVal > bestMatch:
                    bestMatch = matchVal
                    selectedComponent = comp

        # returning no matter what: if selected Comp is none, we don't care, we just return none since this is only used
        # for getting the target windows that have already been defined in Facile
        if selectedComponent:
            return selectedComponent.getId()
    
    def _forceShow(self, compObj: 'Component'):
        """
        Attempts to force the component to be visible using visibility behaviors.
        Uses a simple breadth-first search algorithm.

        :param compObj: Component to show
        :type compObj: Component
        :return: None
        """
        
        # --- This may be useful for other search algorithms later --- #
        # # First, get all necessary lists.
        # # The instantiated Visibility Behaviors (These are the edges)
        # visBs = self._tgm.getVisibilityBehaviors()
        # # All top-level windows in the TGUIM (These are the nodes)
        # tlwComps = self._tgm.getTopLevelWindows()
        # ------------------------------------------------------------ #

        # Get the window that we want to show. This is the starting point.
        startWindow, pos = compObj.getPathFromRoot()[-2]  # -1 position is root, -2 is window
        
        # Get the currently active windows, which are the algorithm's targets.
        # We want the component objects for these, not the actual handles.
        targets = []
        handles = self.app.windows()
        while handles:
            handle = handles.pop()
            for child in handle.children():
                if child.is_dialog():
                    handles.append(child)
            targets.append(self._getWindowObjectIDFromHandle(handle))  # Ids are faster to compare than Comps
        
        # Find path to one of the windows from desired component's window.
        # How this works:
        # Store lists of (component, window, VB) tuples, where the VB is performed on component.
        # These lists are the path to the most recent item in the list, and the containing list holds all paths
        work = [[(compObj, startWindow, None)]]
        seen = []
        path = []
        success = False
        while work:  # TODO: Might want to modify this to have a "backup" path as well: just keep the first 2 paths
            path = work.pop(0)
            curComp, window, visB = path[-1]
            
            if window.getId() in targets:  # Found closest path
                success = True
                break
            elif window.getId() in seen:  # already saw window; ignoring it
                continue
            else:
                seen.append(window.getId())  # avoids seeing a window multiple times and getting an infinite loop
                for vb in (curComp.getDestVisibilityBehaviors() + window.getDestVisibilityBehaviors()):
                    # if vb.getReactionType() is VisibilityBehavior.ReactionType.Show:
                    tmp = path[:]
                    tmpComp = vb.getSrcComponent()
                    tmpWin, pos = vb.getSrcComponent().getPathFromRoot()[-2]
                    tmp.append((tmpComp, tmpWin, vb))
                    work.append(tmp)
        
        if not success:
            print(compObj, startWindow)
            pyautogui.alert('Could not force component appearance. Please manually ensure that component "' +
                            compObj.getName() + '" in window "' + startWindow.getName() + '" is visible, then press '
                                                                                          'OK.')
        else:
            # Now, window is one of the active windows, so we can now interact with the application and
            # force comp's appearance.
            while path:
                curComp, window, visB = path.pop()
                if visB:
                    # if curComp.getSuperToken().getTokens()[0].type not in ['Menu', 'MenuItem']:
                    #     comp = self._compFinder.find(curComp.getSuperToken())
                    # else:
                    #     comp = curComp
                    methodName = visB.methodName
                    exec("self." + methodName + "()")
    
    def _selectMenuItem(self, component: 'Component'):
        """
        MenuItems can't be clicked the same way as other components, so this function takes care of this.

        :param component: menuItem to be selected
        :type component: Component
        :return: None
        """
        
        curComp = component
        nxtParent = curComp.getParent()
        compPath = [curComp]
        # Getting the lowest level component containing the menu/menuitem that can be force-shown
        while nxtParent.getSuperToken().getTokens()[0].type in ['Menu', 'MenuItem']:
            curComp = nxtParent
            nxtParent = curComp.getParent()
            compPath.append(curComp)
        # Now compPath has the list of components, including the component itself, in the reverse order that component
        # can be found with.
        
        # Create the string that can be input into the menu_select function of pywinauto
        pathStr = ''
        while compPath:
            comp = compPath.pop()
            pathStr += comp.getSuperToken().getTokens()[0].title + '->'
        pathStr = pathStr[:-2]
        
        # Then get the containing top-level window
        windowComp, pos = nxtParent.getPathFromRoot()[-2]  # -1 position is root, -2 is window
        
        # Now force show the window, and get its handle
        self._forceShow(windowComp)
        window = self._compFinder.find(windowComp.getSuperToken())
        
        # Then finally select the menuItem
        window.menu_select(pathStr)
