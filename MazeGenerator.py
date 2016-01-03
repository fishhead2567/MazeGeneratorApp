__author__ = 'best'


import numpy as np
from scipy.spatial.distance import euclidean
from copy import copy, deepcopy

from Maze import Maze, LoadMaze
from MazeSolver import AStarMazeSolver

"""
Abstract Maze Generator
"""
class MazeGenerator(object):
    def __init__(self, endpointMethod=None, verbosity=0):
        self.mVerbosity = verbosity

        self.mEndpointMethods = {
            "naive" : self.SetStartEndNaive,
            "longest" : self.SetStartEndLongest,
            "astar" : self.SetStartEndRandomAStar
        }
        self.mEndpointMethod = "naive"
        self.SetEndpointMethod(endpointMethod)

        self.mMaxSteps = 10000

    def SetEndpointMethod(self, endpointMethod):
        if endpointMethod in self.mEndpointMethods:
            self.mEndpointMethod = endpointMethod


    def GenerateMaze(self, width, height):
        raise(NotImplementedError)

    def SetMaxSteps(self, steps):
        self.mMaxSteps = steps

    def SetStartEnd(self, theMaze, start=None, end=None):
        if self.mVerbosity > 0:
            print "Set Enpoints using %s method" % self.mEndpointMethod
        self.mEndpointMethods[self.mEndpointMethod](theMaze, start, end)

    # sets the endpoints to either those specified, or one opposite the other
    def SetStartEndNaive(self, theMaze, start, end):
        # we may need to find the corners, so store them
        corners = [
            [0, 0],
            [0, theMaze.width - 1],
            [theMaze.height - 1, theMaze.width -1],
            [theMaze.height - 1, 0]
        ]

        bestCorner = None
        if start is not None:
            theMaze.start_cell = start
            if end is not None:
                theMaze.end_cell = end

            else:
                bestDistance = 1e10
                for index in xrange(4):
                    distance = euclidean(start, corners[index])
                    if distance < bestDistance:
                        bestDistance = distance
                        bestCorner = index

                theMaze.end_cell = corners[(bestCorner + 2) % 4]
        else:
            # pick them both in corners
            bestCorner = np.random.randint(0, 4)
            if self.mVerbosity > 0:
                print "    Start corner randomly set to %d" % (bestCorner)
            theMaze.start_cell = corners[bestCorner]
            theMaze.end_cell = corners[(bestCorner + 2) % 4]

        if self.mVerbosity > 0:
            print "    Start: %s, End: %s" % (str(theMaze.start_cell), str(theMaze.end_cell))

    # use A-Star to find the longest maze possible in this configuration
    def SetStartEndLongest(self, theMaze, start, end):
        # using A-Star, we are going to run the end points of the maze away from the center to find the optimal length
        # maze
        nodeHeap = []
        visitedList = []
        bestNode = []
        bestFitness = -1e10
        bestStep = 0
        trees = 5
        step = 0

        maxSteps = self.mMaxSteps if self.mMaxSteps > 500 else 500

        #if self.mVerbosity > 0:
        print "Max Steps: %d, trees: %d" % (maxSteps, trees)

        while len(nodeHeap) < trees - 1:
            # seed a random tree
            current_path = [[np.random.randint(0, theMaze.height),
                            np.random.randint(0, theMaze.width)]]
            if self.mVerbosity > 0:
                print "    add seed %d,%d" % (current_path[0][0], current_path[0][1])
            self.AddNodeToHeap(nodeHeap, visitedList, current_path)

        # make sure we seed on the middle of the maze as well
        current_path = [map(int, [theMaze.height / 2.0, theMaze.width / 2.0])]
        self.AddNodeToHeap(nodeHeap, visitedList, current_path)

        while len(nodeHeap) > 0 and step < maxSteps:
            # print my current node if I am in verbose mode
            nodeToVisit = nodeHeap[0]
            nodeHeap.pop(0)
            nodePath = nodeToVisit[1]
            node_key = nodeToVisit[0]

            self.AddNodeToVisited(visitedList, nodePath)
            step += 1
            if step % 500 == 0:
                print "Generating tough maze... %d combinations tried" % step

            if self.mVerbosity > 0:
                print "Step", step,"-", nodeToVisit[-1]
                if self.mVerbosity > 1:
                    print "    ", nodePath

            if nodeToVisit[-1] > bestFitness:
                bestFitness = nodeToVisit[-1]
                bestNode = nodePath
                bestStep = step

            # add start cell's children to the heap
            test_nodes = []
            for child in theMaze.GetNeighborCells(nodePath[0]):
                if child not in nodePath:
                    test_nodes.append([child] + nodePath)

            if len(nodePath) > 1:
                for child in theMaze.GetNeighborCells(nodePath[-1]):
                    if child not in nodePath:
                        test_nodes.append(nodePath + [child])

            for test_node in test_nodes:
                self.AddNodeToHeap(nodeHeap, visitedList, test_node)

            # sort the list
            nodeHeap.sort(key=lambda x: x[-1], reverse=True)

        if self.mVerbosity > 0:
            print "Begin and End Chosen", bestNode[0], bestNode[-1]
            print "    fitness: ", bestFitness, "Len: ", len(bestNode)
            if self.mVerbosity > 1:
                print "    Path: ", bestNode
        print "    Path found on step %d : %d " % (bestStep, len(bestNode))

        theMaze.start_cell = bestNode[0]
        theMaze.end_cell = bestNode[-1]

    # Add a node to my A-Star Heap
    def AddNodeToHeap(self, nodeHeap, visitedList, node):
        # get the node endpoints
        start = node[0]
        end = node[-1]

        visited_node = self._makeNodeKey(node)

        if visited_node in visitedList:
            return

        if visited_node not in [n[0] for n in nodeHeap]:
            if self.mVerbosity > 0:
                 print "    add new option", node[0], node[-1]
            nodeHeap.append((
                visited_node,
                node,
                len(node),
                euclidean(start, end),
                len(node) + euclidean(start, end)
            ))

    def AddNodeToVisited(self, visitedList, node):
        visited_node = self._makeNodeKey(node)
        if visited_node in visitedList:
            return
        visitedList.append(visited_node)

    def _makeNodeKey(self, node):
        # get the node endpoints
        start = node[0]
        end = node[-1]
        if end[0] < start[0] or (end[0] == start[0] and end[1] < start[1]):
            t = copy(end)
            end = start
            start = t

        node_key = [start, end]
        # print "TEST", node_key
        return node_key

    def SetStartEndRandomAStar(self, theMaze, start, end):
        # use A-Star to find the longest maze possible in this configuration
        bestLength = 0
        bestStart = None
        bestEnd = None
        maxSteps = self.mMaxSteps if self.mMaxSteps > 100 else 100

        # randomly produce start and end nodes. Solve them with A-Star. Evaluate their difficulty.
        for iteration in xrange(maxSteps):

            test_start = [np.random.randint(0, theMaze.height),
                            np.random.randint(0, theMaze.width)]

            test_end = [np.random.randint(0, theMaze.height),
                            np.random.randint(0, theMaze.width)]

            if self.mVerbosity > 0:
                print "Random A-Star %d,%d to %d, %d" % (test_start[0], test_start[1],
                                                    test_end[0], test_end[1] )

            solver = AStarMazeSolver(theMaze)
            while not solver.Finished():
                solver.Step()
            # print solver.mStep, len(solver.mAnswer)
            if len(solver.mAnswer) > bestLength:
                bestLength = len(solver.mAnswer)
                bestStart = test_start
                bestEnd = test_end
                if self.mVerbosity > 0:
                    print "    new best: %d" % bestLength

            if iteration % 50 == 0:
                print "iteration %d finished" % iteration

        theMaze.start_cell = bestStart
        theMaze.end_cell = bestEnd

        if self.mVerbosity > 0:
            print "Begin and End Chosen", bestStart, bestEnd
            print "    fitness: ", bestLength

