#
# pygame_utils -- Game Example
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygame_utils

#
# create a new game
#

class MyGame(pygame_utils.Game):

    def init(self):
        # this code is optional and can be removed or replaced
        self.size = (640, 480)
        self.caption = 'Example Game'
        self.icon = pygame.image.load('images\character.png')
        self.blue = 0

    def update(self):
        # this code is optional and can be removed or replaced
        # cycle a value between 0 and 255
        self.blue = (self.blue + 1) % 255

    def draw(self):
        # this code is optional and can be removed or replaced
        self.screen.fill('cornflowerblue')
        pygame_utils.drawText(self.screen, 'pygame_utils example game!', 25, 25, colour=(0, 0, self.blue))
        pygame_utils.drawText(self.screen, 'Add code to init(), update() and draw() methods.', 25, 50)

#
# create a new game instance
#

myGame = MyGame()
myGame.run()