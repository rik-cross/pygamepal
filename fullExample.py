#
# pygame_utils -- Full Game Example
# part of the pygame_utils library
#  -- github.com/rik-cross/pygame_utils
#
# Instructions
#  -- arrow keys to move player
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

import pygame
import pygame_utils
import os

#
# load spritesheet and split into separate images
#

# load a texture
texture = pygame.image.load(os.path.join('images','character_spritesheet.png'))
# double the texture size
texture = pygame.transform.scale(texture, (texture.get_width()*2,texture.get_height()*2))
# split texture into a 2D list of sub-textures
splitTextures = pygame_utils.splitTexture(texture, 96, 96)

#
# chest
#

chestImage = pygame.image.load(os.path.join('images', 'chest.png'))
chestPosition = (250, 250)

#
# create a new game
#

class MyGame(pygame_utils.Game):

    def init(self):

        # set window properties
        self.size = (800, 500)
        self.caption = 'Full game example'
        
        # create an input object
        self.input = pygame_utils.Input()

        #
        # create a player sprite
        #

        self.player = pygame.sprite.Sprite()
        
        # add a spriteImage to the player sprite, including 5 different states
        self.player.spriteImage = pygame_utils.SpriteImage()
        self.player.spriteImage.addTextures(splitTextures[0][0], splitTextures[0][1], state='idle')
        self.player.spriteImage.addTextures(splitTextures[0][1], splitTextures[0][2], splitTextures[0][1], splitTextures[0][3], state='walk_down')
        self.player.spriteImage.addTextures(splitTextures[1][1], splitTextures[1][2], splitTextures[1][1], splitTextures[1][3], state='walk_up')
        self.player.spriteImage.addTextures(splitTextures[2][1], splitTextures[2][2], splitTextures[2][1], splitTextures[2][3], state='walk_left')
        self.player.spriteImage.addTextures(splitTextures[3][1], splitTextures[3][2], splitTextures[3][1], splitTextures[3][3], state='walk_right')
        
        # set player position
        self.player.position = [160, 160]

        #
        # create a camera object
        #

        self.camera = pygame_utils.Camera(position=(50, 50),
                                          size=(700, 400),
                                          # center the camera on the player
                                          target=(self.player.position[0] + self.player.spriteImage.getCenter()[0], 
                                                  self.player.position[1] + self.player.spriteImage.getCenter()[1]),
                                          zoom=3,
                                          backgroundColour='darkgreen',
                                          # clamp the camera to the world
                                          clamp=True,
                                          clampRect=(0, 0, 500, 500),
                                          followDelay=0.9)
        
        # create a separate surface for drawing the world
        # this surface will be used by the camera
        self.worldSurface = pygame.surface.Surface((500, 500), pygame.SRCALPHA, 32)
        

    def update(self):

        # fill the screen
        self.screen.fill('cornflowerblue')

        # update the input
        self.input.update()

        # arrow keys to:
        # - change state of player sprite
        # - change player sprite position (clamped to world)
        if self.input.isKeyDown(pygame.K_UP):
            self.player.spriteImage.setState('walk_up')
            self.player.position[1] = max(0-16*2, self.player.position[1] - 1)
        elif self.input.isKeyDown(pygame.K_DOWN):
            self.player.spriteImage.setState('walk_down')
            self.player.position[1] = min (500-96+16*2, self.player.position[1] + 1)
        elif self.input.isKeyDown(pygame.K_LEFT):
            self.player.spriteImage.setState('walk_left')
            self.player.position[0] = max(0-18*2, self.player.position[0] - 1)
        elif self.input.isKeyDown(pygame.K_RIGHT):
            self.player.spriteImage.setState('walk_right')
            self.player.position[0] = min(500-96+18*2, self.player.position[0] + 1)
        # idle state is the default
        else:
            self.player.spriteImage.setState('idle')

        # update the sprite image
        self.player.spriteImage.update()
        
        # update the camera
        self.camera.update()
        
        # track the player with the camera
        self.camera.target = (self.player.position[0] + self.player.spriteImage.getCenter()[0], 
                              self.player.position[1] + self.player.spriteImage.getCenter()[1])
        
        

    def draw(self):
        self.worldSurface.fill((0, 0, 0, 0))
        self.player.spriteImage.draw(self.worldSurface, self.player.position[0], self.player.position[1])
        self.worldSurface.blit(chestImage, chestPosition)
        self.camera.draw(self.worldSurface, self.screen)

#
# create a new game instance
#

myGame = MyGame()
myGame.run()