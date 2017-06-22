# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MazeToObjDialog.ui'
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

class Ui_MazeToObj_Dialog(object):
    def setupUi(self, MazeToObj_Dialog):
        MazeToObj_Dialog.setObjectName(_fromUtf8("MazeToObj_Dialog"))
        MazeToObj_Dialog.resize(550, 204)
        self.gridLayout_2 = QtGui.QGridLayout(MazeToObj_Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(MazeToObj_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cellWidthSpin = QtGui.QDoubleSpinBox(MazeToObj_Dialog)
        self.cellWidthSpin.setDecimals(1)
        self.cellWidthSpin.setSingleStep(0.1)
        self.cellWidthSpin.setProperty("value", 1.0)
        self.cellWidthSpin.setObjectName(_fromUtf8("cellWidthSpin"))
        self.gridLayout.addWidget(self.cellWidthSpin, 0, 1, 1, 1)
        self.wallHeightSpin = QtGui.QDoubleSpinBox(MazeToObj_Dialog)
        self.wallHeightSpin.setDecimals(1)
        self.wallHeightSpin.setSingleStep(0.5)
        self.wallHeightSpin.setProperty("value", 1.0)
        self.wallHeightSpin.setObjectName(_fromUtf8("wallHeightSpin"))
        self.gridLayout.addWidget(self.wallHeightSpin, 1, 1, 1, 1)
        self.label = QtGui.QLabel(MazeToObj_Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(MazeToObj_Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(MazeToObj_Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(MazeToObj_Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(MazeToObj_Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.objFileName = QtGui.QLineEdit(MazeToObj_Dialog)
        self.objFileName.setObjectName(_fromUtf8("objFileName"))
        self.gridLayout.addWidget(self.objFileName, 2, 1, 1, 1)
        self.wallThicknessSpin = QtGui.QDoubleSpinBox(MazeToObj_Dialog)
        self.wallThicknessSpin.setDecimals(1)
        self.wallThicknessSpin.setSingleStep(0.1)
        self.wallThicknessSpin.setProperty("value", 0.1)
        self.wallThicknessSpin.setObjectName(_fromUtf8("wallThicknessSpin"))
        self.gridLayout.addWidget(self.wallThicknessSpin, 0, 3, 1, 1)
        self.openMazeExits = QtGui.QComboBox(MazeToObj_Dialog)
        self.openMazeExits.setObjectName(_fromUtf8("openMazeExits"))
        self.gridLayout.addWidget(self.openMazeExits, 1, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(MazeToObj_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MazeToObj_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MazeToObj_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MazeToObj_Dialog)
        MazeToObj_Dialog.setTabOrder(self.objFileName, self.buttonBox)

    def retranslateUi(self, MazeToObj_Dialog):
        MazeToObj_Dialog.setWindowTitle(_translate("MazeToObj_Dialog", "Maze to OBJ", None))
        self.label.setText(_translate("MazeToObj_Dialog", "Cell Width (meters)", None))
        self.label_2.setText(_translate("MazeToObj_Dialog", "Wall Thickness (meters)", None))
        self.label_4.setText(_translate("MazeToObj_Dialog", "Open Exit Walls?", None))
        self.label_3.setText(_translate("MazeToObj_Dialog", "Wall Height", None))
        self.label_5.setText(_translate("MazeToObj_Dialog", "Obj FileName", None))
        self.objFileName.setToolTip(_translate("MazeToObj_Dialog", "If left blank, defaults to maze name", None))

