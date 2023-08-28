#
# pygamewrapper, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamewrapper
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamewrapper' to use
#

import pygame
import pygamewrapper

#
# create a new game
#

class MyGame(pygamewrapper.Game):

    def init(self):
        # replace 'pass' below with your code
        pass

    def update(self):
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