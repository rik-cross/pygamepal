#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- arrow keys to move trigger 1
#

import pygame
import pygamepal

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Collider Example')
clock = pygame.time.Clock() 

# create 2 colliders

collider1 = pygamepal.Collider(position = (50, 50), size = (100, 100))
collider2 = pygamepal.Collider(position = (290, 180), size = (100, 100))

# add input, to allow camera control
input = pygamepal.Input()

# game loop
running = True
while running:

    # advance clock at 60 FPS
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # input
    #

    # arrow keys to pan
    if input.isKeyDown(pygame.K_LEFT):
        collider1.x -= 2
    if input.isKeyDown(pygame.K_RIGHT):
        collider1.x += 2
    if input.isKeyDown(pygame.K_UP):
        collider1.y -= 2
    if input.isKeyDown(pygame.K_DOWN):
        collider1.y += 2

    #
    # update
    #

    input.update()

    # the trigger update method needs to be explicitly called
    # if it isn't added to a scene or a sprite
    collider1.update()
    collider2.update()

    #
    # draw
    #
  
    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
  
    # the trigger draw method needs to be explicitly called
    # if it isn't added to a scene or a sprite
    collider1.draw(screen)
    collider2.draw(screen)

    pygamepal.drawText(screen, "Arrow keys to move collider 1", (10, 10))

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()