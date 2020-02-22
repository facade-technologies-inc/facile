
import sys
import os

sys.path.insert(0, os.path.abspath("./src/"))
sys.path.insert(0, os.path.abspath("./src/gui/rc/"))

import unittest
from data.apim.componentaction import ComponentAction
from data.apim.actionpipeline import ActionPipeline
from data.apim.actionwrapper import ActionWrapper
from data.apim.action import Action, ActionException
from data.apim.port import Port, PortException
from data.apim.wire import Wire, WireException
from data.apim.wireset import WireSet

class TestCompiler(unittest.TestCase):
	
	def test_ActionMethodSignatures(self):
		"""
		This function makes sure that the method signatures are generated
		correctly for any action with an arbitrary number of ports.
		"""
		ap = ActionPipeline()
		ap.setName("myAction")
		
		# set the input ports
		p1 = Port()
		p1.setDataType(int)
		p1.setName("input1")
		p1.setOptional(False)
		ap.addInputPort(p1)
		p2 = Port()
		p2.setDataType(bool)
		p2.setName("input2")
		p2.setOptional(False)
		ap.addInputPort(p2)
		
		# set the output ports
		p3 = Port()
		p3.setDataType(str)
		p3.setName("output1")
		ap.addOutputPort(p3)
		
		self.assertTrue(ap.getMethodSignature() == "def myAction(input1:int, input2:bool) -> str:")
		
		# TODO: Add more tests here by creating more actions and ports and verifying that the
		#  signatures are generated correctly.
	
	def test_ActionMethodDocStrings(self):
		pass
		# TODO: Test the docstrings
	
	# TODO: Create more tests

		
		
		