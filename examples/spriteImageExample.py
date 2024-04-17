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

# setup screen
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('SpriteImage Example')
clock = pygame.time.Clock() 

# load a texture
texture = pygame.image.load(os.path.join('images','character_spritesheet.png'))
# double the texture size
texture = pygame.transform.scale(texture, (texture.get_width() * 2,texture.get_height() * 2))
# split texture into a 2D list of sub-textures
splitTextures = pygamepal.splitTexture(texture, 96, 96)

# an animated sprite with multiple textures
spriteImage = pygamepal.SpriteImage()
spriteImage.addTextures(splitTextures[3][1], splitTextures[3][2], splitTextures[3][1], splitTextures[3][3], offset=(17 * 2, 16 * 2))
# simple alternative for single textures:
# spriteImage1.addTextures(pygame.image.load('image1.png'), pygame.image.load('image2.png'))

# game loop
running = True
while running:

    # advance clock
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # update
    #

    spriteImage.update()

    #
    # draw
    #

    # clear screen
    screen.fill('cornflowerblue')
    
    # draw sprites and accompanying text
    spriteImage.draw(screen, 50, 50)

    # draw to screen
    pygame.display.flip()

# quit Pygame
pygame.quit()