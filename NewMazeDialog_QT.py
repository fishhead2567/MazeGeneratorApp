# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewMazeDialog.ui'
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

class Ui_NewMaze_Dialog(object):
    def setupUi(self, NewMaze_Dialog):
        NewMaze_Dialog.setObjectName(_fromUtf8("NewMaze_Dialog"))
        NewMaze_Dialog.resize(550, 223)
        self.gridLayout_2 = QtGui.QGridLayout(NewMaze_Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(NewMaze_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(NewMaze_Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mazeGeneratorBox = QtGui.QComboBox(NewMaze_Dialog)
        self.mazeGeneratorBox.setObjectName(_fromUtf8("mazeGeneratorBox"))
        self.gridLayout.addWidget(self.mazeGeneratorBox, 1, 1, 1, 1)
        self.mazeHeightSpin = QtGui.QSpinBox(NewMaze_Dialog)
        self.mazeHeightSpin.setProperty("value", 10)
        self.mazeHeightSpin.setObjectName(_fromUtf8("mazeHeightSpin"))
        self.gridLayout.addWidget(self.mazeHeightSpin, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(NewMaze_Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(NewMaze_Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.mazeWidthSpin = QtGui.QSpinBox(NewMaze_Dialog)
        self.mazeWidthSpin.setProperty("value", 10)
        self.mazeWidthSpin.setObjectName(_fromUtf8("mazeWidthSpin"))
        self.gridLayout.addWidget(self.mazeWidthSpin, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(NewMaze_Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.goalPlacementBox = QtGui.QComboBox(NewMaze_Dialog)
        self.goalPlacementBox.setObjectName(_fromUtf8("goalPlacementBox"))
        self.gridLayout.addWidget(self.goalPlacementBox, 1, 3, 1, 1)
        self.label_5 = QtGui.QLabel(NewMaze_Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.mazeFileName = QtGui.QLineEdit(NewMaze_Dialog)
        self.mazeFileName.setObjectName(_fromUtf8("mazeFileName"))
        self.gridLayout.addWidget(self.mazeFileName, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(NewMaze_Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.maxIterationsSpin = QtGui.QSpinBox(NewMaze_Dialog)
        self.maxIterationsSpin.setMaximum(999999)
        self.maxIterationsSpin.setProperty("value", 10000)
        self.maxIterationsSpin.setObjectName(_fromUtf8("maxIterationsSpin"))
        self.gridLayout.addWidget(self.maxIterationsSpin, 2, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 3, 1, 1)
        self.label_7 = QtGui.QLabel(NewMaze_Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.branchBiasCheck = QtGui.QCheckBox(NewMaze_Dialog)
        self.branchBiasCheck.setObjectName(_fromUtf8("branchBiasCheck"))
        self.gridLayout.addWidget(self.branchBiasCheck, 3, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.label_8 = QtGui.QLabel(NewMaze_Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.branchHorizontalSpin = QtGui.QDoubleSpinBox(NewMaze_Dialog)
        self.branchHorizontalSpin.setMaximum(10.0)
        self.branchHorizontalSpin.setSingleStep(0.1)
        self.branchHorizontalSpin.setProperty("value", 1.0)
        self.branchHorizontalSpin.setObjectName(_fromUtf8("branchHorizontalSpin"))
        self.gridLayout.addWidget(self.branchHorizontalSpin, 4, 1, 1, 1)
        self.label_9 = QtGui.QLabel(NewMaze_Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 2, 1, 1)
        self.branchVerticalSpin = QtGui.QDoubleSpinBox(NewMaze_Dialog)
        self.branchVerticalSpin.setMaximum(10.0)
        self.branchVerticalSpin.setSingleStep(0.1)
        self.branchVerticalSpin.setProperty("value", 1.0)
        self.branchVerticalSpin.setObjectName(_fromUtf8("branchVerticalSpin"))
        self.gridLayout.addWidget(self.branchVerticalSpin, 4, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(NewMaze_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewMaze_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewMaze_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewMaze_Dialog)
        NewMaze_Dialog.setTabOrder(self.mazeWidthSpin, self.mazeHeightSpin)
        NewMaze_Dialog.setTabOrder(self.mazeHeightSpin, self.mazeGeneratorBox)
        NewMaze_Dialog.setTabOrder(self.mazeGeneratorBox, self.goalPlacementBox)
        NewMaze_Dialog.setTabOrder(self.goalPlacementBox, self.mazeFileName)
        NewMaze_Dialog.setTabOrder(self.mazeFileName, self.maxIterationsSpin)
        NewMaze_Dialog.setTabOrder(self.maxIterationsSpin, self.buttonBox)

    def retranslateUi(self, NewMaze_Dialog):
        NewMaze_Dialog.setWindowTitle(_translate("NewMaze_Dialog", "New Maze", None))
        self.label.setText(_translate("NewMaze_Dialog", "Maze Width", None))
        self.label_2.setText(_translate("NewMaze_Dialog", "Maze Height", None))
        self.label_4.setText(_translate("NewMaze_Dialog", "Goal Placement", None))
        self.label_3.setText(_translate("NewMaze_Dialog", "Maze Generator", None))
        self.label_5.setText(_translate("NewMaze_Dialog", "Maze FileName", None))
        self.label_6.setText(_translate("NewMaze_Dialog", "Max Itereations", None))
        self.label_7.setText(_translate("NewMaze_Dialog", "Bias Branching Direction? ", None))
        self.branchBiasCheck.setText(_translate("NewMaze_Dialog", "CheckBox", None))
        self.label_8.setText(_translate("NewMaze_Dialog", "Biases: Horizontal Weight", None))
        self.label_9.setText(_translate("NewMaze_Dialog", "Vertical Weight", None))

