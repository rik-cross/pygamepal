#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import pygamepal
import os

#
# create a new game
#

class MyGame(pygamepal.Game):

    def init(self):
        # this code is optional and can be removed or replaced
        self.size = (640, 480)
        self.caption = 'Example Game'
        self.icon = pygame.image.load(os.path.join('images', 'character.png'))
        self.blue = 0
        
    def update(self, deltaTime):
        # this code is optional and can be removed or replaced
        # cycle a value between 0 and 255
        self.blue = (self.blue + 1) % 255

    def draw(self):
        # this code is optional and can be removed or replaced
        self.screen.fill('cornflowerblue')
        pygamepal.drawText(self.screen, 'PygamePal example game!', (25, 25), color = (0, 0, self.blue))
        pygamepal.drawText(self.screen, 'Add code to init(), update() and draw() methods.', (25, 50))
        pygamepal.drawText(self.screen, str(round(self.gameTime / 1000, 2)), (25, 75))

#
# create a new game instance
#

myGame = MyGame()
myGame.run()
