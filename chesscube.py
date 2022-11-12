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
    # +---+---+---+---+---+
    # | U | L | D | R | B |
    # +---+---+---+---+---+
    #
    # U | D | L | R | B | F 
    # 0 | 1 | 2 | 3 | 4 | 5


    def draw(self):
        for y in range(0, self.size):
            for z in range(0, self.size):
                for x in range(0, self.size):
                    if x in [0, self.size-1] or y in [0, self.size-1] or z in [0, self.size-1]:
                        self.cubelets[y][z][x].draw()