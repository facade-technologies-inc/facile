@echo off

echo Compiling Windows and Widgets...
pyside2-uic ../src/gui/ui/facileview.ui > ../src/gui/ui/ui_facileview.py
pyside2-uic ../src/gui/ui/copyprojectdialog.ui > ../src/gui/ui/ui_copyprojectdialog.py
pyside2-uic ../src/gui/ui/newprojectdialog.ui > ../src/gui/ui/ui_newprojectdialog.py
pyside2-uic ../src/gui/ui/manageprojectdialog.ui > ../src/gui/ui/ui_manageprojectdialog.py
pyside2-uic ../src/gui/ui/validatorview.ui > ../src/gui/ui/ui_validatorview.py

echo Done.

