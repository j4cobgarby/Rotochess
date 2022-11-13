#!/usr/bin/env python

import pyray as pr
import random
import time as t

def main():
    size = 7
    cubelet_size = 2
    pr.set_config_flags(pr.ConfigFlags.FLAG_MSAA_4X_HINT)
    pr.set_config_flags(pr.ConfigFlags.FLAG_VSYNC_HINT)

    pr.init_window(700, 700, "Rotochess")
    
    #####################
    # POST INIT IMPORTS #
    #####################
    
    from chesscube import ChessCube

    pr.set_target_fps(60)

    world = ChessCube(size,cubelet_size)

    camera = pr.Camera3D([18.0, world.size*3+16, 18.0], [0.0, world.size*3, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
    camera.projection = pr.CameraProjection.CAMERA_ORTHOGRAPHIC
    pr.set_camera_mode(camera, pr.CAMERA_FREE)
    pr.set_camera_alt_control(pr.KEY_LEFT_SHIFT)

    # Shaders
    # Background
    imBlank = pr.gen_image_color(1024, 1024, pr.WHITE)
    bg_texture = pr.load_texture_from_image(imBlank)
    pr.unload_image(imBlank)

    grad = pr.load_shader("shaders/base.vs","shaders/bg.fs")
    time = 0
    timeLoc = pr.get_shader_location(grad, "uTime")
    pr.set_shader_value(grad, timeLoc, time, pr.ShaderUniformDataType.SHADER_UNIFORM_FLOAT)

    # Bloom
    bloom = pr.load_shader("shaders/base.vs", "shaders/base.fs")
    target = pr.load_render_texture(pr.get_screen_width(), pr.get_screen_height())

    camera.fovy = world.size*1.87+2

    animation = 1
    ani_state = -1
    running = False

    dragging = 0

    rot_table = [
        [[1,0,0,0],[3,0,0,0],[0,0,1,0],[0,0,3,0]], # Up
        [[3,0,0,1],[1,0,0,1],[0,0,1,0],[0,0,3,0]], # Down
        [[0,3,0,0],[0,1,0,0],[0,0,1,0],[0,0,3,0]], # Left
        [[0,1,0,1],[0,3,0,1],[0,0,1,0],[0,0,3,0]], # Right
        [[0,1,0,1],[0,3,0,1],[1,0,0,1],[3,0,0,1]], # Front
        [[0,1,0,1],[0,3,0,1],[3,0,0,0],[1,0,0,0]], # Back


    ]

    while not pr.window_should_close():
        pr.set_shader_value(grad, timeLoc, pr.get_time(), pr.ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
        if ani_state == -1:
            if pr.is_key_down(pr.KEY_SPACE):
                ani_state = 0

        # Start up easing
        if ani_state == 0:
            animation = animation * 0.95
            camera.position.y = 16 + world.size*animation*3
            camera.target.y = world.size*animation*3

            if animation <= 0.001:
                ani_state = 1
                camera.position.y = 16
                camera.target.y = 0
                animation = 1

        if ani_state == 1:
            animation = animation * 0.97
            world.offset = world.size*animation*3 +0.04
            if animation <= 0.001:
                print("AHHHHHHHh")
                ani_state = 2
                running = True
                world.offset = 0.05

        if running:
            #world.offset = max(world.offset -0.1,0)

            if pr.is_key_down(pr.KEY_W):
                world.rotate_x(random.randrange(world.size))
            if pr.is_key_down(pr.KEY_S):
                world.rotate_y(random.randrange(world.size))
            if pr.is_key_down(pr.KEY_D):
                world.rotate_z(random.randrange(world.size))

            if pr.is_mouse_button_down(pr.MOUSE_LEFT_BUTTON):
                if dragging == 0:
                    print("Click")
                    dragging = 1
                    last_mouse = world.mouse
                if dragging == 1:
                    if last_mouse != world.mouse:
                        dragging = 2

                        print("Going")
                        if last_mouse[0] == world.mouse[0]:
                            if last_mouse[1] == world.mouse[1] +1:
                                world.spin(rot_table[last_mouse[0]][0],last_mouse[2])
                            if last_mouse[1] == world.mouse[1] -1:
                                world.spin(rot_table[last_mouse[0]][1],last_mouse[2])
                            if last_mouse[2] == world.mouse[2] +1:
                                world.spin(rot_table[last_mouse[0]][2],last_mouse[1])
                            if last_mouse[2] == world.mouse[2] -1:
                                world.spin(rot_table[last_mouse[0]][3],last_mouse[1])
            if pr.is_mouse_button_up(pr.MOUSE_LEFT_BUTTON):
                dragging = 0
        pr.update_camera(camera)
        # Update lighting

        camPos = [camera.position.x, camera.position.y, camera.position.y]
        #pr.set_shader_value(lighting, lighting.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW], camPos, pr.ShaderUniformDataType.SHADER_UNIFORM_VEC3)

        # Render Cube
        pr.begin_texture_mode(target) # START TEXTURE
        
        pr.clear_background(pr.RAYWHITE)
        
        # Background Shader
        time = pr.get_time()
        pr.set_shader_value(grad,timeLoc,time, pr.ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
        pr.begin_shader_mode(grad)
        pr.draw_texture(bg_texture, 0, 0, pr.WHITE)
        pr.end_shader_mode()

        pr.begin_mode_3d(camera)
        
        world.ray = pr.get_mouse_ray(pr.get_mouse_position(), camera)
        world.draw()
        world.mousedist = 1000

        pr.end_mode_3d()
        pr.end_texture_mode() # END TEXTURE

        # Post Processing Shader

        pr.begin_drawing()

        # Post Processing Shader
        pr.begin_shader_mode(bloom)

        pr.draw_texture_rec(
            target.texture, 
            pr.Rectangle(0, 0, target.texture.width, -target.texture.height), 
            pr.Vector2(0, 0), 
            pr.WHITE
        )

        pr.end_shader_mode()

        pr.end_drawing()
    pr.close_window()

if __name__ == "__main__":
    main()