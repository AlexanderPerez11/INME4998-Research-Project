import pygame as pg

pg.init()
screen_width = 1280
screen_height = 720
screen = pg.display.set_mode((screen_width, screen_height))
# Create colors for backgrounds and text
black = (0, 0, 0)
white = (255, 255, 255)
def text_rectangles(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def text_objects(text, font):
    paragraph_size = (800, 600)
    font_size = font.get_height()

    paragraph_surface = pg.Surface(paragraph_size)
    paragraph_surface.fill(black)
    paragraph_surface.set_colorkey(black)

    splitlines = text.splitlines()
    offset =((paragraph_size[1] - len(splitlines)) * (font_size + 1))//2

    for idx, line in enumerate(splitlines):
        currentTextline = font.render(line, False, (0, 0, 0))
        currentPosition = (0, idx * font_size + offset)
        paragraph_surface.blit(currentTextline, currentPosition)
    return paragraph_surface, paragraph_size

running = True

paragraph = """
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

app_font = pg.font.SysFont("Times New Roman", 12)
text_surface, text_rect = text_objects(paragraph, app_font)
screen.blit(text_surface, text_rect)

# text_objects(paragraph, app_font)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    pg.display.update()
    pg.time.wait(10)
