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

import json

from typing import Dict
from data.apim.port import Port

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
	def fromDict(aS: Dict) -> 'ActionSpecification':
		newAS = ActionSpecification()
		newAS.name = aS['name']
		newAS.description = aS['description']
		newAS.viableTargets = [eval(target) for target in aS['targets']]
		newAS.inputs = [Port.fromDict(p) for p in aS['inputs']]
		newAS.outputs = [Port.fromDict(p) for p in aS['outputs']]
		newAS.code = aS['code']
		
	def toDict(self) -> Dict:
		d = {}
		d['name'] = self.name
		d['description'] = self.description
		d['targets'] = self.viableTargets
		d['inputs'] = [p.toDict() for p in self.inputs]
		d['outputs'] = [p.toDict() for p in self.outputs]
		d['code'] = self.code
		
		return d
		
if __name__ == "__main__":
	aS = ActionSpecification()
	aS.name = "click"
	aS.description = "Click a button."
	aS.viableTargets = ['Button', 'ComboBox', 'MenuItem', 'Menu', 'Edit']
	aS.inputs = []
	aS.outputs = []
	aS.code = """
	comp.click()
	"""
	
	print(json.dumps(aS.toDict(), indent=4))
	
	