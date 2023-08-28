#
# pygameTemplate.py
# part of the pygame_utils library
# github.com/rik-cross/pygame_utils
#

import pygame

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('[Caption]')
clock = pygame.time.Clock() 

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

    # add code here

    #
    # draw
    #

    # add code here

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
