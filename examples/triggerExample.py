#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- arrow keys to move trigger 1
#

import pygame
import pygamepal

import pygamepal

#
# collision functions
#

def trigger2OnEnter(thisTrigger, otherTrigger):
    print("Trigger 2 collision enter")

def trigger2OnExit(thisTrigger, otherTrigger):
    print("Trigger 2 collision exit")

#
# game code
#

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Triggers Example')
clock = pygame.time.Clock() 

# create 2 triggers
trigger1 = pygamepal.Trigger(100, 100, 50, 50)
trigger2 = pygamepal.Trigger(200, 200, 100, 100,
                             onEnter = trigger2OnEnter,
                             onCollide = None,
                             onExit = trigger2OnExit)

# add input, to allow camera control
input = pygamepal.Input()

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
        trigger1.x -= 1
    if input.isKeyDown(pygame.K_RIGHT):
        trigger1.x += 1
    if input.isKeyDown(pygame.K_UP):
        trigger1.y -= 1
    if input.isKeyDown(pygame.K_DOWN):
        trigger1.y += 1

    #
    # update
    #

    input.update()
    trigger1.update()
    trigger2.update()

    #
    # draw
    #
  
    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
  
    trigger1.draw(screen)
    trigger2.draw(screen)

    pygamepal.drawText(screen, "Arrow keys to move trigger 1", 10, 10)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()