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

This file contains the component finder, a class that gets a PyWinAuto handle based on a SuperToken
"""
from typing import Set

import pywinauto
from pywinauto import timings

try:  # Facile imports
    from tguiil.tokens import Token
    from tguiil.matchoption import MatchOption
    from tguiil.application import Application
    from tguiil.supertokens import SuperToken
except ImportError:  # API imports
    from .tokens import Token
    from .matchoption import MatchOption
    from .application import Application
    from .supertokens import SuperToken


class ComponentNotFoundException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class ComponentFinder:
    """
    The ComponentFinder can be used to match a super token to a component in the target GUI using
    the specified matching schemes.
    """

    PYWINAUTO_TIMEOUT = 5  # seconds

    def __init__(self, app: Application, options: Set[MatchOption], defaultOption=MatchOption.CloseToken):
        """
        Initialize a component finder object.

        :param app: The application instance used to traverse the target GUI.
        :type app: tguiil.application.Application (preferred) OR pywinauto.application.Application
        :param options: The set of matching schemes that will be used to match the super token to a component.
        :type options: Set[MatchOption]
        :param defaultOption: If the options are empty, the default option will be used.
        :type defaultOption: MatchOption
        """
        self._app = app
        self._matchOptions = []
        for option in options:
            self._matchOptions.append(option.value)

        if not self._matchOptions:
            self._matchOptions.append(defaultOption.value)

        timings.Timings.window_find_timeout = ComponentFinder.PYWINAUTO_TIMEOUT

    def find(self, superToken: SuperToken, path: list = None):
        """
        Finds a superToken in the target GUI.

        :param superToken: The super token to find.
        :type superToken: SuperToken
        :param path: The SuperToken path that leads to the provided SuperToken, starting with window's ST.
        :type path: list
        :return: The component that matches the super token.
        :rtype: pywinauto.base_wrapper
        """

        def checkAppIsRunning():
            if not self._app.is_process_running():
                msg = "The application stopped before we could locate the component"
                raise ComponentNotFoundException(msg)

        checkAppIsRunning()

        # TOKEN COMPARISON:
        # |  traverse the GUI, build tokens for each component and compare to the tokens within the super token given to
        # |  determine if there is a match. Depending on the match options, we may return if we find an exact match
        # |  or we may return a match that's close enough.
        if MatchOption.CloseToken.value in self._matchOptions or MatchOption.ExactToken.value in self._matchOptions:
            timestamp = self._app.getStartTime()

            if path:  # If the path is provided, no need to use the given ST as it is the last one in the path.
                print('using path')
                for depth in range(0, len(path)):
                    if depth is 0:  # Only on first run should we get the windows, otherwise the target comps' children
                        work = [win for win in self._app.windows()]

                        # In special cases, new dialogs spawn as children of the main dialog.
                        children = [child for win in work for child in win.children()]
                        for child in children:
                            if child.is_dialog():
                                work.append(child)
                    else:
                        work = [child for child in bestComp.children()]

                    currentST = path[depth]  # Current SuperToken from path
                    exactFound = False
                    closestComponent = None
                    bestCertainty = 0

                    while len(work) > 0:
                        checkAppIsRunning()
                        curComponent = work.pop()

                        try:
                            token = Token.createToken(timestamp, curComponent)
                        except Token.CreationException as e:
                            print(str(e))
                        else:
                            decision, certainty = currentST.shouldContain(token)
                            if decision.value == Token.Match.EXACT.value:
                                if MatchOption.ExactToken.value in self._matchOptions:
                                    exactFound = True
                                    break
                            elif decision.value == Token.Match.CLOSE.value:
                                if certainty > bestCertainty:
                                    closestComponent = curComponent
                                    bestCertainty = certainty

                    if exactFound:
                        if depth == len(path) - 1:
                            # We have the droi... SuperToken we're looking for. If it's not exact, handled later.
                            return curComponent
                        bestComp = curComponent
                    elif closestComponent:  # For the path, this is regardless of chosen search options
                        bestComp = closestComponent
                    else:
                        # This means none of the children match, so we give up with this method and let PWA do the rest.
                        break

            else:
                bestCertainty = 0
                work = [win for win in self._app.windows()]
                while len(work) > 0:
                    checkAppIsRunning()
                    curComponent = work.pop()

                    try:
                        token = Token.createToken(timestamp, curComponent)
                    except Token.CreationException as e:
                        print(str(e))
                    else:
                        decision, certainty = superToken.shouldContain(token)
                        if decision.value == Token.Match.EXACT.value:
                            if MatchOption.ExactToken.value in self._matchOptions:
                                return curComponent
                        elif decision.value == Token.Match.CLOSE.value:
                            if certainty > bestCertainty:
                                closestComponent = curComponent
                                bestCertainty = certainty

                    children = curComponent.children()
                    for child in children:
                        work.append(child)

            if closestComponent:
                if MatchOption.CloseToken.value in self._matchOptions:
                    return closestComponent

        # PYWINAUTO BEST MATCH:
        # |  To do pywinauto best match, we need the control identifier of the dialog and the control identifier of the
        # |  component that we care about. In the event that the component we care about is a dialog, we just need the
        # |  dialog information.
        # |
        # |  WARNING: There are weird issues with PWA Best Match not finding the component. For now, This is only
        # |           acceptable to use as a fallback method for finding components
        # |
        # |  TODO:    Improve this search. If PWA Best Match becomes reliable and fast, use it before token comparison.
        # |
        # |  NOTES:   Using our Application class to find the component, it's possible that the found component is from
        # |           a different application, which is a critical bug. This is because our Application class inherits
        # |           from pywinauto.Desktop.
        # |
        # |           To get around this, we create pywinauto.application.Application instances for each process in the
        # |           that belongs to the application and search it for the dialog, then the component that we care
        # |           about.
        if MatchOption.PWABestMatch.value in self._matchOptions:
            tokens = superToken.getTokens()
            isDialog = tokens[0].isDialog

            # find the order of attempts to result in the most accurate identification of the component
            controlIDs = []
            for token in tokens:
                for dialogControlID in token.getTopLevelParentControlIDs():
                    for controlID in token.getControlIDs():
                        controlIDs.append((dialogControlID, Token.control_ID_count[dialogControlID], controlID,
                                           Token.control_ID_count[controlID]))

            controlIDs = sorted(list(set(controlIDs)), key=lambda tup: tup[1 if isDialog else 3])

            # in the case that the target app uses multiple processes, we have to search all of them.
            apps = [pywinauto.application.Application().connect(process=pid) for pid in self._app.getPIDs()]
            for app in apps:
                dlgs = {}  # maps dialog identifier to dialog component
                for dlgCtrlId, temp1, ctrlId, temp2 in controlIDs:

                    # If we've already used this dialog control ID to identify a dialog, don't look for it again
                    if dlgCtrlId in dlgs:
                        if dlgs[dlgCtrlId] is None:
                            continue
                        else:
                            dlg, dlgWrapper = dlgs[dlgCtrlId]

                    # if we haven't used this dialog control ID, search for the dialog.
                    else:
                        try:
                            dlg = app[dlgCtrlId]
                            dlgWrapper = dlg.wrapper_object()
                        except pywinauto.findbestmatch.MatchError as e:
                            dlgs[dlgCtrlId] = None
                            continue
                        else:
                            if isDialog:
                                return dlgWrapper
                            dlgs[dlgCtrlId] = (dlg, dlgWrapper)

                    try:
                        return dlg[ctrlId].wrapper_object()
                    except pywinauto.findbestmatch.MatchError as e:
                        continue

        raise ComponentNotFoundException("The selected component could not be\nfound in the target GUI.")
