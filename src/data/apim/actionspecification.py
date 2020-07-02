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
	
This module contains the ActionSpecification class.
"""

import os, sys
sys.path.append(os.path.abspath("../../"))

import data.apim.port as pt


class ActionSpecificationException(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)


class ActionSpecification:
	"""
	The ActionSpecification class is used to represent an action that can be performed.
	"""
	
	def __init__(self):
		self.name = ""
		self.description = ""
		self.viableTargets = []
		self.inputs = []
		self.outputs = []
		self.code = ""
	
	def asDict(self) -> dict:
		"""
		Get a dictionary representation of the component action.

		:return: The dictionary representation of the object.
		:rtype: dict
		"""
		d = {}
		d["name"] = self.name
		d["description"] = self.description
		d["targets"] = self.viableTargets
		d["inputs"] = [port.asDict() for port in self.inputs]
		d["outputs"] = [port.asDict() for port in self.outputs]
		d["code"] = self.code
		
		return d
	
	@staticmethod
	def fromDict(d: dict) -> 'ActionSpecification':
		"""
		Creates object from a dictionary.

		:param d: The dictionary that represents the object.
		:type d: dict
		:return: The ActionSpecification object that was constructed from the dictionary
		:rtype: ActionSpecification
		"""
		
		if d is None:
			return None
		
		actS = ActionSpecification()
		actS.name = d["name"]
		actS.description = d["description"]

		actS.viableTargets = d["viableTargets"]
		for inPDict in d["inputs"]:
			actS.inputs.append(pt.Port.fromDict(inPDict))
		for outPDict in d["outputs"]:
			actS.outputs.append(pt.Port.fromDict(outPDict))

		actS.code = d["code"]

		if d["targets"]:
			actS.viableTargets = d["targets"]
		else:
			actS.viableTargets = None

		for inputDict in d["inputs"]:
			p = pt.Port.fromDict(inputDict)
			actS.inputs.append(p)

		for outputDict in d["outputs"]:
			p = pt.Port.fromDict(outputDict)
			actS.outputs.append(p)
		
		return actS
	
	@staticmethod
	def fromFile(specFile: "str") -> 'ActionSpecification':
		with open(specFile, 'r+') as f:
			specContents = f.read()
		
		name = None
		description = None
		targets = None
		inputs = None
		outputs = None
		code = None
		
		globals = {
			#"__builtins__" : None
		}
		
		locals = {
			'name': name,
			'description': description,
			'targets': targets,
			'inputs': inputs,
			'outputs': outputs,
			'code': code
		}
		
		exec(compile(specContents, specFile, 'exec'), globals, locals)
		
		name = locals['name']
		description = locals['description']
		targets = locals['targets']
		inputs = locals['inputs']
		outputs = locals['outputs']
		code = locals['code']
		
		try:
			assert(name != None)
			assert(description != None)
			assert(targets != None)
			assert(inputs != None)
			assert(outputs != None)
			assert(code != None)
		except:
			raise ActionSpecificationException("Required variable not set in specification!")

		return ActionSpecification.fromDict(locals)
	
if __name__ == "__main__":
	file = "../../../database/component_actions/click.action"
	aS = ActionSpecification.fromFile(file)
	
	print(aS.name)
	print(aS.description)
	print(aS.viableTargets)
	print(aS.inputs)
	print(aS.outputs)
	print(aS.code)