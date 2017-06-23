MazeGeneratorApp
--

This is a small QT GUI app created to generate, visualize, and solve mazes.

Dependencies:
* PYQT 4.x (4.8 tested)
* Numpy
* DocOpt

Usage:

Launch by running MazeManager_UI.py.

To create a maze, choose File -> new

to load   .  .     .      .   -> open

New Mazes have the following parameters
* the width of the maze (in cells)
* the height of the maze (in cells)
* which generation algorithm to use:
  * Modified Prim's or Depth First (see wikipedia on maze generation)
* How to place the start and end points of the maze
     * Naive corners: Choose two random opposing corners
     * Longest Path: Seed an A-Star algorithm to generate the longest path possible in (iterations) steps. The algorithms maximizes: path_length + distance(start, end)
     * Randomized A-Star: Seed (iterations) pairs of start and end points and runs a solver against each of them. The longest path is chosen. This can take a LONG TIME.
 * Number of iterations (for goal placement algorithms)
 * The filename under which to store the new maze.

To Play the maze interactively, choose maze -> run maze. Use WSAD to move.

To watch the A-Star solver, choose maze -> solve maze

Todo:
* Enable mouse wheel zooming on the maze.
* Enable panning on the maze.
* Allow the view to be tied to the player solver.
* Substantially reduce the hackiness of the rendering
* Fix repetitions in the maze class. There are too many repeated blocks

Changelog
---
**V.2**

-Added biasing to maze generation. Mazes can now be biased to vertical or horizontal corridors
-Rewrote implementations for wall focus not cell focus. May reduce branching but much easier to deal with.
-Added some randomization based on the roulette wheel algorithm


**V.12**

-Added option to export maze to OBJ in UI integrated CLI tool


**V.11**

-Added command line options to convert a maze to an obj file for use with 3d engines.

**V.1**

-Initial commit. 
