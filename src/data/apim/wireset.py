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
    A collection of all the wires in an ActionPipeline. An ActionPipeline has only one WireSet.
    """
    def __init__(self):
        """

        """
        self._wires: list = None

    def addWire(self, newWire: 'Wire') -> None:
        """
        Adds a given wire to the set of wires (WireSet).

        :param newWire: A wire to be added to the wire set.
        :type newWire: Wire
        :return: None
        :rtype: NoneType
        """
        # Check to see if the new wire is redundant with a wire that already exists in the WireSet.
        newWireAlreadyInSet = False
        for wire in self._wires:
            if newWire.asTuple() == wire.asTuple():
                newWireAlreadyInSet = True
                break

        # Only add wires that are unique (not redundant).
        if not newWireAlreadyInSet:
            self._wires.append(newWire)

    def deleteWire(self, sourcePort: 'Port', destPort: 'Port') -> None:
        """
        Deletes a wire with the given ports from the set. If there is no wire with the specified ports,
        nothing happens.

        :param sourcePort: The Port on the input end of the wire.
        :type sourcePort: Port
        :param destPort: The Port on the output end of the wire.
        :type destPort: Port
        :return: None
        :rtype: NoneType
        """
        # Search for wire in set with the given ports.
        for wire in self._wires:
            if wire.asTuple() == (sourcePort, destPort):
                pass
                # Delete the wire: Remove the wire reference from both ports and from the wire set.
                # TODO: Complete this
                #wire.getSourcePort().