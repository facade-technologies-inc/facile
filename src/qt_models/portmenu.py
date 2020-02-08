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

This module contains the PortMenu class which is the context menu that is seen when a
Port is right-clicked.
"""

from PySide2.QtWidgets import QMenu


class PortMenu(QMenu):
    """
    This class is the menu that shows when a port is right clicked in the APIM View.
    Menu items: "Delete", "Rename", "Configure Ports".
    """

    def __init__(self):
        """
        Constructs a PortMenu Object.
        """
        QMenu.__init__(self)

        # delete
        self.deleteAction = self.addAction("Delete")

        # rename
        self.renameAction = self.addAction("Rename")

        # configure ports
        self.configurePortsAction = self.addAction("Configure Ports")
