import sys
import os
from cx_Freeze import setup, Executable
from src.tools.api_compiler.copy_file_manifest import necessary_source_files


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
                 "src.tools",
                 ],

    "includes": ["scipy.sparse.csgraph._validation",
                 "scipy.ndimage._ni_support",
                 "scipy._distributor_init",
                 ],

    "include_files": [
        "database/",
        (f"{os.path.abspath('./src/tools/api_compiler/baseapplication.py')}", "tools/api_compiler/baseapplication.py"),
        (f"{os.path.abspath('./src/tools/api_compiler/setup-template.txt')}", "tools/api_compiler/setup-template.txt"),
        (f"{os.path.abspath('./src/tools/api_compiler/__init__template.txt')}", "tools/api_compiler/__init__template.txt"),
        (f"{os.path.abspath('./src/tools/api_compiler/application-template.py')}", "tools/api_compiler/application-template.py"),
        (f"{os.path.abspath('./src/tools/api_compiler/automate-template.txt')}", "tools/api_compiler/automate-template.txt"),
        (f"{os.path.abspath('./src/tools/api_compiler/run-script.bat')}", "tools/api_compiler/run-script.bat"),
        (f"{os.path.abspath('./src/tools/doc_generator/sphinx_src/')}", "sphinx_src/"),
    ] + [(os.path.abspath(os.path.join("src", sf)), sf) for sf in necessary_source_files],

    "excludes": ["scipy.spatial.cKDTree"]
}


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
          "build_exe": buildOptions
      },
      executables = executables)