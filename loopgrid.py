from random import randint

class LoopCube:
    def __init__(self, size):
        self.size = size
        self.faces = [[[0 for col in range(self.size)] for row in range(self.size)] for face in range(6)]

    def move_posrow(self, index):
        if index[1] + 1 >= self.size:
            new_face = None
            new_row = None
            new_col = None
            

            if index[0] == 0:
                new_face = 4
                new_row = self.size - 1 - index[2]
                new_col = 0
            elif index[0] == 1:
                new_face = 4
                new_row = index[2]
                new_col = self.size - 1
            elif index[0] == 2:
                new_face = 4
                new_row = self.size - 1
                new_col = index[2]
            elif index[0] == 3:
                new_face = 4
                new_row = 0
                new_col = self.size - 1 - index[2]
            elif index[0] == 4:
                new_face = 3
                new_row = 0
                new_col = self.size - 1 - index[2]
            elif index[0] == 5:
                new_face = 2
                new_row = self.size - 1
                new_col = index[2]
            return (new_face, new_row, new_col)
        else:
            return (index[0], index[1] + 1, index[2])

    def move_negrow(self, index):
        print(f"!! {index}, size={self.size}")
        if index[1] - 1 < 0:
            new_face = None
            new_row = None
            new_col = None
            if index[0] == 0:
                new_face = 5
                new_row = index[2]
                new_col = 0
            elif index[0] == 1:
                new_face = 5
                new_row = self.size - 1 - index[2]
                new_col = self.size - 1
            elif index[0] == 2:
                new_face = 5
                new_row = self.size - 1
                new_col = index[2]
            elif index[0] == 3:
                new_face = 5
                new_row = 0
                new_col = self.size - 1 - index[2]
            elif index[0] == 4:
                new_face = 2
                new_row = self.size - 1
                new_col = index[2]
            elif index[0] == 5:
                new_face = 3
                new_row = 0
                new_col = self.size - 1 - index[2]
            return (new_face, new_row, new_col)
        else:
            return (index[0],index[1] - 1, index[2])

    def move_poscol(self, index):
        if index[2] + 1 >= self.size:
            new_face = None
            new_row = None
            new_col = None
            if index[0] == 0:
                new_face = 2
                new_row = index[1]
                new_col = 0
            elif index[0] == 1:
                new_face = 3
                new_row = index[1]
                new_col = 0
            elif index[0] == 2:
                new_face = 1
                new_row = index[1]
                new_col = 0
            elif index[0] == 3:
                new_face = 0
                new_row = index[1]
                new_col = 0
            elif index[0] == 4:
                new_face = 1
                new_row = self.size - 1
                new_col = index[1]
            elif index[0] == 5:
                new_face = 1
                new_row = 0
                new_col = self.size - 1 - index[1]
            return (new_face, new_row, new_col)
        else:
            return (index[0], index[1], index[2] + 1)

    def move_negcol(self, index):
        if index[2] - 1 < 0:
            new_face = None
            new_row = None
            new_col = None
            if index[0] == 0:
                new_face = 3
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 1:
                new_face = 2
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 2:
                new_face = 0
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 3:
                new_face = 1
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 4:
                new_face = 0
                new_row = self.size - 1
                new_col = self.size - 1 - index[1]
            elif index[0] == 5:
                new_face = 0
                new_row = 0
                new_col = index[1]
            return (new_face, new_row, new_col)
        else:
            return (index[0], index[1], index[2] - 1)

    # Index is of the form (face, row, col)
    def __getitem__(self, index):
        if type(index) == int:
            return self.faces[index]
        elif type(index) == tuple:
            if 0 <= index[1] < self.size and 0 <= index[2] < self.size:
                return self.faces[index[0]][index[1]][index[2]]
            else:
                raise KeyError("Out of bounds")
        raise KeyError("Must be [f] or [f,r,c]")

    def __setitem__(self, index, newvalue):
        if type(index) == int:
            self.faces[index] = newvalue[::]
        elif type(index) == tuple:
            if 0 <= index[1] < self.size and 0 <= index[2] < self.size:
                self.faces[index[0]][index[1]][index[2]] = newvalue
            else:
                raise KeyError("Out of bounds")
        else:
            raise KeyError("Must be [f] or [f,r,c]")

    def __str__(self):
        ret = ""
        for i, f in enumerate(self.faces):
            ret = ret + f"Face {i}\n"
            for r in range(self.size):
                for c in range(self.size):
                    ret = ret + str(f[r][c]) + " "
                ret = ret + "\n"
        return ret