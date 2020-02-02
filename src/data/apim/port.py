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
from data.apim.wire import Wire


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
        self._outputs: list = []  # list of wires.
        self._dataType: type = dataType
        self._optional: bool = isOptional
        self._Action: 'Action' = action

    def addOutputWire(self, newWire: 'Wire') -> None:
        """
        Connects a wire to the output of the port by adding it to the list of output wires. If a wire is passed in that
        is redundant with one already in the list, it is ignored.

        This function assumes that this Port is set as the Wire's source port outside of this function.

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

    def setInputWire(self, newWire: 'Wire') -> None:
        """
        Connects the given wire to the input of the port. (There can be only one input wire).

        This function assumes that this Port is set as the Wire's destination port outside of this function.

        :param newWire: A wire which is to be connected to the input of the port.
        :type newWire: Wire
        :return: None
        :rtype: NoneType
        """
        self._input = newWire

    def removeOutputWire(self, wireToRemove: 'Wire') -> None:
        """
        Removes the given wire from the Port's list of output wires.

        This function assumes that the given Wire's Port references are updated outside of this function.

        :param wireToRemove: The wire to be removed from the Port's list of output wires.
        :type wireToRemove: Wire
        :return: None
        :rtype: NoneType
        """
        # Check to see if the given wire is really one of the port's output wires.
        if wireToRemove in self._outputs:
            self._outputs.remove(wireToRemove)

    def removeInputWire(self) -> None:
        """
        Removes the Port's input Wire.

        This function assumes that the input Wire's Port references are updated outside of this function.

        :return: None
        :rtype: NoneType
        """
        self._input = None


    def getOutputWires(self) -> list:
        """
        Gets a list of the Port's output Wire's.

        :return: A list of the Port's output Wire's.
        :rtype: list of Wires
        """
        return self._outputs

    def getInputWire(self) -> 'Wire':
        """
         Gets the Port's input Wire.

        :return: The Port's input Wire.
        :rtype: Wire
        """
        return self._input

    def getDataType(self) -> type:
        """
        Returns the data type of this Port.

        :return: The data type as a Python type.
        :rtype: type
        """
        return self._dataType

    def setDataType(self, newType: type) -> None:
        """
        Sets the data type of the port. (A Python type [e.g. int, str, bool, etc.])

        :param newType: A Python type [e.g. int, str, bool, etc.].
        :type newType: type
        :return: None
        :rtype: NoneType
        TODO: add exception doc string info.
        """
        if type(newType) == type:
            self._dataType = newType
        else:
            raise TypeError("setDataType()'s input parameter must specify a Python type [e.g. int, str, bool].")

    def setOptional(self, isOptional: bool) -> None:
        """
        Sets whether the Port must be connected or not.

        :param isOptional: True if the Port is optionally connected. False if it MUST be connected.
        :type isOptional: bool
        :return: None
        :rtype: NoneType
        """
        self._optional = isOptional

    def isOptional(self) -> bool:
        """
        Returns True if the Port doesn't necessarily have to be connected, False if it MUST be connected.

        :return: A bool: True if the Port doesn't necessarily have to be connected, False if it MUST be connected.
        :rtype: bool
        """
        return self._optional