#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#
# Instructions
#  -- arrow keys to move player
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygamepal
import os

#
# load spritesheet and split into separate images
#

# load a texture
texture = pygame.image.load(os.path.join('images','character_spritesheet.png'))
# double the texture size
texture = pygame.transform.scale(texture, (texture.get_width()*2,texture.get_height() * 2))
# split texture into a 2D list of sub-textures
splitTextures = pygamepal.splitTexture(texture, 96, 96)

#
# chest (just an image)
#

chestImage = pygame.image.load(os.path.join('images', 'chest.png'))
chestPosition = (200, 200)

#
# create a new game
#

class MyGame(pygamepal.Game):

    def init(self):

        # set window properties
        self.size = (800, 500)
        self.caption = 'Full game example'
        
        # create an input object
        self.input = pygamepal.Input()

        #
        # create a player sprite
        #

        self.player = pygame.sprite.Sprite()
        
        # add a spriteImage to the player sprite, including 5 different states
        self.player.spriteImage = pygamepal.SpriteImage()
        self.player.spriteImage.addTextures(splitTextures[0][0], splitTextures[0][1], state='idle', offset=(17 * 2, 16 * 2))
        self.player.spriteImage.addTextures(splitTextures[0][1], splitTextures[0][2], splitTextures[0][1], splitTextures[0][3], state='walk_down', offset=(17 * 2, 16 * 2))
        self.player.spriteImage.addTextures(splitTextures[1][1], splitTextures[1][2], splitTextures[1][1], splitTextures[1][3], state='walk_up', offset=(17 * 2, 16 * 2))
        self.player.spriteImage.addTextures(splitTextures[2][1], splitTextures[2][2], splitTextures[2][1], splitTextures[2][3], state='walk_left', offset=(17 * 2, 16 * 2))
        self.player.spriteImage.addTextures(splitTextures[3][1], splitTextures[3][2], splitTextures[3][1], splitTextures[3][3], state='walk_right', offset=(17 * 2, 16 * 2))
        
        # set player position and size
        self.player.rect = pygame.Rect(160, 160, 28, 32)

        #
        # create a camera object
        #

        self.camera = pygamepal.Camera(position = (50, 50),
                                       size = (700, 400),
                                       # center the camera on the player
                                       target = (self.player.rect.x + self.player.rect.w / 2, 
                                                 self.player.rect.y + self.player.rect.h / 2),
                                       zoom = 3,
                                       backgroundColour = 'darkgreen',
                                       # clamp the camera to the world
                                       clamp = True,
                                       clampRect = (0, 0, 500, 500),
                                       followDelay = 0.9)
        
        # create a separate surface for drawing the world
        # this surface will be used by the camera
        self.worldSurface = pygame.surface.Surface((500, 500), pygame.SRCALPHA, 32)
        

    def update(self, deltaTime):

        # fill the screen
        self.screen.fill('cornflowerblue')

        # update the input
        self.input.update()

        # calculate distance
        dist = 60 * deltaTime

        # arrow keys to:
        # - change state of player sprite
        # - change player sprite position (clamped to world)
        if self.input.isKeyDown(pygame.K_UP):
            self.player.spriteImage.setState('walk_up')
            self.player.rect.y = max(0, self.player.rect.y - dist)
        elif self.input.isKeyDown(pygame.K_DOWN):
            self.player.spriteImage.setState('walk_down')
            self.player.rect.y = min (500 - self.player.rect.h, self.player.rect.y + dist)
        elif self.input.isKeyDown(pygame.K_LEFT):
            self.player.spriteImage.setState('walk_left')
            self.player.rect.x = max(0, self.player.rect.x - dist)
        elif self.input.isKeyDown(pygame.K_RIGHT):
            self.player.spriteImage.setState('walk_right')
            self.player.rect.x = min(500 - self.player.rect.w, self.player.rect.x + dist)
        # idle state is the default
        else:
            self.player.spriteImage.setState('idle')

        # update the sprite image
        self.player.spriteImage.update()
        
        # update the camera
        self.camera.update()
        
        # track the player with the camera
        self.camera.target = (self.player.rect.x + self.player.rect.w / 2,
        self.player.rect.y + self.player.rect.h / 2)
        
    def draw(self):

        # clear the world surface
        self.worldSurface.fill((0, 0, 0, 0))
        # draw the player sprite image to the world surface
        self.player.spriteImage.draw(self.worldSurface, self.player.rect.x, self.player.rect.y)
        # draw the chest to the world surface
        self.worldSurface.blit(chestImage, chestPosition)
        # use the camera to draw the world surface to the screen
        self.camera.draw(self.worldSurface, self.screen)

#
# create a new game instance
#

myGame = MyGame()
myGame.run()