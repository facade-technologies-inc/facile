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

This module contains the WireSet class.
"""

from data.apim.port import Port
from data.apim.wire import Wire


class WireSet:
    """

    """
    def __init__(self):
        """

        """
        self._wires: list = None

    def addWire(self, newWire: 'Wire'):
        """

        :param newWire:
        :return:
        """
        # Check to see if the new wire is redundant with a wire that already exists in the WireSet.
        newWireAlreadyInSet = False
        for wire in self._wires:
            if newWire.getSourcePort() == wire.getSourcePort() and newWire.getDestPort() == wire.getDestPort():
                newWireAlreadyInSet = True
                break

        if not newWireAlreadyInSet:
            self._wires.append(newWire)

    def deleteWire(self, sourcePort: 'Port', destPort: 'Port'):
        """

        :param sourcePort:
        :param destPort:
        :return:
        """
        # Search for wire in set with the given ports.
        for wire in self._wires:
            if wire.getSourcePort() == sourcePort and wire.getDestPort() == destPort:
                # Delete the wire: Remove the wire reference from both ports, and from the wire set.
                wire.getSourcePort().