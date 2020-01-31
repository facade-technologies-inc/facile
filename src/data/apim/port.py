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

This module contains the Port class.
"""
from data.apim.wire import Wire #TODO: this will probably cause a circular import.


class PortException(Exception):
    def __init__(self, msg: str):
        Exception.__init__(msg)

class Port:
    """
    A Port defines the interface between an Action (ActionPipeline or ComponentAction) and the outside world.
    A Port has one input (could be None), and as many outputs as desired. In effect, the input of the Port is
    duplicated across all of its outputs. Ports specify the data type that may be passed across it.
    (Ports between different Actions are connected with Wires).
    """
    def __init__(self, action: 'Action', dataType: type = None, isOptional: bool = False):
        """
        Constructs a Port Object.

        :param action: The Action Object that the Port belongs to.
        :type action: Action
        :param dataType: The data type that is to be passed across the Port.
        :type dataType: type
        :param isOptional: Boolean specifying if the Port must be connected for the Port's Action to remain valid.
        :type isOptional: bool
        """
        self._input: 'Wire' = None
        self._outputs: list = None  # list of wires.
        self._dataType: type = dataType
        self._optional: bool = isOptional
        self._Action: 'Action' = action

    def addOutputWire(self, newWire: 'Wire') -> None:
        """
        Connects a wire to the output of the port by adding it to the list of output wires. If a wire is passed in that
        is redundant with one already in the list, it is ignored.

        :param newWire: A wire to be connected to the output of the port.
        :type newWire: Wire
        :return: None
        :rtype: NoneType
        """
        # Check if the new wire is redundant (has the same ports) with a wire already in the list.
        newWireAlreadyInList = False
        for wire in self._outputs:
            if newWire.asTuple() == wire.asTuple():
                newWireAlreadyInList = True
                break

        # Add the new wire to the list of outputs if it's not redundant.
        if not newWireAlreadyInList:
            self._outputs.append(newWire)
            newWire.setSourcePort(self)  # Connect the wire to the port from the wire's perspective.

    def addInputWire(self, newWire: 'Wire') -> None:
        """
        Connects the given wire to the input of the port. (There can be only one input wire)

        :param newWire: A wire which
        :type newWire: Wire
        :return: None
        :rtype: NoneType
        """

    def removeOutputWire(self, ):
        pass

    def removeInputWire(self):
        pass

