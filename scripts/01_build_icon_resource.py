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
	
This is a simple script that produces the icon resource file used by Qt Creator.

.. warning::
	This script will overwrite the file "icons.qrc" in the facile directory
	
"""

import os

facile_dir = os.path.abspath("../")
src_dir = os.path.abspath("../src/")

icons_dir = os.path.abspath("../resources/icons")
icons_resouce_file = os.path.abspath("../icons.qrc")

wrapper = """
<RCC>
    <qresource prefix="/icon">
        {file_list}
    </qresource>
</RCC>
"""

file_list_item = """
        <file alias="{alias}">{filepath}</file>
"""


if __name__ == "__main__":
	
	file_list = ""
	for root, dirs, files in os.walk(icons_dir):
		for file in files:
			fpath = os.path.join(root, file)
			from_facile = os.path.relpath(fpath, facile_dir)
			from_src = os.path.relpath(fpath, src_dir)
			file_list += file_list_item.format(alias=from_src, filepath=from_facile)
			
	qrc_contents = wrapper.format(file_list=file_list).replace("\\", "/")
	
	with open(icons_resouce_file, "w") as icons_file:
		icons_file.write(qrc_contents)

