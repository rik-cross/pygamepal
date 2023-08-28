#
# pygame_utils -- Camera Example
# part of the pygame_utils library
#  -- github.com/rik-cross/pygame_utils
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

# create surface for the camera to draw
cameraSurface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)

camera = pygame_utils.Camera(position=(300, 100),
                        size=(300, 300),
                        zoom=5,
                        # the camera center
                        target=(0, 0),
                        borderThickness=4,
                        backgroundColour='gray10',
                        # lazy follow
                        followDelay=0.9)

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
        camera.target = (camera.target[0]-1, camera.target[1])
    if input.isKeyDown(pygame.K_RIGHT):
        camera.target = (camera.target[0]+1, camera.target[1])
    if input.isKeyDown(pygame.K_UP):
        camera.target = (camera.target[0], camera.target[1]-1)
    if input.isKeyDown(pygame.K_DOWN):
        camera.target = (camera.target[0], camera.target[1]+1)
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

    # don't forget to clear the camera surface!
    cameraSurface.fill((0, 0, 0, 0))

    # draw multiple images to the surface to be rendered by the camera
    for i in range(0, 200, 25):
        for j in range(0, 200, 25):
                cameraSurface.blit(texture, (i, j))

    # draw the images (without the camera) 
    screen.blit(cameraSurface, (0, 0))

    # draw the instructions
    pygame_utils.drawText(screen, 'Arrow keys to pan, z/x to zoom', 300, 60)

    # use the camera to draw the images on the cameraSurface to the screen
    camera.draw(cameraSurface, screen)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
