
import sys
import os

sys.path.insert(0, os.path.abspath("./src/"))
sys.path.insert(0, os.path.abspath("./src/gui/rc/"))

import unittest
from data.apim.componentaction import ComponentAction
from data.apim.actionpipeline import ActionPipeline
from data.apim.action import Action, ActionException
from data.apim.port import Port, PortException
from data.apim.wire import Wire, WireException
from data.apim.wireset import WireSet

class TestAction(unittest.TestCase):
	
	def test_ActionPipeline(self):
		
		# create top-level action pipeline
		readAccountBalance = ActionPipeline()
		self.assertTrue(readAccountBalance.actions == [])
		self.assertTrue(readAccountBalance.inputs == [])
		self.assertTrue(readAccountBalance.outputs == [])
		
		# create ports and add them to the top-level action pipeline
		username = Port()
		username.setOptional(False)
		username.setDataType(str)
		self.assertFalse(username.isOptional())
		self.assertTrue(username.getDataType() == str)
		pwd = Port()
		pwd.setOptional(False)
		pwd.setDataType(str)
		self.assertFalse(pwd.isOptional())
		self.assertTrue(pwd.getDataType() == str)
		accountBalance = Port()
		readAccountBalance.addInputPort(username)
		readAccountBalance.addInputPort(pwd)
		readAccountBalance.addOutputPort(accountBalance)
		self.assertTrue(readAccountBalance.actions == [])
		self.assertTrue(readAccountBalance.inputs == [username, pwd])
		self.assertTrue(readAccountBalance.outputs == [accountBalance])
		
		# create another action pipeline that won't be a child of the top-level
		temp = ActionPipeline()
		tempPort = Port()
		temp.addInputPort(tempPort)
		
		# Create a sub-action pipeline with ports
		login = ActionPipeline()
		uname = Port()
		password = Port()
		login.addInputPort(uname)
		login.addInputPort(password)
		self.assertTrue(login.actions == [])
		self.assertTrue(login.inputs == [uname, password])
		self.assertTrue(login.outputs == [])
		
		# Add sub-action pipeline to top-level action pipeline.
		readAccountBalance.addAction(login)
		self.assertTrue(readAccountBalance.actions == [login])
		
		# Make sure we can't add the same action again
		self.assertRaises(ActionException, lambda: readAccountBalance.addAction(login))
		
		# make sure we can't add the uname port again
		self.assertRaises(PortException, lambda: login.addInputPort(uname))
		self.assertRaises(PortException, lambda: login.addOutputPort(uname))
		self.assertRaises(PortException, lambda: readAccountBalance.addInputPort(uname))
		self.assertRaises(PortException, lambda: readAccountBalance.addOutputPort(uname))
		self.assertRaises(PortException, lambda: ActionPipeline().addInputPort(uname))
		self.assertRaises(PortException, lambda: ActionPipeline().addOutputPort(uname))
		
		# connect wires
		readAccountBalance.connect(username, uname)
		readAccountBalance.connect(pwd, password)
		
		# make sure wires exist
		self.assertTrue(readAccountBalance.wireSet.containsWire(username, uname))
		self.assertTrue(readAccountBalance.wireSet.containsWire(pwd, password))
		
		# make sure that you can't connect the wires again.
		self.assertRaises(PortException, lambda: readAccountBalance.connect(username, uname))
		self.assertRaises(PortException, lambda: readAccountBalance.connect(pwd, uname))
		
		# disconnect the username wire
		readAccountBalance.disconnect(username, uname)
		self.assertRaises(WireException, lambda: readAccountBalance.disconnect(username, uname))
		
		# remove the ports from the top-level action, add them to the sub-action, then move them
		# back.
		readAccountBalance.removePort(username)
		readAccountBalance.removePort(accountBalance)
		self.assertTrue(readAccountBalance.inputs == [pwd])
		self.assertTrue(readAccountBalance.outputs == [])
		self.assertTrue(username.action is None)
		self.assertTrue(accountBalance.action is None)
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(username))
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(accountBalance))
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(Port()))
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(tempPort))
		self.assertFalse(readAccountBalance.wireSet.containsWire(username, uname))
		login.addInputPort(username)
		login.addOutputPort(accountBalance)
		login.removePort(username)
		login.removePort(accountBalance)
		readAccountBalance.addInputPort(username)
		readAccountBalance.addOutputPort(accountBalance)
		readAccountBalance.connect(username, uname)
		self.assertTrue(readAccountBalance.wireSet.containsWire(username, uname))
		self.assertTrue(readAccountBalance.wireSet.containsWire(pwd, password))
		
		# change sequence of actions
		readAccountBalance.changeSequence([login])
		self.assertRaises(ActionException, lambda: readAccountBalance.changeSequence([login,ActionPipeline]))
		self.assertRaises(ActionException, lambda: readAccountBalance.changeSequence([login,login]))
		self.assertRaises(ActionException, lambda: readAccountBalance.changeSequence([]))
		
		# Make sure we can't connect/disconnect ports that we don't have access to.
		self.assertRaises(PortException, lambda: readAccountBalance.connect(username, Port()))
		self.assertRaises(PortException, lambda: readAccountBalance.connect(Port(), username))
		self.assertRaises(PortException, lambda: readAccountBalance.disconnect(username, Port()))
		self.assertRaises(PortException, lambda: readAccountBalance.disconnect(Port(), username))
		
		# make sure we can't connect the username ports backwards
		self.assertRaises(WireException, lambda: readAccountBalance.connect(uname, username))
	
		# action deletion
		self.assertRaises(ActionException, lambda: readAccountBalance.removeAction(ActionPipeline()))
		readAccountBalance.removeAction(login)
		self.assertFalse(readAccountBalance.wireSet.containsWire(username, uname))
		self.assertFalse(readAccountBalance.wireSet.containsWire(pwd, password))
		
		# Add a component action to read from the account balance field
		readField = ComponentAction(None, "This is a bullshit component action")
		balanceStr = Port()
		readField.addOutputPort(balanceStr)
		readAccountBalance.addAction(readField)
		readAccountBalance.connect(balanceStr, accountBalance)
		
	def test_ComponentAction(self):
		ca1 = ComponentAction()
		ca2 = ComponentAction()
		p1 = Port()
		ca1.addInputPort(p1)
		self.assertRaises(PortException, lambda: ca2.removePort(p1))
		self.assertRaises(PortException, lambda: ca2.removePort(Port()))
		
	def test_WireSet(self):
		myWireSet = WireSet()
		portA = Port(dataType=int)
		portB = Port()
		portC = Port()
		
		# Make some wires.
		myWireSet.addWire(portA, portB)
		myWireSet.addWire(portA, portC)
		wires1 = myWireSet.getWires()
		
		self.assertTrue(portA.getInputWire() is None)
		self.assertTrue(portC.getOutputWires() == [])
		self.assertTrue(portA.getOutputWires()[0].getDestPort() == portB)
		self.assertTrue(portA.getOutputWires()[1].getDestPort() == portC)
		
		# make sure that duplicates can't be added
		myWireSet.addWire(portA, portB)
		wires2 = myWireSet.getWires()
		self.assertTrue(wires1 == wires2)
		
		# delete port A and make sure all wires are deleted.
		myWireSet.deleteWiresConnectedToPort(portA)
		self.assertTrue(myWireSet.getWires() == [])
		self.assertTrue(portA.getInputWire() is None)
		self.assertTrue(portB.getInputWire() is None)
		self.assertTrue(portC.getInputWire() is None)
		self.assertTrue(portA.getOutputWires() == [])
		self.assertTrue(portB.getOutputWires() == [])
		self.assertTrue(portC.getOutputWires() == [])
		
		# make sure we can't force two wires into one port
		myWireSet.addWire(portA, portB)
		self.assertRaises(PortException, lambda: myWireSet.addWire(portC, portB))
		self.assertTrue(myWireSet.containsWire(portA, portB))
		self.assertFalse(myWireSet.containsWire(portB, portC))
		
		# chain ports together and delete the middle one.
		myWireSet.addWire(portA, portB)
		myWireSet.addWire(portB, portC)
		myWireSet.deleteWiresConnectedToPort(portB)
		self.assertTrue(myWireSet.getWires() == [])
		self.assertTrue(portA.getInputWire() is None)
		self.assertTrue(portB.getInputWire() is None)
		self.assertTrue(portC.getInputWire() is None)
		self.assertTrue(portA.getOutputWires() == [])
		self.assertTrue(portB.getOutputWires() == [])
		self.assertTrue(portC.getOutputWires() == [])
		
	def test_Port(self):
		myWireSet = WireSet()
		portA = Port(dataType=int)
		portB = Port()
		portC = Port()
		
		# Make some wires.
		myWireSet.addWire(portA, portB)
		myWireSet.addWire(portA, portC)
		wires = myWireSet.getWires()
		
		AtoB = wires[0]
		portA.addOutputWire(AtoB)
		
		self.assertRaises(TypeError, lambda: portB.setDataType("not a type"))