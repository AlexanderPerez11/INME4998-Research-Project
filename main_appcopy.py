import pygame_textinput
import SensorDataProcessingModule
import os
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
import pyrr
import numpy as np
from TextureLoader import load_texture_pygame
from ObjLoader import ObjLoader
from camera import Camera

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

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

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (100, 100, 100)
dark_gray = (50, 50, 50)

screen_size = width, length = (1080, 520)

filename = "Text"

title_font = pygame.font.SysFont("Times New Roman", 24)
general_font = pygame.font.SysFont('Times New Roman', 18)

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True

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


def blit_text(surface, text, pos, font, color=white):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()

    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def main():
    global filename, kinematic_data
    # Create TextInput-object
    textinput = pygame_textinput.TextInput()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    title = "INME 4998 Research Project"
    instructions = """
    This application takes in two sets of information from a six degree of freedom IMU unit and process the
    data to produce an animation in a 3-D space created with Open GL for an easy to interpret visualization 
    of the sensor data. Data must adhere to the following guidelines so that the limitations of the program
    do not become an issue. 
    -- Data for the sensors must be of similar length and should not exceed values of 50
    -- Data may only include movements that are not to rash and a calibration time of at least 5 seconds should 
       be allowed to permit for noise removal algorithm to work appropriately
    -- If data should contain pauses in movement (zero velocity instances) then a reasonable window of at least
       4.5 seconds should be allowed for the program to register such an event
    """

    options_1 = """Enter file name here and press Enter:"""
    options_2 = """Press Esc to exit"""

    typing = False
    while True:
        screen.fill(black)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()

        blit_text(screen, title, (20, 20), title_font)
        blit_text(screen, instructions, (20, 40), general_font)
        blit_text(screen, options_1, (20, 300), general_font)
        blit_text(screen, options_2, (930, 20), general_font)

        mouse_pos = pygame.mouse.get_pos()
        xpos = mouse_pos[0]
        ypos = mouse_pos[1]

        if xpos > 20 and (xpos < 20 + 500) and ypos > 320 and (ypos < 320 + 25) \
                and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            textinput.clear_text()
            typing = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                filename = textinput.get_text()
                kinematic_data = np.array(SensorDataProcessingModule.process_data(filename))
                typing = False

        if typing:
            textinput.update(events)
            pygame.draw.lines(screen, light_gray, True, [[20, 320], [520, 320], [520, 345], [20, 345]])
            screen.blit(textinput.get_surface(), (25, 325))

        if not typing:
            pygame.draw.lines(screen, white, True, [[20, 320], [520, 320], [520, 345], [20, 345]])

        if xpos > 150 and (xpos < 150 + 200) and ypos > 400 and (ypos < 400 + 50):
            pygame.draw.rect(screen, dark_gray, (150, 400, 200, 50))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                graphing_menu()
        else:
            pygame.draw.rect(screen, light_gray, (150, 400, 200, 50))

        textSurf, textRect = text_objects("To Graphing Module", general_font)
        textRect.center = ((150 + (200 / 2)), (400 + (50 / 2)))
        screen.blit(textSurf, textRect)

        if xpos > 730 and (xpos < 730 + 200) and ypos > 400 and (ypos < 400 + 50):
            pygame.draw.rect(screen, dark_gray, (730, 400, 200, 50))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                animation_menu()
        else:
            pygame.draw.rect(screen, light_gray, (730, 400, 200, 50))

        textSurf, textRect = text_objects("To Animation Module", general_font)
        textRect.center = ((730 + (200 / 2)), (400 + (50 / 2)))
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(30)


def graphing_menu():
    global filename
    global kinematic_data
    running = True
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    while running:
        screen.fill(black)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.quit()

        textSurf, textRect = text_objects(str(filename), general_font)
        textRect.center = ((150 + (200 / 2)), (400 + (50 / 2)))
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(30)


