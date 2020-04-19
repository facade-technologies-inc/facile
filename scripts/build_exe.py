if __name__ == "__main__":
    import os, sys

    if os.path.exists("../venv/"):
        if "venv" not in sys.executable:
            print("=================================== ERROR ===================================")
            print("It appears you have a virtual environment set up, but have not activated it.")
            print("    Please activate your virtual environment before running this script.")
            print("=============================================================================")
            sys.exit(1)

    os.chdir("../")

    print("Building exe...", end="", flush=True)

    if not os.path.exists("build"):
        os.mkdir("build")
    os.system("python setup.py build 1> build/build_exe.log 2>&1")

    build_path = os.path.abspath("./build")
    exe_path = os.path.join(build_path, [item for item in os.listdir(build_path) if item.startswith("exe.")][0])
    lib_path = os.path.join(exe_path, "lib")
    multiprocessing_path = os.path.join(lib_path, "multiprocessing")

    # rename multiprocessing.Pool to multiprocessing.pool to fix imports in executable.
    os.rename(os.path.join(multiprocessing_path, "Pool.pyc"), os.path.join(multiprocessing_path, "pool.pyc"))
    print("done.", flush=True)

    os.chdir("scripts/")
