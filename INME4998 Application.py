import pygame as pg
import SensorDataProcessingModule

def main(running):
    w = 1280
    h = 720
    pg.init()
    display = pg.display.set_mode((w, h))
    running = True
    while running:
        print(
            "This application takes in two sets of information from a six degree of freedom IMU unit and process the \n"
            "data to produce an animation in a 3-D space created with Open GL for an easy to interpret visualization \n"
            "of the sensor data")
        a = input()
        if a == "e":
            running = False
