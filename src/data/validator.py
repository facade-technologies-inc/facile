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
		
		for algoNum in range(len(algorithms)):
			algo = algorithms[algoNum]
			if not self._running:
				return
			
			self.updateProgress.emit(100 * (algoNum+1)/(len(algorithms)+1))
			algo()
			
		self.updateProgress.emit(100)

	def algorithm_at_least_one_actionpipeline(self):
		"""
		Validate if there is at least one action pipeline. If not, send out error messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIModel = sm.StateMachine.instance._project.getAPIModel()
		if len(tempAPIModel.getActionPipelines()) == 0:
			message = ValidatorMessage("ERROR: There is no action pipeline existing in the project",
			                           ValidatorMessage.Level.Error)
			self.sentMessage.emit(message)
	
	def algorithm_all_actions_inports_has_wiresin(self):
		"""
		Validate if all of the required input ports for all the ACTIONS inside action pipelines have incoming wires.
		If not, send out error messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()

		for pipe in tempAPIPipes:
			for action in pipe.getActions():
				for port in action.getInputPorts():
					if port.getInputWire() is None and not port.isOptional():
						message = ValidatorMessage(
							"ERROR: There is no input wire for the input port " + port.getName() + " at action " + action.getName(),
							ValidatorMessage.Level.Error)
						self.sentMessage.emit(message)
	
	# def algorithm_all_actionpips_inport_has_wiresin(self):
	# 	"""
	# 	Validate if all of the input ports for all the ACTION PIPELINES have incoming wires. If not, send out error messages.
	#
	# 	:return: None
	# 	:rtype: NoneType
	# 	"""
	# 	tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()
	#
	# 	for pipe in tempAPIPipes:
	# 		for port in pipe.getInputPorts():
	# 			if port.getInputWire() is None:
	# 				message = ValidatorMessage("ERROR: There is no input wire for the input port " + port.getName() +
	# 				                           " at action pipeline " + pipe.getName(),
	# 				                           ValidatorMessage.Level.Error)
	# 				self.sentMessage.emit(message)

	def algorithm_all_actionpips_outport_has_wiresin(self):
		"""
		Validate if all of the output ports for all the ACTION PIPELINES have incoming wires. If not, send out error messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()
		
		for pipe in tempAPIPipes:
			for port in pipe.getOutputPorts():
				if port.getInputWire() is None:
					message = ValidatorMessage("ERROR: There is no input wire for the output port " + port.getName() +
					                           " for action pipeline " + pipe.getName(),
					                           ValidatorMessage.Level.Error)
					self.sentMessage.emit(message)
	
	def algorithm_no_duplicated_action_name(self):
		"""
		Validate if there are two or more actions having the same name. If so, send out error messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()

		allActionNames = set()
		for pipe in tempAPIPipes:
			for action in pipe.getActions():
				if action.getName() in allActionNames:
					message = ValidatorMessage("ERROR: There is a duplicated name '" + action.getName() +
					                           "' for action " + action.getName(),
					                           ValidatorMessage.Level.Error)
					self.sentMessage.emit(message)
				else:
					allActionNames.add(action.getName())
	

	def algorithm_all_actionpips_inport_wiresout(self):
		"""
		Validate if all input ports for all ACTION PIPELINES having outgoing wires. If not, send out warning messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()

		for pipe in tempAPIPipes:
			for port in pipe.getInputPorts():
				if len(port.getOutputWires()) == 0:
					message = ValidatorMessage("WARNING: There is no output wire for the input port " + port.getName() +
					                           " at action pipeline " + pipe.getName(),
					                           ValidatorMessage.Level.Warning)
					self.sentMessage.emit(message)
	
	def algorithm_action_names_are_python_identifiers(self):
		"""
		Validate if all action names are valid python identifiers. If not, send out warning messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()

		for pipe in tempAPIPipes:
			for action in pipe.getActions():
				if not action.getName().isidentifier():
					message = ValidatorMessage("WARNING: The action name " + action.getName() + " is not python valid identifier",
					                           ValidatorMessage.Level.Warning)
					self.sentMessage.emit(message)
	
	def algorithm_wire_not_connect_to_previous_action(self):
		"""
		Validate if wire connect an action to a previous action. If so, send out an error message.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()

		for pipe in tempAPIPipes:
			for wire in pipe.getWireSet().getWires():
				srcAction = wire.getSourcePort().getAction()
				dstAction = wire.getDestPort().getAction()
				actions = pipe.getActions()

				if srcAction is pipe or dstAction is pipe:
					continue

				destActionIndex = actions.index(srcAction)
				currActionIndex = actions.index(dstAction)
				if destActionIndex < currActionIndex:
					message = ValidatorMessage(
						"Wrong Sequence from action " + srcAction.getName() + " to action "
						+ dstAction.getName()
						+ " . Cannot connect an action from later in the sequence of execution to a previous one.",
						ValidatorMessage.Level.Error)
					self.sentMessage.emit(message)
							
	def algorithm_connected_ports_should_have_same_dataType(self):
		"""
		Validate if two connected ports have same data type. If not, send out warning messages.
		
		:return: None
		:rtype: NoneType
		"""
		tempAPIPipes = sm.StateMachine.instance._project.getAPIModel().getActionPipelines()

		for pipe in tempAPIPipes:
			for wire in pipe.getWireSet().getWires():
				dataTypeSrc = wire.getSourcePort().getDataType()
				dataTypeDest = wire.getDestPort().getDataType()
				if dataTypeSrc is not dataTypeDest:
					message = ValidatorMessage("WARNING: The source port " + wire.getSourcePort().getName()
					                           + " and the destination port " + wire.getDestPort().getName()
					                           + " do not have the same data type.",
					                           ValidatorMessage.Level.Warning)
					self.sentMessage.emit(message)
					
	
	# TODO: what if I put actionpipeline inside of actionpipeline. Do more manual testing on it.
		
	
	@Slot()
	def stop(self):
		"""
		Stop validator.
		
		:return: None
		:rtype: NoneType
		"""
		self._running = False