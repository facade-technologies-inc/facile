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
        Exception.__init__(self, msg)

class Wire:
    """
    The Wire class defines a data connection between two Actions inside of an ActionPipeline. (An Action
    may be dependant upon data that is output from another Action.)
    A Wire object consists of a reference to the source Action's desired output Port, and a reference
    to the destination Action's input Port.
    
    .. note:: Wires are *immutable* meaning they cannot be changed once they've been created.
        Rather than changing the source or destination of a wire, the wire should be deleted and a
        new one should be created.
    
    .. warning:: Although this class provides methods to make port/wire connections, this should
        only be performed from the WireSet class. Using methods that establish wire connections
        should be used carefully to ensure that references between ports and wires maintain
        synchronized.
    """
    def __init__(self, sourcePort: 'pt.Port', destinationPort: 'pt.Port'):
        """
        Constructs a Wire object.

        :param sourcePort: An output Port from the source Action (the Action that data is flowing from).
        :type sourcePort: Port
        :param destinationPort: An input Port from the destination Action - (the Action that data is flowing to.)
        :type destinationPort: Port
        """
        self._src: 'pt.Port' = sourcePort
        self._dest: 'pt.Port' = destinationPort

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

    def asTuple(self) -> tuple:
        """
        Returns the source port and destination port as a tuple. Useful for quickly comparing wires when checking
        for duplicates.

        :return: A tuple with the format: (source_port, destination_port)
        :rtype: tuple
        """

        return (self._src, self._dest)