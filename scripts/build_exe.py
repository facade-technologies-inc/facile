import shutil

if __name__ == "__main__":
    import os, sys

    if os.path.exists("../venv/"):
        if "venv" not in sys.executable:
            print("=================================== ERROR ===================================")
            print("It appears you have a virtual environment set up, but have not activated it.")
            print("    Please activate your virtual environment before running this script.")
            print("=============================================================================")
            sys.exit(1)

    os.chdir("obfuscation/")

    exit_code = os.system("python obfuscate_files.py")

    os.chdir('..')

    if exit_code != 0:
        print("File compilation was unsuccessful, which will cause exe building to fail.")
        sys.exit(1)

    os.chdir("../")

    if os.path.exists("build/"):
        print("Removing old build directory...", end='')
        shutil.rmtree("build/")
        print(" Done.")

    print("Building exe...", end="", flush=True)

    if not os.path.exists("build"):
        os.mkdir("build")
    os.system("python setup.py build 1> build/build_exe.log 2>&1")

    definitely_failed = True
    for item in os.listdir("build"):
        if os.path.isdir(os.path.realpath(os.path.join("./build", item))) and item.startswith("exe."):
            definitely_failed = False

    with open(os.path.join("build", "build_exe.log")) as f:
        if "Traceback (most recent call last):" in f.read():
            definitely_failed = True

    if definitely_failed:
        print("\nBuilding definitely failed. Check build_exe.log")
        sys.exit(1)

    build_path = os.path.abspath("./build")
    exe_path = os.path.join(build_path, [item for item in os.listdir(build_path) if item.startswith("exe.")][0])
    lib_path = os.path.join(exe_path, "lib")
    multiprocessing_path = os.path.join(lib_path, "multiprocessing")

    # rename multiprocessing.Pool to multiprocessing.pool to fix imports in executable.
    os.rename(os.path.join(multiprocessing_path, "Pool.pyc"), os.path.join(multiprocessing_path, "pool.pyc"))
    print("done.", flush=True)

    buildDir = os.path.abspath(os.path.join('.', 'build'))
    oldName = [os.path.join(buildDir, d) for d in os.listdir(buildDir) if os.path.isdir(os.path.join(buildDir, d))][0]
    os.rename(oldName, os.path.join(buildDir, 'exe'))

    # Removing the compiled directory now that it has been copied by setup.py
    # NOTE: Must be changed if trying to compile independent files
    os.chdir(os.path.join("scripts", 'obfuscation'))
    shutil.rmtree('compiled')

    # Setting current directory back to scripts
    os.chdir('..')
