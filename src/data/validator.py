# run is the most important function.
# one function for one checking algorithm and call all of them in run

# targetguimodel and aplmodel are the two things

# action is the parent object
# actionpipeline, component action and action wrapper all inherited from it
# actionpipeline could have component actions or actionpipelines in it
# action wrapper wrap around actionpipipeline or component action.
# So we only need to create one instance of an actionpipeline, but multiple wrappers refer to it.

from PySide2.QtCore import QThread, Slot, Signal

from data.apim.actionpipeline import ActionPipeline
from data.validatormessage import ValidatorMessage
from datetime import datetime
import data.statemachine as sm

class Validator(QThread):
	"""
	This Validator class run algorithms to validate user's action pipeline. It communicates with ValidatorView class with
	signal/slot and sends message to the graphical view.
	"""
	
	sentMessage = Signal(ValidatorMessage)
	updateProgress = Signal(float)
	
	def __init__(self):
		"""
		Construct the validator.
		"""
		QThread.__init__(self)
	
	def run(self):
		"""
		Run validation. Send validator message through emitting signal.
		
		:return: None
		:rtype: NoneType
		"""
		self._running = True
		
		# TODO: acquire references to TGUIM and APIM
		
		# accumulate list of algorithm method objects:
		algorithms = [getattr(self, method_name) for method_name in dir(self)
		              if callable(getattr(self, method_name)) and
		              method_name.startswith("algorithm_")]
		print(algorithms)
		
		for algoNum in range(len(algorithms)):
			algo = algorithms[algoNum]
			if not self._running:
				return
			
			self.updateProgress.emit(100 * (algoNum+1)/(len(algorithms)+1))
			algo()
			
		self.updateProgress.emit(100)
			
	def algorithm_at_least_one_actionpipeline(self):
		tempAPIModel = sm.StateMachine.instance._project.getAPIModel()
		if len(tempAPIModel.getActionPipelines()) == 0:
			message = ValidatorMessage("ERROR: There is no action pipeline existing in the project",
			                           ValidatorMessage.Level.Error)
			self.sentMessage.emit(message)
	
	# Validate if all of the input ports for all the ACTIONS inside action pipelines have incoming wires.
	def algorithm_all_actions_inports_has_wiresin(self):
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()
		for i in tempAPIPipes[:]:
			if not isinstance(i, ActionPipeline):
				tempAPIPipes.remove(i)

		for pipes in tempAPIPipes:
			for action in pipes.getActions():
				for port in action.getInputPorts():
					if port.getInputWire() is None:
						message = ValidatorMessage(
							"ERROR: There is no input wire for the input port " + port.getName() + " at action " + action.getName(),
							ValidatorMessage.Level.Error)
						self.sentMessage.emit(message)
	
	# Validate if all of the input ports for all the ACTION PIPELINES have incoming wires.
	def algorithm_apipip_inport_has_wiresin(self):
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()
		for i in tempAPIPipes[:]:
			if not isinstance(i, ActionPipeline):
				tempAPIPipes.remove(i)

		for pipes in tempAPIPipes:
			for port in pipes.getInputPorts():
				if port.getInputWire() is None:
					message = ValidatorMessage("ERROR: There is no input wire for the input port " + port.getName() +
					                           " at action pipeline " + pipes.getName(),
					                           ValidatorMessage.Level.Error)
					self.sentMessage.emit(message)

	# Validate if all of the output ports for all the ACTION PIPELINES have incoming wires.
	def algorithm_apipip_outport_has_wiresin(self):
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()
		for i in tempAPIPipes[:]:
			if not isinstance(i, ActionPipeline):
				tempAPIPipes.remove(i)
		
		for pipes in tempAPIPipes:
			for port in pipes.getOutputPorts():
				if port.getInputWire() is None:
					message = ValidatorMessage("ERROR: There is no input wire for the output port " + port.getName() +
					                           " for action pipeline " + pipes.getName(),
					                           ValidatorMessage.Level.Error)
					self.sentMessage.emit(message)
	
	# Validate if there are two or more actions having the same name.
	def algorithm_no_duplicated_action_name(self):
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()
		for i in tempAPIPipes[:]:
			if not isinstance(i, ActionPipeline):
				tempAPIPipes.remove(i)
		
		allActionNames = {}
		for pipes in tempAPIPipes:
			for action in pipes.getActions():
				if action.getName() in allActionNames:
					message = ValidatorMessage("ERROR: There is a duplicated name '" + action.getName() +
					                           "' for action " + action.getName(),
					                           ValidatorMessage.Level.Error)
					self.sentMessage.emit(message)
				else:
					allActionNames.add(action.getName())
	
	

	@Slot()
	def stop(self):
		"""
		Stop validator.
		
		:return: None
		:rtype: NoneType
		"""
		self._running = False



# def algorithm_01_test_INFO(self):
# 	for i in range(100):
# 		if not self._running:
# 			return
# 		now = datetime.now()
# 		message = ValidatorMessage("INFO: test Message" + str(now), ValidatorMessage.Level.Info)
# 		self.sentMessage.emit(message)
#
# def algorithm_02_test_WARNING(self):
# 	for i in range(100):
# 		if not self._running:
# 			return
# 		now = datetime.now()
# 		message = ValidatorMessage("WARNING: test Message" + str(now), ValidatorMessage.Level.Warning)
# 		self.sentMessage.emit(message)
#
# def algorithm_03_test_ERROR(self):
# 	for i in range(100):
# 		if not self._running:
# 			return
# 		now = datetime.now()
# 		message = ValidatorMessage("ERROR: test Message" + str(now), ValidatorMessage.Level.Error)
# 		self.sentMessage.emit(message)