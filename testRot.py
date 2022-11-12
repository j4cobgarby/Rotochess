#!/usr/bin/env python

import pyray as pr
from loopgrid import LoopCube
from chesscube import ChessCube

cols = [pr.RED,pr.ORANGE,pr.GREEN,pr.YELLOW,pr.PURPLE,pr.BLUE,pr.WHITE]

def addv(v1, v2):
    return pr.Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sclv(v1, s):
    return pr.Vector3(v1.x * s, v1.y * s, v1.z * s)

def mulv(v1, v2):
    return pr.Vector3(v1.x * v2.x, v1.y * v2.y, v1.z * v2.z)

def draw_xz_face(face, face_center, r_dir, c_dir, size, col):
    dirsum = addv(r_dir, c_dir)
    offs = sclv(dirsum, -0.5)
    dirsum = sclv(dirsum, size/2)
    dirsum = addv(dirsum, offs)
    dirsum = sclv(dirsum, -1)
    face_center = addv(face_center, dirsum)

    for r in range(size):
        for c in range(size):
            offset = addv(sclv(r_dir, r), sclv(c_dir, c))
            pr.draw_cube(addv(offset, face_center), 0.8,0.1,0.8, cols[face[r][c]])
            #pr.draw_cube(addv(face_center, pr.Vector3(r,0,c)), 0.8, 0.05, 0.8, pr.WHITE if face[r][c] == 1 else col)

def draw_xy_face(face, face_center, r_dir, c_dir, size, col):
    dirsum = addv(r_dir, c_dir)
    offs = sclv(dirsum, -0.5)
    dirsum = sclv(dirsum, size/2)
    dirsum = addv(dirsum, offs)
    dirsum = sclv(dirsum, -1)
    face_center = addv(face_center, dirsum) # Face center is now the point where r=0, c=0

    for r in range(size):
        for c in range(size):
            offset = addv(sclv(r_dir, r), sclv(c_dir, c))
            pr.draw_cube(addv(offset, face_center), 0.8, 0.8, 0.1, cols[face[r][c]])

def draw_zy_face(face, face_center, r_dir, c_dir, size, col):
    dirsum = addv(r_dir, c_dir)
    offs = sclv(dirsum, -0.5)
    dirsum = sclv(dirsum, size/2)
    dirsum = addv(dirsum, offs)
    dirsum = sclv(dirsum, -1)
    face_center = addv(face_center, dirsum) # Face center is now the point where r=0, c=0

    for r in range(size):
        for c in range(size):
            offset = addv(sclv(r_dir, r), sclv(c_dir, c))
            pr.draw_cube(addv(offset, face_center), 0.1, 0.8, 0.8, cols[face[r][c]])

def main():
    pr.set_config_flags(pr.ConfigFlags.FLAG_MSAA_4X_HINT)
    pr.set_config_flags(pr.ConfigFlags.FLAG_VSYNC_HINT)

    pr.init_window(700, 700, "Rotochess")
    pr.set_target_fps(60)

    camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
    camera.projection = pr.CameraProjection.CAMERA_PERSPECTIVE
    pr.set_camera_mode(camera, pr.CAMERA_FREE)
    pr.set_camera_alt_control(pr.KEY_LEFT_SHIFT)

    sz = 1

    cc = ChessCube(sz, 0)
    lc = cc.pieces

    #lc[0,2,2] = 6
    #lc[2,2,2] = 6
    #lc[3,2,2] = 6
    #lc[1,2,2] = 6
    print(lc)

    while not pr.window_should_close():
        if pr.is_key_pressed(pr.KeyboardKey.KEY_W):
            cc.rotate_x(0)
            print(lc)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_S):
            cc.rotate_y(0)
            print(lc)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_D):
            cc.rotate_z(0)
            print(lc)

        pr.update_camera(camera)
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        pr.begin_mode_3d(camera)
        pr.draw_grid(16, 2)

        pr.draw_cube(pr.Vector3(0,0,0), sz,sz,sz, pr.DARKGRAY)

        draw_xz_face(lc[0], pr.Vector3(0,sz/2,0), pr.Vector3(0,0,1), pr.Vector3(1,0,0), sz, pr.RED)
        draw_xz_face(lc[1], pr.Vector3(0,-sz/2,0), pr.Vector3(0,0,1), pr.Vector3(-1,0,0), sz, pr.ORANGE)

        draw_xy_face(lc[4], pr.Vector3(0,0,sz/2), pr.Vector3(-1,0,0), pr.Vector3(0,-1,0), sz, pr.GREEN)
        draw_xy_face(lc[5], pr.Vector3(0,0,-sz/2), pr.Vector3(1,0,0), pr.Vector3(0,-1,0), sz, pr.YELLOW)

        draw_zy_face(lc[2], pr.Vector3(-sz/2,0,0), pr.Vector3(0,0,1), pr.Vector3(0,1,0), sz, pr.PURPLE)
        draw_zy_face(lc[3], pr.Vector3(sz/2,0,0), pr.Vector3(0,0,1), pr.Vector3(0,-1,0), sz, pr.BLUE)

        pr.end_mode_3d()
        pr.end_drawing()
    pr.close_window()

if __name__ == "__main__":
    main()