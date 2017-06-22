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
from MazeToObjDialog_UI import MazeToObjDialog

# get the maze code
from Maze import Maze, LoadMaze
from MazeSolver import InteractiveMazeSolver, AStarMazeSolver
from JsonConfig import CreateOrLoadConfig
from MazeToObj import MazeToObj

class MazeManagerApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        #config
        self.config = CreateOrLoadConfig()
        print "C", self.config

        # color for the solver
        self.nextColor = 0
        # shortcut for color choice
        self.mNumColors = len(self.config["maze"]["solution_colors"])

        # buld the scene which will hold my maze
        self.scene = QtGui.QGraphicsScene()
        self.ui.MazeView.setScene(self.scene)

        # set the scene... height? what does it do
        self.scene.setSceneRect(0, 0, 1024, 768)

        # accelerate the viewport
        self.ui.MazeView.setViewport(QtOpenGL.QGLWidget())

         # set the scene background color
        self.scene.setBackgroundBrush(QtGui.QColor(self.config["maze"]["background_color"]))

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

        # dialog remembers where it opened last file from
        self.last_maze_dir = None

        # timer for the solver
        self.solverTimer = QtCore.QTimer()
        self.solverTimer.timeout.connect(self.SolverStep)



        # bind the menus
        self.ui.actionExit.triggered.connect(QtGui.qApp.quit)
        self.ui.actionOpenMaze.triggered.connect(self.LoadMazeFromFile)
        self.ui.actionRunMaze.triggered.connect(self.StartManualRun)
        self.ui.actionSolve_Maze.triggered.connect(self.StartAStarRun)
        self.ui.actionNew_Maze.triggered.connect(self.newMaze)
        self.ui.actionExport_to_Obj.triggered.connect(self.MazeToObj)


    # produce a new maze from the dialog
    def newMaze(self):
        self.popup = NewMazeDialog()
        self.popup.exec_()
        data =  self.popup.GetData()
        self.last_maze_dir = None
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
            self.solverIcon.setBrush(QtGui.QBrush(QtGui.QColor(self.config["maze"]["pawn_color"])))
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
            self.statusBar().showMessage("Solving Maze")

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
                self.statusBar().showMessage("Solving Maze: %d steps" % self.solver.mStep)

                if len(current_path) > 1:
                    self.solverPath = QtGui.QGraphicsPathItem()
                    self.solverPath.setPos(0,0)
                    color = self.config["maze"]["solution_colors"][self.nextColor]
                    self.nextColor = (self.nextColor + 1 ) % self.mNumColors
                    pen = QtGui.QPen(QtGui.QColor(color))
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
            self.ui.MazeView.scale(self.config["zoom_speed"], self.config["zoom_speed"])
        elif event.delta() < 0:
            print "out"
            self.ui.MazeView.scale(1.0 / self.config["zoom_speed"], 1.0 / self.config["zoom_speed"])
        return True
    # load default maze
    # def loadDefaultMaze(self):
        # print "load default maze"
        # self.loadMaze("mPrims_naive.maze")


    def LoadMazeFromFile(self):
        if self.last_maze_dir is None:
            directory = os.path.dirname(os.path.realpath(__file__))
        else:
            directory = self.last_maze_dir

        fd = QtGui.QFileDialog(self, directory=directory)
        mazeFile = fd.getOpenFileName()
        if isfile(mazeFile):
            if self.mazeLoaded:
                print "Reset Maze Before Loading"
                self.ResetMaze()
            self.mazeFile = mazeFile
            self.maze = LoadMaze(self.mazeFile)
            self.last_maze_dir =os.path.dirname(str(self.mazeFile))
            self.statusBar().showMessage("Maze Loaded",5000)
            self.RenderMaze()


    def MazeToObj(self):
        if self.mazeFile is None:
            self.statusBar().showMessage("Load a Maze First!", 5000)
            return False

        self.popup = MazeToObjDialog()
        self.popup.exec_()
        data =  self.popup.GetData()

        filename = data[0]

        if filename == 0 or filename == "":
            filename = str(self.mazeFile).replace(".maze",".obj")

        cell_size = data[1]
        wall_thickness = data[2]
        wall_height = data[3]
        open_exits = data[4]

        success = MazeToObj(self.maze,
                  cell_size, wall_thickness, wall_height,
                  filename, open_exits)

        self.popup = None
        if success:
            self.statusBar().showMessage("Obj saved to: %s" % filename, 5000)
        else:
            self.statusBar().showMessage("Failed to save OBJ file", 5000)


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
            font.setPointSize(self.mazeScale * .9)

            wallPen = QtGui.QPen(QtGui.QColor(self.config["maze"]["walls_color"]))


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
                            line = None
                            if border in [0,1,2,3]:
                                line = QtGui.QGraphicsLineItem()
                                line.setPen(wallPen)
                            if border == 0:
                                line.setLine(col * self.mazeScale, row * self.mazeScale,
                                             (col + 1) * self.mazeScale, (row + 0) * self.mazeScale)
                                self.mazeLines.append(line)

                            elif border == 1:
                                line.setLine((col + 1) * self.mazeScale, (row + 0) * self.mazeScale,
                                             (col + 1) * self.mazeScale, (row + 1) * self.mazeScale)
                                self.mazeLines.append(line)

                            elif border == 2:
                                line.setLine((col + 0) * self.mazeScale, (row + 1) * self.mazeScale,
                                             (col + 1) * self.mazeScale, (row + 1) * self.mazeScale)
                                self.mazeLines.append(line)

                            elif border == 3:
                                line.setLine((col + 0) * self.mazeScale, (row + 0) * self.mazeScale,
                                             (col + 0) * self.mazeScale, (row + 1) * self.mazeScale)
                                self.mazeLines.append(line)
                            """
                            """

            # Use large squares for start and end
            text = QtGui.QGraphicsTextItem('S')
            text.setFont(font)
            text.setDefaultTextColor(QtGui.QColor(255, 0, 255))
            text.setPos(self.maze.start_cell[1] * self.mazeScale, self.maze.start_cell[0] * self.mazeScale - self.mazeScale / 2.0)
            text.setZValue(1.0)
            self.mazeLines.append(text)

            text = QtGui.QGraphicsTextItem('E')
            text.setFont(font)
            text.setDefaultTextColor(QtGui.QColor(0, 0, 255))
            text.setPos(self.maze.end_cell[1] * self.mazeScale, self.maze.end_cell[0] * self.mazeScale- self.mazeScale / 2.0)
            text.setZValue(1.0)
            self.mazeLines.append(text)

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
