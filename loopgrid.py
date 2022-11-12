class LoopCube:
    def __init__(self, size):
        self.faces = [[[None for col in range(size)] for row in range(size)] for face in range(6)]

    # Index is of the form (face, x, y)
    def __getitem__(self, index):
        return self.faces[index[0]][index[1]][index[2]]

    def __setitem__(self, index, newvalue):
        self.faces[index[0]][index[1]][index[2]] = newvalue