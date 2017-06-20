"""

This file does exactly what it claims to, convert a maze to an obj
"""

import numpy as np
from Maze import Maze, LoadMaze
from copy import copy

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
        maze_length_offset = -maze_length_meters / 2.0

        print "maze dimensions: %d x %d cells (total: %d). %0.4f x %0.4f meters." %(
            maze.width, maze.height, maze.width * maze.height,
            maze_width_meters, maze_length_meters
        )

        print "Up to %d vertices will be generated" % (
            maze.width * maze.height * 2 * 8
        )

        if simplify:
            raise NotImplementedError("Haven't gotten around to this yet")

        # dump each wall at the give height and size
        all_vertices = []
        all_faces = []

        # there are 8 uv coords
        #     the 4 corners normally
        #     and 2 short ones per axis for small faces
        #     5 and 6 are 0, short and 1, short
        #     7 and 8 are short,0 and short, 1

        v_small_faces = (wall_width / cell_width)


        for row in xrange(maze.height):
        # for row in [0]:
            print "row %d of %d" % (row, maze.height)

            for column in xrange(maze.width):
                # a note.  ithink objs are y up.

                if open_exits and maze.IsEnd(row, column) or maze.IsStart(row, column):
                    skip_first = True
                else:
                    skip_first = False
                skipped_first = False
        #   for column in [0]:
                # get the top corner
                cell_top_x = column * (cell_width + wall_width) + maze_width_offset
                cell_top_y = row * (cell_width + wall_width) + maze_length_offset

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
                        if skip_first and not skipped_first and cell_borders[border] <0:
                            skipped_first = True
                            continue

                        # setup a basic uv set which we will ajdust later
                        base_uvs = [3,4,2,1]
                        uvs = []

                        vertices = []
                        # north wall
                        if border == 0:
                            # the 8 vertices are located above the cell
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x, height, cell_top_y),
                                    # add wall width?
                                    Vertex(cell_top_x + cell_width, height, cell_top_y),
                                    Vertex(cell_top_x + cell_width, height, cell_top_y- wall_width),
                                    Vertex(cell_top_x,  height, cell_top_y - wall_width),
                                ]

                            # adjust length if we're first row and there is
                            # no left wall
                            if row == 0:
                                vertices[0].coords[0] -= wall_width
                                vertices[3].coords[0] -= wall_width
                                vertices[4].coords[0] -= wall_width
                                vertices[7].coords[0] -= wall_width


                        # east wall
                        elif border == 1:
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x + cell_width,
                                            height,
                                           cell_top_y + cell_width),
                                    Vertex(cell_top_x + cell_width + wall_width,
                                            height,
                                           cell_top_y + cell_width),
                                    Vertex(cell_top_x + cell_width + wall_width,
                                            height,
                                           cell_top_y- wall_width),
                                    Vertex(cell_top_x + cell_width,
                                            height,
                                           cell_top_y- wall_width),
                                ]


                        # south  wall
                        elif border == 2:

                            # the 8 vertices are located above the cell
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x,
                                            height,
                                           cell_top_y + cell_width + wall_width),
                                    Vertex(cell_top_x + cell_width,
                                            height,
                                           cell_top_y + cell_width + wall_width),
                                    Vertex(cell_top_x + cell_width,
                                            height,
                                           cell_top_y + cell_width),
                                    Vertex(cell_top_x,
                                            height,
                                           cell_top_y + cell_width),
                                ]

                            # if there is no west wall then we need to
                            # extend this to cover corners
                            if cell_borders[3] >=1:
                                vertices[0].coords[0] -= wall_width
                                vertices[3].coords[0] -= wall_width
                                vertices[4].coords[0] -= wall_width
                                vertices[7].coords[0] -= wall_width



                        # west wall
                        elif border == 3:
                            for height in [0, wall_height]:
                                vertices += [
                                    Vertex(cell_top_x - wall_width,
                                            height,
                                           cell_top_y + cell_width),
                                    Vertex(cell_top_x,
                                            height,
                                           cell_top_y + cell_width),
                                    Vertex(cell_top_x,
                                            height,
                                           cell_top_y - wall_width),
                                    Vertex(cell_top_x - wall_width,
                                            height,
                                           cell_top_y- wall_width)
                                ]

                        # setup uvs
                        if border == 0 or border == 2:
                            # bottom
                            uvs.append(copy(base_uvs))
                            uvs[-1][0] = 5
                            uvs[-1][1] = 6

                            # south
                            uvs.append(copy(base_uvs))

                            # east
                            uvs.append(copy(base_uvs))
                            uvs[-1][1] = 8
                            uvs[-1][2] = 7

                            #north
                            uvs.append(copy(base_uvs))

                            # west
                            uvs.append(copy(base_uvs))
                            uvs[-1][1] = 8
                            uvs[-1][2] = 7

                            # top
                            uvs.append(copy(base_uvs))
                            uvs[-1][0] = 5
                            uvs[-1][1] = 6

                        elif border == 1 or border == 3:
                            uvs.append(copy(base_uvs))
                            uvs[-1][1] = 8
                            uvs[-1][2] = 7

                            # south
                            uvs.append(copy(base_uvs))
                            uvs[-1][1] = 8
                            uvs[-1][2] = 7

                            # east
                            uvs.append(copy(base_uvs))


                            #north
                            uvs.append(copy(base_uvs))
                            uvs[-1][1] = 8
                            uvs[-1][2] = 7


                            # west
                            uvs.append(copy(base_uvs))

                            # top
                            uvs.append(copy(base_uvs))
                            uvs[-1][1] = 8
                            uvs[-1][2] = 7
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
                            Face([vertex_indices[3],
                                  vertex_indices[2],
                                  vertex_indices[1],
                                  vertex_indices[0],],
                                 uvs[0][::-1]),

                            # south face
                            Face([vertex_indices[0],
                                  vertex_indices[1],
                                  vertex_indices[5],
                                  vertex_indices[4],],
                                 uvs[1]),

                            # east face
                            Face([vertex_indices[1],
                                  vertex_indices[2],
                                  vertex_indices[6],
                                  vertex_indices[5]],
                                 uvs[2]),

                            # north face
                            Face([vertex_indices[2],
                                  vertex_indices[3],
                                  vertex_indices[7],
                                  vertex_indices[6],],
                                 uvs[3]),

                            # west
                            Face([vertex_indices[3],
                                  vertex_indices[0],
                                  vertex_indices[4],
                                  vertex_indices[7],],
                                 uvs[4]),

                            # top face
                            Face([vertex_indices[4],
                                  vertex_indices[5],
                                  vertex_indices[6],
                                  vertex_indices[7],],
                                 uvs[5]),

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
vt 0 %0.4f
vt 1 %0.4f
vt %0.4f 0
vt %0.4f 1
""" % (v_small_faces, v_small_faces, v_small_faces, v_small_faces))
            fp.write("\n")

            for face in all_faces:
                fp.write(face.objRepr() + "\n")

        print " Generated %d vertices and %d faces " % (
            len(all_vertices), len(all_faces)
        )
if __name__ == "__main__":
    #m = LoadMaze("Difficult1.maze")
    #MazeToObj(m, 1, .1, 1, "HardMaze.obj", open_exits=True)
    m = LoadMaze("TestMaze1.maze")
    MazeToObj(m, 1, .1, 1, "EasyMaze1.obj", open_exits=True)

    print "generated new file"
