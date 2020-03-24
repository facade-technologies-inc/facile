import os

DOC_DIR = os.path.abspath("./")

Exclude = ['ATP', 'CCL', 'ConOps', 'DataSheets', 'Drawings', 'Proposal', 'Risk', 'SCG', '']

def do_all_docs(cmd="latex"):
	# build all sub-docs
	for root, dirs, files in os.walk(DOC_DIR):
		for dir in dirs:
			item = os.path.join(DOC_DIR, dir)
			
			if "_common" in item or "TDP" in item:
				continue
				
			make_script = os.path.join(item, "make.bat")
			doc = item.strip(os.path.sep).split(os.path.sep)[-1]
			
			if os.path.exists(make_script):
				print("="*80)
				print("|     Building {} {}".format(doc, cmd))
				print("=" * 80)
				print()
				os.chdir(item)
				
				if cmd == "latex":
					os.system("make clean")
					os.system("make latex")
				elif cmd == "pdf":
					os.chdir('./build/latex')
					os.system('make')
				
			else:
				print("=" * 80)
				print("No make script found for {}".format(doc))
				print("=" * 80)
				print()
		break
	

do_all_docs("latex")

# run latex combine cleanup tool
print("\n\n/" + "-" * 79)
print("|")
print("|     Running Latex Combine Cleanup Tool")
print("|")
print("\\" + "-" * 79)
print()
os.chdir(DOC_DIR)
os.chdir("./_common/tools")
os.system("python latex_combine_cleanup.py")

do_all_docs("pdf")

# build TDP
doc="TDP"
print("="*80)
print("|     Building {}".format(doc))
print("=" * 80)
print()
os.chdir(DOC_DIR)
os.chdir("./{}".format(doc))
os.system("python build.py")

# # compile TDP latex into PDF
# doc="TDP"
# print("="*80)
# print("|     Compiling {} LaTeX into PDF".format(doc))
# print("=" * 80)
# print()
# os.chdir(DOC_DIR)
# os.chdir("./TDP/build/latex")
# os.system("make")
