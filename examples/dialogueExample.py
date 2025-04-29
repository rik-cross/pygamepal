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
pygame.display.set_caption('Dialogue Example')
clock = pygame.time.Clock()

# create new dialogue box
dialogueBox = pygamepal.Dialogue(
    font = pygamepal.largeFont,
    position = (20, 300),
    size = (640, 140),
    textColor = (24, 20, 37),
    borderColor = (24, 20, 37),
    backgroundColor = (234, 212, 170),
    borderWidth = 6,
    textEffect = 'tick',
    tickSound = pygame.mixer.Sound(os.path.join('sounds', 'blip.wav')),
    borderRadius = 6
)

dialogueBox.addPage(
    "Here is some text, automatically split across multiple rows! You can set the text speed, colour and effect. Press [Enter] to skip / advance.",
)

dialogueBox.addPage(
    "You can also add images to dialogue pages, as well as specify the background colour.",
    texture = pygame.image.load(os.path.join('images', 'character.png')),
    textureBackgroundColor = (194, 133, 105)
)

dialogueBox.addPage(
    "You can add a different image to each dialogue page, as well as left- or right-align the image.",
    textureBackgroundColor = (194, 133, 105),
    texture = pygame.image.load(os.path.join('images', 'chest.png')),
    textureAlignment = 'right'
)

input = pygamepal.Input()

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

    # update input
    input.update()

    # update dialogue box
    dialogueBox.update()

    #
    # input
    #

    # enter to advance the dialogue
    if input.isKeyPressed(pygame.K_RETURN):
        dialogueBox.advance()

    #
    # draw
    #

    # clear screen
    screen.fill('cornflowerblue')

    # draw dialogue box
    dialogueBox.draw(screen)

    # draw to screen
    pygame.display.flip()

# quit Pygame
pygame.quit()