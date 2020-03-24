
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

class TestAction(unittest.TestCase):
	
	def test_ActionPipeline(self):
		
		# create top-level action pipeline
		readAccountBalance = ActionPipeline()
		self.assertTrue(readAccountBalance.getActions() == [])
		self.assertTrue(readAccountBalance.getInputPorts() == [])
		self.assertTrue(readAccountBalance.getOutputPorts() == [])
		
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
		self.assertTrue(readAccountBalance.getActions() == [])
		self.assertTrue(readAccountBalance.getInputPorts() == [username, pwd])
		self.assertTrue(readAccountBalance.getOutputPorts() == [accountBalance])
		
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
		self.assertTrue(login.getActions() == [])
		self.assertTrue(login.getInputPorts() == [uname, password])
		self.assertTrue(login.getOutputPorts() == [])
		
		# Create a wrapper for the sub-action pipeline
		loginWrapper = ActionWrapper(login, readAccountBalance)
		w_uname, w_password = loginWrapper.getInputPorts()
		
		self.assertTrue(type(w_uname) == Port)
		self.assertTrue(type(w_password) == Port)
		self.assertTrue(w_uname.isOptional() == uname.isOptional())
		self.assertTrue(w_uname.getDataType() == uname.getDataType())
		self.assertTrue(w_password.isOptional() == password.isOptional())
		self.assertTrue(w_password.getDataType() == password.getDataType())
		
		uname = w_uname
		password = w_password
		
		# Add sub-action pipeline to top-level action pipeline.
		#readAccountBalance.addAction(loginWrapper)
		self.assertTrue(readAccountBalance.getActions() == [loginWrapper])
		
		# Make sure we can't add a non-wrapper action to an action pipeline
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
		self.assertTrue(readAccountBalance.getWireSet().containsWire(username, uname))
		self.assertTrue(readAccountBalance.getWireSet().containsWire(pwd, password))
		
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
		self.assertTrue(readAccountBalance.getInputPorts() == [pwd])
		self.assertTrue(readAccountBalance.getOutputPorts() == [])
		self.assertTrue(username.getAction() is None)
		self.assertTrue(accountBalance.getAction() is None)
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(username))
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(accountBalance))
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(Port()))
		self.assertRaises(PortException, lambda: readAccountBalance.removePort(tempPort))
		self.assertFalse(readAccountBalance.getWireSet().containsWire(username, uname))
		login.addInputPort(username)
		login.addOutputPort(accountBalance)
		login.removePort(username)
		login.removePort(accountBalance)
		readAccountBalance.addInputPort(username)
		readAccountBalance.addOutputPort(accountBalance)
		readAccountBalance.connect(username, uname)
		self.assertTrue(readAccountBalance.getWireSet().containsWire(username, uname))
		self.assertTrue(readAccountBalance.getWireSet().containsWire(pwd, password))
		
		# change sequence of actions
		readAccountBalance.changeSequence([loginWrapper])
		self.assertRaises(ActionException, lambda: readAccountBalance.changeSequence([loginWrapper,ActionPipeline]))
		self.assertRaises(ActionException, lambda: readAccountBalance.changeSequence([loginWrapper,loginWrapper]))
		self.assertRaises(ActionException, lambda: readAccountBalance.changeSequence([]))
		
		# Make sure we can't connect/disconnect ports that we don't have access to.
		self.assertRaises(PortException, lambda: readAccountBalance.connect(username, Port()))
		self.assertRaises(PortException, lambda: readAccountBalance.connect(Port(), username))
		self.assertRaises(PortException, lambda: readAccountBalance.disconnect(username, Port()))
		self.assertRaises(PortException, lambda: readAccountBalance.disconnect(Port(), username))
		
		# make sure we can't connect the username ports backwards
		self.assertRaises(WireException, lambda: readAccountBalance.connect(uname, username))
	
		# action deletion
		self.assertRaises(ActionException, lambda: readAccountBalance.removeAction(login))
		readAccountBalance.removeAction(loginWrapper)
		self.assertFalse(readAccountBalance.getWireSet().containsWire(username, uname))
		self.assertFalse(readAccountBalance.getWireSet().containsWire(pwd, password))
		
		# Add a component action to read from the account balance field

		# TODO: Update ComponentAction constructor call
		#readField = ComponentAction(None, "This is a bullshit component action")
		readField = ActionPipeline()
		balanceStr = Port()
		readField.addOutputPort(balanceStr)
		
		readFieldWrapper = ActionWrapper(readField, readAccountBalance)
		balanceStr2, = readFieldWrapper.getOutputPorts()
		
		#readAccountBalance.addAction(readFieldWrapper)
		readAccountBalance.connect(balanceStr2, accountBalance)
		self.assertRaises(PortException, lambda: readAccountBalance.connect(balanceStr, accountBalance))
		
	def test_ComponentAction(self):
		pass
		# This test is not relevant anymore because the constructor of Component Action has been changed.
		# TODO: Update ComponentAction contructor calls.
		# ca1 = ComponentAction()
		# ca2 = ComponentAction()
		# p1 = Port()
		# ca1.addInputPort(p1)
		# self.assertRaises(PortException, lambda: ca2.removePort(p1))
		# self.assertRaises(PortException, lambda: ca2.removePort(Port()))
		
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
		
		portA.setOptional(False)
		self.assertRaises(PortException, lambda: portA.setDefaultValue(1))
		portA.setOptional(True)
		portA.setDefaultValue(1)
		
	def test_ActionWrapper(self):
		# make an action pipeline
		ap = ActionPipeline()
		p1 = Port()
		p2 = Port()
		ap.addInputPort(p1)
		ap.addOutputPort(p2)
		
		# make a wrapper for it
		parent = ActionPipeline()
		w = ActionWrapper(ap, parent)
		p1Mirror, = w.getInputPorts()
		p2Mirror, = w.getOutputPorts()
		
		self.assertTrue(p1Mirror is not p1)
		self.assertTrue(p2Mirror is not p2)
		self.assertTrue(type(p1Mirror) == Port)
		self.assertTrue(type(p2Mirror) == Port)
		self.assertTrue(p1Mirror.isOptional() == p1.isOptional())
		self.assertTrue(p1Mirror.getDataType() == p1.getDataType())
		self.assertTrue(p2Mirror.isOptional() == p2.isOptional())
		self.assertTrue(p2Mirror.getDataType() == p2.getDataType())
		
		# Add another port to the action pipeline and make sure the wrapper is updated
		ap.addInputPort(Port())
		self.assertTrue(len(ap.getInputPorts()) == len(w.getInputPorts()))
		
		ap.removePort(p1)
		self.assertTrue(len(ap.getInputPorts()) == len(w.getInputPorts()))
		
		ap.removePort(p2)
		self.assertTrue(len(ap.getInputPorts()) == len(w.getInputPorts()))
		
		self.assertRaises(ActionException, lambda: ActionPipeline().registerWrapper(w))
		self.assertRaises(ActionException, lambda: ActionPipeline().unRegisterWrapper(w))
		self.assertRaises(ActionException, lambda: ap.unRegisterWrapper(w))
		
		w.forgetActionReference()
		ap.unRegisterWrapper(w)
		
		self.assertRaises(ActionException, lambda: ActionPipeline().addAction(w))
		self.assertRaises(ActionException, lambda: parent.addAction(w))
		