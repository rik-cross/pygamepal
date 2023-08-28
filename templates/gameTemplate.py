#
# pygame_utils -- Game Template
# part of the pygame_utils library
#  -- github.com/rik-cross/pygame_utils
#

import pygame
import pygame_utils

#
# create a new game
#

class MyGame(pygame_utils.Game):

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