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
	
This module contains the **Action** class which serves as the base class to the *ComponentAction*
and *ActionPipeline* classes.
"""

from abc import ABC as AbstractBaseClass

from typecheck import typecheck

from data.apim.port import Port, PortException


class ActionException(Exception):
	def __init__(self, msg: str):
		Exception.__init__(self, msg)


class Action(AbstractBaseClass):
	
	allPorts = set()
	
	def __init__(self):
		"""
		The **Action** class is the abstract base class of both *ActionPipeline* and
		*ComponentAction*. It stores all of the common functionality of the derived classes.
		
		The Action class is responsible for managing ports. Actions can have any number of
		inputs and outputs. Each input and output is a port. A single port instance cannot be
		both an input and an output, nor can it be shared between actions.
		
		The action class maintains a set of all ports to prevent misuse of ports.
		"""
		# inputs and outputs are lists of ports.
		self.inputs = []
		self.outputs = []
		
	@typecheck
	def addInputPort(self, port: Port) -> None:
		"""
		Adds a port to the list of inputs for this action.
		
		The port may have wires connected to it when added, but it is not recommended.
		The port instance cannot be used anywhere else.
		
		:raises: PortException if the port is used elsewhere.
		
		:param port: The new port to be added.
		:type port: Port
		:return: None
		:rtype: NoneType
		"""
		if port in Action.allPorts:
			raise PortException("Port is already used. Can't add port to action.")
		
		self.inputs.append(port)
	
	@typecheck
	def addOutputPort(self, port: Port) -> None:
		"""
		Adds a port to the list of outputs for this action.
		
		The port may have wires connected to it when added, but it is not recommended.
		The port instance cannot be used anywhere else.
		
		:raises: PortException if the port is used elsewhere.
		
		:param port: The new port to be added.
		:type port: Port
		:return: None
		:rtype: NoneType
		"""
		if port in Action.allPorts:
			raise PortException("Port is already used. Can't add port to action.")
		
		self.outputs.append(port)
	
	@typecheck
	def removePort(self, port) -> bool:
		"""
		Removes a port from this action - no need to specify input or output.

		Removing the port from the action does not destroy the port. The caller should take
		special care to remove any wires if desired.

		:raises: PortException if the port is not found.

		:param port: The port instance to be removed.
		:type port: Port
		:return: True if the port was successfully removed, False otherwise.
		:rtype: bool
		"""
		
		if port not in Action.allPorts:
			raise PortException("Port not found in any actions.")
		
		found = False
		if port in self.inputs:
			found = True
			self.inputs.remove(port)
		elif port in self.outputs:
			found = True
			self.outputs.remove(port)
		else:
			raise PortException("Port not found in this action.")
			
		if found:
			Action.allPorts.remove(port)
		
		return found
