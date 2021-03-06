# Import necessary libraries and dependencies
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
import numpy as np
import pyrr
from TextureLoader import load_texture_pygame
from ObjLoader import ObjLoader

from camera import Camera

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True

# Write out the shader program source code in Open GL C++
vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
out vec2 v_texture;
void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


def mouse_look(xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)


def main_menu():
    pass




# Load 3d Meshes
cube_indices, cube_buffer = ObjLoader.load_model("meshes/Rubiks Cube.obj")
grid_indices, grid_buffer = ObjLoader.load_model("meshes/uv grid floor.obj")

# Initialize a pygame application
pygame.init()

# Set up a pygame display with Open GL buffer and double buff an d resizable tags
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

# pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Compile the shader program with the source vertex and fragment codes
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Generate Vertex Array Objects, Vertex Buffer Objects and Element Buffer Objects for each geometry
VAO = glGenVertexArrays(2)
VBO = glGenBuffers(2)
EBO = glGenBuffers(2)
# Cube VAO
glBindVertexArray(VAO[0])
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)

# Cube Element Buffer Object
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[0])
glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))

# Grid Floor VAO
glBindVertexArray(VAO[1])
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, grid_buffer.nbytes, grid_buffer, GL_STATIC_DRAW)

# Quad Element Buffer Object
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[1])
glBufferData(GL_ELEMENT_ARRAY_BUFFER, grid_buffer.nbytes, grid_buffer, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, grid_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, grid_buffer.itemsize * 8, ctypes.c_void_p(12))

# Generate and load all necessary textures
texture = glGenTextures(2)

load_texture_pygame("textures/Complete Rubiks Cube.png", texture[0])
load_texture_pygame("textures/uv grid floor.png", texture[1])

# Load Shader program and set up environment on window
glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Create all necessary matrices for projections, positions and views

# Perspective, aspect ratio, near clipping plane, far clipping plane
projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 50)

grid_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -2, 0]))

# Position, target, up
# view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2.5, 10]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

# Call matrices locations in the shader source code
model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
switcher_loc = glGetUniformLocation(shader, "switcher")

# Upload static matrices to the shader program
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
# glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

def animation(x_translation, y_translation, z_translation):
    # Import position data for x y z coordinates
    # x = 10*x_translation
    # y = 10*y_translation
    # z = 10*z_translation

    theta_x = x_translation
    theta_y = z_translation
    theta_z = y_translation
    # Set up main application loop
    running = True
    default_view = False
    # do_move = False
    i = 0

    while running:
        for event in pygame.event.get():

            # Check if the window was closed
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # Check if the window was resized
            if event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
                projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
                glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        velocity = 0.08
        keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[pygame.K_KP_ENTER]:
        #     do_move = True
        if keys_pressed[pygame.K_LSHIFT]:
            velocity = 0.5
        if keys_pressed[pygame.K_a]:
            cam.process_keyboard("LEFT", velocity)
        if keys_pressed[pygame.K_d]:
            cam.process_keyboard("RIGHT", velocity)
        if keys_pressed[pygame.K_w]:
            cam.process_keyboard("FORWARD", velocity)
        if keys_pressed[pygame.K_s]:
            cam.process_keyboard("BACKWARD", velocity)
        if keys_pressed[pygame.K_SPACE]:
            cam.process_keyboard("UP", velocity)
        if keys_pressed[pygame.K_LCTRL]:
            cam.process_keyboard("DOWN", velocity)
        if keys_pressed[pygame.K_1]:
            cam.camera_mode("TOPVIEW")
        if keys_pressed[pygame.K_2]:
            cam.camera_mode("FRONTVIEW")
        if keys_pressed[pygame.K_ESCAPE]:
            running = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_look(mouse_pos[0], mouse_pos[1])

        if mouse_pos[0] == 0:
            pygame.mouse.set_pos((1279, mouse_pos[1]))
        elif mouse_pos[0] == 1279:
            pygame.mouse.set_pos((0, mouse_pos[1]))

        ct = pygame.time.get_ticks() / 1000

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        # glUniform1i(switcher_loc, 0)

        rot_x = pyrr.Matrix44.from_x_rotation(theta_x[i])
        rot_y = pyrr.Matrix44.from_y_rotation(theta_y[i])
        rot_z = pyrr.Matrix44.from_z_rotation(theta_z[i])

        rotation = pyrr.matrix44.multiply(rot_x, rot_y)
        rotation = pyrr.matrix44.multiply(rotation, rot_z)
        # if do_move == False:
        #     cube_translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        # elif do_move == True:
        #     cube_translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([x[i], y[i], z[i]]))
        # cube_translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,0]))

        # model = pyrr.matrix44.multiply(rotation, cube_translation)

        glBindVertexArray(VAO[0])
        glBindTexture(GL_TEXTURE_2D, texture[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, rotation)
        glDrawArrays(GL_TRIANGLES, 0, len(cube_indices))

        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, texture[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, grid_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(grid_indices))

        pygame.display.flip()
        pygame.time.wait(10)
        if i < len(theta_x) - 1:
            i += 1

    pygame.quit()



