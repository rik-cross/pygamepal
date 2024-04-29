#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions
#  -- press / hold / release the left mouse button
#  -- and watch console output
#

# import modules
import pygame
import pygamepal

# initialise Pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Mouse Input Example')
clock = pygame.time.Clock()

input = pygamepal.Input()

# game loop
running = True
while running:

    # advance clock
    clock.tick(60)

    deltaTime = clock.get_time()

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # update
    #

    # update input manager
    input.update()

    #
    # draw
    #

    # clear screen
    screen.fill('cornflowerblue')
    
    # input text
    mouseButton = 0
    text = "Mouse position: " + str(input.getMouseCursorPosition()) + \
        ", down: " + str(input.isMouseButtonDown(0)) + \
        ", pressed: " + str(input.isMouseButtonPressed(0)) + \
        ", double pressed: " + str(input.isMouseButtonDoublePressed(0)) + \
        ", released: " + str(input.isMouseButtonReleased(0)) + \
        ", long down: " + str(input.isMouseButtonLongDown(0)) + \
        ", long press: " + str(input.isMouseButtonLongPressed(0)) + \
        ", long%: " + \
        "{:.2f}".format(input.getMouseButtonLongPressPercentage(mouseButton))

    print(text)

    # draw to screen
    pygame.display.flip()

#  quit Pygame
pygame.quit()
