import os
import subprocess

qrc = os.path.abspath("../icons.qrc")
out = os.path.abspath("../src/gui/rc/icons_rc.py")

print("Compiling Resource Files... ", end="")
if os.path.exists(os.path.abspath("../venv/")):
    python = os.path.abspath("../venv/Scripts/python.exe")
    rcc = os.path.abspath("../venv/Scripts/pyside2-rcc.exe")

    with open(out, 'w') as fout:
        proc = subprocess.Popen([python, rcc, qrc], stdout=fout)
        return_code = proc.wait()

else:
    with open(out, 'w') as fout:
        proc = subprocess.Popen(["pyside2-rcc", qrc], stdout=fout)
        return_code = proc.wait()

print("Done")