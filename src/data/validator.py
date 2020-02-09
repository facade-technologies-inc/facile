# inherited from QThread
# Look at observer, blinker, explorer. Mainly blinker because it's straight-forward

# run is the most important function.
# one function for one checking algorithm and call all of them in run

# targetguimodel and aplmodel are the two things
# integrate validator in to the facile

#first step: get the validator to send out some kind of message. Emit a signal with a message and get it printed out. 
import threading

from PySide2.QtCore import QThread, Slot

class Validator(QThread):
	
	def __init__(self):
		QThread.__init__(self)
	
	@Slot()
	def run(self):
		print(threading.get_ident())
		print('run')
		# while True:
		# 	pass
	
	@Slot()
	def stop(self):
		print('stop')
		self.quit()
		
		if self.isRunning():
			print("still running")
		else:
			print("stopped running")
	
	