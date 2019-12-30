# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../src/data/apim'))
sys.path.insert(0, os.path.abspath('../../src/data/tguim'))
sys.path.insert(0, os.path.abspath('../../src/data'))
sys.path.insert(0, os.path.abspath('../../src/graphics/apim'))
sys.path.insert(0, os.path.abspath('../../src/graphics/tguim'))
sys.path.insert(0, os.path.abspath('../../src/graphics'))
sys.path.insert(0, os.path.abspath('../../src/gui/ui'))
sys.path.insert(0, os.path.abspath('../../src/gui'))
sys.path.insert(0, os.path.abspath('../../src/libs'))
sys.path.insert(0, os.path.abspath('../../src/qt_models'))
sys.path.insert(0, os.path.abspath('../../src/tguiil'))
sys.path.insert(0, os.path.abspath('../../src/'))


# -- Project information -----------------------------------------------------

project = 'Facile'
copyright = '2019, Facade Technologies Inc.'
author = 'Facade Technologies Inc.'
version = "0.2.0"
release = "0.2.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'autoapi.extension'
]

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**/ui"]

# -- Options for AutoAPI -----------------------------------------------------
autoapi_add_toctree_entry = True
autoapi_type = "python"
autoapi_dirs = ['../../src']
autoapi_template_dir = "templates"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Set Facade Technologies Inc. logo
html_logo = "Facade @0.5x.png"
html_favicon = "facade_logo_favicon.ico"

# -- Options for LaTeX output -------------------------------------------------

# Set Facade Technologies Inc. logo
latex_logo = "facade_logo_small.png"
latex_favicon = "facade_logo_favicon.ico"

# latex_engine = 'xelatex'
# latex_elements = {
#     'fontpkg':
#         r'''
#         \setmainfont{DejaVu Serif}
#         \setsansfont{DejaVu Sans}
#         \setmonofont{DejaVu Sans Mono}
#         ''',
#     'preamble':
#         r'''
#         \usepackage[titles]{tocloft}
#         \cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
#         \setlength{\cftchapnumwidth}{0.75cm}
#         \setlength{\cftsecindent}{\cftchapnumwidth}
#         \setlength{\cftsecnumwidth}{1.25cm}
#         ''',
#     'fncychap':
#         r'''
#         \usepackage[Bjornstrup]{fncychap}
#         ''',
#     'printindex':
#         r'''
#         \footnotesize\raggedright\printindex
#         ''',
# }
# latex_show_urls = 'footnote'