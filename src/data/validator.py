# inherited from QThread
# Look at observer, blinker, explorer. Mainly blinker because it's straight-forward

# run is the most important function.
# one function for one checking algorithm and call all of them in run

# targetguimodel and aplmodel are the two things
# integrate validator in to the facile

#first step: get the validator to send out some kind of message. Emit a signal with a message and get it printed out. 
import threading

from PySide2.QtCore import QThread, Slot, Signal
from data.validatormessage import ValidatorMessage

from datetime import datetime
import time


class Validator(QThread):
	"""
	This Validator class run algorithms to validate user's action pipline. It communicates with ValidatorView class with
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
	
	def algorithm_01_test_INFO(self):
		for i in range(100):
			if not self._running:
				return
			now = datetime.now()
			message = ValidatorMessage("INFO: test Message" + str(now), ValidatorMessage.Level.Info)
			self.sentMessage.emit(message)
		
	def algorithm_02_test_WARNING(self):
		for i in range(100):
			if not self._running:
				return
			now = datetime.now()
			message = ValidatorMessage("WARNING: test Message" + str(now), ValidatorMessage.Level.Warning)
			self.sentMessage.emit(message)
		
	def algorithm_03_test_ERROR(self):
		for i in range(100):
			if not self._running:
				return
			now = datetime.now()
			message = ValidatorMessage("ERROR: test Message" + str(now), ValidatorMessage.Level.Error)
			self.sentMessage.emit(message)
			
		
			
		
	


	@Slot()
	def stop(self):
		"""
		Stop validator.
		
		:return: None
		:rtype: NoneType
		"""
		self._running = False