def animation_menu():
    global filename
    global kinematic_data
    title = "INME 4998 Research Project Animation Module"
    instructions = """
    This module allows the visualization of the provided data in a 
    3-D environment created using Open GL. There are 4 camera modes 
    binded to numbers 1, 2, 3, and 4 respectively:
    --Press 1 for a Top View of the scene
    --Press 2 for a Front View of the scene
    --Press 3 for an Isometric View of the scene
    --Press 4 for Free Roam of the scene
    
    In Free Roam mode you can move about the scene however you like. 
    --Use WASD keys to move forward, left, backwards
        and right respectively
    --Press Space bar to ascend
    --Press left control to descend
    --Press shift + any direction to 
        speed up in that direction
    --Look around with your mouse.
        
    To start the animation press Enter
    To reset the animation and view again press R
    Press Escape to return to this menu
    """

    options_1 = """Press Esc to return to Main Menu"""

    running = True
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    while running:
        screen.fill(black)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        blit_text(screen, title, (20, 20), title_font)
        blit_text(screen, instructions, (20, 40), general_font)
        blit_text(screen, options_1, (930, 20), general_font)

        mouse_pos = pygame.mouse.get_pos()
        xpos = mouse_pos[0]
        ypos = mouse_pos[1]

        if xpos > 730 and (xpos < 730 + 200) and ypos > 400 and (ypos < 400 + 50):
            pygame.draw.rect(screen, dark_gray, (730, 400, 200, 50))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                animation()
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                screen = pygame.display.set_mode(screen_size)
        else:
            pygame.draw.rect(screen, light_gray, (730, 400, 200, 50))

        textSurf, textRect = text_objects("View Animation", general_font)
        textRect.center = ((730 + (200 / 2)), (400 + (50 / 2)))
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(30)


def animation():
    # Import position data for x y z coordinates
    global kinematic_data, model
    x = kinematic_data[7][0]
    y = kinematic_data[8][0]
    z = kinematic_data[9][0]

    # Load 3d Meshes
    cube_indices, cube_buffer = ObjLoader.load_model("meshes/Rubiks Cube.obj")
    grid_indices, grid_buffer = ObjLoader.load_model("meshes/uv grid floor.obj")

    # Set up a pg display with Open GL buffer and double buff an d resizable tags
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

    pygame.mouse.set_visible(False)
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

    # Perspective, aspect ratio, near clipping plane, far clipping plane
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 50)

    grid_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -2, 0]))

    # Call matrices locations in the shader source code
    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")

    # Upload static matrices to the shader program
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    # Set up main application loop
    running = True
    do_move = False
    reset = False
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
        if keys_pressed[pygame.K_RETURN]:
            do_move = True
        if keys_pressed[pygame.K_r]:
            reset = True
        if keys_pressed[pygame.K_1]:
            cam.camera_mode("TOPVIEW")
        if keys_pressed[pygame.K_2]:
            cam.camera_mode("FRONTVIEW")
        if keys_pressed[pygame.K_3]:
            cam.camera_mode("ISOMETRICVIEW")
        if keys_pressed[pygame.K_4]:
            cam.camera_mode("FREECAM")
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

        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] <= 0:
            pygame.mouse.set_pos((1279, mouse_pos[1]))
        elif mouse_pos[0] >= 1279:
            pygame.mouse.set_pos((0, mouse_pos[1]))

        mouse_look(mouse_pos[0], mouse_pos[1])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        if not do_move:
            model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

        elif do_move:
            model = pyrr.matrix44.create_from_translation(pyrr.Vector3([x[i], y[i], z[i]]))

        glBindVertexArray(VAO[0])
        glBindTexture(GL_TEXTURE_2D, texture[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(cube_indices))

        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, texture[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, grid_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(grid_indices))

        pygame.display.flip()
        pygame.time.wait(10)
        if reset:
            i = 0
            reset = False
            do_move = False
        if do_move:
            if i < len(x) - 1:
                i += 1


main()
