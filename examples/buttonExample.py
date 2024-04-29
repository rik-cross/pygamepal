#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- click buttons or press [1] / [2] keys to activate
#

import pygame
import pygamepal
import os
from math import cos

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Button Example')
clock = pygame.time.Clock() 

# add input, to allow camera control
input = pygamepal.Input()

# button callbacks
# (note that callbacks need the button as the first argument)

def buttonClicked(button):
    print(button.label, 'clicked!')

def button2Update(button):
    # if creating your own button update method,
    # you may want to update the highlighted
    # and selected values
    button.setHighlighted()
    button.setSelected()
    # update a counter for drawing an arrow
    button.counter += 0.15
    # change the foreground and border if highlighted
    if button.isHighlighted:
        button.fgColor = 'white'
        button.borderWidth = 1
    else:
        button.fgColor = 'gray50'
        button.borderWidth = 0

def button2Draw(button, screen):
    # if creating your own button draw method,
    # you may want to call the methods to draw
    # the component parts of the button
    button.drawBackground(screen)
    button.drawImage(screen)
    button.drawText(screen)
    button.drawBorder(screen)
    # add another image to the highlighted button
    # that moved in a cosine wave left-to-right
    if button.isHighlighted:
        position = (button.position[0] - button.arrow.get_width() + cos(button.counter) * 8,
                    button.position[1] + button.size[1] / 2 - button.arrow.get_height() / 2)
        screen.blit(button.arrow, position)

#
# create some buttons
#

# button 1 is a simple button implementation
button1 = pygamepal.Button(input=input,
                           position = (100, 100),
                           label = 'Button 1',
                           onSelected = buttonClicked,
                           keyCode = pygame.K_1)

# button 2 demonstrates more advanced features
button2 = pygamepal.Button(input = input,
                           position = (100, 300),
                           label = 'Button 2',
                           updateMethod = button2Update,
                           drawMethod = button2Draw,
                           onSelected = buttonClicked,
                           keyCode = pygame.K_2)

# additional properties for button 2
button2.counter = 0
button2.arrow = pygame.image.load(os.path.join('images','arrow.png'))

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

    input.update()
    button1.update()
    button2.update()

    #
    # draw
    #
  
    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
  
    # draw buttons
    button1.draw(screen)
    button2.draw(screen)

    # draw instructions
    pygamepal.drawText(screen, 'Click or press [1]', (100, 60))
    pygamepal.drawText(screen, 'Click or press [2]', (100, 260))

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()