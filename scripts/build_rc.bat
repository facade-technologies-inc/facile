@echo off

echo Compiling Resource Files...
pyside2-rcc ../icons.qrc > ../src/gui/rc/icons_rc.py

echo Done.