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

This module contains the Wire class.
"""
import data.apim.port as pt


class WireException(Exception):
    def __init__(self, msg):
        Exception.__init__(msg)

class Wire:
    """
    The Wire class defines a data connection between two Actions inside of an ActionPipeline. (An Action
    may be dependant upon data that is output from another Action.)
    A Wire object consists of a reference to the source Action's desired output Port, and a reference
    to the destination Action's input Port.
    """
    def __init__(self, sourcePort: 'pt.Port', destinationPort: 'pt.Port'):
        """
        Constructs a Wire object.

        :param sourcePort: An output Port from the source Action (the Action that data is flowing from).
        :type sourcePort: Port
        :param destinationPort: An input Port from the destination Action - (the Action that data is flowing to.)
        :type destinationPort: Port
        """
        self._src: 'Port' = sourcePort;
        self._dest: 'Port' = destinationPort;

    def getSourcePort(self) -> 'pt.Port':
        """
        Returns the output Port of the source Action (the Action outputting data) connected to the wire.

        :return: The output Port of the source Action.
        :rtype: Port
        """
        return self._src

    def getDestPort(self) -> 'pt.Port':
        """
        Returns the input Port of the destination Action (the Action receiving data) connected to the wire.

        :return: The input Port of the destination Action.
        :rtype: Port
        """
        return self._dest

    ''' These Two functions probably aren't necessary, and might cause issues if someone were to change the 
        wire's ports without changing the port's wire references. For now, the syncing of references is handled
        by the WireSet class.
    def setSourcePort(self, newSourcePort: 'pt.Port') -> None:
        """
        Sets the Port connected to the input of the wire.

        :param newSourcePort: The desired output Port of the Action that is to be connected to the input of the wire.
        :type newSourcePort: Port
        :return: None
        :rtype: NoneType
        """
        self._src = newSourcePort


    def setDestPort(self, newDestPort: 'pt.Port') -> None:
        """
        Sets the Port connected to the output of the wire.

        :param newDestPort: The desired input Port of the Action that is to be connected to the output of the wire.
        :type newDestPort: Port
        :return: None
        :rtype: NoneType
        """
        self._dest = newDestPort
    '''

    def asTuple(self) -> tuple:
        """
        Returns the source port and destination port as a tuple. Useful for quickly comparing wires when checking
        for duplicates.

        :return: A tuple with the format: (source_port, destination_port)
        :rtype: tuple
        """

        return (self._src, self._dest)