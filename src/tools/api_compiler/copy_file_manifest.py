"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This file contains a list of files that need to be copied into generated APIs.
The list is also used to determine which files need to be included in the installer so that
the files are available to be copied into the generated APIs.
"""

import os

# List of files that will be processed during the API compilation process. This does not include templated files.
compilation_copy_files = [
    ("tguiil.componentfinder",          os.path.join("tguiil", "componentfinder.py")),
    ("tguiil.application",              os.path.join("tguiil", "application.py")),
    ("tguiil.tokens",                   os.path.join("tguiil", "tokens.py")),
    ("tguiil.supertokens",              os.path.join("tguiil", "supertokens.py")),
    ("tguiil.matchoption",              os.path.join("tguiil", "matchoption.py")),
    ("data.tguim.component",            os.path.join("data", "tguim", "component.py")),
    ("data.tguim.visibilitybehavior",   os.path.join("data", "tguim", "visibilitybehavior.py")),
    ("data.tguim.condition",            os.path.join("data", "tguim", "condition.py")),
    ("data.tguim.targetguimodel",       os.path.join("data", "tguim", "targetguimodel.py")),
    ("data.properties",                 os.path.join("data", "properties.py")),
    ("data.property",                   os.path.join("data", "property.py")),
    ("data.entity",                     os.path.join("data", "entity.py")),
    ("libs.env",                        os.path.join("libs", "env.py")),
    ("baseapplication",                 os.path.join("tools", "api_compiler", "baseapplication.py"))
]

# List of other files that are necessary for compilation, but will NOT be directly copied during the compilation process.
#
# This list must contain tuples specifying the current location of the file and where the file will be copied to
# relative to the facile.exe file.
#
# NOTE: This list will only be used by the setup.py file, so the current working directory will be facile/
additional_files_for_compilation = [
    (f"{os.path.abspath('./src/tools/api_compiler/setup-template.txt')}", "tools/api_compiler/setup-template.txt"),
    (f"{os.path.abspath('./src/tools/api_compiler/__init__template.txt')}", "tools/api_compiler/__init__template.txt"),
    (f"{os.path.abspath('./src/tools/api_compiler/application-template.py')}", "tools/api_compiler/application-template.py"),
    (f"{os.path.abspath('./src/tools/api_compiler/automate-template.txt')}", "tools/api_compiler/automate-template.txt"),
    (f"{os.path.abspath('./src/tools/api_compiler/run-script-template.bat')}", "tools/api_compiler/run-script-template.bat"),
    (f"{os.path.abspath('./src/tools/api_compiler/api_requirements.txt')}", "tools/api_compiler/api_requirements.txt"),
    (f"{os.path.abspath('./src/tools/doc_generator/sphinx_src/')}", "sphinx_src/"),
]

# THIS IS FOR OBFUSCATING ALL FILES INDEPENDENTLY
#
# necessary_files_for_installation = [
#     (os.path.abspath(os.path.join("scripts", "apifiles", f + 'd')), f + 'd')
#     for tmp, f in compilation_copy_files
#                                    ] + additional_files_for_compilation

necessary_files_for_installation = additional_files_for_compilation + \
   [(os.path.abspath(os.path.join("scripts", "obfuscation", 'compiled', 'apicore.pyd')), 'apicore.pyd')]
