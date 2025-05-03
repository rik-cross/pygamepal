#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Scene:

    '''
    A pygamepal.Game is made up of one or more scenes, which includes a camera, sprites, triggers and colliders.
    Everything added to a scene is handled automatically, with optional init(), update() and draw() methods to define.
    
    `Example Scene code`_.

    .. _Example Scene code: https://github.com/rik-cross/pygamepal/blob/main/examples/sceneExample.py
    
    :param (int, int) surfaceSize: Restricts the size of the scene surface for improved performance (default = the size of the parent pygamepal.Game window).
    '''

    #
    # static sprite ordering methods
    #

    @staticmethod
    def sortByLayer(s):
        
        '''
        Static method to sort sprites by their layer property.
        '''
        
        return s.layer

    @staticmethod
    def sortByTop(s):
        
        '''
        Static method to sort sprites by their top (y-position).
        '''
        
        if s.position is None:
            return 1
        return s.position[1]

    @staticmethod
    def sortByBottom(s):
        
        '''
        Static method to sort sprites by their bottom position (y-position + height).
        '''
        
        if hasattr(s, 'position') is False or s.position is None or hasattr(s, 'size') is False or s.size is None:
            return 1
        return s.position[1] + s.size[1]
    
    @staticmethod
    def sortByLeft(s):
        
        '''
        Static method to sort sprites by their left property (x-position).
        '''
        
        if s.position is None:
            return 1
        return s.position[0]
    
    @staticmethod
    def sortByRight(s):
        
        '''
        Static method to sort sprites by their right position (x-position + width).
        '''

        if s.position is None or s.size is None:
            return 1
        return s.position[0] + s.size[0]

    #
    # main scene methods
    #

    def __init__(self, game, surfaceSize = None):

        from pygamepal import Camera, Lighting

        # a reference to the main game object
        self.game = game

        if surfaceSize is None:
            self.surfaceSize = game.size
        else:
            self.surfaceSize = surfaceSize

        self.backgroundColor = 'cornflowerblue'
        # frame value is incremented each game tick
        self.frame = 0
        # scene and overlay (UI) surfaces
        self.sceneSurface = pygame.Surface(self.surfaceSize, pygame.SRCALPHA, 32)
        self.overlaySurface = pygame.Surface(game.size, pygame.SRCALPHA, 32)
        # default camera takes up the whole scene, target is the middle of the scene
        self.camera = Camera(position=(0, 0), size=game.size, target=(self.game.size[0] / 2, self.game.size[1] / 2))
        # sort sprites by their z (depth) value
        self.sortKey = Scene.sortByLayer
        # a list of the sprites added to the scene
        self.sprites = []

        self._colliders = []
        self._triggers = []
        self._buttons = []
        
        self.lighting = Lighting(self.surfaceSize, lightLevel = 1)

        # run the user-defined sprite init() method
        self.init()

        # update the camera in case its state has changed
        if self.camera is not None:
            self.camera.update()
    
    def addCollider(self, collider):
        '''
        Adds a collider to the scene.

        :param pygamepal.Collider collider: The collider to add.
        '''
        self._colliders.append(collider)
    def removeCollider(self, collider):
        '''
        Removes a collider from the scene.

        :param pygamepal.Collider collider: The collider to remove.
        '''
        self._colliders.remove(collider)
    def addTrigger(self, trigger):
        '''
        Adds a trigger to the scene.

        :param pygamepal.Trigger trigger: The trigger to add.
        '''
        self._triggers.append(trigger)
    def removeTrigger(self, trigger):
        '''
        Removes a trigger from the scene.

        :param pygamepal.Trigger trigger: The trigger to remove.
        '''
        self._triggers.remove(trigger)
    def addButton(self, button):
        '''
        Adds a button to the scene.

        :param pygamepal.Button button: The button to add.
        '''
        self._buttons.append(button)
    def removeButton(self, button):
        '''
        Removes a button from the scene.

        :param pygamepal.Button button: The button to remove.
        '''
        self._buttons.remove(button)

    def _update(self):

        '''
        Internal update method, called automatically once per frame.
        '''

        from pygamepal import Trigger, Collider

        # update the frame counter
        self.frame += 1
        # update the scene camera
        if self.camera is not None:
            self.camera.update()
        # sort the sprites
        self.sprites.sort(key=self.sortKey)

        #
        # set scene for colliders
        #

        # set any colliders in the scene as owned
        # by the scene
        for collider in self._colliders:
            collider._scene = self
            collider.update()

        # set the sprite collider's scene for all sprites
        # in the current scene
        for sprite in self.sprites:
            if hasattr(sprite, 'collider') and sprite.collider is not None:
                sprite.collider._scene = self

        #
        # set scene for triggers
        #

        # set any triggers in the scene as owned
        # by the scene
        for trigger in self._triggers:
            trigger._scene = self
            trigger.update()
        
        # set the sprite trigger's scene for all sprites
        # in the current scene
        for sprite in self.sprites:
            if hasattr(sprite, 'trigger') and sprite.trigger is not None:
                sprite.trigger._scene = self
        
        #
        # set scene for buttons
        #

        # set any triggers in the scene as owned
        # by the scene
        for button in self._buttons:
            button._scene = self
            button.update()

        # update each sprite in the scene
        for s in self.sprites:
            s._update()

        # update the lighting
        self.lighting.update()

        # call the user-defined update() method
        self.update()

    def _draw(self):

        '''
        Internal draw method, called automatically once per frame.
        '''

        from pygamepal import DEBUG

        # clear the surfaces
        self.sceneSurface.fill(self.backgroundColor)
        self.overlaySurface.fill((0, 0, 0, 0))
        # call the user-defined draw() method
        self.draw()

        # draw each scene sprite
        for sprite in self.sprites:
            sprite._draw(self.sceneSurface)

        # draw each button
        for button in self._buttons:
            button.draw(self.overlaySurface)

        if DEBUG is True:

            # draw scene triggers
            for trigger in self._triggers:
                trigger.draw(self.sceneSurface)

            # draw scene colliders
            for collider in self._colliders:
                collider.draw(self.sceneSurface)
        
        # draw the lighting onto the scene screen
        self.lighting.draw(self.sceneSurface)

        # use the camera to draw the scene
        if self.camera is not None:
            self.camera.draw(self.sceneSurface, self.game.screen)
        
        # draw the overlay scene (without the camera)
        self.game.screen.blit(self.overlaySurface, (0, 0))
    
    #
    # user-defined methods, initially empty
    # as they are all optional
    #

    def init(self):

        '''
        Optional scene method called once when created.
        '''
        
        pass

    def update(self):

        '''
        Optional scene method called once per frame.
        '''
        
        pass

    def draw(self):

        '''
        Optional scene method called once per frame.
        '''
        
        pass
    
    def onActive(self):

        '''
        This method is called once when the scene becomes the current scene.
        '''
        
        pass
    
    def onInactive(self):

        '''
        This method is called once when the scene is no longer the current scene.
        '''
        
        pass
    
    #
    # scene helper methods
    #

    def addSprite(self, sprite):

        '''
        Adds a sprite to the scene (and removes from other scenes).

        :param pygamepal.Sprite sprite: The sprite to add.
        '''
        
        # remove from previous scene
        self.removeSprite(sprite)
        # add to new scene
        if sprite not in self.sprites:
            self.sprites.append(sprite)
            sprite.currentScene = self
            sprite.onAddedToScene(self)
    
    # remove a sprite from the scene
    def removeSprite(self, sprite):

        '''
        Removes a sprite from the scene.
        
        :param pygamepal.Sprite sprite: The sprite to remove.
        '''
        
        if self.game.currentScene is not None and sprite.currentScene is not None and sprite in self.currentScene.sprites:
            sprite.onRemovedFromScene(self)
            sprite.currentScene.sprites.remove(sprite)