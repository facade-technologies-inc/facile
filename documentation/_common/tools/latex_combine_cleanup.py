
import os, glob
import sys
import re
sys.path.append(os.path.abspath("../../_common/"))
from documents import order

DOC_DIR = os.path.abspath("../../")


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



for root, dirs, files in os.walk(DOC_DIR):
	for dir in dirs:
		item = os.path.join(DOC_DIR, dir)
		
		if "_common" in item:
			continue
		
		curdoc = os.path.abspath(os.path.join(item, 'build/latex'))
		
		make_script = os.path.join(item, "make.bat")
		docname = item.strip(os.path.sep).split(os.path.sep)[-1]
		
		if os.path.exists(make_script):
			
			for file in os.listdir(curdoc):
				file = os.path.abspath(os.path.join(curdoc, file))
				if file.endswith(".tex"):
					texcontents = read(file)
					
					if docname == "TDP":
						texcontents = texcontents.replace(r"\sphinxtableofcontents",
						                                  r"\tableofcontents")
						
					else:
						o = r"\newcommand{\sphinxlogo}{\sphinxincludegraphics{facade_logo_small.png}\par}"
						n = r"\providecommand{\sphinxlogo}{\sphinxincludegraphics{facade_logo_small.png}\par}"
						n += r"\renewcommand{\sphinxlogo}{\sphinxincludegraphics{facade_logo_small.png}\par}"
						
						obegin = r"\begin{document}"
						nbegin = obegin + r"\setcounter{chapter}{" + str(
							order.index(docname) + 2) + "}"
						
						texcontents = r"\begingroup" + texcontents.replace(o, n) + r"\endgroup"
						texcontents = texcontents.replace(obegin, nbegin)
						
						
						
					texcontents = texcontents.replace(r"\makeindex", "")
					texcontents = texcontents.replace(r"\printindex", "")
					
					texcontents = re.sub(r"\\begin{sphinxtheindex}[\s\S]*\\end{sphinxtheindex}", "", texcontents)
						
					write(file, texcontents)
	break
