"""
This is a script that will properly build the TDP. To build the TDP correctly,
latex must compile it twice.

In the first run, the latex of each of the sub-documents is inserted directly
into the TDP. This will create an almost-correct document, but the page
numbering will be not be entirely correct. It will be drastically affected by
the title pages, tables of contents, and indecies lack of page numbers. Only the
table of contents from the first compilation will be used.

In the second run, the PDFs will be inserted for the inner documents rather than
the latex source code. This will nest the inner document inside of each page, so
we'll have double page numbers. The side effect is that the table of contents
will be completely incorrect. To fix this, we'll remove the table of contents
from this run and insert the table of contents from the first run.
"""
import re
import os
import sys
from distutils.dir_util import copy_tree

sys.path.append(os.path.abspath("../_common/"))
from documents import docnames


tdp_pdf = "19033_Technical_Data_Package.pdf"
first_run_pdf = "1st_run_" + tdp_pdf


def read(filename):
	for encoding in ["utf8", "ANSI"]:
		try:
			with open(filename, 'r', encoding=encoding) as texfile:
				print(filename)
				texcontents = texfile.read()
		except:
			continue
		else:
			return texcontents
	
	raise Exception("Could not read file")


def write(filename, contents):
	with open(filename, 'w', encoding="utf8") as texfile:
		texfile.write(contents)


################################################################################
#
#    FIRST RUN
#
################################################################################

# remove all existing build
os.system("make clean")

# make the latex source
os.system("make latex")

# copy over required resources
copy_tree("./source/include_for_latex", "./build/latex")

# read latex source
latex_source = read("./build/latex/19033_Technical_Data_Package.tex")
copy_1 = latex_source[:]

# find all document flags
doc_flags = re.findall(r"INSERT_DOC=\S*", latex_source)
start = len("INSERT_DOC=")
docs = [flag[start:] for flag in doc_flags]

# edit the latex source to include all sub-documents
run1_replacement = r"""
\renewcommand{{\sphinxmaketitle}}{{
    \newgeometry{{left=.75in,right=.75in,top=1in,bottom=1in}}
    \pagestyle{{empty}}
    \includepdf[pages=1,pagecommand={{}},width=1.2\textwidth,offset=0in 0in]{{../../../{}/build/latex/{}.pdf}}
    \restoregeometry
}}
\renewcommand{{\sphinxtableofcontents}}{{
    \newgeometry{{left=.75in,right=.75in,top=1in,bottom=1in}}
    \pagestyle{{empty}}
    \includepdf[pages=2,pagecommand={{}},width=1.2\textwidth,offset=0in 0in]{{../../../{}/build/latex/{}.pdf}}
    \restoregeometry
}}
\newpage
\import{{../../../{}/build/latex/}}{{{}}}
"""

for abbrev in docs:
	doc = docnames[abbrev]
	copy_1 = copy_1.replace("INSERT_DOC=" + abbrev, run1_replacement.format(abbrev, doc, abbrev,
	                                                                       doc, abbrev, doc))

write("./build/latex/19033_Technical_Data_Package.tex", copy_1)

# clean up for combining
os.chdir("../_common/tools")
os.system("python latex_combine_cleanup.py")
os.chdir("../../TDP")

# build PDF from latex
os.chdir("./build/latex")
os.system("make")



# Copy PDF elsewhere (save for later)
os.rename(tdp_pdf, first_run_pdf)


################################################################################
#
#    SECOND RUN
#
################################################################################

copy_2 = latex_source[:]

run2_replacement_1 = r"\includepdf[pages={2,3},pagecommand={},fitpaper=true]{" + first_run_pdf + "}"
run2_replacement_2 = r"""
\includepdf[pages=-,frame,scale=0.872,offset=0 3.5,pagecommand={{\pagestyle{{plain}}}},fitpaper=true]{{../../../{}/build/latex/{}.pdf}}
"""
copy_2 = copy_2.replace(r"\sphinxtableofcontents", run2_replacement_1)

for abbrev in docs:
	doc = docnames[abbrev]
	copy_2 = copy_2.replace("INSERT_DOC=" + abbrev, run2_replacement_2.format(abbrev, doc))
	
write("./19033_Technical_Data_Package.tex", copy_2)
	
os.system("make")