"""
Depth First Maze Generator
"""
class DepthFirstMazeGenerator(MazeGenerator):
    def __init__(self, endpointMethod=None, verbosity=0):
        super(DepthFirstMazeGenerator, self).__init__(endpointMethod, verbosity)

    def GenerateMaze(self, width, height):
        theMaze = Maze()
        theMaze.SetDimensions(width, height)

        # treat the maze generation as a depth first search
        # start with the top corner as the first cell
        active_cells = []
        dead_cells = []
        active_cells.append([0, 0])


        while len(active_cells) > 0:
            thisCell = active_cells[-1]

            if self.mVerbosity > 0:
                print "active cell", thisCell,

            # remove a wall from this cell
            exits = theMaze.GetBorders(thisCell)

            # choose a random exit to open
            walls = exits == 0
            wallToOpen = None


            choices = list(np.arange(4)[walls])
            if self.mVerbosity > 0:
                print "walls", choices

            while wallToOpen is None and len(choices) > 0:
                wallIndex = np.random.randint(len(choices))
                wallToOpen = choices[wallIndex]
                choices.pop(wallIndex)
                newCell = deepcopy(thisCell)
                # wallToOpen = np.random.choice(choices)
                # choices.remove(wallToOpen)

                if wallToOpen == 0:
                    newCell[0] -= 1
                elif wallToOpen == 1:
                    newCell[1] += 1
                elif wallToOpen == 2:
                    newCell[0] += 1
                else:
                    newCell[1] -= 1

                if self.mVerbosity > 0:
                    print "    choose: ", wallToOpen, newCell, (wallToOpen + 2) % 4

                if newCell in active_cells or newCell in dead_cells:
                    if self.mVerbosity > 0:
                        print "        Bad choice", "Active" if newCell in active_cells else "Dead"
                    wallToOpen = None

            # if choice is none, we ran out of options
            if wallToOpen is None:
                active_cells.pop(-1)
                dead_cells.append(thisCell)
            else:
                # alright! neighbbor!
                rWallToOpen = (wallToOpen + 2) % 4
                # print "        open %d and %d" % (wallToOpen, rWallToOpen)
                theMaze.cells[thisCell[0], thisCell[1], wallToOpen] = 1
                theMaze.cells[newCell[0], newCell[1], rWallToOpen] = 1

                active_cells.append(newCell)

            # if np.count_nonzero(exits > 0) >= 2:
            #    active_cells.pop(-1)
            #    dead_cells.append(thisCell)

        # theMaze.end_cell = [0, 0]
        # theMaze.start_cell = [theMaze.height -1, theMaze.width -1]
        if self.mVerbosity > 0:
            print
        return theMaze

