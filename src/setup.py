import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
	base = "Win32GUI"

build_exe_options = {"packages": ["os", "gui", "qt_models", "data", "libs",
					"tguiil", "graphics"], "excludes": ["tkinter"],}

setup(
	name = "Facile",
	version = "0.4",
	#options = {'build_exe': build_exe_options},
	executables = [Executable("facile.py", base=base, icon="facade_logo.ico")]
)

def find_data_file(filename):
	
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)