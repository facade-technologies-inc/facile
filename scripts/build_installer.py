import subprocess

INNO_DIR = "C:\Program Files (x86)\Inno Setup 6"

if __name__ == "__main__":
    import os, sys

    if os.path.exists("../venv/"):
        if "venv" not in sys.executable:
            print("=================================== ERROR ===================================")
            print("It appears you have a virtual environment set up, but have not activated it.")
            print("    Please activate your virtual environment before running this script.")
            print("=============================================================================")
            sys.exit(1)

    exit_code = os.system("python build_exe.py")

    if exit_code != 0:
        print("Executable not properly built. Cannot create an installer.")
        sys.exit(1)

    os.chdir("../")

    print("building installer...", end="", flush=True)
    iscc = os.path.abspath(os.path.join(INNO_DIR, 'Compil32.exe'))
    iss = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Facile_Installer_Setup_Script.iss'))
    exit_code = subprocess.call([iscc, '/cc', iss])

    if exit_code == 0:
        print("done.", flush=True)
    elif exit_code == 1:
        print("The installer command was invalid.")
    elif exit_code == 2:
        print("The executable failed to build properly.")
    else:
        print("Unkown exit code.")
    os.chdir("../")

    sys.exit(exit_code)