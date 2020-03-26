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
from typing import Set

import pywinauto
from pywinauto import timings

from tguiil.tokens import Token
from tguiil.matchoption import MatchOption
from tguiil.application import Application
from tguiil.supertokens import SuperToken

class ComponentNotFoundException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ComponentFinder:
    """
    The ComponentFinder can be used to match a super token to a component in the target GUI using
    the specified matching schemes.
    """

    PYWINAUTO_TIMEOUT = 5 # seconds

    def __init__(self, app: Application, options: Set[MatchOption], defaultOption=MatchOption.CloseToken):
        """
        Initialize a component finder object.

        :param app: The application instance used to traverse the target GUI.
        :type app: tguiil.application.Application (preffered) OR pywinauto.application.Application
        :param options: The set of matching schemes that will be used to match the super token to a component.
        :type options: Set[MatchOption]
        :param defaultOption: If the options are empty, the default option will be used.
        :type defaultOption: MatchOption
        """
        self._app = app
        self._matchOptions = options

        if self._matchOptions == {}:
            self._matchOptions.add(defaultOption)

        timings.Timings.window_find_timeout = ComponentFinder.PYWINAUTO_TIMEOUT

    def find(self, superToken: SuperToken):
        """
        Finds a superToken in the target GUI.

        :param superToken: The super token to find.
        :type superToken: SuperToken
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
        if MatchOption.CloseToken in self._matchOptions or MatchOption.ExactToken in self._matchOptions:
            timestamp = self._app.getStartTime()
            bestCertainty = 0
            closestComponent = None

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
                    if decision == Token.Match.EXACT:
                        if MatchOption.ExactToken in self._matchOptions:
                            return curComponent
                    elif decision == Token.Match.CLOSE:
                        if certainty > bestCertainty:
                            closestComponent = curComponent
                            bestCertainty = certainty

                children = curComponent.children()
                for child in children:
                    work.append(child)

            if closestComponent:
                if MatchOption.CloseToken in self._matchOptions:
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
        if MatchOption.PWABestMatch in self._matchOptions:
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