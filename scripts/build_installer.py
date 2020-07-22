import subprocess
import os
import sys

INNO_DIR = "C:\Program Files (x86)\Inno Setup 6"
INNO_COMPILER = os.path.join(INNO_DIR, 'Compil32.exe')
INNO_SCRIPT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'Facile_Installer_Setup_Script.iss'))


if __name__ == "__main__":

    if not os.path.exists(INNO_DIR):
        print(f"INNO Setup is not installed o is not installed in the correct location. Please install it at {INNO_DIR}")
        sys.exit(1)

    if not os.path.exists(INNO_SCRIPT):
        print(f"It appears your INNO script doesn't exist. Please make sure it exists ar {INNO_SCRIPT}")
        sys.exit(1)

    if os.path.exists("../venv/"):
        if "venv" not in sys.executable:
            print("=================================== ERROR ===================================")
            print("It appears you have a virtual environment set up, but have not activated it.")
            print("    Please activate your virtual environment before running this script.")
            print("=============================================================================")
            sys.exit(1)

    exit_code = subprocess.check_call("python build_exe.py", shell=True)

    if exit_code != 0:
        print("Executable not properly built. Cannot create an installer.")
        sys.exit(1)

    os.chdir("../")

    print("building installer...", end="", flush=True)
    exit_code = subprocess.call([INNO_COMPILER, '/cc', INNO_SCRIPT])

    if exit_code == 0:
        print("done.", flush=True)
    elif exit_code == 1:
        print("The installer command was invalid.")
    elif exit_code == 2:
        print("The installer failed to build properly.")
    else:
        print("Unkown exit code.")
    os.chdir("../")

    sys.exit(exit_code)