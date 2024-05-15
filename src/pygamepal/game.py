#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import pygamepal

class Game:

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

        self.init()

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

    #
    # core methods
    #

    def _update(self):

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
        if self.currentScene is not None:
            self.currentScene._draw()
        # call user-defined draw() method
        self.draw()
        pygame.display.flip()

    # call run() to start the game
    def run(self):
        self._running = True
        while self._running:
            self._update()
            self._draw()
        pygame.quit()

    # call quit() to end the game
    def quit(self):
        self._running = False

    #
    # user-defined methods
    #

    def init(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    #
    # alternative methods to add / remove
    # sprites, triggers, colliders and buttons
    # from the current scene, via the game
    #

    # sprite

    def addSprite(self, sprite):
        if self.currentScene is not None:
            self.currentScene.addSprite(sprite)
    
    def removeSprite(self, sprite):
        if self.currentScene is not None:
            self.currentScene.removeSprite(sprite)
    
    # trigger

    def addTrigger(self, trigger):
        if self.currentScene is not None:
            self.currentScene.addTrigger(trigger)
    
    def removeTrigger(self, trigger):
        if self.currentScene is not None:
            self.currentScene.removeTrigger(trigger)

    # collider

    def addCollider(self, collider):
        if self.currentScene is not None:
            self.currentScene.addCollider(collider)
    
    def removeCollider(self, collider):
        if self.currentScene is not None:
            self.currentScene.removeCollider(collider)
    
    # button

    def addButton(self, button):
        if self.currentScene is not None:
            self.currentScene.addButton(button)
    
    def removeButton(self, button):
        if self.currentScene is not None:
            self.currentScene.removeButton(button)

    #
    # properties
    #

    @property
    def icon(self):
        return self._icon
    
    @icon.setter
    def icon(self, value):
        self._icon = value
        pygame.display.set_icon(self._icon)
