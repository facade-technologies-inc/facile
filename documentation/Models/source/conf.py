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

sys.path.append(os.path.abspath('../../_common/extensions'))


# -- Project information -----------------------------------------------------

project = 'Models'
copyright = '2020, Facade Technologies Inc.'

author = "Facade Technologies Inc."

import sys, os
sys.path.append(os.path.abspath("../../_common/"))
from documents import releases
version = releases["SDP"]
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.todo'
]

numfig = True
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**/ui"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Set Facade Technologies Inc. logo
html_logo = "../../_common/images/Facade @0.5x.png"
html_favicon = "../../_common/images/facade_logo_favicon.ico"

# -- Options for LaTeX output -------------------------------------------------

# Set Facade Technologies Inc. logo
latex_logo = "../../_common/images/facade_logo_small.png"
latex_favicon = "../../_common/images/facade_logo_favicon.ico"

latex_show_pagerefs = True
latex_show_urls = "footnote"

latex_documents = [(
	"index",

	"19033_Models.tex",

	"Models",

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

# latex_toplevel_sectioning = 'section'

latex_elements = {
	'extraclassoptions': r'oneside',
	'preamble': r'''
		\usepackage{pdfpages}
		\usepackage{standalone}
		\usepackage{import}
		\usepackage{titletoc}
		\usepackage{fancyhdr}

		\rfoot{Proprietary - Limited Use and Access}
		\cfoot{Duplication and dissemination of these documents is prohibited \\
		without the prior written consent of Facade Technologies Inc.}
	'''

	# 	\definecolor{myblue}{rgb}{0.4, 0.4, 0.5}
	# 	\titlecontents{chapter}[ 0em ]{ \vspace{0.75em} }
	#           {Doc \, \contentslabel{.2em} \hspace{.5em}-- \hspace{.5em}}{}
	#           {\hfill \textbf{\contentspage}}[]
	# 	\titlecontents{section}[ 2em ]{  }
	#           {\hspace{3.5em} \contentslabel{2.5em}}{}
	#           {\titlerule*[0.5pc]{.}\contentspage}[]
	# ''',
}
