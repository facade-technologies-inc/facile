import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
	base = "Win32GUI"

build_exe_options = {"packages": ["facile"]}

setup(
	name = "Facile",
	version = "1.0",
	options = {'build_exe': build_exe_options},
	executables = [Executable("facile.py", base=base, icon="facade_logo.ico")]
)