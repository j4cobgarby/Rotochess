import pyray as pr
import random

class Piece:
    msh = [
       pr.load_model("Mesh/Knight.obj"),
       pr.load_model("Mesh/Bishop.obj"),
       pr.load_model("Mesh/Pawn.obj"),
       pr.load_model("Mesh/Queen.obj"),
       pr.load_model("Mesh/Rook.obj"),
       pr.load_model("Mesh/King.obj")
    ]
    def __init__(self):
        self.mesh = random.choice(self.msh)
