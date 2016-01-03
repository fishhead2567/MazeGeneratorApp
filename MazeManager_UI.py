from PyQt4.uic.Compiler.qtproxies import QtGui

__author__ = 'best'

"""

Main Application. Generates UI and sets up bindings.

"""

# main python imports
import os, sys, time
from os.path import isfile
from copy import copy

# QT modules!
from PyQt4 import QtCore,QtGui, QtOpenGL

# Get The Compiled QT GUI
from MazeManager_QT import Ui_MainWindow
from NewMazeDialog_UI import NewMazeDialog

# get the maze code
from Maze import Maze, LoadMaze
from MazeSolver import InteractiveMazeSolver, AStarMazeSolver


class MazeManagerApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # buld the scene which will hold my maze
        self.scene = QtGui.QGraphicsScene()
        self.ui.MazeView.setScene(self.scene)

        # set the scene... height? what does it do
        self.scene.setSceneRect(0, 0, 1024, 768)

        # accelerate the viewport
        self.ui.MazeView.setViewport(QtOpenGL.QGLWidget())

        #enable zoom
        # self.ui.MazeView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)

        # maze information
        self.maze = None
        self.mazeLoaded = False
        self.mazeLines = []
        self.mazeScale = 20.0
        self.mazeFile = None

        # solver information
        self.solver = None
        self.solverRunning = False
        self.solverIcon = None
        self.solverPath = None
        self.illustrateSolverPath = None
        self.solverInteractive = False

        # timer for the solver
        self.solverTimer = QtCore.QTimer()
        self.solverTimer.timeout.connect(self.SolverStep)

        # color for the solver
        self.nextColor = 0
        self.colors = [
            (255.0, 0.0, 0.0),
            (0.0, 255.0, 0.0),
            (0.0, 0.0, 255.0),
            (255.0, 255.0, 0.0),
            (0.0, 255.0, 255.0),
        ]

        # bind the menus
        self.ui.actionExit.triggered.connect(QtGui.qApp.quit)
        self.ui.actionOpenMaze.triggered.connect(self.LoadMazeFromFile)
        self.ui.actionRunMaze.triggered.connect(self.StartManualRun)
        self.ui.actionSolve_Maze.triggered.connect(self.StartAStarRun)
        self.ui.actionNew_Maze.triggered.connect(self.newMaze)

    # produce a new maze from the dialog
    def newMaze(self):
        self.popup = NewMazeDialog()
        self.popup.exec_()
        data =  self.popup.GetData()

        self.ResetMaze()
        filename = data[0]

        if filename == 0:
            print "NO FILE"
            return
        elif filename.split(".")[-1] != ".maze":
            filename += ".maze"

        newMaze = data[3].GenerateMaze(data[1], data[2])
        self.maze = newMaze
        self.mazeFile = filename
        data[3].SetStartEnd(self.maze)
        self.maze.SaveMaze(self.mazeFile)
        self.RenderMaze()

        self.popup = None


    def ResetMaze(self):
        if self.mazeLoaded:

            self.ResetSolver()
            self.mazeScale = 1.0
            self.mazeFile = ""
            self.maze = None
            for line in self.mazeLines:
                self.scene.removeItem(line)
            self.mazeLines = []
            self.mazeLoaded = False


    def ResetSolver(self):
        if self.solverRunning:
            if self.solverIcon is not None:
                self.scene.removeItem(self.solverIcon)
                self.solverIcon = None
            if self.solverPath is not None:
                self.scene.removeItem(self.solverPath)
                self.solverPath = None
            self.solver = None
            self.solverRunning = False
            self.solverIcon = None
            self.solverPath = None
            self.illustrateSolverPath = False
            self.solverInteractive = False



    def StartManualRun(self):
        if not self.solverRunning:
            print "Manual Maze Run"
            self.solverRunning = True
            self.solver = InteractiveMazeSolver(self.maze, 0)
            self.solverInteractive = True

            self.solverIcon = QtGui.QGraphicsRectItem()
            self.solverIcon.setZValue(2)
            self.solverIcon.setRect(0, 0, self.mazeScale / 2.0, self.mazeScale / 2.0)
            self.solverIcon.setBrush(QtGui.QBrush(QtGui.QColor(100, 100, 0)))
            self.scene.addItem(self.solverIcon)
            self.solverIcon.setPos(self.solver.mCurrentNode[1] * self.mazeScale  + self.mazeScale/4.0,
                                   self.solver.mCurrentNode[0] * self.mazeScale  + self.mazeScale/4.0)
        self.SolverStep()

    def StartAStarRun(self):
        if self.solverRunning:
            self.ResetSolver()

        if not self.solverRunning:
            print "AStar Maze Run"
            self.solverRunning = True
            self.solverInteractive = False
            self.solverIcon = None
            self.illustrateSolverPath = True
            self.solver = AStarMazeSolver(self.maze, 0)
            self.solverPath = None

        self.SolverStep()

    def SolverStep(self):
        if self.solverRunning:
            self.solver.Step()
            if self.solver.Finished():
                self.ResetSolver()

            self.solverTimer.start(1000.0 / 30.0)

            if self.illustrateSolverPath:
                if self.solverPath is not None:
                    self.scene.removeItem(self.solverPath)

                current_path = copy(self.solver.mCurrentPath)
                if len(current_path) > 1:
                    self.solverPath = QtGui.QGraphicsPathItem()
                    self.solverPath.setPos(0,0)
                    color = self.colors[self.nextColor]
                    self.nextColor = (self.nextColor + 1 ) % len(self.colors)
                    pen = QtGui.QPen(QtGui.QColor(color[0], color[1], color[2]))
                    self.solverPath.setPen(pen)
                    # self.solverPath.setBrush(QtGui.QBrush(QtGui.QColor(color[0], color[1], color[2])))

                    painterPath = QtGui.QPainterPath()

                    self.solverPath.setZValue(2)
                    # print current_path
                    path_node = current_path[0]
                    painterPath.moveTo(path_node[1] * self.mazeScale + self.mazeScale / 2.0,
                                       path_node[0] * self.mazeScale + self.mazeScale / 2.0)
                    current_path.pop(0)
                    while len(current_path) > 0:
                        path_node = current_path[0]
                        current_path.pop(0)
                        painterPath.lineTo(path_node[1] * self.mazeScale + self.mazeScale / 2.0,
                                           path_node[0] * self.mazeScale + self.mazeScale / 2.0)
                    self.solverPath.setPath(painterPath)
                    self.scene.addItem(self.solverPath)





    def keyPressEvent(self, event):
        print "KP",
        # if the solver is running, then pass through any moves
        if type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_A:
            print "West"
            if self.solverRunning and self.solverInteractive:
                self.solver.moves.append("w")
                self.solver.Step()

        elif type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_D:
            print "East"
            if self.solverRunning and self.solverInteractive:
                self.solver.moves.append("e")
                self.solver.Step()

        elif type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_W:
            print "North"
            if self.solverRunning and self.solverInteractive:
                self.solver.moves.append("n")
                self.solver.Step()

        elif type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_S:
            print "South"
            if self.solverRunning and self.solverInteractive:
                self.solver.moves.append("s")
                self.solver.Step()


        if self.solverRunning and self.solverInteractive and self.solverIcon:
            self.solverIcon.setPos(self.solver.mCurrentNode[1] * self.mazeScale + self.mazeScale/4.0 ,
                                   self.solver.mCurrentNode[0] * self.mazeScale + self.mazeScale/4.0)


    def wheelEvent(self, event):
        print "WHEEL",
        if event.delta() > 0:
            print "in"
        elif event.delta() < 0:
            print "out"

    # load default maze
    # def loadDefaultMaze(self):
        # print "load default maze"
        # self.loadMaze("mPrims_naive.maze")


    def LoadMazeFromFile(self):
        fd = QtGui.QFileDialog(self, directory=os.path.dirname(os.path.realpath(__file__)))
        mazeFile = fd.getOpenFileName()
        if isfile(mazeFile):
            if self.mazeLoaded:
                print "Reset Maze Before Loading"
                self.ResetMaze()
            self.mazeFile = mazeFile
            self.maze = LoadMaze(self.mazeFile)
            self.RenderMaze()


    # load and render a maze
    def RenderMaze(self):
        # make sure the maze opens
        if not self.mazeLoaded:
            # self.maze.PrintMaze()
            self.mazeLoaded = True
            self.maze.PrintMaze()
            print self.scene.sceneRect().width()
            self.mazeScale = self.scene.sceneRect().width() / self.maze.width
            self.mazeScale = min(self.mazeScale, self.scene.sceneRect().height() / self.maze.height)
            # maze font
            font=QtGui.QFont('White Rabbit')
            font.setPointSize(self.mazeScale / 3.0)

            # add the maze to the scene. Just for now, do the processing here
            for row in xrange(self.maze.height):
                for col in xrange(self.maze.width):
                # for col in xrange(1):

                    """
                    text = QtGui.QGraphicsTextItem('%d' % (row * self.maze.width + col))
                    text.setFont(font)
                    text.setDefaultTextColor(QtGui.QColor(0, 0, 0))
                    text.setPos(col * self.mazeScale,
                                row * self.mazeScale)
                    self.mazeLines.append(text)
                    """

                    borders = self.maze.GetBorders([row,col])
                    for border in xrange(len(borders)):
                        if borders[border] < 1:

                            if border == 0:
                                line = QtGui.QGraphicsLineItem()
                                line.setLine(col * self.mazeScale, row * self.mazeScale,
                                             (col + 1) * self.mazeScale, (row + 0) * self.mazeScale)
                                self.mazeLines.append(line)

                            elif border == 1:
                                line = QtGui.QGraphicsLineItem()
                                line.setLine((col + 1) * self.mazeScale, (row + 0) * self.mazeScale,
                                             (col + 1) * self.mazeScale, (row + 1) * self.mazeScale)
                                self.mazeLines.append(line)

                            elif border == 2:
                                line = QtGui.QGraphicsLineItem()
                                line.setLine((col + 0) * self.mazeScale, (row + 1) * self.mazeScale,
                                             (col + 1) * self.mazeScale, (row + 1) * self.mazeScale)
                                self.mazeLines.append(line)

                            elif border == 3:
                                line = QtGui.QGraphicsLineItem()
                                line.setLine((col + 0) * self.mazeScale, (row + 0) * self.mazeScale,
                                             (col + 0) * self.mazeScale, (row + 1) * self.mazeScale)
                                self.mazeLines.append(line)
                            """
                            """

            start = QtGui.QGraphicsTextItem('St')
            start.setFont(font)
            start.setDefaultTextColor(QtGui.QColor(255, 0, 0))
            start.setPos(self.maze.start_cell[1] * self.mazeScale, self.maze.start_cell[0] * self.mazeScale)
            start.setZValue(1)
            self.mazeLines.append(start)

            end = QtGui.QGraphicsTextItem('En')
            end.setFont(font)
            end.setDefaultTextColor(QtGui.QColor(0, 0, 255))
            end.setPos(self.maze.end_cell[1] * self.mazeScale, self.maze.end_cell[0] * self.mazeScale)
            end.setZValue(1.0)
            self.mazeLines.append(end)

            # add all the lines to the maze
            for item in self.mazeLines:
                self.scene.addItem(item)


def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window = MazeManagerApp()
    window.show()

    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()