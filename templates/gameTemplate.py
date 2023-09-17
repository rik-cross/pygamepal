#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import pygamepal

#
# create a new game
#

class MyGame(pygamepal.Game):

    def init(self):
        # replace 'pass' below with your code
        pass

    def update(self, deltaTime):
        # replace 'pass' below with your code
        pass

    def draw(self):
        # replace the code below with your code
        self.screen.fill('cornflowerblue')

#
# create a new game instance
#

myGame = MyGame()
myGame.run()