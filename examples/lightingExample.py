#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- arrow keys to move light
#

import pygame
import pygamepal

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Lighting Example')
clock = pygame.time.Clock() 

# add input, to allow light control
input = pygamepal.Input()

# create a new lighting object and add a light
lighting = pygamepal.Lighting(surfaceSize=(680, 460), lightLevel=0.1)
lighting.addLight(pygamepal.Light(position=(340, 230), radius=300, name='testLight'))

# add a map texture
mapTexture = pygame.image.load('images/map.png')
# TODO -- scale function
mapTexture = pygame.transform.scale(mapTexture, (mapTexture.get_width() * 4, mapTexture.get_height() * 4))

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

    if input.isKeyDown(pygame.K_LEFT):
        lighting.getLight('testLight').position[0] -= 4
    if input.isKeyDown(pygame.K_RIGHT):
        lighting.getLight('testLight').position[0] += 4
    if input.isKeyDown(pygame.K_UP):
        lighting.getLight('testLight').position[1] -= 4
    if input.isKeyDown(pygame.K_DOWN):
        lighting.getLight('testLight').position[1] += 4
    
    if input.isKeyDown(pygame.K_w):
        lighting.getLight('testLight').radius += 1
    if input.isKeyDown(pygame.K_s):
        lighting.getLight('testLight').radius -= 1

    if input.isKeyPressed(pygame.K_t):
        lighting.getLight('testLight').toggle()

    #
    # update
    #

    input.update()
    lighting.update()

    #
    # draw
    #
  
    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')

    # draw the map
    screen.blit(mapTexture, (0, 0))

    # draw the lighting
    lighting.draw(screen)

    # draw the instructions (after / on top of the lighting)
    pygamepal.drawText(screen, "Arrow keys to move the light, W/S to change intensity, T to toggle", (10, 10))

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()