#
# pygameTemplate.py
# part of the pygame_utils library
# github.com/rik-cross/pygame_utils
#

import pygame
import pygame_utils

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('[Caption]')
clock = pygame.time.Clock() 

s = pygame_utils.SpriteImage()

# game loop
running = True
while running:

    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')

    # advance clock at 60 FPS
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # input
    #

    # add code here

    #
    # update
    #

    s.update()

    #
    # draw
    #

    s.draw(screen, 10, 10)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
