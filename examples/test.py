import pygame
import pygamepal
import os

#
# create sprite subclasses
#

class Player(pygamepal.Sprite):

    def init(self):
        
        #
        # player textures from spritesheet
        #

        # load a texture
        playerSpritesheet = pygame.image.load(os.path.join('images','character_spritesheet.png'))
        # split texture into a 2D list of 48x48 sub-textures
        splitTextures = pygamepal.splitTexture(playerSpritesheet, 48, 48)
        
        #
        # create a player
        #

        self.size = (14, 16)
        self.position = (119, 120)
        self.collider = pygamepal.Collider(offset = (2, 12), size = (10, 4))

        self.spriteImage = pygamepal.SpriteImage()
        # states and images
        self.spriteImage.addTextures(
            splitTextures[0][0], splitTextures[0][1],
            state = 'idle',
            offset = (17, 16)
        )
        self.spriteImage.addTextures(
            splitTextures[1][1], splitTextures[1][2], splitTextures[1][1], splitTextures[1][3],
            state = 'up',
            animationDelay = 4,
            offset = (17, 16)
        )
        self.spriteImage.addTextures(
            splitTextures[0][1], splitTextures[0][2], splitTextures[0][1], splitTextures[0][3],
            state = 'down',
            animationDelay = 4,
            offset = (17, 16)
        )
        self.spriteImage.addTextures(
            splitTextures[2][1], splitTextures[2][2], splitTextures[2][1], splitTextures[2][3],
            state = 'left',
            animationDelay = 4,
            offset =(17, 16)
        )
        self.spriteImage.addTextures(
            splitTextures[3][1], splitTextures[3][2], splitTextures[3][1], splitTextures[3][3],
            state = 'right',
            animationDelay = 4,
            offset = (17, 16)
        )
        self.trigger = pygamepal.Trigger(size = (24, 26), offset = (-5, -5))
    
    def update(self):

        # WASD to move and change state
        if gameExample.input.isKeyDown(pygame.K_w):
            self.y -= 1
            self.spriteImage.state = 'up'
        elif gameExample.input.isKeyDown(pygame.K_a):
            self.x -= 1
            self.spriteImage.state = 'left'
        elif gameExample.input.isKeyDown(pygame.K_s):
            self.y += 1
            self.spriteImage.state = 'down'
        elif gameExample.input.isKeyDown(pygame.K_d):
            self.x += 1
            self.spriteImage.state = 'right'
        else:
            self.spriteImage.state = 'idle'

#
# create scene subclasses
#

class GameScene(pygamepal.Scene):
    
    def zoomCamera(self, this, other, zoom):
        self.camera.zoom = zoom
    
    def setChestState(self, this, other, state):
        self.chest.spriteImage.pause = False
        self.chest.spriteImage.state = state

    def init(self):
        
        #
        # add textures
        #

        self.map = pygame.image.load(os.path.join('images', 'map.png'))

        #
        # add sprites
        #

        # player

        self.player = Player()
        self.addSprite(self.player)

        # trees

        self.addSprite(
            pygamepal.Sprite(
                imageName = os.path.join('images', 'tree.png'),
                position = (40, 50),
                collider = pygamepal.Collider(offset = (6, 25), size = (12, 5))
            )
        )
        self.addSprite(
            pygamepal.Sprite(
                imageName = os.path.join('images', 'tree.png'),
                position = (70, 40),
                collider = pygamepal.Collider(offset = (6, 25), size = (12, 5))
            )
        )
        self.addSprite(
            pygamepal.Sprite(
                imageName = os.path.join('images', 'tree.png'),
                position = (20, 10),
                collider = pygamepal.Collider(offset = (6, 25), size = (12, 5))
            )
        )

        # chest

        # load a texture
        chestSpritesheet = pygame.image.load(os.path.join('images','chest_spritesheet.png'))
        # split texture into a 2D list of sub-textures
        splitTextures = pygamepal.splitTexture(chestSpritesheet, 48, 48)
        
        self.chest = pygamepal.Sprite(position = (175, 175), size = (16, 14))
        self.chest.collider = pygamepal.Collider(offset = (0, 8), size = (16, 6))
        self.chest.spriteImage = pygamepal.SpriteImage()
        self.chest.spriteImage.addTextures(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2], splitTextures[0][3], offset = (16, 18), state = 'open', animationDelay = 4, loop = False)
        self.chest.spriteImage.addTextures(splitTextures[0][3], splitTextures[0][2], splitTextures[0][1], splitTextures[0][0], offset = (16, 18), state = 'close', animationDelay = 4, loop = False)
        self.chest.spriteImage.pause = True
        self.chest.trigger = pygamepal.Trigger(size = (26, 24), offset = (-5, -5),
            onEnter = lambda this, other, state = 'open': self.setChestState(this, other, state),
            onExit = lambda this, other, state = 'close': self.setChestState(this, other, state))
        self.addSprite(self.chest)

        #
        # customise the scene
        #

        self.backgroundColor = 'black'
        self.sortKey = self.sortByBottom

        #
        # customise the scene camera
        #
        
        self.camera.backgroundColor = 'black'
        #self.camera.target = self.player.getCenter()
        self.camera.setTarget(self.player.getCenter(), instant = True)
        self.camera.lazyFollow = 0
        self.camera.setZoom(4, instant = True)
        self.camera.lazyZoom = 0
        self.camera.clamp = True
        self.camera.clampRect = (0, 0, 256, 256)
        
        #
        # add triggers for the camera
        #

        self.forestTrigger = pygamepal.Trigger(position = (10, 20), size = (100, 70),
            onEnter = lambda this, other, zoom = 6 : self.zoomCamera(this, other, zoom),
            onExit = lambda this, other, zoom = 4 : self.zoomCamera(this, other, zoom))
        self.addTrigger(self.forestTrigger)

        #
        # add map bounds colliders
        #

        # top
        self.addCollider(pygamepal.Collider((0, 0), (256, 2)))
        # bottom
        self.addCollider(pygamepal.Collider((0, 254), (256, 2)))
        # left
        self.addCollider(pygamepal.Collider((0, 0), (2, 256)))
        # right
        self.addCollider(pygamepal.Collider((254, 0), (2, 256)))

    def update(self):

        # [ESC] to return to menu scene
        if self.game.input.isKeyPressed(pygame.K_ESCAPE):
            self.game.currentScene = menuScene
        
        # camera tracks the player
        self.camera.target = self.player.getCenter()

    def draw(self):

        self.sceneSurface.blit(self.map, (0, 0))

#
# create game subclass
#

class GameExample(pygamepal.Game):

    def update(self):

        # press [q] qt any time to quit
        if self.input.isKeyPressed(pygame.K_q):
            self.quit()
        
        # press 'z' to toggle debug mode
        if self.input.isKeyPressed(pygame.K_z):
            pygamepal.DEBUG = not pygamepal.DEBUG

#
# create game and scenes
#

gameExample = GameExample(size=(800, 600), caption = 'Full game example', fps = 1)
gameScene = GameScene(gameExample)

#
# set up game and run
#

gameExample.currentScene = gameScene
gameExample.run()
