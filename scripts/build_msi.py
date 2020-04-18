import os, sys

if os.path.exists("../venv/"):
    if "venv" not in sys.executable:
        print("=================================== ERROR ===================================")
        print("It appears you have a virtual environment set up, but have not activated it.")
        print("    Please activate your virtual environment before running this script.")
        print("=============================================================================")
        sys.exit(1)

os.system("python build_exe.py")
os.chdir("../")

print("building msi...", end="", flush=True)
os.system("python setup.py bdist_msi 1> build/build_msi.log 2>&1")
print("done.", flush=True)

os.chdir("../")