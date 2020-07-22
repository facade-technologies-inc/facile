import os
from subprocess import check_call, DEVNULL, STDOUT
import shutil
from src.tools.api_compiler.copy_file_manifest import compilation_copy_files

if __name__ == '__main__':

    if os.path.exists("build/"):
        print("Removing old build directory...", end='')
        shutil.rmtree("build/")
        print(" Done.")

    # THIS IS FOR CREATING A SINGLE API CORE FILE

    print("Copying source files to temporary directory and removing all comments...", end='')
    srcDir = os.path.abspath(os.path.join('..', '..', 'src'))
    dstDir = os.path.abspath('tmp')
    thisDir = os.path.abspath('.')

    if os.path.exists(dstDir):
        shutil.rmtree(dstDir)
    os.mkdir(dstDir)

    os.chdir('tmp')
    folders = ['data', os.path.join('data', 'tguim'), 'libs', 'tguiil']
    for folder in folders:
        os.mkdir(folder)

    os.chdir('..')
    for tmp, path in compilation_copy_files:
        if path.endswith('baseapplication.py'):
            newPath = 'baseapplication.py'
        else:
            newPath = path
        check_call(f'pyminifier "{os.path.join(srcDir, path)}" > "{os.path.join(dstDir, newPath)}"', shell=True)

    # Copy apicore.pyx into tmp dir
    shutil.copyfile(os.path.join(thisDir, 'apicore.pyx'), os.path.join(dstDir, 'apicore.pyx'))
    print(' Done.')

    print("Compiling API Core File...", end='')
    # comment out stdout=...etc for debugging
    check_call('python compile.py build_ext', shell=True)  # , stdout=DEVNULL, stderr=STDOUT)
    print(' Done.')

    print("Moving file into compiled dir...", end='')
    buildDir = os.path.abspath('build')
    libPath = [os.path.join(buildDir, d) for d in os.listdir(buildDir) if d.startswith('lib.')][0]
    compDir = os.path.abspath('compiled')

    if os.path.exists(compDir):
        shutil.rmtree(compDir)
    os.mkdir(compDir)

    shutil.copyfile(os.path.join(libPath, os.listdir(libPath)[0]),  os.path.join(compDir, 'apicore.pyd'))
    print(' Done.')

    # Cleanup
    print("Cleaning up files... ", end='')
    shutil.rmtree("build")
    shutil.rmtree('tmp')
    print(" Done.")

    # THIS IS FOR OBFUSCATING ALL FILES INDEPENDENTLY (but this file and compile.py should be in scripts/ to work)
    #
    # print("Compiling all files...", end='')
    # check_call('python compile.py build_ext', shell=True)  # , stdout=DEVNULL, stderr=STDOUT)
    # print(' Done.')
    #
    # print("Creating API Core file...", end='')
    # buildDir = os.path.abspath('build')
    # libPath = [os.path.join(buildDir, d) for d in os.listdir(buildDir) if d.startswith('lib.')][0]
    # apiFilesDir = os.path.abspath('apifiles')
    #
    # if os.path.exists(apiFilesDir):
    #     shutil.rmtree(apiFilesDir)
    #
    # shutil.copytree(libPath, apiFilesDir)
    #
    # with open(os.path.join(apiFilesDir, 'apicore.pyx'), 'w+') as f:
    #     for path, dirs, files in os.walk(apiFilesDir):
    #         for file in files:
    #             if file.endswith('apicore.pyx'):
    #                 continue
    #
    #             newName = os.path.join(path, file.split('.')[0] + '.pyd')
    #             os.rename(os.path.join(path, file), newName)
    #             f.write(f'include "{newName.split("apifiles")[-1][1:]}"\n')
    #
    # print(' Done.')
    #
    # # Cleanup
    # print("Cleaning up files... ", end='')
    #
    # os.chdir('../src')
    # for tmp, filePath in compilation_copy_files:
    #     cfile = filePath[:-2] + 'c'
    #     if os.path.exists(cfile):
    #         os.remove(cfile)
    #
    # os.chdir('../scripts')
    # shutil.rmtree("build/")
    #
    # print('Done.')
