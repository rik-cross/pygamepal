import pygame

class Scene:

    #
    # static sprite ordering methods
    #

    @staticmethod
    def sortByZ(s):
        return s.z

    @staticmethod
    def sortByTop(s):
        if s.position is None:
            return 1
        return s.position[1]

    @staticmethod
    def sortByBottom(s):
        if s.position is None or s.size is None:
            return 1
        return s.position[1] + s.size[1]
    
    @staticmethod
    def sortByLeft(s):
        if s.position is None:
            return 1
        return s.position[0]
    
    @staticmethod
    def sortByRight(s):
        if s.position is None or s.size is None:
            return 1
        return s.position[0] + s.size[0]

    #
    # main scene methods
    #

    def __init__(self, game):

        from pygamepal import Camera

        # a reference to the main game object
        self.game = game
        self.backgroundColor = 'cornflowerblue'
        # frame value is incremented each game tick
        self.frame = 0
        # scene and overlay (UI) surfaces
        self.sceneSurface = pygame.Surface(game.size, pygame.SRCALPHA, 32)
        self.overlaySurface = pygame.Surface(game.size, pygame.SRCALPHA, 32)
        # default camera takes up the whole scene, target is the middle of the scene
        self.camera = Camera(position=(0, 0), size=game.size, target=(self.game.size[0] / 2, self.game.size[1] / 2))
        # sort sprites by their z (depth) value
        self.sortKey = Scene.sortByZ
        # a list of the sprites added to the scene
        self.sprites = []
        # run the user-defined sprite init() method
        self.init()
        # update the camera in case its state has changed
        if self.camera is not None:
            self.camera.update()
    
    def _update(self):
        # update the frame counter
        self.frame += 1
        # update the scene camera
        if self.camera is not None:
            self.camera.update()
        # sort the sprites
        self.sprites.sort(key=self.sortKey)
        # update each sprite in the scene
        for s in self.sprites:
            s._update()
        # call the user-defined update() method
        self.update()

    def _draw(self):
        # clear the surfaces
        self.sceneSurface.fill(self.backgroundColor)
        self.overlaySurface.fill((0, 0, 0, 0))
        # call the user-defined draw() method
        self.draw()
        # draw each scene sprite
        for s in self.sprites:
            s._draw(self.sceneSurface)
        if self.camera is not None:
            self.camera.draw(self.sceneSurface, self.game.screen)
        self.game.screen.blit(self.overlaySurface, (0, 0))
    
    #
    # user-defined methods
    #

    def init(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass
    
    # this method is called when the scene
    # becomes the current scene
    def onActive(self):
        pass
    
    # this method is called when the scene is
    # no longer the current scene
    def onInactive(self):
        pass
    
    #
    # scene helped methods
    #

    # add a sprite to the scene
    def addSprite(self, sprite):
        # remove from previous scene
        self.removeSprite(sprite)
        # add to new scene
        if sprite not in self.sprites:
            self.sprites.append(sprite)
            sprite.currentScene = self
            sprite.onAddedToScene()
    
    # remove a sprite from the scene
    def removeSprite(self, sprite):
        if self.game.currentScene is not None and sprite.currentScene is not None and sprite in self.currentScene.sprites:
            sprite.onRemovedFromScene()
            sprite.currentScene.sprites.remove(sprite)