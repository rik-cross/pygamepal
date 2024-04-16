#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

# import modules
import pygame
import pygamepal
import os

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Transition Example')
clock = pygame.time.Clock() 

# load a texture
texture = pygame.image.load(os.path.join('images','character_spritesheet.png'))

# first surface
surface1 = pygame.Surface((680, 460))
surface1.fill('mediumpurple')
surface1.blit(texture, (400, 100))

# second surface
surface2 = pygame.Surface((680, 460))
surface2.fill('goldenrod')
surface2.blit(texture, (100, 100))

# transition
transition = pygamepal.TransitionWipeRight(
    surface1, 
    surface2, 
    duration = 200, 
    easingFunction=pygamepal.bounceEaseOut)

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
    # update
    #

    # update the transition if it hasn't finished
    if transition.finished is False:
        transition.update()

    #
    # draw
    #

    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
  
    # draw the transition if it isn't finished...
    if transition.finished is False:
        transition.draw(screen)
    # ...otherwise draw the second surface
    else:
        screen.blit(surface2, (0, 0))

    # draw to the screen
    pygame.display.flip()

#quit Pygame on exit
pygame.quit()
