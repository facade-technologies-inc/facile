import os

qrc = os.path.abspath("../icons.qrc")
out = os.path.abspath("../src/gui/rc/icons_rc.py")

print("Compiling Resource Files... ", end="")
if os.path.exists(os.path.abspath("../venv/")):
    python = os.path.abspath("../venv/Scripts/python.exe")
    rcc = os.path.abspath("../venv/Scripts/pyside2-rcc.exe")

    os.system('"{}" "{}" "{}" > "{}"'.format(python, rcc, qrc, out))

else:
    os.system('pyside2-rcc "{}" > "{}"'.format(qrc, out))
print("Done")