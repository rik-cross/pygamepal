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
pygame.display.set_caption('Animator Example')
clock = pygame.time.Clock() 

# create player sprite
playerTexture = pygame.image.load(os.path.join('images', 'character.png'))
playerTexture = pygame.transform.scale(playerTexture, (playerTexture.get_width() * 4, playerTexture.get_height() * 4))
playerSprite = pygamepal.Sprite(texture=playerTexture, size=(playerTexture.get_width(), playerTexture.get_height()), position=(100, 100))

# create rectangle
rectangle = pygame.Rect(300, 99, 50, 66)

# create a colour
colour = pygame.Color(255, 255, 255)

# create an animator
animator = pygamepal.Animator()

# create a frame counter
frame = 0

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

    # move the rectangle to the right
    if frame == 50:
        animator.addAnimation(rectangle, 'x', 500, 20)

    # bounce the player sprite to the right
    if frame == 150:
        animator.addAnimation(playerSprite.position, 'x', 501, 50, easingFunction=pygamepal.easeBounceOut)
    
    # change the colour to blue (by setting to (0, 0, 255))
    if frame == 250:
        animator.addAnimation(colour, 'r', 0, 50, type=int)
        animator.addAnimation(colour, 'g', 0, 50, type=int)
    
    # move the rectangle to the left
    if frame == 350:
        animator.addAnimation(rectangle, 'x', 100, 50)
    
    # change the position and size of the rectangle
    if frame == 450:
        animator.addAnimation(rectangle, 'x', 110, 50)
        animator.addAnimation(rectangle, 'y', 110, 50)
        animator.addAnimation(rectangle, 'w', 30, 50)
        animator.addAnimation(rectangle, 'h', 46, 50)
    
    # make the rectangle bigger, using a bounce effect
    if frame == 550:
        animator.addAnimation(rectangle, 'x', 80, 50, pygamepal.easeBounceOut)
        animator.addAnimation(rectangle, 'y', 80, 50, pygamepal.easeBounceOut)
        animator.addAnimation(rectangle, 'w', 90, 50, pygamepal.easeBounceOut)
        animator.addAnimation(rectangle, 'h', 106, 50, pygamepal.easeBounceOut)

    # bounce the player sprite to the left
    if frame == 650:
        animator.addAnimation(playerSprite.position, 'x', 100, 100, easingFunction=pygamepal.easeBounceOut)

    # update the player sprite (without a parent scene)
    playerSprite.updateWithoutParentScene()

    # update the animator
    animator.update()

    #
    # draw
    #

    # clear screen
    screen.fill('cornflowerblue')

    # draw the rectangle in the specified colour
    pygame.draw.rect(screen, colour, rectangle)

    # draw the player sprite (without a parent scene)
    playerSprite.drawWithoutParentScene(screen)

    # draw to screen
    pygame.display.flip()

    # increment frame counter
    frame += 1

# quit Pygame
pygame.quit()