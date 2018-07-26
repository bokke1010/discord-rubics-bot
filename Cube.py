DIRECTIONS = (
        ( 1,  0,  0), #right
        ( 0,  1,  0), #up
        ( 0,  0,  1), #front 
        (-1,  0,  0), #left
        ( 0, -1,  0), #down
        ( 0,  0, -1)  #back
    )

DIRECTIONS_NAME = dict(zip(DIRECTIONS, "rufldb"))

class Cube():
    # The six directions

    def cross(self, axis, direction):
        # cross product
        return (axis[1]*direction[2] - axis[2]*direction[1],
                axis[2]*direction[0] - axis[0]*direction[2],
                axis[0]*direction[1] - axis[1]*direction[0])

    def dot(self, va, vb):
        # dot product
        return sum(a*b for (a,b) in zip(va,vb))

    def scale(self, alpha, v):
        # scaling a vector
        (x,y,z) = v
        return (alpha*x, alpha*y, alpha*z)

    def add(self, u, v):
        # adding two vectors
        return (u[0] + v[0], u[1] + v[1], u[2] + v[2])

    def rotate(self, axis, u):
        # rotation by a quarter in the
        # positive sense around a normal vector.
        axis_projection = self.scale(self.dot(axis,u), axis)
        ortho_projection = self.cross(axis, u)
        return self.add(axis_projection, ortho_projection)

