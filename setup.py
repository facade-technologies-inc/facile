import sys
import os
from cx_Freeze import setup, Executable

sys.path.append(os.path.abspath("./src/"))
sys.path.append(os.path.abspath("./src/gui/rc/"))
sys.path.append(os.path.abspath("./database/component_actions"))

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = {
    "packages": [
                # Facile sub-packages
                 "src.gui",
                 "src.qt_models",
                 "src.data",
                 "src.libs",
                 "src.tguiil",
                 "src.graphics",

                # External dependencies
                 "distutils"
                 ],

    "includes": ["scipy.sparse.csgraph._validation",
                 "scipy.ndimage._ni_support",
                 "scipy._distributor_init",
                 ],

    "include_files": ["database/",
                      "src/tguiil/",
                      "src/data/",
                      ] + ["./venv/Scripts/"+ file for file in os.listdir("./venv/Scripts/") if file.endswith(".dll")],

    "excludes": ["scipy.spatial.cKDTree"]
}

installOptions = {}

bdistOptions = {}

base = None

# Uncomment for GUI applications to NOT show cmd window while running.
if sys.platform =='win32':
    base = 'Win32GUI'

executables = [
    Executable(script = 'src/facile.py', base=base, targetName = 'facile.exe', icon = 'resources/facade_logo_256.ico')
]

setup(name='Facile',
      version = '1.0',
      description = 'A platform for generating Python APIs used to control graphical user interfaces.',
      options = {
          "build_exe": buildOptions,
          "install_exe": installOptions,
          "bdist_msi": bdistOptions,
      },
      executables = executables)