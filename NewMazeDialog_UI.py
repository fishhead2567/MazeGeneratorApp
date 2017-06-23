__author__ = 'best'


# main python imports
import os, sys, time

# QT modules!
from PyQt4 import QtCore, QtGui

# Get The Compiled QT GUI
from NewMazeDialog_QT import Ui_NewMaze_Dialog
from MazeGenerator import DepthFirstMazeGenerator, ModifiedPrimMazeGenerator

class NewMazeDialog(QtGui.QDialog):
    def __init__(self):
        # super(NewMazeDialog, self).__init__()

        QtGui.QWidget.__init__(self)
        self.ui = Ui_NewMaze_Dialog()
        self.ui.setupUi(self)

        #setup the  generator methods
        self.generators = {
            "Depth First"    : DepthFirstMazeGenerator(),
            "Modified Prims" : ModifiedPrimMazeGenerator(),
        }

        self.goalPlacements = {
            "Naive Corners" : "naive",
            "Longest Path"  : "longest",
            "Random A-Star" : "astar"
        }

        # seed the combo boxes
        for generator in self.generators:
            self.ui.mazeGeneratorBox.addItem(generator)

        for goal in self.goalPlacements:
            self.ui.goalPlacementBox.addItem(goal)

        # disable the spinboxes by deafult
        self.ui.branchHorizontalSpin.setDisabled(True)
        self.ui.branchVerticalSpin.setDisabled(True)

        # connect the on changed
        self.ui.goalPlacementBox.currentIndexChanged.connect(self.ChangeGoalPlacement)
        self.ui.maxIterationsSpin.valueChanged.connect(self.ChangeMaxSteps)
        self.ui.branchBiasCheck.stateChanged.connect(self.EnableDisableBias)

    def EnableDisableBias(self):
        if self.ui.branchBiasCheck.isChecked():
            self.ui.branchHorizontalSpin.setDisabled(False)
            self.ui.branchVerticalSpin.setDisabled(False)
        else:
            self.ui.branchHorizontalSpin.setDisabled(True)
            self.ui.branchVerticalSpin.setDisabled(True)

    def ChangeMaxSteps(self):
        iterations = self.ui.maxIterationsSpin.value()
        print "i", iterations

        for generator in self.generators:
            self.generators[generator].SetMaxSteps(iterations)

    def ChangeGoalPlacement(self):
        placement = str(self.ui.goalPlacementBox.currentText())
        print "GP", placement
        for generator in self.generators:
            self.generators[generator].SetEndpointMethod(self.goalPlacements[placement])

    def GetData(self):
        """
            filename,
            mazewidth
            mazeheight
            generators,
            bias?
            horizontalbias
            verticalbias

        :return:
        """
        genText = str(self.ui.mazeGeneratorBox.currentText())
        print "GT - GenTextData", genText
        return (
            str(self.ui.mazeFileName.text()),
            self.ui.mazeWidthSpin.value(),
            self.ui.mazeHeightSpin.value(),
            self.generators[genText],
            self.ui.branchBiasCheck.isChecked(),
            self.ui.branchHorizontalSpin.value(),
            self.ui.branchVerticalSpin.value(),
        )



