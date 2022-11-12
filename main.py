#!/usr/bin/env python

import pyray as pr
import random
from chesscube import ChessCube

def main():
    size = 8
    cubelet_size = 3
    pr.set_config_flags(pr.ConfigFlags.FLAG_MSAA_4X_HINT)
    pr.set_config_flags(pr.ConfigFlags.FLAG_VSYNC_HINT)

    pr.init_window(700, 700, "Rotochess")
    pr.set_target_fps(60)

    world = ChessCube(size,cubelet_size)

    camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
    camera.projection = pr.CameraProjection.CAMERA_ORTHOGRAPHIC
    pr.set_camera_mode(camera, pr.CAMERA_FREE)
    pr.set_camera_alt_control(pr.KEY_LEFT_SHIFT)

    while not pr.window_should_close():
        pr.update_camera(camera)
        pr.begin_drawing()
        pr.clear_background(pr.Color(182,191,239,255))
        pr.begin_mode_3d(camera)
        
        world.draw()

        pr.end_mode_3d()
        pr.end_drawing()
    pr.close_window()

if __name__ == "__main__":
    main()