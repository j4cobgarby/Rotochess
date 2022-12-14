import pyray as pr
from loopgrid import LoopCube
from piece import *

cols = [pr.WHITE,pr.YELLOW,pr.ORANGE,pr.RED,pr.DARKGREEN,pr.BLUE,pr.WHITE]

cube = pr.load_model("Mesh/cube.obj")

rots = [
        [pr.Vector3(1,0,0),0],
        [pr.Vector3(1,0,0),180],
        [pr.Vector3(0,0,1),90],
        [pr.Vector3(0,0,1),270],
        [pr.Vector3(0,1,1),180],
        [pr.Vector3(0,-1,1),180],
    ]

face_vect = [
    pr.Vector3(0,1,0),
    pr.Vector3(0,-1,0),
    pr.Vector3(-1,0,0),
    pr.Vector3(1,0,0),
    pr.Vector3(0,0,1),
    pr.Vector3(0,0,-1),
]

face_sizes = [
    pr.Vector3(0.8,0.1,0.8),
    pr.Vector3(0.8,0.1,0.8),
    pr.Vector3(0.1, 0.8, 0.8),
    pr.Vector3(0.1, 0.8, 0.8),
    pr.Vector3(0.8, 0.8, 0.1),
    pr.Vector3(0.8, 0.8, 0.1)
]

def addv(v1, v2):
        return pr.Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sclv(v1, s):
    return pr.Vector3(v1.x * s, v1.y * s, v1.z * s)

def mulv(v1, v2):
    return pr.Vector3(v1.x * v2.x, v1.y * v2.y, v1.z * v2.z)

