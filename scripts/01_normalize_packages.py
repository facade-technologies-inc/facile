import os
import pygit2
import pip
import subprocess

temp_req_file = "temp_requirements.txt"
perm_req_file = "../requirements.txt"

# Mapping of dependencies to download and install from Facade Technologies github
# These are generally repositories that needed to be forked and modified to work with Facile.
requirements_from_source = {
    "qtmodern":              ("https://github.com/facade-technologies-inc/qtmodern.git",   "master"),
    "qnotifications":        ("https://github.com/facade-technologies-inc/QNotifications", "master"),
}


if __name__ == "__main__":

    # -- Get current list of installed packages. -----------------------------------------------------------------------
    os.system(f"pip freeze > {temp_req_file}")

    with open(temp_req_file) as f:
        cur_reqs = set(f.readlines())
    os.remove(temp_req_file)

    # -- Get list of necessary requirements ----------------------------------------------------------------------------
    with open(perm_req_file) as f:
        needed_reqs = set(f.readlines())

    # -- Determine which requirements we have, need to get rid of, or need to install. ---------------------------------
    unnecessary_packages = [p for p in cur_reqs - needed_reqs if p not in requirements_from_source]
    have_packages = cur_reqs.intersection(needed_reqs)
    needed_packages = list(needed_reqs - cur_reqs)

    # -- Uninstall unnecessary packages --------------------------------------------------------------------------------
    for package in unnecessary_packages:
        print(f"Uninstalling {package}")
        os.system(f"pip uninstall -y {package} 1>nul 2>&1")

    # -- Install all required dependencies (if not installing from source) ---------------------------------------------
    for package in needed_packages:
        stripped_package = package.replace("="," ").replace(">", " ").replace("<", " ").split()[0].lower()
        if stripped_package not in requirements_from_source:
            os.system(f"pip install --no-deps {package} 1>nul 2>&1")

    # -- Clone/Pull any dependencies which are not hosted on PyPi) -----------------------------------------------------
    for package, repo in requirements_from_source.items():
        url, branchName = repo
        repo_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../", package))

        # if the repo already exists, switch to the target branch and pull
        if os.path.exists(repo_path):
            print('')
            print(f"Pulling: {package} @ branch: {branchName}")
            repoObj = pygit2.Repository(os.path.join(repo_path, ".git"))
            branch = repoObj.lookup_branch(branchName)
            ref = repoObj.lookup_reference(branch.name)
            repoObj.checkout(ref)

            freeze_loc = os.getcwd()
            os.chdir(repo_path)
            output = subprocess.check_output(["git", "pull"])
            os.chdir(freeze_loc)

        else:
            print(f"Cloning: {package} @ branch: {branchName}")
            pygit2.clone_repository(url, repo_path, checkout_branch=branchName)

        print(f"Installing from source: {package}")
        pip.main(["install", repo_path])
        print('')

    # -- Print a report of what was done -------------------------------------------------------------------------------
    report = {
        "These are extra (we uninstalled them for you)": unnecessary_packages,
        "You have these required packages already (no action)": have_packages,
        "You need these packages (we installed them for you)": needed_packages,
        "We also pulled the following packages from github": requirements_from_source.keys()
    }

    for x, l in report.items():
        l = '\t'.join(l).rstrip() if l != [] else None
        print("\n{x}:\n\t{l}".format(x=x, l=l))

    print() # extra whitespace to look good
