#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions:
#  -- up / down arrow to change transition
#  -- left / right arrow to change duration
#  -- w / s to change easing function
#  -- space key to start / pause
#  -- click and drag mouse to progress transition
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygamepal
import os

def resetTransitions():
    # use global data
    global transitionList
    global surface1
    global surface2
    global duration
    global currentEasingFunction
    # reset each transition
    for t in transitionList:
        # set easing function
        t.easingFunction = currentEasingFunction
        # set duration
        t.duration = duration
        t.reset()
    # reset surface alpha
    surface1.set_alpha(255)
    surface2.set_alpha(255)

# initialise Pygame
pygame.init()

# setup screen to required size
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Transition Showcase')
clock = pygame.time.Clock() 

# load a texture
texture = pygame.image.load(os.path.join('images','character_spritesheet.png'))

surface1 = pygame.Surface((680, 460))
surface1.fill('mediumpurple')
surface1.blit(texture, (400, 100))

surface2 = pygame.Surface((680, 460))
surface2.fill('goldenrod')
surface2.blit(texture, (100, 100))

transitionList = [
    pygamepal.TransitionFade(surface1, surface2),
    pygamepal.TransitionFadeToBlack(surface1, surface2),
    pygamepal.TransitionWipeLeft(surface1, surface2),
    pygamepal.TransitionWipeRight(surface1, surface2),
    pygamepal.TransitionWipeUp(surface1, surface2),
    pygamepal.TransitionWipeDown(surface1, surface2),
    pygamepal.TransitionMoveLeft(surface1, surface2),
    pygamepal.TransitionMoveRight(surface1, surface2),
    pygamepal.TransitionMoveUp(surface1, surface2),
    pygamepal.TransitionMoveDown(surface1, surface2)
]
transitionIndex = 0
currentTransition = transitionList[transitionIndex]

easingList = [
    pygamepal.linear,
    pygamepal.bounceEaseOut
]
easingIndex = 0
currentEasingFunction = easingList[easingIndex]

duration = 100

play = False
circlePos = (100, 410)
mouseDown = False

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

    # check mouseDown to control scrubber
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouseDown = True
    if event.type == pygame.MOUSEBUTTONUP:
        mouseDown = False

    # space to play / pause
    if input.isKeyPressed(pygame.K_SPACE):
        play = not play

    # up / down arrow to change transition
    if input.isKeyPressed(pygame.K_UP):
        transitionIndex = max(0, min(len(transitionList) - 1, transitionIndex - 1))
        currentTransition = transitionList[transitionIndex]
        resetTransitions()
    if input.isKeyPressed(pygame.K_DOWN):
        transitionIndex = max(0, min(len(transitionList) - 1, transitionIndex + 1))
        currentTransition = transitionList[transitionIndex]
        resetTransitions()

    # left / right arrow to change duration
    if input.isKeyDown(pygame.K_LEFT):
        duration = max(10, min(1000 - 1, duration - 1))
        resetTransitions()
    if input.isKeyDown(pygame.K_RIGHT):
        duration = max(10, min(1000 - 1, duration + 1))
        resetTransitions()

    # w / s to change easing function
    if input.isKeyPressed(pygame.K_w):
        easingIndex = max(0, min(len(easingList) - 1, easingIndex - 1))
        currentEasingFunction = easingList[easingIndex]
        resetTransitions()
    if input.isKeyPressed(pygame.K_s):
        easingIndex = max(0, min(len(easingList) - 1, easingIndex + 1))
        currentEasingFunction = easingList[easingIndex]
        resetTransitions()

    input.update()

    currentTransition = transitionList[transitionIndex]

    # scrubber should reflect the current transition percentage
    if not mouseDown:
        if play:
            currentTransition.update()
            xPos = 100 + (480 / 100 * currentTransition.currentPercentage)
            circlePos = (xPos, 410)
    # scrubber is controlled by mouse position
    else:
        xPos = max(100, min(580, pygame.mouse.get_pos()[0]))
        circlePos = (xPos, 410)
        calculatedPercentage = (xPos - 100) / (480) * 100
        transitionList[transitionIndex].currentPercentage = calculatedPercentage

    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')
    
    currentTransition.draw(screen)
    
    pygamepal.drawText(screen, str(currentTransition), (20, 20))
    pygamepal.drawText(screen, 'Duration: ' + str(currentTransition.duration), (20, 40))
    pygamepal.drawText(screen, 'Easing function: ' + str(currentTransition.easingFunction), (20, 60))
    pygamepal.drawText(screen, '% complete: ' + str(round(currentTransition.currentPercentage, 2)), (20, 80))
    pygamepal.drawText(screen, 'Playing: ' + str(play), (20, 100))

    # draw scrubber
    pygame.draw.line(screen, 'white', (100, 410), (580, 410), width=4)
    pygame.draw.circle(screen, 'white', circlePos, 10)

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
