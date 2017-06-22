# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MazeManager.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(709, 558)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.MazeView = QtGui.QGraphicsView(self.centralwidget)
        self.MazeView.setMouseTracking(False)
        self.MazeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MazeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MazeView.setInteractive(False)
        self.MazeView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.MazeView.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.MazeView.setObjectName(_fromUtf8("MazeView"))
        self.verticalLayout.addWidget(self.MazeView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 709, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSolver = QtGui.QMenu(self.menubar)
        self.menuSolver.setObjectName(_fromUtf8("menuSolver"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Maze = QtGui.QAction(MainWindow)
        self.actionNew_Maze.setObjectName(_fromUtf8("actionNew_Maze"))
        self.actionOpenMaze = QtGui.QAction(MainWindow)
        self.actionOpenMaze.setObjectName(_fromUtf8("actionOpenMaze"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionRunMaze = QtGui.QAction(MainWindow)
        self.actionRunMaze.setObjectName(_fromUtf8("actionRunMaze"))
        self.actionSolve_Maze = QtGui.QAction(MainWindow)
        self.actionSolve_Maze.setObjectName(_fromUtf8("actionSolve_Maze"))
        self.actionExport_to_Obj = QtGui.QAction(MainWindow)
        self.actionExport_to_Obj.setObjectName(_fromUtf8("actionExport_to_Obj"))
        self.menuFile.addAction(self.actionNew_Maze)
        self.menuFile.addAction(self.actionOpenMaze)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSolver.addAction(self.actionRunMaze)
        self.menuSolver.addAction(self.actionSolve_Maze)
        self.menuSolver.addSeparator()
        self.menuSolver.addAction(self.actionExport_to_Obj)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSolver.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Maze Manager", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSolver.setTitle(_translate("MainWindow", "Maze", None))
        self.actionNew_Maze.setText(_translate("MainWindow", "New Maze", None))
        self.actionOpenMaze.setText(_translate("MainWindow", "Open Maze", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionRunMaze.setText(_translate("MainWindow", "Run Maze", None))
        self.actionSolve_Maze.setText(_translate("MainWindow", "Solve Maze...", None))
        self.actionExport_to_Obj.setText(_translate("MainWindow", "Export to Obj", None))

