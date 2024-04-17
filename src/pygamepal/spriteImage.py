import pygame
from .textureList import *

class SpriteImage():

    def __init__(self):
        self._reset()

    # set object to initial values
    def _reset(self):
        # maps a state to a list of textures
        self._textureLists = {}
        self._currentState = None
        # keeps track of current animation frame and progress
        self._animationIndex = 0
        self._animationTimer = 0
        self.pause = False

    # add one or more textures, with an associated state
    def addTextures(self, firstTexture, *moreTextures, state = None, animationDelay = 8, loop = True, hFlip = False, vFlip = False, offset = (0, 0)):
        # allow textures with no attached state (for single-state images/animations)
        if state is None:
            state = 'default'
        # get existing textureList or create a new one
        if state not in self._textureLists:
            textureList = TextureList()
        else:
            textureList = self._sprites[state]
        # add textures to list
        textureList._textures.append(firstTexture)
        for texture in moreTextures:
            textureList._textures.append(texture)
        # add attributes for the current state
        textureList._animationDelay = animationDelay
        textureList._loop = loop
        textureList._hFlip = hFlip
        textureList._vFlip = vFlip
        textureList._offset = offset
        self._textureLists[state] = textureList
        if len(self._textureLists) == 1:
            self._currentState = state

    def getCenter(self):
        if self._currentState is None or self.pause:
            return (0, 0)
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        return (currentTexture.get_width() / 2, currentTexture.get_height() / 2)

    # must be called once per frame to update sprite
    def update(self):
        # only animate if there's at least one image and it's not paused
        if self._currentState is None or self.pause:
            return
        # increment timer
        self._animationTimer += 1
        # advance animation if timer reaches delay value
        if self._animationTimer >= self._textureLists[self._currentState]._animationDelay:
            self._animationTimer = 0
            self._animationIndex += 1
            if self._animationIndex > len(self._textureLists[self._currentState]._textures) - 1:
                if self._textureLists[self._currentState]._loop:
                    self._animationIndex = 0
                else:
                    self._animationIndex = len(
                        self._textureLists[self._currentState]._textures) - 1

    def setState(self, state):
        # only change state if the new state is different
        if self._currentState == state:
            return
        # set the new state
        self._currentState = state
        # reset index and timer for the new state
        self.resetState()

    def draw(self, screen, x, y):
        # don't draw if there's nothing to draw
        if self._currentState is None or self._textureLists[self._currentState] == None:
            return
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        # draw (optionally flipped) texture
        screen.blit(pygame.transform.flip(currentTexture,
                                          self._textureLists[self._currentState]._hFlip,
                                          self._textureLists[self._currentState]._vFlip),
                    (x - self._textureLists[self._currentState]._offset[0],
                     y - self._textureLists[self._currentState]._offset[1],
                     currentTexture.get_width(),
                     currentTexture.get_height()))
    # puts sprite animation back to start

    def resetState(self):
        self._animationIndex = 0
        self._animationTimer = 0
