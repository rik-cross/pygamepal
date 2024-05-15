#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions
#  -- WASD to move
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygamepal
import os

#
# Create a player sprite subclass
#

class Player(pygamepal.Sprite):

    def update(self):
        # WASD to move
        if myGame.input.isKeyDown(pygame.K_w):
            self.y -= 1
        if myGame.input.isKeyDown(pygame.K_s):
            self.y += 1
        if myGame.input.isKeyDown(pygame.K_a):
            self.x -= 1
        if myGame.input.isKeyDown(pygame.K_d):
            self.x += 1

#
# Create game scene subclass
#

class GameScene(pygamepal.Scene):

    def init(self):
        self.backgroundColor = 'black'
        # change some camera parameters
        self.camera.backgroundColor = 'black'
        self.camera.zoom = 4
        self.camera.target = player.getCenter()
        self.camera.clamp = True
        self.camera.clampRect = (0, 0, 256, 256)
        # add the player to the scene
        self.addSprite(self.player)
        # add the trees to the scene
        for t in trees:
            self.addSprite(t)
        # sort sprites by their bottoms
        self.sortKey = self.sortByBottom

        
    def update(self):
        # camera centers on the middle of the player
        self.camera.target = player.getCenter()
    
    def draw(self):
        # draw a map to the scene surface
        self.sceneSurface.blit(pygame.image.load(os.path.join('images', 'map.png')), (0, 0))
        # draw some instructions on the overlay surface
        pygamepal.drawText(self.overlaySurface, 'WASD to move player', (20, 20), backgroundColor='black')

#
# Create a game
#

class MyGame(pygamepal.Game):
    def init(self):
        # create a new scene and set as the current scene
        self.currentScene = GameScene(self)

#
# create sprites
#

player = Player(imageName = os.path.join('images', 'character.png'), position = pygame.math.Vector2(140, 128), collider = pygamepal.Collider(offset = (0, 10), size = (12, 6)))

# create some tree sprites
trees = []
for x in range(10, 250, 50):
    for y in range(10, 250, 50):
        trees.append(pygamepal.Sprite(imageName = os.path.join('images', 'tree.png'), position = (x, y), collider = pygamepal.Collider(offset = (6, 25), size = (12, 5))))

# uncomment the line below to see sprite sizes and colliders
#pygamepal.DEBUG = True
myGame = MyGame(caption = 'Sprite example')
myGame.run()