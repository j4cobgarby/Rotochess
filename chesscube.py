import pyray as pr

class Cubelet:
    def __init__(self, pos, size, cs):
        self.dims = [cs, cs, cs]
        self.pos = [n for n in pos]
        self.pieces = [None, None, None, None, None, None] # up,down,left,right,front,back
        self.col = pr.Color(60, 124, 58, 255) \
            if (self.pos[0] + self.pos[1]*3 + self.pos[2] * 9) % 2 != 0 else pr.WHITE
        self.cs = cs
        self.size = size

    def draw(self):
        pr.draw_cube_v([(n*3) - (self.size*self.cs)/2 + self.cs/2 for n in self.pos], self.dims, self.col)

class ChessCube:
    def __init__(self,size,cubelet_size):
        self.size = size
        self.cubelet_size = cubelet_size


        # Initilise Cubelet Array
        self.cubelets = [[[] for i in range(0,size)]for i in range(0,size)]

        for y in range(0, size):
            for z in range(0, size):
                for x in range(0, size):
                    self.cubelets[y][z].append(Cubelet([x,y,z], size, cubelet_size))

        # Initilise empty piece array
        self.pieces = [[[None for i in range(size)] for i in range(size)] for i in range (6)]

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


    def draw(self):
        for y in range(0, self.size):
            for z in range(0, self.size):
                for x in range(0, self.size):
                    if x in [0, self.size-1] or y in [0, self.size-1] or z in [0, self.size-1]:
                        self.cubelets[y][z][x].draw()

    def rotate_x(self,n):
        hold = [None]*self.size

        # Read UP
        for i in range(self.size):
            hold[i] = self.pieces[0,i,n]

        # Read write Back
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[5, n, size-1-i]
            self.pieces[5, n, size-1-i] = a
            
        # Read Write Down
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[1, size-1-i, size-1-n]
            self.pieces[1, size-1-i, n] = a

        # Read Write Front
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[4, size-1-n, i]
            self.pieces[4, size-1-n, i] = a

        # Write Up
        for i in range(self.size):
            self.peices[0,i,n] = hold[i]

        if n == 0:
            a = list(zip(*list(zip(*list(zip(*self.pieces[3][::-1]))[::-1]))[::-1]))
            self.pieces[3] = a
            

        if n == size-1:
            a = list(zip(*self.pieces[2][::-1]))
            self.pieces[2] = a
        

    def rotate_y(self):
        hold = [None]*self.size

        # Read Right
        for i in range(self.size):
            hold[i] = self[3,n,i]

        # Back
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[5, size-1-i, size-1-n]
            self.pieces[5, size-1-i, size-1-n] = a

        # Left
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[2, size-1-i, size-1-n]
            self.pieces[2, size-1-i, size-1-n] = a

        # Front
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[4, size-1-i, size-1-n]
            self.pieces[4, size-1-i, size-1-n] = a

        # WriteRight
        for i in range(self.size):
            self[3,n,i] = hold[i]

        if n == 0 :
            a = list(zip(*self.pieces[1][::-1]))
            self.pieces[1] = a # Down

        if n == size-1:
            a = list(zip(*list(zip(*list(zip(*self.pieces[0][::-1]))[::-1]))[::-1]))
            self.pieces[0] = a

    def rotate_z(self):
        hold = [None]*self.size

        # Read Up
        for i in range(self.size):
            hold[i] = self.pieces[0,n,i]

        # Left
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[2,n,i]
            self.pieces[2,n,i]

        # Down
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[1,n,i]
            self.pieces[1,n,i]

        # Right
        for i in range(self.size):
            a = hold[i]
            hold[i] = self.pieces[3,n,i]
            self.pieces[3,n,i]

        # Write up
        for i in range(self.size):
            self.pieces[0,i,n] = hold[i]

        if n == 0:
            a = list(zip(*list(zip(*list(zip(*self.pieces[5][::-1]))[::-1]))[::-1]))
            self.pieces[5] = a #Back

        if n == size-1:
            a = list(zip(*self.pieces[4][::-1]))
            self.pieces[4] = a # Front