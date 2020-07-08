import os
temp_req_file = "temp_requirements.txt"
perm_req_file = "../requirements.txt"

if __name__ == "__main__":

    # -- Get current list of installed packages. -----------------------------------------------------------------------
    os.system(f"pip freeze > {temp_req_file}")

    with open(temp_req_file) as f:
        cur_reqs = set(f.readlines())

    # -- Get list of. --------------------------------------------------------------------------------------------------
    with open(perm_req_file) as f:
        needed_reqs = set(f.readlines())

    # -- Determine which requirements we have, need to get rid of, or need to install. ---------------------------------
    unnecessary_packages = list(cur_reqs - needed_reqs)
    have_packages = cur_reqs.intersection(needed_reqs)
    needed_packages = list(needed_reqs - cur_reqs)

    # -- Uninstall unnecessary packages --------------------------------------------------------------------------------
    with open(temp_req_file, 'w') as f:
        f.writelines(unnecessary_packages)

    os.system(f"pip uninstall -y -r {temp_req_file} 1>nul 2>&1")
    os.remove(temp_req_file)

    # -- Install all required dependencies -----------------------------------------------------------------------------
    os.system(f"pip install --no-deps -r {perm_req_file} 1>nul 2>&1")

    # -- Print a report of what was done -------------------------------------------------------------------------------
    report = {
        "These are extra (we uninstalled them for you)": unnecessary_packages,
        "You have these required packages already (no action)": have_packages,
        "You need these packages (we installed them for you)": needed_packages
    }

    for x, l in report.items():
        l = '\t'.join(l).rstrip() if l != [] else None
        print("\n{x}:\n\t{l}".format(x=x, l=l))

    print() # extra whitespace to look good
