@echo off

echo Compiling Windows and Widgets...
pyside2-uic ../src/gui/ui/facileview.ui > ../src/gui/ui/ui_facileview.py
pyside2-uic ../src/gui/ui/copyprojectdialog.ui > ../src/gui/ui/ui_copyprojectdialog.py
pyside2-uic ../src/gui/ui/newprojectdialog.ui > ../src/gui/ui/ui_newprojectdialog.py
pyside2-uic ../src/gui/ui/manageprojectdialog.ui > ../src/gui/ui/ui_manageprojectdialog.py
pyside2-uic ../src/gui/ui/blackboxeditordialog.ui > ../src/gui/ui/ui_blackboxeditordialog.py
pyside2-uic ../src/gui/ui/porteditorwidget.ui > ../src/gui/ui/ui_porteditorwidget.py
pyside2-uic ../src/gui/ui/actionmenu.ui > ../src/gui/ui/ui_actionmenu.py
pyside2-uic ../src/gui/ui/actionmenuitem.ui > ../src/gui/ui/ui_actionmenuitem.py

echo Done.

