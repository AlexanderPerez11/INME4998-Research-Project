#!/usr/bin/python3
import pygame_textinput
import pygame
from pygame.locals import *
import numpy as np
import SensorDataProcessingModule

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (100, 100, 100)
dark_gray = (50, 50, 50)
screen_size = width, length = (1080, 520)

filename = "Text"
kinematic_data = None
title_font = pygame.font.SysFont("Times New Roman", 24)
general_font = pygame.font.SysFont('Times New Roman', 18)
global action_1
action_1 = False


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

        # Feed it with events every frame

        # Blit its surface onto the screen
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
                kinematic_data = SensorDataProcessingModule.process_data(filename)
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

        pygame.display.update()
        clock.tick(30)


def graphing_menu():
    global filename
    global kinematic_data
    global action_1
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
                action_1 = True
                pygame.quit()

        textSurf, textRect = text_objects(str(filename), general_font)
        textRect.center = ((150 + (200 / 2)), (400 + (50 / 2)))
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(30)
    return action_1, kinematic_data


def animation_menu():
    global filename
    global kinematic_data
    running_1 = True
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    while running_1:
        screen.fill(black)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_1 = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass

        textSurf, textRect = text_objects(str(filename), general_font)
        textRect.center = ((150 + (200 / 2)), (400 + (50 / 2)))
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(30)

