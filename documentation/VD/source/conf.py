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
sys.path.insert(0, os.path.abspath('../../../src/data/apim'))
sys.path.insert(0, os.path.abspath('../../../src/data/tguim'))
sys.path.insert(0, os.path.abspath('../../../src/data'))
sys.path.insert(0, os.path.abspath('../../../src/graphics/apim'))
sys.path.insert(0, os.path.abspath('../../../src/graphics/tguim'))
sys.path.insert(0, os.path.abspath('../../../src/graphics'))
sys.path.insert(0, os.path.abspath('../../../src/gui/ui'))
sys.path.insert(0, os.path.abspath('../../../src/gui'))
sys.path.insert(0, os.path.abspath('../../../src/libs'))
sys.path.insert(0, os.path.abspath('../../../src/qt_models'))
sys.path.insert(0, os.path.abspath('../../../src/tguiil'))
sys.path.insert(0, os.path.abspath('../../../src/'))

sys.path.append(os.path.abspath('../../_common/extensions'))


# -- Project information -----------------------------------------------------

project = 'Facile Verification Document'
copyright = '2020, Facade Technologies Inc.'

author = "Facade Technologies Inc."

import sys, os
sys.path.append(os.path.abspath("../../_common/"))
from documents import releases
version = releases["VD"]
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'ext_test_procedure',
	'sphinx.ext.todo',
	'ext_numfig'
]

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**/ui"]

# -- Options for numfig ------------------------------------------------------
numfig_number_figures = True
numfig_figure_caption_prefix = "Figure"

# # -- Options for HTML output -------------------------------------------------
#
# # The theme to use for HTML and HTML Help pages.  See the documentation for
# # a list of builtin themes.
# #
# html_theme = 'sphinx_rtd_theme'
#
# # Add any paths that contain custom static files (such as style sheets) here,
# # relative to this directory. They are copied after the builtin static files,
# # so a file named "default.css" will overwrite the builtin "default.css".
# # html_static_path = ['_static']
#
# # Set Facade Technologies Inc. logo
# html_logo = "../../_common/images/Facade @0.5x.png"
# html_favicon = "../../_common/images/facade_logo_favicon.ico"
#
# # -- Options for LaTeX output -------------------------------------------------

# Set Facade Technologies Inc. logo
latex_logo = "../../_common/images/facade_logo_small.png"
latex_favicon = "../../_common/images/facade_logo_favicon.ico"

latex_show_pagerefs = True
latex_show_urls = "footnote"

latex_documents = [(
	"index",

	"19033_Facile_Verification_Document.tex",

	"Facile Verification Document",

	"\\textbf{Team 19033:} \\\\"
	"Andrew Kirima \\\\ "
	"Jiuru Chen \\\\ "
	"Nikhith Vankireddy \\\\ "
	"Philippe Cutillas \\\\ "
	"Sam Badger \\\\ "
	"Sean Farris",

	"manual",

	"False"
)]

latex_toplevel_sectioning = 'chapter'

latex_elements = {
	'extraclassoptions': 'openany,oneside'
}