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

This file contains the Application class - an alternative to pywinauto's Application class that builds off of
pywinauto's Desktop class.
"""

import pywinauto
import psutil
import time


class Application(pywinauto.Desktop):
    """
    This class is an alternative to pywinauto's Application class that will detect windows in all of an application's
    processes.
    
    To use:
        process = psutil.Popen(["path/to/target/application.exe", ...], stdout=PIPE)
        app = Application(backend="uia")
        app.setProcess(process)
        appWindows = app.windows()
    """

    #TODO: If the original process was just used to create other processes and then it disappears, the child processes
    # are called zombies. currently, this class does not work with applications that fit this description. This class
    # could be made more robust.
    
    def setProcess(self, process: psutil.Process) -> None:
        """
        Sets the application's process. This method should be called directly after the Application object is
        instantiated
        
        :param process: the target application's main process
        :type process: psutil.Process
        :return: None
        :rtype: NoneType
        """
        self._process = process
        
    def getPIDs(self) -> list:
        """
        Gets the target application's main process ID and all child process IDs.
        
        :return: list of all process IDs belonging to the target application.
        :rtype: list[int]
        """
        pids = [self._process.pid]
        for child in self._process.children():
            pids.append(child.pid)
        return pids
    
    def windows(self) -> list:
        """
        Gets all windows which belong to the target application and child processes.
        
        :return: list of windows that belong to the target application and it's children processes
        :type: list[pywinauto.application.WindowSpecification]
        """
        wins = pywinauto.Desktop.windows(self)
        appWins = []
        pids = self.getPIDs()
        for win in wins:
            if win.process_id() in pids:
                appWins.append(win)
        return appWins
    
if __name__ == "__main__":
    desktop = pywinauto.Desktop(backend="uia")
    print(desktop.windows())
    
    # Notepad++ doesn't use multiple processes, so I'm not completely testing this correctly. I should run with the
    # calculator app.
    process = psutil.Popen(["C:\\Program Files (x86)\\Notepad++\\notepad++.exe"])
    app = Application(backend="uia")
    app.setProcess(process)
    time.sleep(2)
    print(app.getPIDs())
    print(app.windows())