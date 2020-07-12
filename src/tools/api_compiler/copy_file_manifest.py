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

# all files are listed starting from the facile/src/ directory because that directory does not exist when installed.
necessary_source_files = [
    os.path.join("tguiil", "componentfinder.py"),
    os.path.join("tguiil", "application.py"),
    os.path.join("tguiil", "tokens.py"),
    os.path.join("tguiil", "supertokens.py"),
    os.path.join("tguiil", "matchoption.py"),
    os.path.join("data", "tguim", "component.py"),
    os.path.join("data", "tguim", "visibilitybehavior.py"),
    os.path.join("data", "tguim", "condition.py"),
    os.path.join("data", "tguim", "targetguimodel.py"),
    os.path.join("data", "properties.py"),
    os.path.join("data", "property.py"),
    os.path.join("data", "entity.py"),
    os.path.join("libs", "env.py"),
]

