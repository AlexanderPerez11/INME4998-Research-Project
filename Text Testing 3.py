import pygame
import pygame_textinput
pygame.init()


SIZE = WIDTH, HEIGHT = (1280, 720)
FPS = 30
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
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

def main():
    textinput = pygame_textinput.TextInput()
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

    options_1 = """
            Press 1 to view graphs
            """
    options_2 = """
            Press 2 to view animations
            """

    title_font = pygame.font.SysFont("Times New Roman", 24)
    instructions_font = pygame.font.SysFont('Times New Roman', 18)
    options_font = pygame.font.SysFont('Times New Roman', 18)

    while True:

        dt = clock.tick(FPS) / 1000
        events = pygame.event.get()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        events = pygame.event.get()

        screen.fill(pygame.Color('white'))
        blit_text(screen, title, (20, 20), title_font)
        blit_text(screen, instructions, (20, 40), instructions_font)
        blit_text(screen, options_1, (20, 300), options_font)
        blit_text(screen, options_2, (20, 350), options_font)
        textinput.update(events)
        screen.blit(textinput.get_surface(), (20, 600))
        pygame.display.update()
        clock.tick(30)

main()