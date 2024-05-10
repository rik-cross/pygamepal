#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions
#  -- Enter to move to scene 2
#  -- Esc to move to scene 1
#

import pygame
import pygamepal

#
# create 2 scene subclasses
#

class Scene1(pygamepal.Scene):

    def init(self):
        self.backgroundColor = 'blue'

    def update(self):
        # RETURN to move to scene 2
        if self.game.input.isKeyPressed(pygame.K_RETURN):
            self.game.currentScene = scene2

    def draw(self):
        # draw some instructions on the overlay surface
        pygamepal.drawText(self.overlaySurface, 'Enter to move to Scene 2', (20, 20), backgroundColor='black')

class Scene2(pygamepal.Scene):

    def init(self):
        self.backgroundColor = 'red'

    def update(self):
        # ESC to move back to scene 1
        if self.game.input.isKeyPressed(pygame.K_ESCAPE):
            self.game.currentScene = scene1

    def draw(self):
        # draw some instructions on the overlay surface
        pygamepal.drawText(self.overlaySurface, 'Esc to move to Scene 1', (20, 20), backgroundColor='black')

#
# create objects and run game
#

myGame = pygamepal.Game(caption = 'Scene example')
scene1 = Scene1(myGame)
scene2 = Scene2(myGame)
myGame.currentScene = scene1
myGame.run()