class ChessCube:
    def __init__(self,size,cubelet_size):
        self.size = size
        self.cubelet_size = cubelet_size
        self.offset=-1.5
        self.ray = None
        self.mouse = (0,0,0)
        self.mousedist = 100000
        self.to_move = None
        self.making_move = False


        # Initilise Cubelet Array
        self.cubelets = [[[] for i in range(0,size)]for i in range(0,size)]
        self.pieces = LoopCube(size)

        self.pieces[0,2,3] = [0, Rook(Piece.WHITE)]
        self.pieces[0,3,3] = [0, Queen(Piece.WHITE)]
        self.pieces[0,4,3] = [0, King(Piece.WHITE)]
        self.pieces[0,5,3] = [0, Rook(Piece.WHITE)]
        self.pieces[0,3,2] = [0, Bishop(Piece.WHITE)]
        self.pieces[0,3,4] = [0, Bishop(Piece.WHITE)]

        self.pieces[1,2,3] = [1, Rook(Piece.BLACK)]
        self.pieces[1,3,3] = [1, Queen(Piece.BLACK)]
        self.pieces[1,4,3] = [1, King(Piece.BLACK)]
        self.pieces[1,5,3] = [1, Rook(Piece.BLACK)]
        self.pieces[1,3,2] = [1, Bishop(Piece.BLACK)]
        self.pieces[1,3,4] = [1, Bishop(Piece.BLACK)]
    
    def spin(self,sides,n):
        if sides[3]:
            n = self.size-1-n
        print(sides)
        for i in range(sides[0]):
            self.rotate_x(n)
        for i in range(sides[1]):
            self.rotate_y(n)
        for i in range(sides[2]):
            self.rotate_z(n)


    # ^
    # | Y
    # |      X
    # |___----->
    #  \
    #   \ Z
    #    v
    
    #     +---+
    #     | B |
    # +---+---+---+---+
    # | U | L | D | R |
    # +---+---+---+---+
    #     | F |
    #     +---+
    #
    # +---+---+---+---+---+---+
    # | U | D | L | R | F | B |
    # +---+---+---+---+---+---+
    #
    # U | D | L | R | F | B 
    # 0 | 1 | 2 | 3 | 4 | 5

    def draw_face(self,face_num, face_center, r_dir, c_dir, size):
        face = self.pieces[face_num]
        dirsum = addv(r_dir, c_dir)
        offs = sclv(dirsum, -0.5)
        dirsum = sclv(dirsum, size/2)
        dirsum = addv(dirsum, offs)
        dirsum = sclv(dirsum, -1)
        face_center = addv(face_center, dirsum) # Face center is now the point where r=0, c=0

        valid_moves = []
        if self.making_move:
            valid_moves = self.pieces.get_valid_moves(*self.to_move)

        for r in range(size):
            for c in range(size):
                offset = addv(sclv(r_dir, r), sclv(c_dir, c))

                #pr.draw_cube(addv(offset, face_center), *face_sizes[face_num], cols[face[r][c][0]])
                #pr.draw_model_ex(cube, addv(offset, face_center), rots[face_num][0],rots[face_num][1],face_sizes[0],cols[face_num])

                tr = addv(addv(offset, face_center),sclv(face_sizes[face_num], 0.5))
                bl = addv(addv(offset, face_center),sclv(face_sizes[face_num], -0.5))

                ra = pr.get_ray_collision_box(self.ray, pr.BoundingBox(bl, tr)) 
                co = cols[face[r][c][0]]
                if (face_num, r,c) in valid_moves:
                    co = pr.PURPLE

                if ra.hit:
                    if ra.distance < self.mousedist:
                        self.mouse = (face_num,r,c)
                        self.mousedist = ra.distance
                        co = pr.GREEN

                pr.draw_model_ex(cube, addv(offset, face_center), rots[face_num][0],rots[face_num][1],face_sizes[0],co)

                if face[r][c][1] != None:
                    loc = addv(addv(offset, face_center),sclv(face_vect[face_num],self.offset))

                    pr.draw_model_ex(face[r][c][1].mesh,loc, rots[face_num][0],rots[face_num][1],pr.Vector3(0.2, 0.2, 0.2),face[r][c][1].colour)


    def draw(self):
        sz = self.size
        pr.draw_model(cube,pr.Vector3(0,0,0),self.size,pr.DARKGRAY)

        self.draw_face(0, pr.Vector3(0,sz/2,0), pr.Vector3(0,0,1), pr.Vector3(1,0,0), sz)
        self.draw_face(1, pr.Vector3(0,-sz/2,0), pr.Vector3(0,0,1), pr.Vector3(-1,0,0), sz)

        self.draw_face(4, pr.Vector3(0,0,sz/2), pr.Vector3(-1,0,0), pr.Vector3(0,-1,0), sz)
        self.draw_face(5, pr.Vector3(0,0,-sz/2), pr.Vector3(1,0,0), pr.Vector3(0,-1,0), sz)

        self.draw_face(2, pr.Vector3(-sz/2,0,0), pr.Vector3(0,0,1), pr.Vector3(0,1,0), sz)
        self.draw_face(3, pr.Vector3(sz/2,0,0), pr.Vector3(0,0,1), pr.Vector3(0,-1,0), sz)

    def rotate_x(self,n):
        hold = [None]*self.size

        # Read UP
        for i in range(self.size):
            hold[i] = self.pieces[0,i,n]

        # Read write Back
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[5, n, self.size-1-i]
            self.pieces[5, n, self.size-1-i] = a
            
        # Read Write Down
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[1, self.size-1-i, self.size-1-n]
            self.pieces[1, self.size-1-i, self.size-1-n] = a

        # Read Write Front
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[4, self.size-1-n, i]
            self.pieces[4, self.size-1-n, i] = a

        # Write Up
        for i in range(self.size):
            self.pieces[0,i,n] = hold[i]

        if n == 0:
            a = list(zip(*list(zip(*list(zip(*self.pieces[2][::-1]))[::-1]))[::-1]))
            a = [list(x) for x in a]
            self.pieces[2] = a
            

        if n == self.size-1:
            a = list(zip(*self.pieces[3][::-1]))
            a = [list(x) for x in a]
            self.pieces[3] = a
        

    def rotate_y(self,n):
        hold = [None]*self.size

        # Read Right
        for i in range(self.size):
            hold[i] = self.pieces[3,i,self.size-1-n]

        # Back
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[5, i, self.size-1-n]
            self.pieces[5, i, self.size-1-n] = a

        # Left
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[2, self.size-1-i, n]
            self.pieces[2, self.size-1-i, n] = a

        # Front
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[4, i, self.size-1-n]
            self.pieces[4, i, self.size-1-n] = a

        # WriteRight
        for i in range(self.size):
            self.pieces[3,i,self.size-1-n] = hold[i]

        if n == 0 :
            a = list(zip(*self.pieces[1][::-1]))
            a = [list(x) for x in a]
            self.pieces[1] = a # Down

        if n == self.size-1:
            a = list(zip(*list(zip(*list(zip(*self.pieces[0][::-1]))[::-1]))[::-1]))
            a = [list(x) for x in a]
            self.pieces[0] = a

    def rotate_z(self,n):
        hold = [None]*self.size

        # Read Up
        for i in range(self.size):
            hold[i] = self.pieces[0,n,i]

        # Left
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[2,n,i]
            self.pieces[2,n,i] = a

        # Down
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[1,n,i]
            self.pieces[1,n,i] = a 

        # Right
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[3,n,i]
            self.pieces[3,n,i] = a

        # Write up
        for i in range(self.size):
            self.pieces[0,n,i] = hold[i]

        if n == 0:
            a = list(zip(*self.pieces[5][::-1]))
            a = [list(x) for x in a]
            self.pieces[5] = a #Back

        if n == self.size-1:
            a = list(zip(*list(zip(*list(zip(*self.pieces[4][::-1]))[::-1]))[::-1]))
            a = [list(x) for x in a]
            self.pieces[4] = a # Front