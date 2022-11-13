from random import randint
from piece import *
import random

class LoopCube:
    def __init__(self, size):
        self.size = size
        self.faces = [[[[face, None] for col in range(self.size)] for row in range(self.size)] for face in range(6)]

    # Just converts a delta_r and delta_c to a move_* call
    # only one of delta_r and delta_c should be set, and to 1 or -1
    def move_helper(self, index, delta_r, delta_c):
        if delta_r == 1:
            return self.move_posrow(index)
        elif delta_r == -1:
            return self.move_negrow(index)
        elif delta_c == 1:
            return self.move_poscol(index)
        elif delta_c == -1:
            return self.move_negcol(index)

    # Move in one direction, one square
    # Returns (r, (new_face, new_row, new_col))
    # r is the amount of 90 degree turns to rotate by
    def move(self, index, delta_r, delta_c):
        start = index[::]
        target = self.move_helper(start, delta_r, delta_c)

        # Hasn't moved over an edge
        if start[0] == target[0]:
            return (0, target)

        if target[0] == 4:
            # Here we're moving to front face, which is a problem
            # because it's like a crossroads
            if start[0] == 0:
                return (3, target) # we're not moving right along F
            if start[0] == 1:
                return (1, target) # from D to F, into the side
            if start[0] == 2:
                return (2, target) # coming in from right below

        if target[0] == 0:
            if start[0] == 4:
                return (1, target)
            if start[0] == 5:
                return (3, target)
        
        if target[0] == 1:
            if start[0] == 4:
                return (3, target)
            if start[0] == 5:
                return (1, target)

        if target[0] == 2:
            if start[0] == 4:
                return (2, target)
            if start[0] == 5:
                return (2, target)

        if target[0] == 5:
            if start[0] == 0:
                return (1, target)
            if start[0] == 1:
                return (3, target)
            if start[0] == 2:
                return (2, target)

        return (0, target)

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
                new_col = self.size - 1 - index[2]
            elif index[0] == 3:
                new_face = 4
                new_row = 0
                new_col = index[2]
            elif index[0] == 4:
                new_face = 2
                new_row = self.size - 1
                new_col = self.size - 1 - index[2]
            elif index[0] == 5:
                new_face = 3
                new_row = 0
                new_col = index[2]
            return (new_face, new_row, new_col)
        else:
            return (index[0], index[1] + 1, index[2])

    def move_negrow(self, index):
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
            elif index[0] == 3:
                new_face = 5
                new_row = self.size - 1
                new_col = index[2]
            elif index[0] == 2:
                new_face = 5
                new_row = 0
                new_col = self.size - 1 - index[2]
            elif index[0] == 4:
                new_face = 3
                new_row = self.size - 1
                new_col = index[2]
            elif index[0] == 5:
                new_face = 2
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
                new_face = 3
                new_row = index[1]
                new_col = 0
            elif index[0] == 1:
                new_face = 2
                new_row = index[1]
                new_col = 0
            elif index[0] == 3:
                new_face = 1
                new_row = index[1]
                new_col = 0
            elif index[0] == 2:
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
                new_face = 2
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 1:
                new_face = 3
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 3:
                new_face = 0
                new_row = index[1]
                new_col = self.size - 1
            elif index[0] == 2:
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

    def rotate_v2d(self, x, y, cw, steps):
        ret = [x, y]
        for i in range(steps):
            if (cw):
                ret[0], ret[1] = ret[1], -ret[0]
            else:
                ret[0], ret[1] = -ret[1], ret[0]
        return ret

    def get_valid_moves(self, face, r, c):
        p = self.faces[face][r][c][1]
        moves = []

        if type(p) == Knight:
            print("Neigh!!")

            rots = []

        if type(p) in [Rook, Queen]:
            print("It's a rook!")

            rots = [0,0,0,0]
            blocked = [False for i in range(4)]
            poss = [[face,r,c] for i in range(4)]
            for i in range(self.size):
                tmprots = [0,0,0,0]
                tmprots[0], poss[0] = self.move(poss[0], *self.rotate_v2d(-1, 0, True, rots[0]))
                tmprots[1], poss[1] = self.move(poss[1], *self.rotate_v2d(1, 0, True, rots[1]))
                tmprots[2], poss[2] = self.move(poss[2], *self.rotate_v2d(0, 1, True, rots[2]))
                tmprots[3], poss[3] = self.move(poss[3], *self.rotate_v2d(0, -1, True, rots[3]))
                for i in range(4):
                    rots[i] += tmprots[i]
                    f = self.faces[poss[i][0]][poss[i][1]][poss[i][2]]
                    if f[1] != None:
                        if f[1].side == self.faces[face][r][c][1].side:
                            # encountered my own side
                            blocked[i] = True
                            continue
                        else:
                            #encounterd enemy
                            blocked[i] = True
                            moves.append(poss[i])
                            continue

                    if not blocked[i]: 
                        moves.append(poss[i])

        if type(p) in [Bishop, Queen]:
            print("Bishop moment")

            rots = [0 for i in range(8)]
            poss = [[face,r,c] for i in range(8)]
            blocked = [False for i in range(8)]

            for i in range(self.size):
                tmprots = [0 for i in range(8)]
                tmprots[0], poss[0] = self.move(poss[0], *self.rotate_v2d(0, -1, True, rots[0]))
                tmprots[1], poss[1] = self.move(poss[1], *self.rotate_v2d(0, 1, True, rots[1]))
                tmprots[2], poss[2] = self.move(poss[2], *self.rotate_v2d(-1, 0, True, rots[2]))
                tmprots[3], poss[3] = self.move(poss[3], *self.rotate_v2d(1, 0, True, rots[3]))
                tmprots[4], poss[4] = self.move(poss[4], *self.rotate_v2d(0, -1, True, rots[4]))
                tmprots[5], poss[5] = self.move(poss[5], *self.rotate_v2d(0, 1, True, rots[5]))
                tmprots[6], poss[6] = self.move(poss[6], *self.rotate_v2d(-1, 0, True, rots[6]))
                tmprots[7], poss[7] = self.move(poss[7], *self.rotate_v2d(1, 0, True, rots[7]))
                for i in range(8):
                    rots[i] += tmprots[i]
                tmprots[0], poss[0] = self.move(poss[0], *self.rotate_v2d(-1, 0, True, rots[0]))
                tmprots[1], poss[1] = self.move(poss[1], *self.rotate_v2d(-1, 0, True, rots[1]))
                tmprots[2], poss[2] = self.move(poss[2], *self.rotate_v2d(0, 1, True, rots[2]))
                tmprots[3], poss[3] = self.move(poss[3], *self.rotate_v2d(0, 1, True, rots[3]))
                tmprots[4], poss[4] = self.move(poss[4], *self.rotate_v2d(1, 0, True, rots[4]))
                tmprots[5], poss[5] = self.move(poss[5], *self.rotate_v2d(1, 0, True, rots[5]))
                tmprots[6], poss[6] = self.move(poss[6], *self.rotate_v2d(0, -1, True, rots[6]))
                tmprots[7], poss[7] = self.move(poss[7], *self.rotate_v2d(0, -1, True, rots[7]))

                for i in range(8):
                    rots[i] += tmprots[i]
                    f = self.faces[poss[i][0]][poss[i][1]][poss[i][2]]
                    if f[1] != None:
                        if f[1].side == self.faces[face][r][c][1].side:
                            blocked[i] = True
                            continue
                        else:
                            blocked[i] = True
                            moves.append(poss[i])
                            continue
                            
                    if not blocked[i]:
                        moves.append(poss[i])

        if type(p) == King:
            print("King!")

            rots = [0 for i in range(4)]
            tmprots = rots[::]
            poss = [[face, r, c] for i in range(8)]
            _, poss[0] = self.move(poss[0], 0, -1)
            _, poss[1] = self.move(poss[1], 0, 1)
            _, poss[2] = self.move(poss[2], -1, 0)
            _, poss[3] = self.move(poss[3], 1, 0)
            tmprots[0], poss[4] = self.move(poss[4], 0, -1)
            tmprots[1], poss[5] = self.move(poss[5], 0, 1)
            tmprots[2], poss[6] = self.move(poss[6], 0, -1)
            tmprots[3], poss[7] = self.move(poss[7], 0, 1)
            for i in range(4):
                rots[i] = tmprots[i]
            tmprots[0], poss[4] = self.move(poss[4], *self.rotate_v2d(-1, 0, True, rots[i]))
            tmprots[1], poss[5] = self.move(poss[5], *self.rotate_v2d(-1, 0, True, rots[i]))
            tmprots[2], poss[6] = self.move(poss[6], *self.rotate_v2d(1, 0, True, rots[i]))
            tmprots[3], poss[7] = self.move(poss[7], *self.rotate_v2d(1, 0, True, rots[i]))

            for i in range(8):
                moves.append(poss[i])


        return moves

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