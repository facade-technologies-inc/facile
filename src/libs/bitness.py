import os
import platform
import struct

import pywintypes
import win32api
import win32file


def isExecutable(filename: str) -> bool:
	"""
	Determines if a file is executable or not. NOTE: Windows only
	
	Adapted from this source:
	http://timgolden.me.uk/python/win32_how_do_i/tell-if-a-file-is-executable.html
	
	:param filename: the name of the file in question.
	:return: True if file is executable. False otherwise.
	"""
	
	filename = filename.replace("/", "\\")  # windows-style paths only
	if not os.path.exists(filename):
		raise FileNotFoundError("{} does not exist.".format(filename))
	
	filename = win32api.GetLongPathName(filename)
	
	try:
		r, executable = win32api.FindExecutable(filename)
		executable = win32api.GetLongPathName(executable)
	except pywintypes.error as e:
		print(e)
		return False
	else:
		if executable == filename:
			return True
		else:
			return False


def getExeBitness(exeFile: str) -> int:
	"""NOTE: For windows only
	
	Solution found at
	https://stackoverflow.com/questions/1345632/determine-if-an-executable-or-library-is-32-or-64-bits-on-windows
	"""
	
	if not isExecutable(exeFile):
		raise Exception("{} is not an executable file".format(exeFile))
	
	type = win32file.GetBinaryType(exeFile)
	if type == win32file.SCS_32BIT_BINARY:
		return 32
	else:
		return 64


def getPythonBitness() -> int:
	"""
	Solution found at:
	https://stackoverflow.com/questions/1405913/how-do-i-determine-if-my-python-shell-is-executing-in-32bit-or-64bit-mode-on-os
	"""
	return struct.calcsize("P") * 8


def getSystemBitness() -> int:
	"""
	Solution adapted from
	https://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python
	"""
	machine = platform.machine()
	if machine.endswith('64'):
		return 64
	else:
		return 32


def appBitnessMatches(exeFile: str) -> bool:
	"""
	Returns True if the executable and the currently running version of python are teh same bitness.
	"""
	return getPythonBitness() == getExeBitness(exeFile)


if __name__ == "__main__":
	# NOTE: I am running 32-bit python on a 64-bit windows 10 OS
	assert (getSystemBitness() == 64)
	assert (getPythonBitness() == 32)
	assert (getExeBitness("C:/Program Files/PuTTY/putty.exe") == 64)
	assert (getExeBitness("C:\\Program Files (x86)\\Notepad++\\notepad++.exe") == 32)
	assert (appBitnessMatches("C:\\Program Files (x86)\\Notepad++\\notepad++.exe"))
	assert (not appBitnessMatches("C:/Program Files/PuTTY/putty.exe"))
	print("SUCCESS!")
