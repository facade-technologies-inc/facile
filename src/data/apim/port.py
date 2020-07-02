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
import data.apim.wire as wr
import data.apim.action as ac
from data.entity import Entity
from data.properties import Properties
import data.apim.actionpipeline as ap
import data.apim.actionwrapper as aw


class PortException(Exception):
    def __init__(self, msg: str):
        Exception.__init__(self, msg)

class InvalidDataTypeException(PortException):
    def __init__(self, msg: str):
        Exception.__init__(self, msg)


class Port(Entity):
    """
    A Port defines the interface between an Action (ActionPipeline or ComponentAction) and the outside world.
    A Port has one input (could be None), and as many outputs as desired. In effect, the input of the Port is
    duplicated across all of its outputs. Ports specify the data type that may be passed across it.
    (Ports between different Actions are connected with Wires).
    
    .. warning:: Although this class provides methods to add wires, this should only be performed from
        the WireSet class. Using methods that establish wire connections should be used carefully to
        ensure that references between ports and wires maintain synchronized.
    """

    def __init__(self, dataType: type = type(None), isOptional: bool = False):
        """
        Constructs a Port Object.
        
        .. note:: The port's action will be set when the port is added as either an input or
            output of an action.

        :param dataType: The data type that is to be passed across the Port.
        :type dataType: type
        :param isOptional: Boolean specifying if the Port must be connected for the Port's Action to remain valid.
        :type isOptional: bool
        """
        super().__init__()

        predefinedCategories = ["Base", "Port"]
        customCategories = {}
        props = Properties.createPropertiesObject(predefinedCategories, customCategories)
        props.getProperty("ID")[1].setValue(self.getId())
        props.getProperty("Type")[1].setValue("Port")
        props.getProperty("Data Type")[1].setValue(str(dataType))
        self.setProperties(props)
        
        self._input: 'wr.Wire' = None
        self._outputs: list = []  # list of wires.
        self._dataType: type = None
        self._optional: bool = isOptional
        self._action: 'ac.Action' = None
        self._default = None

        self.setDataType(dataType)

    def addOutputWire(self, newWire: 'wr.Wire') -> None:
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

    def setInputWire(self, newWire: 'wr.Wire') -> None:
        """
        Connects the given wire to the input of the port. (There can be only one input wire).

        This function assumes that this Port is set as the Wire's destination port outside of this function.

        :param newWire: A wire which is to be connected to the input of the port.
        :type newWire: Wire
        :return: None
        :rtype: NoneType
        """
        self._input = newWire

    def removeOutputWire(self, wireToRemove: 'wr.Wire') -> None:
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

    def getInputWire(self) -> 'wr.Wire':
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

    def setDataType(self, newType: type, enforceType=True) -> None:
        """
        Sets the data type of the port. (A Python type [e.g. int, str, bool, etc.])

        :raises: InvalidDataTypeError if newType is not a valid type

        :param newType: A Python type [e.g. int, str, bool, etc.].
        :type newType: type
        :param enforceType: If true, a check will be performed to make sure that the type is valid.
        :type enforceType: bool
        :return: None
        :rtype: NoneType
        """
        if type(newType) == type:
            self._dataType = newType
            self.getProperties().getProperty("Data Type")[1].setValue(newType.__name__)
        elif not enforceType:
            self._dataType = newType
            self.getProperties().getProperty("Data Type")[1].setValue(newType)
        else:
            raise InvalidDataTypeException("setDataType()'s input parameter must specify a Python type [e.g. int, str, bool].")
        
        if self._action is not None:
            self._action.synchronizeWrappers()

    def setOptional(self, isOptional: bool) -> None:
        """
        Sets whether the Port must be connected or not.

        :param isOptional: True if the Port is optionally connected. False if it MUST be connected.
        :type isOptional: bool
        :return: None
        :rtype: NoneType
        """
        self._optional = isOptional
        self.getProperties().getProperty("Optional")[1].setValue(self._optional)
        
        if not isOptional:
            self._default = None
        
        if self._action is not None:
            self._action.synchronizeWrappers()
            
    def setDefaultValue(self, value) -> None:
        """
        Sets the default value of the port if the port is optional.
        
        :raises: PortException if the port is not optional
        
        :param value: the default value to set
        :type value: the same type as the port.
        :return: None
        :rtype: NoneType
        """
        if not self._optional:
            raise PortException("Cannot set a default value for a port that is not optional")
        
        self._default = value
        self.getProperties().getProperty("Default Value")[1].setValue(str(value))
        
        if self._action is not None:
            self._action.synchronizeWrappers()
        
    def getDefaultValue(self):
        """
        Get the default value of the port iff the port is optional
        
        :raises: PortException if the port is not optional
        
        :return: The default value
        :rtype: The same type as the port
        """
        if not self._optional:
            raise PortException("The port has no default value because it is not optional.")
        
        return self._default
        
    def setName(self, name: str) -> None:
        """
        Sets the name of the port
        
        :param name: The new name to set
        :type name: str
        :return: None
        :rtype: NoneType
        """
        Entity.setName(self, name)
        if self._action is not None:
            self._action.synchronizeWrappers()

    def isOptional(self) -> bool:
        """
        Returns True if the Port doesn't necessarily have to be connected, False if it MUST be connected.

        :return: A bool: True if the Port doesn't necessarily have to be connected, False if it MUST be connected.
        :rtype: bool
        """
        return self._optional
    
    def setAction(self, action: 'ac.Action') -> None:
        """
        Sets this port's action.
        
        .. warning:: This function should only be called from Action.addInputPort or
            Action.addOutput port. Calling this function elsewhere may result in unsynchronized
            references.
        
        :param action: The action that owns this port.
        :type action: ac.Action
        :return: None
        :rtype: NoneType
        """
        self._action = action
        
    def getAction(self) -> 'ac.Action':
        """
        Get the Action that this port belongs to.
        
        :return: This port's Action.
        :rtype: Action
        """
        return self._action
    
    def copy(self) -> 'Port':
        """
        Creates a copy of a port object and returns it.
        
        .. note:: The copy's action will not be set and no wires wil be connected.
        
        :return: A copy of the port (without wires)
        :rtype: Port
        """
        
        newPort = Port(self._dataType, self._optional)
        newPort.setName(self.getName())
        newPort.setAnnotation(self.getAnnotation())
        if self.isOptional():
            newPort.setDefaultValue(self._default)
        return newPort
    
    def mirror(self, port: 'Port') -> None:
        """
        Sets this port to look just like another one.
        
        .. note:: This port's action, inputs, and outputs will not be affected.
        
        :param port: The port to mirror
        :type port: Port
        :return: None
        :rtype: NoneType
        """
        
        self._optional = port.isOptional()
        self._dataType = port.getDataType()
        self._default = port._default
        self.setName(port.getName())

    def isValidSource(self) -> bool:
        """
        Determine whether the port is a valid source or not.
        
        :return: True if it's a valid source.
        :rtype: bool
        """
        
        if self._action is None:
            return False
        
        at = type(self._action)
        if at == ap.ActionPipeline:
            return self in self._action.getInputPorts()
        
        if at == aw.ActionWrapper:
            return self in self._action.getOutputPorts()
        
        return False

    def asDict(self) -> dict:
        """
        Get a dictionary representation of the action.

        .. note::
            This is not just a getter of the __dict__ attribute.

        :return: The dictionary representation of the object.
        :rtype: dict
        """

        portDict = {}

        portDict["id"] = self.getId()
        portDict["input"] = None
        portDict["outputs"] = None  # Wires take care of these
        portDict["optional"] = self.isOptional()
        portDict["action"] = None  # no need to store action since the action stores the port info
        portDict["default"] = self._default
        portDict["name"] = self.getName()

        try:
            portDict["data type"] = self.getDataType().__name__
        except:
            portDict["data type"] = self.getDataType

        return portDict

    @staticmethod
    def fromDict(d: dict, action: 'Action' = None) -> 'Port':
        """
        Creates a Port from the dictionary

        :param d: The dictionary that represents the Port.
        :type d: dict
        :param action: The port's parent Action
        :type action: Action
        :return: The Port object that was constructed from the dictionary
        :rtype: Port
        """
        port = Port()

        port.setOptional(d['optional'])

        if d['optional']:
            port.setDefaultValue(d['default'])

        port.setName(d['name'])

        if action:
            port.setAction(action)

        try:
            port._dataType = eval(d["data type"])
        except:
            port._dataType = d["data type"]

        return port
