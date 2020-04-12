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
from data.apim.actionspecification import ActionSpecification
import data.apim.port as pt

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
			p = pt.Port.copy(input)
			self.addInputPort(p)
			
		for output in actionSpec.outputs:
			p = pt.Port.copy(output)
			self.addOutputPort(p)
			
		self.setName(actionSpec.name)
		self.setAnnotation(self._spec.description)

	def getTargetComponent(self) -> 'Component':
		"""
		Returns the target component of the action.

		:return: Target component
		:rtype: Component
		"""

		return self._target
	
	def getDocStr(self) -> str:
		"""
		Generates the docstring for the action. Adds the necessary spacing after docstring.
		If the function has no inputs or outputs, the docstring states this.

		:return: doc string describing action, inputs, and outputs
		:rtype: str
		"""
		
		out = '\t\t"""\n'
		noDoc = True
		
		if self.getAnnotation():
			noDoc = False
			out += '\t\t' + self.getAnnotation().replace('{id}', str(self._target.getId())) + '\n\n'
		
		if self._inputs or self._outputs:
			noDoc = False
			
			for p in self._inputs:
				out += '\t\t:param ' + p.getName() + ': ' + p.getAnnotation() + '\n'
				out += '\t\t:type ' + p.getName() + ': ' + p.getDataType().__name__ + '\n'
			
			# we can only have one return tag, so we just combine everything.
			if self._outputs:
				annotations = [p.getAnnotation() for p in self._outputs]
				types = [p.getDataType().__name__ for p in self._outputs]
				out += '\t\t:return: ({})\n'.format(", ".join(annotations))
				out += '\t\t:rtype: ({})\n'.format(", ".join(types))
			else:
				out += '\t\t:return: None\n'
				out += '\t\t:rtype: NoneType\n'
		else:
			out += '\t\t:return: None\n'
			out += '\t\t:rtype: NoneType\n'
		
		if noDoc:
			return '\t\t"""\n\t\tThis action has no annotations, inputs, or outputs.\n\t\t"""\n'
		else:
			out += '\t\t"""\n\n'
			return out

	def getMethodName(self) -> str:
		"""
		Gets the name of the action. *UNIQUE TO COMPONENT STORED*

		:return: Method name
		:rtype: str
		"""

		if self._target is None:
			return '_' + self.getName().replace(' ', '_')  # TODO: We have to make sure that these actions have unique names
		return '_' + str(self._target.getId()) + '_' + self.getName().replace(' ', '_')

	def getMethodCode(self) -> str:
		"""
		Returns the code spec

		:return: code necessary to perform action
		:rtype: str
		"""
		
		if self._target.getSuperToken().getTokens90[0].type not in ['Menu', 'MenuItem']:
			code = '\t\tcomp = self.findComponent(' + str(self._target.getId()) + ')\n'
		else:
			code = '\t\tcomp = self.getComponentObject(' + str(self._target.getId()) + ')\n'
		
		code += '\n\t\ttry:'
		code += self._spec.code.replace('\n', '\n\t\t\t')

		if self._target is None:
			code = code[:-1] + 'except Exception as e:\n\t\t\tprint(e)\n\t\t\traise ActionException("The action \'' \
			       + self.getName() + '\' was not executed correctly. Please contact support for help.")\n'
		else:
			code = code[:-1] + 'except Exception as e:\n\t\t\tprint(e)\n\t\t\traise ActionException("The action \'' \
			       + self.getName() + '\' was not executed correctly on component with ID ' + str(self._target.getId()) \
			       + '. Please contact support for help.")\n'

		return code
