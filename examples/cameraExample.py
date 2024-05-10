#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- arrow keys to pan
#  -- z/x to zoom
#  -- s to shake
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygamepal
import os
from random import choice

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Camera Example')
clock = pygame.time.Clock() 

# add input, to allow camera control
input = pygamepal.Input()

# load textures
mapTexture = pygame.image.load(os.path.join('images','map.png'))
playerTexture = pygame.image.load(os.path.join('images','character.png'))

# create surface for the camera to draw
cameraSurface = pygame.Surface(mapTexture.get_size(), pygame.SRCALPHA, 32)

camera = pygamepal.Camera(
    position = (190, 100),
    size = (300, 300),
    # the camera center is the player center
    target = (100 + playerTexture.get_width() / 2, 100 + playerTexture.get_height() / 2),
    # lazy follow target (between 0 and 1)
    lazyFollow = 0.9,
    zoom = 5,
    backgroundColor = (0, 0, 0, 0),
    borderColor = 'white',
    borderThickness = 4,
    # set a clamp rectangle that is the size of
    # the set of images to be drawn
    clamp = True,
    clampRect = (0, 0, mapTexture.get_size()[0], mapTexture.get_size()[0])
    )

# canera shake direction choices
cameraShakeDirections = ((-0.8, 0.2), (0.6, -0.5), (0.4, 0.7))

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
        camera.zoom -= 0.05
    if input.isKeyDown(pygame.K_x):
        camera.zoom += 0.05

    # s to shake
    if input.isKeyPressed(pygame.K_s):
        camera.shake(direction = choice(cameraShakeDirections))

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

    # draw the map and player
    cameraSurface.blit(mapTexture, (0, 0))
    cameraSurface.blit(playerTexture, (100, 100))

    # draw the instructions
    pygamepal.drawText(screen, 'Arrow keys to pan, z/x to zoom, s to shake', (190, 60))

    # use the camera to draw the images on the cameraSurface to the screen
    camera.draw(cameraSurface, screen)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
