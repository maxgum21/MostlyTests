import PixelEngine
from math import pi, tan, cos, sin, sqrt


class Vector:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return f'({self.x} {self.y} {self.z})'

    def __add__(self, other):
        return Vector(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other):
        return Vector(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __mul__(self, other):
        if other.__class__ == self.__class__:
            return Vector(x=self.x * other.x, y=self.y * other.y, z=self.z * other.z)
        return Vector(x=self.x * other, y=self.y * other, z=self.z * other)

    def __truediv__(self, other):
        if other.__class__ == self.__class__:
            return Vector(x=self.x / other.x, y=self.y / other.y, z=self.z / other.z)
        return Vector(x=self.x / other, y=self.y / other, z=self.z / other)

    def length(self):
        return sqrt(self.dot_product(self))

    def dot_product(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def cross_product(self, vector):
        rv = Vector()
        rv.x = self.y * vector.z - self.z * vector.y
        rv.y = self.z * vector.x - self.x * vector.z
        rv.z = self.x * vector.y - self.y * vector.x
        return rv

    def normalise(self):
        l = self.length()
        self /= l
        return self


class Triangle:
    def __init__(self, tl=[Vector()] * 3, name='StandardTriangle'):
        self.name = name
        self.vecList = tl
        self.col = 0

    def get_middle_point(self, axis):
        if axis == 'x':
            return sum([vec.x for vec in self.vecList]) / 3
        if axis == 'y':
            return sum([vec.y for vec in self.vecList]) / 3
        if axis == 'z':
            return sum([vec.z for vec in self.vecList]) / 3


class Matrix4x4:
    def __init__(self):
        self.mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def matrix_quick_invert(self):
        matrix = Matrix4x4()
        matrix.mat[0][0] = self.mat[0][0]
        matrix.mat[0][1] = self.mat[1][0]
        matrix.mat[0][2] = self.mat[2][0]
        matrix.mat[0][3] = 0.0

        matrix.mat[1][0] = self.mat[0][1]
        matrix.mat[1][1] = self.mat[1][1]
        matrix.mat[1][2] = self.mat[2][1]
        matrix.mat[1][3] = 0.0

        matrix.mat[2][0] = self.mat[0][2]
        matrix.mat[2][1] = self.mat[1][2]
        matrix.mat[2][2] = self.mat[2][2]
        matrix.mat[2][3] = 0.0

        matrix.mat[3][0] = -(self.mat[3][0] * matrix.mat[0][0] + self.mat[3][1] * matrix.mat[1][0] + self.mat[3][2] *
                             matrix.mat[2][0])
        matrix.mat[3][1] = -(self.mat[3][0] * matrix.mat[0][1] + self.mat[3][1] * matrix.mat[1][1] + self.mat[3][2] *
                             matrix.mat[2][1])
        matrix.mat[3][2] = -(self.mat[3][0] * matrix.mat[0][2] + self.mat[3][1] * matrix.mat[1][2] + self.mat[3][2] *
                             matrix.mat[2][2])
        matrix.mat[3][3] = 1.0

        return matrix


class MatrixRotX(Matrix4x4):
    def __init__(self, theta):
        super().__init__()
        self.mat[0][0] = 1
        self.mat[1][1] = cos(theta)
        self.mat[1][2] = sin(theta)
        self.mat[2][1] = -sin(theta)
        self.mat[2][2] = cos(theta)
        self.mat[3][3] = 1


class MatrixRotY(Matrix4x4):
    def __init__(self, theta):
        super().__init__()
        self.mat[0][0] = cos(-theta)
        self.mat[0][2] = sin(-theta)
        self.mat[1][1] = 1
        self.mat[2][0] = -sin(-theta)
        self.mat[2][2] = cos(-theta)
        self.mat[3][3] = 1


class MatrixRotZ(Matrix4x4):
    def __init__(self, theta):
        super().__init__()
        self.mat[0][0] = cos(theta)
        self.mat[0][1] = sin(theta)
        self.mat[1][0] = -sin(theta)
        self.mat[1][1] = cos(theta)
        self.mat[2][2] = 1
        self.mat[3][3] = 1


class Mesh:
    def __init__(self):
        self.triList = []

    def LoadObject(self, filename):
        vl = []
        fl = []
        if 1:
            with open(file=filename) as f:
                for line in f:
                    l = line.split(' ')
                    if l[0] == 'v':
                        vl.append([float(l[1]), float(l[2]), float(l[3])])
                    elif l[0] == 'f':
                        fl.append([int(l[1].rstrip('\n').rstrip('/')), int(l[2].rstrip('\n').rstrip('/')),
                                   int(l[3].rstrip('\n').rstrip('/'))])
                    else:
                        continue
                for f in fl:
                    self.triList.append(Triangle([Vector(vl[f[0] - 1][0], vl[f[0] - 1][1], vl[f[0] - 1][2]),
                                                  Vector(vl[f[1] - 1][0], vl[f[1] - 1][1], vl[f[1] - 1][2]),
                                                  Vector(vl[f[2] - 1][0], vl[f[2] - 1][1], vl[f[2] - 1][2])]))


class CubeMesh(Mesh):
    def __init__(self):
        self.triList = [Triangle([Vector(0.0, 0.0, 0.0), Vector(0.0, 1.0, 0.0), Vector(1.0, 1.0, 0.0)]),  # SOUTH
                        Triangle([Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 0.0), Vector(1.0, 0.0, 0.0)]),
                        Triangle([Vector(1.0, 0.0, 0.0), Vector(1.0, 1.0, 0.0), Vector(1.0, 1.0, 1.0)]),  # EAST
                        Triangle([Vector(1.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0), Vector(1.0, 0.0, 1.0)]),
                        Triangle([Vector(1.0, 0.0, 1.0), Vector(1.0, 1.0, 1.0), Vector(0.0, 1.0, 1.0)]),  # NORTH
                        Triangle([Vector(1.0, 0.0, 1.0), Vector(0.0, 1.0, 1.0), Vector(0.0, 0.0, 1.0)]),
                        Triangle([Vector(0.0, 0.0, 1.0), Vector(0.0, 1.0, 1.0), Vector(0.0, 1.0, 0.0)]),  # WEST
                        Triangle([Vector(0.0, 0.0, 1.0), Vector(0.0, 1.0, 0.0), Vector(0.0, 0.0, 0.0)]),
                        Triangle([Vector(0.0, 1.0, 0.0), Vector(0.0, 1.0, 1.0), Vector(1.0, 1.0, 1.0)]),  # TOP
                        Triangle([Vector(0.0, 1.0, 0.0), Vector(1.0, 1.0, 1.0), Vector(1.0, 1.0, 0.0)]),
                        Triangle([Vector(1.0, 0.0, 1.0), Vector(0.0, 0.0, 1.0), Vector(0.0, 0.0, 0.0)]),  # BOTTOM
                        Triangle([Vector(1.0, 0.0, 1.0), Vector(0.0, 0.0, 0.0), Vector(1.0, 0.0, 0.0)])]


class Engine3D(PixelEngine.PxlEngine):
    def __init__(self, w, h, pixel_w, pixel_h, mesh=CubeMesh(), scale=1, name='3D_Engine_Project'):
        super().__init__(w, h, pixel_w, pixel_h, name)
        self.thetaX, self.thetaY, self.thetaZ = 0, 0, 0
        self.th = 0.0
        self.mesh = mesh
        self.scale = scale
        zNear, zFar = 0.1, 1000.0
        fov = pi / 4
        aspectR = h / w
        fovRad = 1 / tan(fov)
        self.projMatrix = Matrix4x4()
        self.projMatrix.mat[0][0] = fovRad * aspectR
        self.projMatrix.mat[1][1] = fovRad
        self.projMatrix.mat[2][2] = zFar / (zFar - zNear)
        self.projMatrix.mat[3][2] = (zNear * -zFar) / (zFar - zNear)
        self.projMatrix.mat[2][3] = 1.0
        self.projMatrix.mat[3][3] = 0
        self.camera = Vector()
        self.paused = 0

    def on_user_update(self, deltaTime):

        if 'space' in self.t_keys:
            if self.paused:
                self.paused = 0
            else:
                self.paused = 1

        if not self.paused:
            self.fill_screen((0, 0, 0))
            self.thetaZ += 0 * deltaTime
            self.thetaX += 0 * deltaTime
            self.thetaY += 1 * deltaTime

            yRotMatrix = MatrixRotY(self.thetaY)
            xRotMatrix = MatrixRotX(self.thetaX)
            zRotMatrix = MatrixRotZ(self.thetaZ)

            trianglesToRender = set()

            for tri in self.mesh.triList:
                triProjected = Triangle(name='Proj')
                triTranslated = Triangle(name='Trans')
                triRotZ = Triangle(name='rotz')
                triRotZX = Triangle(name='rotzx')
                triRotZXY = Triangle(name='roty')

                triRotZ.vecList[0] = self.Multiply_Vector_Matrix(tri.vecList[0], zRotMatrix)  # Rotation Z
                triRotZ.vecList[1] = self.Multiply_Vector_Matrix(tri.vecList[1], zRotMatrix)
                triRotZ.vecList[2] = self.Multiply_Vector_Matrix(tri.vecList[2], zRotMatrix)

                triRotZX.vecList[0] = self.Multiply_Vector_Matrix(triRotZ.vecList[0], xRotMatrix)  # Rotation X
                triRotZX.vecList[1] = self.Multiply_Vector_Matrix(triRotZ.vecList[1], xRotMatrix)
                triRotZX.vecList[2] = self.Multiply_Vector_Matrix(triRotZ.vecList[2], xRotMatrix)

                triRotZXY.vecList[0] = self.Multiply_Vector_Matrix(triRotZX.vecList[0], yRotMatrix)  # Rotation Y
                triRotZXY.vecList[1] = self.Multiply_Vector_Matrix(triRotZX.vecList[1], yRotMatrix)
                triRotZXY.vecList[2] = self.Multiply_Vector_Matrix(triRotZX.vecList[2], yRotMatrix)

                triTranslated = triRotZXY  # Changing location to see the cube
                triTranslated.vecList[0].x = triRotZXY.vecList[0].x * self.scale
                triTranslated.vecList[1].x = triRotZXY.vecList[1].x * self.scale
                triTranslated.vecList[2].x = triRotZXY.vecList[2].x * self.scale
                triTranslated.vecList[0].y = triRotZXY.vecList[0].y * self.scale
                triTranslated.vecList[1].y = triRotZXY.vecList[1].y * self.scale
                triTranslated.vecList[2].y = triRotZXY.vecList[2].y * self.scale
                triTranslated.vecList[0].z = triRotZXY.vecList[0].z * self.scale + 3
                triTranslated.vecList[1].z = triRotZXY.vecList[1].z * self.scale + 3
                triTranslated.vecList[2].z = triRotZXY.vecList[2].z * self.scale + 3
                triTranslated.name = 'trans'

                # triTranslated.vecList[0].z += cos(self.thetaY - 90)/2
                # triTranslated.vecList[1].z += cos(self.thetaY - 90)/2
                # triTranslated.vecList[2].z += cos(self.thetaY - 90)/2
                #
                # triTranslated.vecList[0].x += sin(self.thetaY - 90)/2
                # triTranslated.vecList[1].x += sin(self.thetaY - 90)/2
                # triTranslated.vecList[2].x += sin(self.thetaY - 90)/2

                normal, line1, line2 = Vector(), Vector(), Vector()

                line1.x = triTranslated.vecList[1].x - triTranslated.vecList[0].x
                line1.z = triTranslated.vecList[1].z - triTranslated.vecList[0].z
                line1.y = triTranslated.vecList[1].y - triTranslated.vecList[0].y

                line2.x = triTranslated.vecList[2].x - triTranslated.vecList[0].x
                line2.y = triTranslated.vecList[2].y - triTranslated.vecList[0].y
                line2.z = triTranslated.vecList[2].z - triTranslated.vecList[0].z

                normal.x = line1.y * line2.z - line1.z * line2.y
                normal.y = line1.z * line2.x - line1.x * line2.z
                normal.z = line1.x * line2.y - line1.y * line2.x

                n = sqrt(normal.x ** 2 + normal.y ** 2 + normal.z ** 2)
                if n != 0:
                    normal.x /= n
                    normal.y /= n
                    normal.z /= n
                else:
                    normal = Vector()

                nval = normal.x * (triTranslated.vecList[0].x - self.camera.x) + normal.y * (
                        triTranslated.vecList[0].y - self.camera.y) + normal.z * (
                               triTranslated.vecList[0].z - self.camera.z)

                if nval < 0:
                    light = Vector(0, 0, -1)
                    l = sqrt(light.x ** 2 + light.y ** 2 + light.z ** 2)
                    light.x /= l
                    light.y /= l
                    light.z /= l
                    lval = light.x * normal.x + light.y * normal.y + light.z * normal.z
                    if lval >= 0:
                        triProjected.col = 255 * lval

                    # Projecting 3D -> 2D
                    triProjected.vecList[0] = self.Multiply_Vector_Matrix(triTranslated.vecList[0], self.projMatrix)
                    triProjected.vecList[1] = self.Multiply_Vector_Matrix(triTranslated.vecList[1], self.projMatrix)
                    triProjected.vecList[2] = self.Multiply_Vector_Matrix(triTranslated.vecList[2], self.projMatrix)

                    triProjected.vecList[0].x += 1.0
                    triProjected.vecList[0].y += 1.0
                    triProjected.vecList[1].x += 1.0
                    triProjected.vecList[1].y += 1.0
                    triProjected.vecList[2].x += 1.0
                    triProjected.vecList[2].y += 1.0

                    triProjected.vecList[0].x *= 0.5 * screen_w
                    triProjected.vecList[0].y *= 0.5 * screen_h
                    triProjected.vecList[1].x *= 0.5 * screen_w
                    triProjected.vecList[1].y *= 0.5 * screen_h
                    triProjected.vecList[2].x *= 0.5 * screen_w
                    triProjected.vecList[2].y *= 0.5 * screen_h

                    trianglesToRender.add(triProjected)

                    self.draw_triangle((triProjected.vecList[0].x, triProjected.vecList[0].y),
                                       (triProjected.vecList[1].x, triProjected.vecList[1].y),
                                       (triProjected.vecList[2].x, triProjected.vecList[2].y),
                                       (100, 255, 100), 1)

            # trisl = list(trianglesToRender)
            # trisl.sort(key=lambda t: t.get_middle_point('z'))
            #
            # for tris in trisl:
            #     self.draw_triangle((tris.vecList[0].x, tris.vecList[0].y),
            #                        (tris.vecList[1].x, tris.vecList[1].y),
            #                        (tris.vecList[2].x, tris.vecList[2].y),
            #                        (tris.col, tris.col, tris.col))

    def Multiply_Vector_Matrix(self, v_in, mat):
        v_out = Vector()
        v_out.x = v_in.x * mat.mat[0][0] + v_in.y * mat.mat[1][0] + v_in.z * mat.mat[2][0] + mat.mat[3][0]
        v_out.y = v_in.x * mat.mat[0][1] + v_in.y * mat.mat[1][1] + v_in.z * mat.mat[2][1] + mat.mat[3][1]
        v_out.z = v_in.x * mat.mat[0][2] + v_in.y * mat.mat[1][2] + v_in.z * mat.mat[2][2] + mat.mat[3][2]
        w = v_in.x * mat.mat[0][3] + v_in.y * mat.mat[1][3] + v_in.z * mat.mat[2][3] + mat.mat[3][3]

        if w != 0:
            v_out.x /= w
            v_out.y /= w
            v_out.z /= w

            return v_out

    def matrix_Multiply(self, m1=Matrix4x4(), m2=Matrix4x4()):
        matrix = Matrix4x4()
        for c in range(4):
            for r in range(4):
                matrix.mat[r][c] = m1.mat[r][0] * m2.mat[0][c] + \
                                   m1.mat[r][1] * m2.mat[1][c] + \
                                   m1.mat[r][2] * m2.mat[2][c] + \
                                   m1.mat[r][3] * m2.mat[3][c]
        return matrix

    def matrix_PointAt(self, pos=Vector(), target=Vector(), up=Vector()):
        newForward = target - pos
        newForward = newForward.normalise()

        a = newForward * up.dot_product(newForward)
        newUp = up - a
        newUp = newUp.normalise()

        newRight = newUp.cross_product(newForward)

        matrix = Matrix4x4()
        matrix.mat[0][0] = newRight.x
        matrix.mat[0][1] = newRight.y
        matrix.mat[0][2] = newRight.z
        matrix.mat[0][3] = 0.0

        matrix.mat[1][0] = newUp.x
        matrix.mat[1][1] = newUp.y
        matrix.mat[1][2] = newUp.z
        matrix.mat[1][3] = 0.0

        matrix.mat[2][0] = newForward.x
        matrix.mat[2][1] = newForward.y
        matrix.mat[2][2] = newForward.z
        matrix.mat[2][3] = 0.0

        matrix.mat[3][0] = pos.x
        matrix.mat[3][1] = pos.y
        matrix.mat[3][2] = pos.z
        matrix.mat[3][3] = 1.0

        return matrix


screen_size = screen_w, screen_h = 600, 300

if __name__ == '__main__':
    mesh = Mesh()
    mesh.LoadObject('models/Teapot.obj')

    demo = Engine3D(600, 300, 4, 4, mesh=mesh, scale=0.3)
    demo.run()
