#
# pygame_utils -- Camera Example
#
# instructions:
#  -- arrow keys to pan
#  -- z/x to zoom
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygame_utils
import os

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Camera Example')
clock = pygame.time.Clock() 

# add input, to allow camera control
input = pygame_utils.Input()

# load a texture
texture = pygame.image.load(os.path.join('images','character.png'))

# drawing surface
d = pygame.Surface((200, 200), pygame.SRCALPHA, 32)

c = pygame_utils.Camera(position=(300, 100),
                        size=(300, 300),
                        zoom=5, target=(0, 0),
                        borderThickness=4)

input = pygame_utils.Input()

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

    # arrow keys to pan
    if input.isKeyDown(pygame.K_LEFT):
        c.target = (c.target[0]-1, c.target[1])
    if input.isKeyDown(pygame.K_RIGHT):
        c.target = (c.target[0]+1, c.target[1])
    if input.isKeyDown(pygame.K_UP):
        c.target = (c.target[0], c.target[1]-1)
    if input.isKeyDown(pygame.K_DOWN):
        c.target = (c.target[0], c.target[1]+1)
    # z/x to zoom
    if input.isKeyDown(pygame.K_z):
        c.zoom -= 0.1
    if input.isKeyDown(pygame.K_x):
        c.zoom += 0.1

    #
    # update
    #

    input.update()
    c.update()

    #
    # draw
    #

    # draw multiple images to the surface to be rendered by the camera
    for i in range(0, 200, 25):
        for j in range(0, 200, 25):
                d.blit(texture, (i, j))

    # draw the images (without the camera) 
    screen.blit(d, (0, 0))

    # draw the instructions
    pygame_utils.drawText(screen, 'Arrow keys to pan, z/x to zoom', 300, 60)

    # use the camera to draw the images
    c.draw(d, screen)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
