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
import data.apim.action as actionModule


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
        #Check if the input parameter types are incorrect.
        if type(action) != actionModule.Action or type(dataType) != type or type(isOptional) != bool:
            raise TypeError("Incorrect parameter types. See doc string")

        self._input: 'Wire' = None
        self._outputs: list = None  # list of wires.
        self._dataType: type = dataType
        self._optional: bool = isOptional
        self._Action: 'Action' = action

    def addOutputWire(self, newWire):
        pass

    def addInputWire(self, newWire):
        pass

    def removeOutputWire(self, ):
        pass

    def removeInputWire(self):
        pass

