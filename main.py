import pyray as pr
import random

class Cubelet:
    def __init__(self, pos):
        self.dims = [3,3,3]
        self.pos = pos
        self.pieces = [None, None, None, None, None, None] # up,down,left,right,front,back
        self.col = random.choice([pr.BLUE, pr.RED, pr.BLACK, pr.MAROON, pr.PURPLE])

    def draw(self):
        pr.draw_cube_v(self.pos, [1,1,1], self.col)

def main():
    cube = [[[] for i in range(0,3)]for i in range(0,3)]

    for y in range(0, 3):
        for z in range(0, 3):
            for x in range(0, 3):
                cube[y][z].append(Cubelet([(x-1) * 3,(y-1) * 3,(z-1) * 3]))
                print((x-1) * 3,(y-1) * 3,(z-1) * 3)
                
    for y in range(0, 3):
        for z in range(0, 3):
            for x in range(0,3):
                print(str(cube[y][z][x]), cube[y][z][x].pos)


    pr.init_window(700, 700, "Rotochess")
    pr.set_target_fps(60)

    camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
    pr.set_camera_mode(camera, pr.CAMERA_FREE)
    pr.set_camera_alt_control(pr.KEY_LEFT_SHIFT)

    while not pr.window_should_close():
        pr.update_camera(camera)
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(camera)
        
        for y in range(0, 3):
            for z in range(0, 3):
                for x in range(0, 3):
                    pr.draw_cube_v(cube[y][z][x].pos, [1,1,1], pr.BLACK)

        pr.end_mode_3d()
        pr.end_drawing()
    pr.close_window()

if __name__ == "__main__":
    main()