import os

scripts = [
    "01_build_icon_resource.py",
    "02_build_rc.py",
    "03_build_ui.py",
]

for script in scripts:
    if script.endswith(".py"):
        os.system("python {}".format(script))
    else:
        os.system(script)