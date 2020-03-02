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
	
This module contains the **ComponentAction** class which is used to tie a user action to a
component from the TGUIM.
"""

from data.apim.action import Action
from data.apim.port import Port
from data.apim.actionspecification import ActionSpecification

class ComponentAction(Action):
	
	def __init__(self, targetComponent: 'Component', actionSpec: 'ActionSpecification'):
		"""
		The ComponentAction class is used to describe an action on a specific component
		
		:param targetComponent: the component to act on
		:type targetComponent: Component
		:param actionSpec: The specification for how to perform the action.
		:type actionSpec: ActionSpecification
		"""
		Action.__init__(self)
		self._target = targetComponent
		self._spec = actionSpec
		
		for input in actionSpec.inputs:
			p = Port.copy(input)
			self.addInputPort(p)
			
		for output in actionSpec.outputs:
			p = Port.copy(output)
			self.addOutputPort(p)
			
		self.setName(actionSpec.name)
		self.setAnnotation(self._spec.description)

	def getTargetComponent(self) -> 'Component':
		"""
		Returns the target componemt of the action.

		:return: Target component
		:rtype: Component
		"""

		return self._target

	def getMethodName(self) -> str:
		"""
		Gets the name of the action. *UNIQUE TO COMPONENT STORED*

		:return: Method name
		:rtype: str
		"""

		if self._target is None:
			return '_' + self.getName()  # TODO: We have to make sure that these actions have unique names
		return '_' + str(self._target.getId()) + '_' + self.getName()

	def getMethodCode(self) -> str:
		"""
		Returns the code spec

		:return: code necessary to perform action
		:rtype: str
		"""

		code = '\t\tcomp = self.findComponent(' + str(self._target.getId()) + ')\n'
		code += '\n\t\ttry:'
		code += self._spec.code.replace('\n', '\n\t\t\t')

		if self._target is None:
			code = code[:-1] + 'except:\n\t\t\tprint("The action \'' + self.getName() + '\' was not executed ' \
								'correctly. Please contact support to fix this issue.")\n\n'
		else:
			code = code[:-1] + 'except:\n\t\t\tprint("The action \'' + self.getName() + '\' was not executed ' \
							   'correctly on component with ID ' + str(self._target.getId()) + '. Please ' \
								'contact support to fix this issue.")\n\n'

		return code
