__author__ = 'best'

from copy import deepcopy
import numpy as np
from scipy.spatial.distance import euclidean
from Maze import Maze


"""
Base class for maze solvers.

Solvers need only have a step function and a finished bool function and take a maze in their constructor

"""
class MazeSolver(object):
    def __init__(self, maze):
        self.mMaze = maze
        self.mFinished = False
        self.mAnswer = None
        self.moves = []

    def Finished(self):
        return self.mFinished

    def Step(self):
        raise NotImplementedError

class AStarMazeSolver(MazeSolver):
    def __init__(self, maze, verbosity=0):
        super(AStarMazeSolver, self).__init__(maze)
        self.mVerbosity = verbosity

        #create AStar specific information for the maze
        self.mNodeHeap = []
        self.mVisitedList = []
        self.mStep = 0
        self.mHScale = 2.0

        # solve the maze backwards
        # self.mCurrentNode = self.mMaze.end_cell
        # self.mTargetNode = self.mMaze.start_cell
        self.mCurrentNode = self.mMaze.start_cell
        self.mTargetNode = self.mMaze.end_cell
        self.AddNodeToHeap(self.mCurrentNode, [])

    # Add a node to my A-Star Heap
    def AddNodeToHeap(self, node, path):
        if node in self.mVisitedList:
            return

        self.mNodeHeap.append((
            node,
            path + [node],
            len(path) + euclidean(node, self.mTargetNode) * self.mHScale
        ))

    def Step(self):
        if self.Finished():
            return

        # print my current node if I am in verbose mode
        nodeToVisit = self.mNodeHeap[0]
        self.mCurrentNode = nodeToVisit[0]
        self.mCurrentPath = nodeToVisit[1]

        self.mNodeHeap.pop(0)
        self.mVisitedList.append(nodeToVisit[0])
        self.mStep += 1
        if self.mVerbosity > 0:
            print "Step", self.mStep, nodeToVisit[0],"-",nodeToVisit[2]

        if nodeToVisit[0] == self.mTargetNode:
            self.mFinished = True
            if self.mVerbosity > 0:
                print "Maze Solved"
            self.mAnswer = nodeToVisit[1]
            # self.mAnswer.reverse()

        # add the node's children to the node list
        for child in self.mMaze.GetNeighborCells(nodeToVisit[0]):
            if child not in self.mVisitedList:
                if self.mVerbosity > 0:
                    print "    add child", child
                self.AddNodeToHeap(child,nodeToVisit[1])

        # sort the list
        self.mNodeHeap.sort(key=lambda x: x[2])

"""
Interactive Maze Solver
"""
class InteractiveMazeSolver(MazeSolver):
    def __init__(self, maze, verbosity=0):
        super(InteractiveMazeSolver, self).__init__(maze)
        self.mVerbosity = verbosity
        self.mCurrentNode = self.mMaze.start_cell
        self.mExitDirMap = {
            "n": (0, "(N)orth"),
            "e": (1, "(E)ast"),
            "s": (2, "(S)outh"),
            "w": (3, "(W)est"),
        }

        self.mExitDirList = np.arange(4)

    def Step(self):
        if len(self.moves) > 0 and not self.Finished():
            self.HandleMoves()

    def HandleMoves(self):
        needExits = True
        exits = None
        neighbors = None
        valid_moves = []
        while len(self.moves) > 0:
            move = self.moves[0]
            self.moves.pop(0)
            if needExits:
                exits = np.array(self.mMaze.GetExits(self.mCurrentNode))
                neighbors = np.array(self.mMaze.GetNeighborCells(self.mCurrentNode))

                valid_choices = []
                for key, item in self.mExitDirMap.items():
                    if item[0] in exits:
                        valid_choices.append(key)
                needExits = False

            if move not in valid_choices:
                continue

            self.mCurrentNode = list(neighbors[exits == self.mExitDirMap[move][0]][0])

            needExits = True
            if self.mMaze.IsEnd(self.mCurrentNode):
                self.mFinished = True
                if self.mVerbosity > 0:
                    print "Maze Solved"
                return

class BlockingPlayerMazeSolver(InteractiveMazeSolver):

    def Step(self):
        super(BlockingPlayerMazeSolver, self).Step()

        if self.Finished():
            return

        # Print the maze, mark my cell, ask for next move
        self.mMaze.PrintMaze(markCell=self.mCurrentNode)
        print "You are located at: (%d, %d). Exits are: " % (self.mCurrentNode[0], self.mCurrentNode[1]),

        # array casting lets me shortcut my indexing later (lazy and bad)
        exits = np.array(self.mMaze.GetExits(self.mCurrentNode))
        neighbors = np.array(self.mMaze.GetNeighborCells(self.mCurrentNode))
        if self.mVerbosity > 0:
            print
            print "    Exits: ", exits
            print "    Neighbors ", neighbors
            if self.mVerbosity > 1:
                for neighbor in neighbors:
                    print "        NEIGHBOR EXITS", neighbor, self.mMaze.GetExits(list(neighbor))
        valid_choices = []
        for key, item in self.mExitDirMap.items():
            if item[0] in exits:
                print "%s, "% item[1],
                valid_choices.append(key)
        direction = None
        while direction is None:
            direction = raw_input("Where do you go? ")

            if len(direction) == 0 or direction.lower()[0] not in valid_choices:
                direction = None
            else:
                direction = direction.lower()[0]

        self.moves.append(direction)

if __name__ == "__main__":
    from Maze import LoadMaze
    m = LoadMaze("mPrims_naive.maze")
    m.PrintMaze()

    solver = AStarMazeSolver(m, 0)
    while not solver.Finished():
        solver.Step()
    print solver.mStep, len(solver.mAnswer)
    print solver.mAnswer

    solver = BlockingPlayerMazeSolver(m, 2)
    while not solver.Finished():
        solver.Step()