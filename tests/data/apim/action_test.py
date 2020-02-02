
import sys
import os

sys.path.insert(0, os.path.abspath("./src/"))

import unittest

from data.apim.actionpipeline import ActionPipeline
from data.apim.port import Port

class TestAction(unittest.TestCase):
	def test_empty_ActionPipeline(self):
		ap = ActionPipeline()
		
		self.assertTrue(ap.actions == [])
		self.assertTrue(ap.inputs == [])
		self.assertTrue(ap.outputs == [])
	
	def test_input_ports_ActionPipeline(self):
		login = ActionPipeline()
		email = Port(login)
		password = Port(login)
		login.addInputPort(email)
		login.addInputPort(password)
		
		self.assertTrue(login.actions == [])
		self.assertTrue(login.inputs == [email, password])
		self.assertTrue(login.outputs == [])

	def test_output_ports_ActionPipeline(self):
		readAccountBalance = ActionPipeline()
		
		self.assertTrue(readAccountBalance.actions == [])
		self.assertTrue(readAccountBalance.inputs == [])
		self.assertTrue(readAccountBalance.outputs == [])
		
		username = Port(readAccountBalance)
		pwd = Port(readAccountBalance)
		accountBalance = Port(readAccountBalance)
		readAccountBalance.addInputPort(username)
		readAccountBalance.addInputPort(pwd)
		readAccountBalance.addOutputPort(accountBalance)
		
		self.assertTrue(readAccountBalance.actions == [])
		self.assertTrue(readAccountBalance.inputs == [username, pwd])
		self.assertTrue(readAccountBalance.outputs == [accountBalance])
		
		login = ActionPipeline()
		uname = Port(login)
		password = Port(login)
		login.addInputPort(uname)
		login.addInputPort(password)
		readAccountBalance.addAction(login)
		
		self.assertTrue(login.actions == [])
		self.assertTrue(login.inputs == [uname, password])
		self.assertTrue(login.outputs == [])
		
		self.assertTrue(readAccountBalance.actions == [login])
		
		readAccountBalance.connect(username, uname)
		readAccountBalance.connect(pwd, password)
		