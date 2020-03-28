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
		
		spec = ActionSpecification()
		spec.name = name
		spec.description = description
		spec.code = code
		
		if not targets:
			spec.viableTargets = None
		else:
			spec.viableTargets = targets
		
		for input in inputs:
			p = pt.Port()
			p.setName(input["name"])
			p.setDataType(input["type"])
			p.setAnnotation(input["description"])
			p.setOptional(input.get("optional", False))
			spec.inputs.append(p)
		
		for output in outputs:
			p = pt.Port()
			p.setName(output["name"])
			p.setDataType(output["type"])
			p.setAnnotation(output["description"])
			spec.outputs.append(p)
			
		return spec
	
if __name__ == "__main__":
	file = "../../../database/component_actions/click.action"
	aS = ActionSpecification.fromFile(file)
	
	print(aS.name)
	print(aS.description)
	print(aS.viableTargets)
	print(aS.inputs)
	print(aS.outputs)
	print(aS.code)