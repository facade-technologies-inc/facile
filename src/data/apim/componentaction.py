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

import data.apim.port as pt
import data.apim.action as act
from data.apim.actionspecification import ActionSpecification
import data.properties as ppts


class ComponentAction(act.Action):
	
	def __init__(self, targetComponent: 'Component' = None, actionSpec: 'ActionSpecification' = None):
		"""
		The ComponentAction class is used to describe an action on a specific component
		
		:param targetComponent: the component to act on
		:type targetComponent: Component
		:param actionSpec: The specification for how to perform the action.
		:type actionSpec: ActionSpecification
		"""
		act.Action.__init__(self)
		self._target = targetComponent
		self._spec = actionSpec

		if targetComponent and actionSpec:
			self.initializeAfterLink()

	def initializeAfterLink(self) -> None:
		"""
		Once the target component and action specification have both been set, this function can be called to complete
		initialization.

		:return: None
		:rtype: NoneType
		"""
		for input in self._spec.inputs:
			p = pt.Port.copy(input)
			self.addInputPort(p)
			
		for output in self._spec.outputs:
			p = pt.Port.copy(output)
			self.addOutputPort(p)
			
		self.setName(self._spec.name)
		self.setAnnotation(self._spec.description)
	
	def getActionSpec(self) -> ActionSpecification:
		"""
		Gets the action spec associated to this item.
		
		:return: the action spec associated to this item
		:rtype: ActionSpecification
		"""
		
		return self._spec

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
				out += '\t\t:type ' + p.getName() + ': ' + p.getDataTypeStr() + '\n'
			
			# we can only have one return tag, so we just combine everything.
			if self._outputs:
				annotations = [p.getAnnotation() for p in self._outputs]
				types = [p.getDataTypeStr() for p in self._outputs]
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
		
		if self._target.getSuperToken().getTokens()[0].type not in ['Menu', 'MenuItem']:
			code = '\t\tcomp = self._findComponent(' + str(self._target.getId()) + ')\n'
		else:
			code = '\t\tcomp = self._getComponentObject(' + str(self._target.getId()) + ')\n'
		
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
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the component action.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		d = act.Action.asDict(self)
		d["target component"] = self._target.getId()
		d["action specification"] = self._spec.name
		
		return d
	
	@staticmethod
	def fromDict(d: dict, tguim: 'TargetGuiModel', actSpecs: dict) -> 'ComponentAction':
		"""
		Creates object from a dictionary.

		:param d: The dictionary that represents the object.
		:type d: dict
		:param tguim: The target GUI model to add the component to
		:type tguim: TargetGuiModel
		:param actSpecs: The dictionary of all action specifications
		:type actSpecs: dict
		:return: The ComponentAction object that was constructed from the dictionary
		:rtype: ComponentAction
		"""
		
		if d is None:
			return None
		
		target = tguim.getComponent(int(d["target component"]))
		spec = actSpecs[d["action specification"]]  # The port stuff is handled in the CA constructor
		ca = ComponentAction(target, spec)
		if d['properties']:
			ca.setProperties(ppts.Properties.fromDict(d['properties']))

		return ca
