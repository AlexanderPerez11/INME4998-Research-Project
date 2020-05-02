import pygame
import SensorDataProcessingModule

pygame.init()wad
def blit_text(surface, text, pos, font, color=pygame.Color('white')):
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
    SIZE = WIDTH, HEIGHT = (1280, 720)
    FPS = 30
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    red = (0, 255, 0)



    # text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
    #        "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
    #        "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
    #        "text will disappear underneath the surface"
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
    running = True
    while running:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

        screen.fill(pygame.Color('black'))
        blit_text(screen, title, (20, 20), title_font)
        blit_text(screen, instructions, (20, 40), instructions_font)
        blit_text(screen, options_1, (20, 300), options_font)
        blit_text(screen, options_2, (20, 350), options_font)
        pygame.display.update()

pygame.quit()
main()