import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
import numpy as np
import pyrr
from TextureLoader import load_texture_pygame
from ObjLoader import ObjLoader

def main_menu():
    pygame.init()
