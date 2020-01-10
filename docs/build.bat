echo off

echo Removing previously created build logs
pushd logs
del /S /Q *.*
popd
rd /S /Q logs

mkdir logs

echo Removing all document builds
call make clean > ./logs/clean_log.txt 2>&1

echo Building HTML documentation
call make html > ./logs/html_build_log.txt 2>&1

echo Building LaTeX documentation
call make latex > ./logs/latex_build_log.txt 2>&1

pushd build
pushd latex
echo Converting LaTeX source into PDF document
call make > ../../logs/pdf_build_log.txt 2>&1
popd
popd
