
import sys
import os

# These lines allow us to import things as if we were running facile.py
sys.path.insert(0, os.path.abspath("../../../src/"))
# sys.path.insert(0, os.path.abspath("./src/gui/rc/"))

import unittest
from data.apim.actionpipeline import ActionPipeline
import data.apim.port as pt

class TestCompiler(unittest.TestCase):
	
	def test_ActionMethodSignatures(self):
		"""
		This function makes sure that the method signatures are generated
		correctly for any action with an arbitrary number of ports.
		"""
		ap = ActionPipeline()
		ap.setName("myAction")
		
		# set the input ports
		p1 = pt.Port()
		p1.setDataType(int)
		p1.setName("input1")
		p1.setOptional(False)
		ap.addInputPort(p1)
		p2 = pt.Port()
		p2.setDataType(bool)
		p2.setName("input2")
		p2.setOptional(False)
		ap.addInputPort(p2)
		
		# set the output ports
		p3 = pt.Port()
		p3.setDataType(str)
		p3.setName("output1")
		ap.addOutputPort(p3)
		
		sig = "\tdef myAction(self, input1: int, input2: bool) -> str:\n"
		self.assertTrue(ap.getMethodSignature() == sig)
		
		# TODO: Still need to handle optional parameters.
		p2.setOptional(True)
		self.assertFalse(ap.getMethodSignature() == sig)
	
	def test_ActionMethodDocStrings(self):
		ap = ActionPipeline()
		ap.setName("myAction")
		
		# set the input ports
		p1 = pt.Port()
		p1.setDataType(int)
		p1.setName("input1")
		p1.setOptional(False)
		ap.addInputPort(p1)
		p2 = pt.Port()
		p2.setDataType(bool)
		p2.setName("input2")
		p2.setOptional(False)
		ap.addInputPort(p2)
		
		# set the output ports
		p3 = pt.Port()
		p3.setDataType(str)
		p3.setName("output1")
		ap.addOutputPort(p3)
		
		doc = '''"""
		Add a comment here...

		:param input1: Add a comment here...
		:type input1: int
		:param input2: Add a comment here...
		:type input2: bool
		:return: (Add a comment here...)
		:rtype: (str)
		"""'''
		self.assertTrue(ap.getDocStr().strip() == doc)
		
		ap.setAnnotation("This is my action pipeline. Only mine.")
		doc = '''"""
		This is my action pipeline. Only mine.

		:param input1: Add a comment here...
		:type input1: int
		:param input2: Add a comment here...
		:type input2: bool
		:return: (Add a comment here...)
		:rtype: (str)
		"""'''
		self.assertTrue(ap.getDocStr().strip() == doc)
		
		ap.setName("login")
		ap.setAnnotation("Login to the Chase Desktop banking app.")
		p1.setName("username")
		p1.setDataType(str)
		p1.setOptional(False)
		p1.setAnnotation("Your username (case-sensitive)")
		p2.setName("Password")
		p2.setDataType(str)
		p2.setOptional(False)
		p2.setAnnotation("Your password (case-sensitive)")
		p3.setName("Success")
		p3.setDataType(bool)
		p3.setOptional(False)
		p3.setAnnotation("A flag saying whether the login attempt was successful or not.")
		
		doc = '''"""
		Login to the Chase Desktop banking app.

		:param username: Your username (case-sensitive)
		:type username: str
		:param Password: Your password (case-sensitive)
		:type Password: str
		:return: (A flag saying whether the login attempt was successful or not.)
		:rtype: (bool)
		"""'''
		self.assertTrue(ap.getDocStr().strip() == doc)
		
		p4 = pt.Port()
		p4.setName("numLoginAttempts")
		p4.setDataType(int)
		p4.setAnnotation("The number of login attempts it took to succeed (-1 if no success).")
		p4.setOptional(False)
		ap.addOutputPort(p4)
		doc = '''"""
		Login to the Chase Desktop banking app.

		:param username: Your username (case-sensitive)
		:type username: str
		:param Password: Your password (case-sensitive)
		:type Password: str
		:return: (A flag saying whether the login attempt was successful or not., The number of login attempts it took to succeed (-1 if no success).)
		:rtype: (bool, int)
		"""'''
		self.assertTrue(ap.getDocStr().strip() == doc)