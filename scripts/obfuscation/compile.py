
import os
from os.path import join, abspath
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from src.tools.api_compiler.copy_file_manifest import compilation_copy_files

# THIS IS FOR OBFUSCATING ALL FILES INDEPENDENTLY
#
# facileDir = abspath('..')
# srcDir = abspath(join(facileDir, 'src'))
#
# ext_modules = []
#
# # Setting the files to compile
# for importLocation, filePath in compilation_copy_files:
#     path = join(srcDir, filePath)
#     ext_modules.append(Extension(importLocation, [path]))
#
# # Setting the files to compile
# for importLocation, filePath in compilation_copy_files:
#     path = join(srcDir, filePath)
#     ext_modules.append(Extension(importLocation, [path]))

tmpDir = abspath('tmp')

ext_modules = [Extension('apicore', [join(tmpDir, 'apicore.pyx')])]

# Explicitly define Python 3 to avoid issues
for e in ext_modules:
    e.cython_directives = {'language_level': "3"}

setup(
    name='API Core Files',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
