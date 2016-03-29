__author__ = 'best'

import numpy as np
from time import time
from Maze import Maze
from MazeGenerator import DepthFirstMazeGenerator, ModifiedPrimMazeGenerator
from MazeSolver import AStarMazeSolver

if __name__ == "__main__":

    # run some tests here
    stats = np.zeros([1 * 3 * 10, 5])
    row = 0
    for generator in xrange(1):
        for placement in xrange(3):
            for iteration in xrange(10):
                g = None
                t_count = time()
                if generator == 0:
                    g = ModifiedPrimMazeGenerator("naive", 0)
                else:
                    g = DepthFirstMazeGenerator("naive", 0)
                if placement == 1:
                    g.mEndpointMethod = "longest"
                elif placement == 2:
                    g.mEndpointMethod = "astar"

                theMaze = g.GenerateMaze(30, 20)
                g.SetStartEnd(theMaze)
                stats[row, 4] = (time() - t_count) * 1000
                stats[row, 0] = generator
                stats[row, 1] = placement
                solver = AStarMazeSolver(theMaze)
                while not solver.Finished():
                    solver.Step()
                # print solver.mStep, len(solver.mAnswer)
                stats[row, 2] = solver.mStep
                stats[row, 3] = len(solver.mAnswer)
                row += 1
                print generator, placement, iteration

    print "Stats"
    for generator in xrange(1):
        for placement in xrange(3):
            filter = np.logical_and(stats[:,0] == generator, stats[:,1] == placement)
            print "%d, %d: " % (generator, placement)
            print np.mean(stats[filter,2:], axis=0)
            print