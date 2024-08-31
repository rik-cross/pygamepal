#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import pygamepal

class Game:

    '''
    Create a game without setup or boilerplate code.
    A Game allows you to add scenes, triggers, colliders, buttons and sprites.

    `Example Game code`_.

    .. _Example Game code: https://github.com/rik-cross/pygamepal/blob/main/examples/gameExample.py

    :param (int, int) size: The size of the game window (default = (640, 480)).
    :param str caption: The game window caption (default = '').
    :param int fps: The frames-per-second of the game (default = 60).
    :param bool fullscreen: Fullscreen flag.
    '''

    def __init__(self, size = (640, 480), caption = '', fps = 60, fullscreen = False):
       
        pygame.init()

        self.size = size
        self.caption = caption
        self.fps = fps
        self.fullscreen = fullscreen

        self.input = pygamepal.Input()
        self.currentScene = None
        self.previousScene = None
        
        self.currentScene = pygamepal.Scene(self)

        # start window in windowed or fullscreen mode
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock() 

        # total elapsed game time
        self.startTime = pygame.time.get_ticks()
        self.gameTime = self.startTime
        self._running = False
        
        # store events so that they aren't 'consumed' by the class
        self.events = []

        self.init()

    #
    # core methods
    #

    def _update(self):

        '''
        The root update method called automatically once per frame.
        This handles all scenes, etc. and doesn't need to be called by the user.
        '''

        self.previousScene = self.currentScene

        # update clock and calculate delta time
        deltaTime = self.clock.tick(self.fps) / 1000
        # calculate total elapsed time
        self.gameTime = pygame.time.get_ticks() - self.startTime

        # reset events
        self.events = []
        # respond to quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            else:
                self.events.append(event)

        # call user-defined update method
        self.update() 

        # update input
        if self.input is not None:
            self.input.update()

        # update the current scene
        if self.currentScene is not None:
            self.currentScene._update()
        
        # call user-defined active methods
        if self.currentScene is not self.previousScene:
            self.previousScene.onInactive()
            self.currentScene.onActive()

    def _draw(self):

        '''
        The root draw method.
        Does not need to be called by the user.
        '''

        if self.currentScene is not None:
            self.currentScene._draw()
        # call user-defined draw() method
        self.draw()
        pygame.display.flip()

    def run(self):

        '''
        Call to start the game.
        '''

        self._running = True
        while self._running:
            self._update()
            self._draw()
        pygame.quit()

    # call quit() to end the game
    def quit(self):

        '''
        Call to end the game.
        '''

        self._running = False

    #
    # user-defined methods
    #

    def init(self):
        
        '''
        Optional, user-defined method.
        Init() is called once when a game is created.
        '''
        
        pass

    def update(self, deltaTime=1):

        '''
        Optional, user-defined method.
        Called once per frame of the game.

        :param float deltaTime: Time elapsed since last update call.
        '''
        
        pass

    def draw(self):

        '''
        Optional, user-defined method.
        Called once per frame of the game, after update() is called.
        '''

        pass

    #
    # alternative methods to add / remove
    # sprites, triggers, colliders and buttons
    # from the current scene, via the game
    #

    # sprite

    def addSprite(self, sprite):

        '''
        Adds a pygamepal.Sprite to the game.

        :param pygamepal.Sprite sprite: The sprite to add to the game.
        '''
        
        if self.currentScene is not None:
            self.currentScene.addSprite(sprite)
    
    def removeSprite(self, sprite):

        '''
        Removes a pygamepal.Sprite from the game.

        :param pygamepal.Sprite sprite: The sprite to remove from the game.
        '''

        if self.currentScene is not None:
            self.currentScene.removeSprite(sprite)
    
    # trigger

    def addTrigger(self, trigger):

        '''
        Adds a pygamepal.Trigger to the game.

        param pygamepal.Trigger trigger: The trigger to remove from the game.
        '''

        if self.currentScene is not None:
            self.currentScene.addTrigger(trigger)
    
    def removeTrigger(self, trigger):

        '''
        Removes a pygamepal.Trigger from the game.

        :param pygamepal.Trigger trigger: The trigger to remove from the game.
        '''

        if self.currentScene is not None:
            self.currentScene.removeTrigger(trigger)

    # collider

    def addCollider(self, collider):

        '''
        Add a pygamepal.Collider to the game.

        :param pygamepal.Collider collider: The collider to add to the game.
        '''

        if self.currentScene is not None:
            self.currentScene.addCollider(collider)
    
    def removeCollider(self, collider):
        
        '''
        Removes a pygamepal.Collider from the game.

        :param pygamepal.Collider collider: The collider to remove from the game.
        '''
        
        if self.currentScene is not None:
            self.currentScene.removeCollider(collider)
    
    # button

    def addButton(self, button):
        
        '''
        Adds a pygamepal.Button to the game.

        :param pygamepal.Button button: The button to add to the game.
        '''
        
        if self.currentScene is not None:
            self.currentScene.addButton(button)
    
    def removeButton(self, button):
        
        '''
        Removes a pygamepal.Button from the game.

        :param pygamepal.Button button: The button to remove from the game.
        '''
        
        if self.currentScene is not None:
            self.currentScene.removeButton(button)

    #
    # properties
    #

    @property
    def icon(self):
        '''
        Get / set the game icon.
        '''
        return self._icon
    
    @icon.setter
    def icon(self, value):
        self._icon = value
        pygame.display.set_icon(self._icon)
