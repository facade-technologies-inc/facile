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
from typing import List

import data.apim.port as pt
from data.apim.wire import Wire


class WireSet:
    """
    A collection of all the wires in an ActionPipeline. An ActionPipeline has only one WireSet.
    The WireSet acts as the interface for creating and deleting wires.
    """
    def __init__(self):
        """
        Constructs a WireSet Object.
        """
        self._wires: list = []

    def addWire(self, sourcePort: 'pt.Port', destPort: 'pt.Port') -> 'Wire or None':
        """
        Creates a new wire and adds it to the set of wires (WireSet).

        .. note:: Adding a wire that already exists will not add a new wire, but it will not 
            raise an exception either.

        :raises: PortException if the the destination port already has an input wire, 
                 but the wire is not a duplication.

        :param sourcePort: The Port to be connected to the input of the wire.
        :type sourcePort: Port
        :param destPort: The Port to be connected to the output of the wire.
        :type destPort: Port
        :return: A reference to the wire newly created wire. Return None if there is already a wire existing between
        the two given ports.
        :rtype: Wire or NoneType
        """
        # Check to see if the new wire is redundant with a wire that already exists in the WireSet.
        newWireAlreadyInSet = False
        for wire in self._wires:
            if (sourcePort, destPort) == wire.asTuple():
                newWireAlreadyInSet = True
                break

        if not newWireAlreadyInSet:
            if destPort.getInputWire() is not None:
                raise pt.PortException("The destination port already has an input!")

        # Only add wires that are unique (not redundant).
        if not newWireAlreadyInSet:
            newWire = Wire(sourcePort, destPort)  # Create the Wire.
            sourcePort.addOutputWire(newWire)  # Connect the wire to its source Port.
            destPort.setInputWire(newWire)  # Connect the wire to its destination Port.
            self._wires.append(newWire)  # Add the Wire to the WireSet.
            return newWire
        else:
            return None

    def deleteWire(self, sourcePort: 'pt.Port', destPort: 'pt.Port') -> None:
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
                # Delete the wire: Remove the wire reference from both ports and from the wire set.
                wire.getSourcePort().removeOutputWire(wire)
                wire.getDestPort().removeInputWire()
                self._wires.remove(wire)

    def deleteWiresConnectedToPort(self, port: 'Port') -> None:
        """
        Deletes all wires connected to a port.

        :param port: The port to remove connections to.
        :type port: Port
        :return: None
        :rtype: NoneType
        """
        # remove outgoing wires
        wires = self.getWiresWithSrcPort(port)[:]
        for wire in wires:
            self.deleteWire(wire.getSourcePort(), wire.getDestPort())
    
        # remove incoming wire if it exists
        wire = self.getWireWithDestPort(port)
        if wire:
            self.deleteWire(wire.getSourcePort(), wire.getDestPort())

    def containsWire(self, sourcePort: 'pt.Port', destPort: 'pt.Port') -> 'bool':
        """
        Checks if a Wire with the given Ports exists in the WireSet.

        :param sourcePort: Port connected to the input of the desired Wire.
        :type sourcePort: Port
        :param destPort: Port connected to the output of the desired Wire.
        :type destPort: Port
        :return: Boolean. True if a Wire with the given ports exists in the set.
        :rtype: bool
        """
        # Search for wire in set with the given ports.
        for wire in self._wires:
            if wire.asTuple() == (sourcePort, destPort):
                return True
        # A Wire was not found...
        return False

    def getWires(self) -> list:
        """
        Gets a list of the Wires in the wireSet.

        :return: List of the Wires in the wireSet.
        :rtype: list of Wires
        """
        return self._wires[:]

    def getWiresWithSrcPort(self, sourcePort: 'pt.Port') -> list:
        """
        Gets a list of the Wires that have the given source Port.

        :param sourcePort: The source Port of the desired wires.
        :type sourcePort: Port
        :return: A list of the Wires with the given source Port.
        :rtype: List[Wire]
        """
        return sourcePort.getOutputWires()

    def getWireWithDestPort(self, destPort: 'pt.Port') -> 'Wire':
        """
        Gets the Wire connected

        :param destPort: The port for which to get wires that are coming in.
        :type destPort: Port
        :return: The wire going into the port
        :rtype: Wire
        """
        return destPort.getInputWire()

    def asDict(self) -> dict:
        """
        Get a dictionary representation of the wire set.

        .. note::
            This is not just a getter of the __dict__ attribute.

        :return: The dictionary representation of the object.
        :rtype: dict
        """
        wsDict = {}

        wsDict["wires"] = [wire.asDict() for wire in self._wires]

        return wsDict

    @staticmethod
    def fromDict(d: dict, parent: 'ActionPipeline') -> 'WireSet':
        """
        Creates a WireSet from the dictionary

        :param d: The dictionary that represents the WireSet.
        :type d: dict
        :param parent: The WireSet's parent ActionPipeline
        :type parent: ActionPipeline
        :return: The WireSet object that was constructed from the dictionary
        :rtype: WireSet
        """
        ws = WireSet()

        for wireDict in d['wires']:

            ws.addWire(Wire.fromDict(wireDict, parent))

        return ws

