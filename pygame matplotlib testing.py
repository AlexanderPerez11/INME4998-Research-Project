import matplotlib
import matplotlib.backends.backend_agg as agg
import pylab
import pygame
from pygame.locals import *

matplotlib.use("Agg")

fig = pylab.figure(figsize=[9, 9], dpi=100)
ax = fig.add_subplot(111, autoscale_on=False,xlim=(-2, 2), ylim=(-2, 2))



pylab.subplots_adjust(wspace=0.2, hspace=0.8)





pygame.init()

window = pygame.display.set_mode((900, 900), DOUBLEBUF)
screen = pygame.display.get_surface()

ax.plot([1, 2, 3, 4])


a = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.10]
crashed = False
i=0
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    ax.plot(a[i], 0, "ko")
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()

    size = canvas.get_width_height()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))

    ax.cla()
    ax.grid()
    ax.xlim = (-2,2)
    ax.autoscale = False

    pygame.display.flip()
    pygame.time.wait(1000)
    if i < len(a)-1:
        i +=1
        print(i)
