# main python imports

#QT Modules
from PyQt4 import QtCore, QtGui

#QT GUI
from MazeToObjDialog_QT import Ui_MazeToObj_Dialog

class MazeToObjDialog(QtGui.QDialog):
    def __init__(self):

        #create widget
        QtGui.QWidget.__init__(self)

        # setup UI
        self.ui = Ui_MazeToObj_Dialog()
        self.ui.setupUi(self)

        #setup the yes/no dialog
        # seed the combo boxes
        for value in ["Yes","No"]:
            self.ui.openMazeExits.addItem(value)
        self.open_exits = True

        # connect the on changed
        self.ui.openMazeExits.currentIndexChanged.connect(self.ChangeOpenWalls)


    def ChangeOpenWalls(self):
        value = self.ui.openMazeExits.value()
        self.open_exits = value == "Yes"
        print "open exits: ", self.open_exits

    # return data in the following format
    #  1) obj filename or blank for same name
    #  2) maze cell size in meters
    #  3) maze wall thickness in meters
    #  4) maze wall height in meters
    #  5) whether to cut open the outer walls at the entrance / exit
    #
    def GetData(self):
        return (
            str(self.ui.objFileName.text()),
            self.ui.cellWidthSpin.value(),
            self.ui.wallThicknessSpin.value(),
            self.ui.wallHeightSpin.value(),
            self.open_exits
        )