class ModifiedPrimMazeGenerator(MazeGenerator):
    def __init__(self, endpointMethod=None, verbosity=0):
        super(ModifiedPrimMazeGenerator, self).__init__(endpointMethod, verbosity)

    def GenerateMaze(self, width, height):
        theMaze = Maze()
        theMaze.SetDimensions(width, height)

        # treat the maze generation as a depth first search
        # start with the top corner as the first cell
        maze_cells = []
        adjacent_cells = {}

        # choose a start cell
        current_cell = [np.random.randint(0, theMaze.height),
                        np.random.randint(0, theMaze.width)]
        maze_cells.append("%d-%d" % (current_cell[0], current_cell[1]))

        # create adjacency list
        borders = theMaze.GetBorders(current_cell)
        for index in xrange(len(borders)):
            if borders[index] == 0:
                new_cell = deepcopy(current_cell)
                if index == 0:
                    new_cell[0] -= 1
                elif index == 1:
                    new_cell[1] += 1
                elif index == 2:
                    new_cell[0] += 1
                elif index == 3:
                    new_cell[1] -= 1
                cell_key = "%d-%d" % (new_cell[0], new_cell[1])
                adjacent_cells[cell_key] = []
                adjacent_cells[cell_key].append([current_cell, index])

        # print "FIRST SET", adjacent_cells, maze_cells
        while len(adjacent_cells) > 0:
            # choose a cell to add to the maze at random
            cell_key = np.random.randint(0, len(adjacent_cells))
            cell_key = adjacent_cells.keys()[cell_key]
            cell = adjacent_cells[cell_key]
            del(adjacent_cells[cell_key])
            maze_cells.append(cell_key)
            cell_key = map(int, cell_key.split("-"))

            if self.mVerbosity > 0:
                print "active cell: ", cell_key, "|", cell, len(cell)

            # choose a random edge from the set of edges connecting me
            connectedCell = np.random.randint(0, len(cell))
            connectedCell = cell[connectedCell]
            wallToOpen = connectedCell[1]
            rWallToOpen = (wallToOpen + 2) % 4
            connectedCell = connectedCell[0]
            if self.mVerbosity > 0:
                print "    connect to", connectedCell, "by", wallToOpen,"-",rWallToOpen

            theMaze.cells[connectedCell[0], connectedCell[1], wallToOpen] = 1
            theMaze.cells[cell_key[0], cell_key[1], rWallToOpen] = 1

            borders = theMaze.GetBorders(cell_key)
            for index in xrange(len(borders)):
                if borders[index] == 0:
                    new_cell = deepcopy(cell_key)
                    if index == 0:
                        new_cell[0] -= 1
                    elif index == 1:
                        new_cell[1] += 1
                    elif index == 2:
                        new_cell[0] += 1
                    elif index == 3:
                        new_cell[1] -= 1
                    new_cell_key = "%d-%d" % (new_cell[0], new_cell[1])
                    if new_cell_key not in maze_cells:
                        if new_cell_key not in adjacent_cells:
                            adjacent_cells[new_cell_key] = []
                        adjacent_cells[new_cell_key].append([cell_key, index])

        theMaze.end_cell = [0, 0]
        theMaze.start_cell = [theMaze.height -1, theMaze.width -1]
        return theMaze


if __name__ == "__main__":
    # depth first
    """
    """
    d = DepthFirstMazeGenerator("naive", verbosity=0)
    m = d.GenerateMaze(15, 8, )
    d.SetStartEnd(m)
    # m.PrintMaze()
    # m.SaveMaze("DepthFirst.maze")
    # m = LoadMaze("DepthFirst.maze")
    # m.PrintMaze()
    m.CheckMaze()


    """
    # modified prims
    d = ModifiedPrimMazeGenerator("naive", verbosity=0)
    m = d.GenerateMaze(15, 8, )
    d.SetStartEnd(m)
    m.PrintMaze()
    m.SaveMaze("mPrims_naive.maze")
    m.CheckMaze()

    d.SetMaxSteps(125)
    d.SetStartEndRandomAStar(m, None, None)
    m.PrintMaze()
    m.SaveMaze("mPrims_astar.maze")
    """

    """
    d.SetStartEndLongest(m, None, None)
    m.PrintMaze()
    m.SaveMaze("mPrims_longest.maze")
    # m = LoadMaze("mPrims.maze")
    # m.PrintMaze()
    """
