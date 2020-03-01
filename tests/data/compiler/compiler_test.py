
import sys
import os

# These lines allow us to import things as if we were running facile.py
sys.path.insert(0, os.path.abspath("../../../src/"))
sys.path.insert(0, os.path.abspath("../../../src/gui/rc/"))

import unittest
import difflib
from data.apim.actionwrapper import ActionWrapper
from data.apim.actionpipeline import ActionPipeline
from data.apim.componentaction import ComponentAction
from data.tguim.component import Component
from data.apim.actionspecification import ActionSpecification
from data.project import Project
import data.apim.port as pt
from PySide2.QtWidgets import QApplication

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

	def test_ActionPipelineCodeGeneration(self):
		"""
		This function makes sure that the code is generated
		correctly for any action pipeline.
		"""
		app = QApplication([])

		proj = Project('test', 'test project', '', 'uia')
		tguim = proj.getTargetGUIModel()

		ap = ActionPipeline()  # should have id 0
		ap2 = ActionPipeline()  # should have id 1

		ap.setName('custom1')
		ap.setAnnotation('testing the first pipeline')

		p = pt.Port()
		p.setName("value")
		p.setDataType(str)
		p.setAnnotation("Value to be written.")
		p.setOptional(False)
		ap.addInputPort(p)

		ap2.setName('custom2')
		ap2.setAnnotation('testing the second pipeline')

		p1 = pt.Port()
		p1.setName("value")
		p1.setDataType(str)
		p1.setAnnotation("Value to be written.")
		p1.setOptional(False)
		ap2.addInputPort(p1)

		comp1 = Component(tguim)  # should have id 2
		comp2 = Component(tguim)  # should have id 3
		comp3 = Component(tguim)  # should have id 4
		comp4 = Component(tguim)  # should have id 5

		spec1 = ActionSpecification.fromFile('../../../database/component_actions/click.action')
		spec2 = ActionSpecification.fromFile('../../../database/component_actions/write.action')
		spec3 = ActionSpecification.fromFile('../../../database/component_actions/read.action')

		a1 = ComponentAction(comp1, spec1) #6 and so on
		a2 = ComponentAction(comp2, spec1)
		a3 = ComponentAction(comp3, spec2)
		a4 = ComponentAction(comp4, spec3)

		aw1 = ActionWrapper(a1, ap)
		aw2 = ActionWrapper(a2, ap)
		aw3 = ActionWrapper(a3, ap)
		aw5 = ActionWrapper(ap, ap2)
		aw4 = ActionWrapper(a4, ap2)

		ap.connect(p, a3.getInputPorts()[0])
		ap2.connect(p1, p)

		method1 = '''\
	def custom1(self, value: str) -> None:
		"""
		testing the first pipeline

		:param value: Value to be written.
		:type value: str
		"""

		_6_click()
		_7_click()
		_8_write(value)

'''

		method2 = '''\
	def custom2(self, value: str) -> None:
		"""
		testing the second pipeline

		:param value: Value to be written.
		:type value: str
		"""

		custom1(value)
		a = _9_read()

'''

		print([li for li in difflib.ndiff(ap.getMethod(), method1) if li[0] != ' '])
		print(ap.getMethod())
		print([li for li in difflib.ndiff(ap2.getMethod(), method2) if li[0] != ' '])
		print(ap2.getMethod())

		self.assertTrue(ap.getMethod() == method1)
		self.assertTrue(ap2.getMethod() == method2)

	def test_ComponentActionCodeGeneration(self):
		"""
		This function makes sure that the method signatures are generated
		correctly for any action with an arbitrary number of ports.
		"""

		app = QApplication([])

		proj = Project('test', 'test project', '', 'uia')
		tguim = proj.getTargetGUIModel()

		comp1 = Component(tguim)  # should have id 0
		comp2 = Component(tguim)  # should have id 1

		spec1 = ActionSpecification.fromFile('../../../database/component_actions/click.action')
		spec2 = ActionSpecification.fromFile('../../../database/component_actions/write.action')

		a1 = ComponentAction(comp1, spec1)
		a2 = ComponentAction(comp2, spec2)

		method1 =  '''\
	def _4_click(self) -> None:
		"""
		Left-click a component.

		:return: None
		:rtype: NoneType
		"""

		comp = self.findComponent(4)

		try:
			comp.set_focus()
			comp.click()

'''
		method2 = '''\
	def _5_write(self, value: str) -> None:
		"""
		Write to a component.

		:param value: Value to be written.
		:type value: str
		:return: None
		:rtype: NoneType
		"""

		comp = self.findComponent(5)

		try:
			comp.set_edit_text(value)

'''
		print([li for li in difflib.ndiff(a1.getMethod(), method1) if li[0] != ' '])

		print([li for li in difflib.ndiff(a2.getMethod(), method2) if li[0] != ' '])

		self.assertTrue(a1.getMethod().replace(" "*4, "\t").strip() == method1.replace(" "*4, "\t").strip())
		self.assertTrue(a2.getMethod().replace(" "*4, "\t").strip() == method2.replace(" "*4, "\t").strip())
