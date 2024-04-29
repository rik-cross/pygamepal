#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- arrow keys to pan
#  -- z/x to zoom
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygamepal
import os

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Camera Example')
clock = pygame.time.Clock() 

# add input, to allow camera control
input = pygamepal.Input()

# load a texture
mapTexture = pygame.image.load(os.path.join('images','map.png'))

# create surface for the camera to draw
cameraSurface = pygame.Surface(mapTexture.get_size(), pygame.SRCALPHA, 32)

camera = pygamepal.Camera(
    position = (190, 100),
    size = (300, 300),
    # the camera center
    target = (100, 100),
    # lazy follow target (between 0 and 1)
    lazyFollow = 0.9,
    zoom = 5,
    backgroundColour = 'gray10',
    borderColour = 'white',
    borderThickness = 4,
    # set a clamp rectangle that is the size of
    # the set of images to be drawn
    clamp = True,
    clampRect = (0, 0, mapTexture.get_size()[0], mapTexture.get_size()[0])
    )

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
        camera.target = (camera.target[0] - 1, camera.target[1])
    if input.isKeyDown(pygame.K_RIGHT):
        camera.target = (camera.target[0] + 1, camera.target[1])
    if input.isKeyDown(pygame.K_UP):
        camera.target = (camera.target[0], camera.target[1] - 1)
    if input.isKeyDown(pygame.K_DOWN):
        camera.target = (camera.target[0], camera.target[1] + 1)
    
    # z/x to zoom
    if input.isKeyDown(pygame.K_z):
        camera.zoom -= 0.1
    if input.isKeyDown(pygame.K_x):
        camera.zoom += 0.1

    #
    # update
    #

    input.update()
    camera.update()

    #
    # draw
    #
  
    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
  
    # don't forget to clear the camera surface!
    cameraSurface.fill((0, 0, 0, 0))

    # draw the map
    cameraSurface.blit(mapTexture, (0, 0))

    # draw the instructions
    pygamepal.drawText(screen, 'Arrow keys to pan, z/x to zoom', 190, 60)

    # use the camera to draw the images on the cameraSurface to the screen
    camera.draw(cameraSurface, screen)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()