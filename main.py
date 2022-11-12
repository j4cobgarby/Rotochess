#!/usr/bin/env python

import pyray as pr
import random

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

def main():
    size = 8
    cubelet_size = 3

    cube = [[[] for i in range(0,size)]for i in range(0,size)]

    for y in range(0, size):
        for z in range(0, size):
            for x in range(0, size):
                cube[y][z].append(Cubelet([x,y,z], size, cubelet_size))

    pr.init_window(700, 700, "Rotochess")
    pr.set_target_fps(60)

    camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
    pr.set_camera_mode(camera, pr.CAMERA_FREE)
    pr.set_camera_alt_control(pr.KEY_LEFT_SHIFT)

    while not pr.window_should_close():
        pr.update_camera(camera)
        pr.begin_drawing()
        pr.clear_background(pr.Color(182,191,239,255))
        pr.begin_mode_3d(camera)
        
        for y in range(0, size):
            for z in range(0, size):
                for x in range(0, size):
                    if x in [0, size-1] or y in [0, size-1] or z in [0, size-1]:
                        cube[y][z][x].draw()

        pr.end_mode_3d()
        pr.end_drawing()
    pr.close_window()

if __name__ == "__main__":
    main()