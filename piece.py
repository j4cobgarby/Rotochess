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
    def __init__(self):
        self.mesh = random.choice(msh)
