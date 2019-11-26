# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'facileview.ui',
# licensing of 'facileview.ui' applies.
#
# Created: Sat Nov 23 05:43:19 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(872, 634)
		MainWindow.setUnifiedTitleAndToolBarOnMac(True)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.viewSplitter = QtWidgets.QSplitter(self.centralwidget)
		self.viewSplitter.setOrientation(QtCore.Qt.Horizontal)
		self.viewSplitter.setObjectName("viewSplitter")
		self.tempView = QtWidgets.QGraphicsView(self.viewSplitter)
		self.tempView.setObjectName("tempView")
		self.horizontalLayout.addWidget(self.viewSplitter)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 872, 19))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.menuNew_Project = QtWidgets.QMenu(self.menuFile)
		self.menuNew_Project.setObjectName("menuNew_Project")
		self.menuRecent_Projects = QtWidgets.QMenu(self.menuFile)
		self.menuRecent_Projects.setObjectName("menuRecent_Projects")
		self.menuWindow = QtWidgets.QMenu(self.menubar)
		self.menuWindow.setObjectName("menuWindow")
		self.menuHelp = QtWidgets.QMenu(self.menubar)
		self.menuHelp.setObjectName("menuHelp")
		self.menuView = QtWidgets.QMenu(self.menubar)
		self.menuView.setObjectName("menuView")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
		self.dockWidget_2.setObjectName("dockWidget_2")
		self.dockWidgetContents_2 = QtWidgets.QWidget()
		self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
		self.verticalLayout.setObjectName("verticalLayout")
		self.projectExplorerView = QtWidgets.QTreeView(self.dockWidgetContents_2)
		self.projectExplorerView.setObjectName("projectExplorerView")
		self.verticalLayout.addWidget(self.projectExplorerView)
		self.dockWidget_2.setWidget(self.dockWidgetContents_2)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)
		self.dockWidget_4 = QtWidgets.QDockWidget(MainWindow)
		self.dockWidget_4.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
		self.dockWidget_4.setObjectName("dockWidget_4")
		self.dockWidgetContents_4 = QtWidgets.QWidget()
		self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.validatorView = QtWidgets.QListView(self.dockWidgetContents_4)
		self.validatorView.setObjectName("validatorView")
		self.verticalLayout_3.addWidget(self.validatorView)
		self.dockWidget_4.setWidget(self.dockWidgetContents_4)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_4)
		self.dockWidget_5 = QtWidgets.QDockWidget(MainWindow)
		self.dockWidget_5.setObjectName("dockWidget_5")
		self.dockWidgetContents_5 = QtWidgets.QWidget()
		self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_5)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.propertyEditorView = QtWidgets.QTreeView(self.dockWidgetContents_5)
		self.propertyEditorView.setObjectName("propertyEditorView")
		self.verticalLayout_2.addWidget(self.propertyEditorView)
		self.dockWidget_5.setWidget(self.dockWidgetContents_5)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_5)
		self.dockWidget_6 = QtWidgets.QDockWidget(MainWindow)
		self.dockWidget_6.setObjectName("dockWidget_6")
		self.dockWidgetContents_6 = QtWidgets.QWidget()
		self.dockWidgetContents_6.setObjectName("dockWidgetContents_6")
		self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dockWidgetContents_6)
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.modulesView = QtWidgets.QTreeWidget(self.dockWidgetContents_6)
		self.modulesView.setObjectName("modulesView")
		self.verticalLayout_4.addWidget(self.modulesView)
		self.dockWidget_6.setWidget(self.dockWidgetContents_6)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_6)
		self.toolBar = QtWidgets.QToolBar(MainWindow)
		self.toolBar.setObjectName("toolBar")
		MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		self.actionOpen_Project = QtWidgets.QAction(MainWindow)
		self.actionOpen_Project.setObjectName("actionOpen_Project")
		self.actionSave_Project = QtWidgets.QAction(MainWindow)
		self.actionSave_Project.setObjectName("actionSave_Project")
		self.actionSave_as = QtWidgets.QAction(MainWindow)
		self.actionSave_as.setObjectName("actionSave_as")
		self.actionFrom_Scratch = QtWidgets.QAction(MainWindow)
		self.actionFrom_Scratch.setObjectName("actionFrom_Scratch")
		self.actionFrom_Existing_Project = QtWidgets.QAction(MainWindow)
		self.actionFrom_Existing_Project.setObjectName("actionFrom_Existing_Project")
		self.actionProject_Tree = QtWidgets.QAction(MainWindow)
		self.actionProject_Tree.setObjectName("actionProject_Tree")
		self.actionProperty_Editor = QtWidgets.QAction(MainWindow)
		self.actionProperty_Editor.setObjectName("actionProperty_Editor")
		self.actionTarget_GUI_Model = QtWidgets.QAction(MainWindow)
		self.actionTarget_GUI_Model.setObjectName("actionTarget_GUI_Model")
		self.actionAPI_Builder = QtWidgets.QAction(MainWindow)
		self.actionAPI_Builder.setObjectName("actionAPI_Builder")
		self.actionValidator = QtWidgets.QAction(MainWindow)
		self.actionValidator.setObjectName("actionValidator")
		self.actionShow_Behaviors = QtWidgets.QAction(MainWindow)
		self.actionShow_Behaviors.setCheckable(True)
		self.actionShow_Behaviors.setObjectName("actionShow_Behaviors")
		self.actionDetailed_View = QtWidgets.QAction(MainWindow)
		self.actionDetailed_View.setCheckable(True)
		self.actionDetailed_View.setObjectName("actionDetailed_View")
		self.actionAutoExplore = QtWidgets.QAction(MainWindow)
		self.actionAutoExplore.setCheckable(True)
		self.actionAutoExplore.setObjectName("actionAutoExplore")
		self.actionManualExplore = QtWidgets.QAction(MainWindow)
		self.actionManualExplore.setCheckable(True)
		self.actionManualExplore.setObjectName("actionManualExplore")
		self.actionAPI_Modules = QtWidgets.QAction(MainWindow)
		self.actionAPI_Modules.setObjectName("actionAPI_Modules")
		self.actionManage_Project = QtWidgets.QAction(MainWindow)
		self.actionManage_Project.setObjectName("actionManage_Project")
		self.actionAdd_Behavior = QtWidgets.QAction(MainWindow)
		self.actionAdd_Behavior.setObjectName("actionAdd_Behavior")
		self.actionStart_App = QtWidgets.QAction(MainWindow)
		self.actionStart_App.setObjectName("actionStart_App")
		self.actionStop_App = QtWidgets.QAction(MainWindow)
		self.actionStop_App.setObjectName("actionStop_App")
		self.menuNew_Project.addAction(self.actionFrom_Scratch)
		self.menuNew_Project.addAction(self.actionFrom_Existing_Project)
		self.menuFile.addAction(self.menuNew_Project.menuAction())
		self.menuFile.addAction(self.actionOpen_Project)
		self.menuFile.addAction(self.menuRecent_Projects.menuAction())
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionSave_Project)
		self.menuFile.addAction(self.actionSave_as)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionManage_Project)
		self.menuWindow.addAction(self.actionProject_Tree)
		self.menuWindow.addAction(self.actionProperty_Editor)
		self.menuWindow.addAction(self.actionTarget_GUI_Model)
		self.menuWindow.addAction(self.actionAPI_Builder)
		self.menuWindow.addAction(self.actionAPI_Modules)
		self.menuWindow.addAction(self.actionValidator)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuView.menuAction())
		self.menubar.addAction(self.menuWindow.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())
		self.toolBar.addAction(self.actionStart_App)
		self.toolBar.addAction(self.actionStop_App)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionAutoExplore)
		self.toolBar.addAction(self.actionManualExplore)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionDetailed_View)
		self.toolBar.addAction(self.actionShow_Behaviors)
		self.toolBar.addAction(self.actionAdd_Behavior)
		self.toolBar.addSeparator()
		
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
	
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(
			QtWidgets.QApplication.translate("MainWindow", "Facile", None, -1))
		self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
		self.menuNew_Project.setTitle(
			QtWidgets.QApplication.translate("MainWindow", "New Project", None, -1))
		self.menuRecent_Projects.setTitle(
			QtWidgets.QApplication.translate("MainWindow", "Recent Projects", None, -1))
		self.menuWindow.setTitle(QtWidgets.QApplication.translate("MainWindow", "Window", None, -1))
		self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
		self.menuView.setTitle(QtWidgets.QApplication.translate("MainWindow", "View", None, -1))
		self.dockWidget_2.setWindowTitle(
			QtWidgets.QApplication.translate("MainWindow", "Project Explorer", None, -1))
		self.dockWidget_4.setWindowTitle(
			QtWidgets.QApplication.translate("MainWindow", "Validator Messages", None, -1))
		self.dockWidget_5.setWindowTitle(
			QtWidgets.QApplication.translate("MainWindow", "Property Editor", None, -1))
		self.dockWidget_6.setWindowTitle(
			QtWidgets.QApplication.translate("MainWindow", "Modules", None, -1))
		self.modulesView.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow",
		                                                                          "Module", None,
		                                                                          -1))
		self.modulesView.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow",
		                                                                          "Description",
		                                                                          None, -1))
		self.toolBar.setWindowTitle(
			QtWidgets.QApplication.translate("MainWindow", "toolBar", None, -1))
		self.actionOpen_Project.setText(
			QtWidgets.QApplication.translate("MainWindow", "Open Project", None, -1))
		self.actionSave_Project.setText(
			QtWidgets.QApplication.translate("MainWindow", "Save Project", None, -1))
		self.actionSave_as.setText(
			QtWidgets.QApplication.translate("MainWindow", "Save As . . .", None, -1))
		self.actionFrom_Scratch.setText(
			QtWidgets.QApplication.translate("MainWindow", "From Scratch", None, -1))
		self.actionFrom_Existing_Project.setText(
			QtWidgets.QApplication.translate("MainWindow", "From Existing Project", None, -1))
		self.actionProject_Tree.setText(
			QtWidgets.QApplication.translate("MainWindow", "Project Tree", None, -1))
		self.actionProperty_Editor.setText(
			QtWidgets.QApplication.translate("MainWindow", "Property Editor", None, -1))
		self.actionTarget_GUI_Model.setText(
			QtWidgets.QApplication.translate("MainWindow", "Target GUI Model", None, -1))
		self.actionAPI_Builder.setText(
			QtWidgets.QApplication.translate("MainWindow", "API Builder", None, -1))
		self.actionValidator.setText(
			QtWidgets.QApplication.translate("MainWindow", "Validator", None, -1))
		self.actionShow_Behaviors.setText(
			QtWidgets.QApplication.translate("MainWindow", "Show Behaviors", None, -1))
		self.actionDetailed_View.setText(
			QtWidgets.QApplication.translate("MainWindow", "Detailed View", None, -1))
		self.actionAutoExplore.setText(
			QtWidgets.QApplication.translate("MainWindow", "Auto Explore", None, -1))
		self.actionAutoExplore.setToolTip(QtWidgets.QApplication.translate("MainWindow",
		                                                                   "Explore the target GUI autonomously (no user control)",
		                                                                   None, -1))
		self.actionAutoExplore.setShortcut(
			QtWidgets.QApplication.translate("MainWindow", "Ctrl+Alt+A", None, -1))
		self.actionManualExplore.setText(
			QtWidgets.QApplication.translate("MainWindow", "Manual Explore", None, -1))
		self.actionManualExplore.setToolTip(QtWidgets.QApplication.translate("MainWindow",
		                                                                     "Watch for changes in the target GUI as the user interacts with it.",
		                                                                     None, -1))
		self.actionManualExplore.setShortcut(
			QtWidgets.QApplication.translate("MainWindow", "Ctrl+Alt+M", None, -1))
		self.actionAPI_Modules.setText(
			QtWidgets.QApplication.translate("MainWindow", "API Modules", None, -1))
		self.actionManage_Project.setText(
			QtWidgets.QApplication.translate("MainWindow", "Project Settings", None, -1))
		self.actionAdd_Behavior.setText(
			QtWidgets.QApplication.translate("MainWindow", "Add Behavior", None, -1))
		self.actionAdd_Behavior.setToolTip(QtWidgets.QApplication.translate("MainWindow",
		                                                                    "Add a visibility behavior to the target GUI model",
		                                                                    None, -1))
		self.actionStart_App.setText(
			QtWidgets.QApplication.translate("MainWindow", "Start App", None, -1))
		self.actionStart_App.setToolTip(QtWidgets.QApplication.translate("MainWindow",
		                                                                 "Start running this project\'s target application",
		                                                                 None, -1))
		self.actionStop_App.setText(
			QtWidgets.QApplication.translate("MainWindow", "Stop App", None, -1))
		self.actionStop_App.setToolTip(QtWidgets.QApplication.translate("MainWindow",
		                                                                "Stop running this project\'s target application",
		                                                                None, -1))
