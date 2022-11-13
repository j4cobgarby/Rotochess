import pyray as pr
import random

# Lighting
lighting = pr.load_shader(
    "shaders/lighting.vs",
    "shaders/lighting.fs"
)
#lighting.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW] = pr.get_shader_location(lighting, "viewPos")
ambientLoc = pr.get_shader_location(lighting, "ambient")
pr.set_shader_value(
    lighting, 
    ambientLoc, 
    pr.Vector4(0.6,0.6,0.6,0.6), 
    pr.ShaderUniformDataType.SHADER_UNIFORM_VEC4
)

msh = [
       pr.load_model("Mesh/Knight.obj"),
       pr.load_model("Mesh/Bishop.obj"),
       pr.load_model("Mesh/Pawn.obj"),
       pr.load_model("Mesh/Queen.obj"),
       pr.load_model("Mesh/Rook.obj"),
       pr.load_model("Mesh/King.obj")
    ]

for i in msh:
    i.materials[0].shader = lighting

for i in range(15):
    msh.append(None)

class Piece:
    BLACK = 0
    WHITE = 1

    def __init__(self, side):
        self.mesh = random.choice(msh)
        self.side = side

class Knight(Piece):
    def __init__(self, side):
        self.mesh = msh[0]

class Bishop(Piece):
    def __init__(self, side):
        self.mesh = msh[1]

class Pawn(Piece):
    def __init__(self, side):
        self.mesh = msh[2]

class Queen(Piece):
    def __init__(self, side):
        self.mesh = msh[3]

class Rook(Piece):
    def __init__(self, side):
        self.mesh = msh[4]

class King(Piece):
    def __init__(self, side):
        self.mesh = msh[5]