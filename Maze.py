__author__ = 'best'

import numpy as np
from copy import deepcopy
"""
Class to represent a maze
"""
class Maze:
    def __init__(self):
        self.cells = None
        self.initialized = False
        self.start_cell = None
        self.end_cell = None
        self.width = None
        self.height = None

    # Get all borders of a cell
    def GetBorders(self, cell, column=None):
        cell = self._formatCell(cell, column)
        if cell is None:
            return None
        return self.cells[cell[0], cell[1]]

    # Gets only valid exits to the cell
    def GetExits(self, cell, column=None):
        cell = self._formatCell(cell, column)
        if cell is None:
            return None

        exits = self.GetBorders(cell)
        exits = np.arange(4)[exits == 1]
        return exits

    # Get the neighbors of the cell (other cells between which there are no walls from this cell
    def GetNeighborCells(self, cell, column=None):
        cell = self._formatCell(cell, column)
        if cell is None:
            return None

        exits = self.GetExits(cell)
        neighbors = []
        for exit in exits:
            neighbor = deepcopy(cell)
            if exit == 0:
                neighbor[0] -= 1
            elif exit == 1:
                neighbor[1] += 1
            elif exit == 2:
                neighbor[0] += 1
            else:
                neighbor[1] -= 1
            neighbors.append(neighbor)

        return neighbors

    # Is this the start cell
    def IsStart(self, cell, column=None):
        cell = self._formatCell(cell, column)
        if cell is None:
            return None
        return cell == self.start_cell

    # Is this the start cell
    def IsEnd(self, cell, column=None):
        cell = self._formatCell(cell, column)
        if cell is None:
            return None
        return cell == self.end_cell

    def SetDimensions(self, width, height):
        self.width = width
        self.height = height
        self.cells = np.zeros([height, width, 4])
        # -1 means the neighbor doesn't exist
        self.cells[0, :, 0] = -1
        self.cells[-1, :, 2] = -1
        self.cells[:, 0, 3] = -1
        self.cells[:, -1, 1] = -1
        self.start_cell = [0,0]
        self.end_cell = [self.height -1, self.width -1]
        self.initialized = True

    def PrintMaze(self, markCell = None):
        """

        print " " + ("%s " % "-") * self.width
        for row in xrange(self.height):
            row_str = ""

            # print side walls
            for col in xrange(self.width):
                row_str += "%s " % ("|" if self.cells[row, col, 3] < 1 else " ")
            row_str += "|"
            print row_str

            # print bottom walls
            row_str = " "
            for col in xrange(self.width):
                row_str += "%s " % ("-" if self.cells[row, col, 2] < 1 else " ")
            print row_str
        """
        cell = np.zeros(2)
        for row in xrange(self.height):
            row_str = ""

            # print side walls
            for col in xrange(self.width):
                cell = [row, col]
                us = " "
                if markCell == cell:
                    us = "X"
                elif self.IsStart(cell):
                    us = "S"
                elif self.IsEnd(cell):
                    us = "E"
                elif self.cells[row, col, 2] < 1:
                    us = "_"
                row_str += "%s%s" % ("|" if self.cells[row, col, 3] < 1 else " ",
                                     us)
            row_str += "|"
            print row_str
        print

    def SaveMaze(self, filename):
        with open(filename, "w+") as fp:
            fp.write("%d %d %d %d %d %d\n" % (self.height, self.width, self.start_cell[0],
                                           self.start_cell[1], self.end_cell[0], self.end_cell[1])
                    )
            for row in xrange(self.height):
                for col in xrange(self.width):
                    for wall in xrange(4):
                        fp.write("%d "% self.cells[row, col, wall])
                    fp.write("\n")

    def _formatCell(self, cell, column):
        if not self.initialized:
            return None

        if type(cell) != list and type(cell) != np.array:
            if column is None:
                return None
            else:
                return [cell, column]

        return cell

    # checks the maze for inconsistancies and returns them
    def CheckMaze(self):
        problems = []
        # for each cell... make sure it agrees with its right most and bottom neighbor
        for row in xrange(self.height):
            for column in xrange(self.width):
                cell_borders = self.GetBorders(row, column)
                if cell_borders[1] != -1:
                    other_borders = self.GetBorders(row, column + 1)
                    if other_borders[3] != cell_borders[1]:
                        problems.append([[row,column],1])
                        print "PROBLEM", row, column, 1, cell_borders, other_borders
                if cell_borders[2] != -1:
                    other_borders = self.GetBorders(row + 1, column)
                    if other_borders[0] != cell_borders[2]:
                        problems.append([[row,column],2])
                        print "PROBLEM", row, column, 2, cell_borders, other_borders

    # computes branching stats
    # total number of brances [0]
    # average branching factor [1]
    # branch chance (percent chance a cell branches)

    def BranchingStats(self):
        branch_count = 0
        move_count = 0
        total_cells = self.height * self.width
        # for each cell... make sure it agrees with its right most and bottom neighbor
        for row in xrange(self.height):
            for column in xrange(self.width):
                cell_borders = self.GetBorders(row, column)
                cell_branches = np.count_nonzero(cell_borders == 1)
                move_count += cell_branches
                if cell_branches > 2:
                    branch_count += (cell_branches - 2)


        branch_factor = float(move_count) / float(total_cells)
        branch_chance = float(branch_count) / float(total_cells)
        return branch_count, branch_factor, branch_chance

def LoadMaze(filename):
    theMaze = Maze()
    with open(filename, "r") as fp:
        cell = [0, 0]
        width = 0
        height = 0
        for line in fp:
            # print "LINE", line.strip()
            line_clean = line.strip().split(" ")
            line_clean = map(int, line_clean)
            if len(line_clean) == 6:
                width = line_clean[1]
                height = line_clean[0]
                theMaze.SetDimensions(width, height)
                theMaze.start_cell = [line_clean[2], line_clean[3]]
                theMaze.end_cell = [line_clean[4], line_clean[5]]
            elif len(line_clean) == 4:
                for wall in xrange(4):
                    theMaze.cells[cell[0], cell[1], wall] = line_clean[wall]
                cell[1] += 1
                if cell[1] == width:
                    cell[1] = 0
                    cell[0] += 1
    return theMaze



if __name__ == "__main__":
    m = Maze()
    m.SetDimensions(12, 12)
    m.PrintMaze()
    m.SaveMaze("default.maze")
    print
    m = LoadMaze("default.maze")
    m.PrintMaze()
