"""

This file does exactly what it claims to, convert a maze to an obj
"""

import numpy as np

from Maze import Maze, LoadMaze

# define a vertex class for easy searching
class Vertex(object):
    def __init__(self, x, y, z):
        self.coords = np.array([x,y,z])

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    def Set(self, x=None, y=None, z=None):
        if x is not None:
            self.coords[0] = x
        if y is not None:
            self.coords[1] = y
        if z is not None:
            self.coords[2] = z

    # helper method because I don't like unpredictable equality
    def _isEqual(self, other):
        if type(other) != type(self):
            return False

        else:
            return np.array_equal(self.coords, other.coords)

    def __eq__(self, other):
        return self._isEqual(other)

    def __ne__(self, other):
        return not self._isEqual(other)

    # componentwise add
    def __add__(self, other):
        if type(other) != type(self):
            raise ValueError("Cannot add unlike types")

        new_coords = self.coords + other.coords

        return Vertex(
            new_coords[0],
            new_coords[1],
            new_coords[2],
        )

    def __repr__(self):
        return "V<%0.04f,%0.04f, %0.04f>" % (
            self.x, self.y, self.z
        )
    def objRepr(self):
        return "v %0.04f %0.04f %0.04f" % (
            self.x, self.y, self.z
        )

# face class for easy searching
class Face(object):
    def __init__(self, vertex_indices, texture_vertex_indices = []):
        self.vertex_indices = np.array(vertex_indices)
        self.texture_vertex_indices = texture_vertex_indices

    def _isEqual(self, other):
        if type(self) != type(other):
            return False

        for item in self.vertex_indices:
            if item not in other.vertex_indices:
                return False

        return True


    def __eq__(self, other):
        return self._isEqual(other)

    def __ne__(self, other):
        return not self._isEqual(other)

    def __repr__(self):
        retStr = "Face<"
        for vertex in self.vertex_indices:
            retStr += "%d," % vertex

        retStr += ">"

        return retStr

    def objRepr(self):
        theRepr = "f "
        for index in xrange(len(self.vertex_indices)):
            if len(self.texture_vertex_indices) > 0:
                theRepr += "%d/%d " % (
                    self.vertex_indices[index],
                    self.texture_vertex_indices[index])
            else:
                theRepr += "%d " % self.vertex_indices[index]

        return theRepr

def MazeToObj(maze, cell_width, wall_width, wall_height,
              file_name,
              open_exits=False, simplify=False):

        # get the size of the maze to find the offset for the origin

        maze_width_meters = (cell_width + wall_width) * maze.width + wall_width
        maze_length_meters = (cell_width + wall_width) * maze.height + wall_width
        maze_width_offset = -maze_width_meters / 2.0
        maze_length_offset = -maze_width_meters / 2.0

        if simplify:
            raise NotImplementedError("Haven't gotten around to this yet")

        # dump each wall at the give height and size
        all_vertices = []
        all_faces = []

        for row in xrange(maze.height):
        # for row in [0]:
            for column in xrange(maze.width):
                if open_exits and maze.IsEnd(row, column) or maze.IsStart(row, column):
                    skip_first = True
                else:
                    skip_first = False
                skipped_first = False
        #   for column in [0]:
                # get the top corner
                cell_top_x = column * cell_width + wall_width + maze_width_offset
                cell_top_y = row * cell_width + wall_width + maze_length_offset

                cell_borders = maze.GetBorders(row, column)

                # special rules for some rows
                skip_borders = []
                if row > 0:
                    skip_borders.append(0)
                if column > 0:
                    skip_borders.append(3)
                for border in xrange(len(cell_borders)):
                    if border in skip_borders:
                        continue

                    # if there is a wall here
                    if cell_borders[border] < 1:
                        if skip_first and not skipped_first:
                            skipped_first = True
                            continue

                        vertices = []
                        # north wall
                        if border == 0:

                            # the 8 vertices are located above the cell
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x, cell_top_y, height),
                                    # add wall width?
                                    Vertex(cell_top_x + cell_width, cell_top_y, height),
                                    Vertex(cell_top_x + cell_width, cell_top_y- wall_width, height),
                                    Vertex(cell_top_x, cell_top_y - wall_width, height),
                                ]
                        # east wall
                        elif border == 1:
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x + cell_width,
                                           cell_top_y + cell_width, height),
                                    Vertex(cell_top_x + cell_width + wall_width,
                                           cell_top_y + cell_width, height),
                                    Vertex(cell_top_x + cell_width + wall_width,
                                           cell_top_y, height),
                                    Vertex(cell_top_x + cell_width,
                                           cell_top_y, height),
                                ]
                        # south  wall
                        elif border == 2:

                            # the 8 vertices are located above the cell
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x,
                                           cell_top_y + cell_width + wall_width,
                                           height),
                                    Vertex(cell_top_x + cell_width,
                                           cell_top_y + cell_width + wall_width,
                                           height),
                                    Vertex(cell_top_x + cell_width,
                                           cell_top_y + cell_width,
                                           height),
                                    Vertex(cell_top_x,
                                           cell_top_y + cell_width,
                                           height),
                                ]
                        elif border == 3:
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x - wall_width,
                                           cell_top_y + cell_width, height),
                                    Vertex(cell_top_x,
                                           cell_top_y + cell_width, height),
                                    Vertex(cell_top_x,
                                           cell_top_y, height),
                                    Vertex(cell_top_x - wall_width,
                                           cell_top_y, height)
                                ]

                        # print vertices

                        #add the veritces to the list
                        vertex_indices = []
                        for vertex in vertices:
                            if vertex not in all_vertices:
                                all_vertices.append(vertex)
                                vertex_indices.append(len(all_vertices))
                            else:
                                vertex_indices.append(
                                    all_vertices.index(vertex) + 1
                                )

                        # setup the faces manually
                        faces = [
                            # bottom face
                            Face([vertex_indices[0],
                                  vertex_indices[1],
                                  vertex_indices[2],
                                  vertex_indices[3],],
                                 [3,2,1,0]),

                            # south face
                            Face([vertex_indices[0],
                                  vertex_indices[1],
                                  vertex_indices[5],
                                  vertex_indices[4],],
                                 [2,3,1,0]),

                            # east face
                            Face([vertex_indices[1],
                                  vertex_indices[2],
                                  vertex_indices[6],
                                  vertex_indices[5]],
                                 [2,3,1,0]),

                            # north face
                            Face([vertex_indices[2],
                                  vertex_indices[3],
                                  vertex_indices[7],
                                  vertex_indices[6],],
                                 [2,3,1,0]),

                            # west
                            Face([vertex_indices[3],
                                  vertex_indices[0],
                                  vertex_indices[4],
                                  vertex_indices[7],],
                                 [2,3,1,0]),

                            # top face
                            Face([vertex_indices[4],
                                  vertex_indices[5],
                                  vertex_indices[6],
                                  vertex_indices[7],],
                                 [2,3,1,0]),

                        ]

                        for faces in faces:
                            if faces not in all_faces:
                                all_faces.append(faces)



        # output all the vertices and faces to a file
        with open(file_name, "w+") as fp:

            # vertices
            for vertex in all_vertices:
                fp.write(vertex.objRepr() + "\n")

            #texture coordinates
            fp.write("""
vt 0 0
vt 1 0
vt 0 1
vt 1 1
""")
            fp.write("\n")
            for face in all_faces:
                fp.write(face.objRepr() + "\n")

if __name__ == "__main__":
    m = LoadMaze("TestMaze1.maze")
    #m.PrintMaze()
    MazeToObj(m, 1, .1, 1, "TestMaze1.obj", open_exits=True)

