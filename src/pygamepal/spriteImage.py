#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from .spriteTextureList import SpriteTextureList

class SpriteImage():

    '''
    Maps states to a 'SpriteTextureList' object
    containing textures and associated info.
    '''

    def __init__(self,

        #
        # parameters for first SpriteTextureList
        #

        # a list of 0 or more textures
        *textures,
        # state to associate with textures
        state = None,
        # delay between animation frames
        animationDelay = 8,
        # looping animation
        loop = True,
        # horizontal and vertical texture flip
        hFlip = False,
        vFlip = False,
        # offset is used to discount part of the image
        # when specifying a drawing position
        # useful for sprites with whitespace or characters
        # holding tools, etc.
        offset = (0, 0),

        #
        # parameters for all states and image lists
        #

        # spriteImage visibility
        visible = True,
        # spriteImage alpha transparency (between 0 and 255)
        alpha = 255,
        pause = False):

        # reset the object
        self.reset()
        # set overall visibility and alpha
        self.visible = visible
        self.alpha = alpha
        self.pause = pause
        # associate textures with a state, along with other info 
        if len(textures) > 0:
            self.addTextures(*textures, state = state, animationDelay = animationDelay, loop = loop, hFlip = hFlip, vFlip = vFlip, offset = offset)

    def update(self):

        '''
        Updates the current sprite animation.
        Must be called once per frame.
        '''

        # only animate if there's at least one image and it's not paused
        if self._currentState is None or self.pause:
            return
        
        # increment timer
        self._animationTimer += 1

        # advance animation if timer reaches the delay value
        if self._animationTimer >= self._textureLists[self._currentState]._animationDelay:
            self._animationTimer = 0
            self._animationIndex += 1
            # loop back to the first texture if specified
            if self._animationIndex > len(self._textureLists[self._currentState]._textures) - 1:
                if self._textureLists[self._currentState]._loop:
                    self._animationIndex = 0
                else:
                    self._animationIndex = len(self._textureLists[self._currentState]._textures) - 1

    def draw(self, surface, x, y):

        '''
        Draws the current frame of the current state's animation.
        Must be called once per frame.
        '''

        # don't draw if there's nothing to draw
        if self._currentState is None or self._textureLists[self._currentState] is None or self.visible is False:
            return
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        # set the texture alpha
        currentTexture.set_alpha(self.alpha)
        # draw (optionally flipped) texture
        surface.blit(pygame.transform.flip(currentTexture,
                                          self._textureLists[self._currentState]._hFlip,
                                          self._textureLists[self._currentState]._vFlip),
                    (x - self._textureLists[self._currentState]._offset[0],
                     y - self._textureLists[self._currentState]._offset[1],
                     currentTexture.get_width(),
                     currentTexture.get_height()))

    def addTextures(self, *textures, state = None, animationDelay = 8, loop = True, hFlip = False, vFlip = False, offset = (0, 0)):

        '''
        Add one or more textures to a (new or existing) state.
        '''

        # allow textures with no attached state (for single-state images/animations)
        if state is None:
            state = 'default'
        
        # get existing textureList or create a new one
        if state not in self._textureLists:
            textureList = SpriteTextureList()
        else:
            textureList = self._sprites[state] 

        # add textures to list
        for texture in textures:
            texture = texture.convert_alpha()
            textureList._textures.append(texture)
        
        # add attributes for the current state
        textureList._animationDelay = animationDelay
        textureList._loop = loop
        textureList._hFlip = hFlip
        textureList._vFlip = vFlip
        textureList._offset = offset

        # add the texture list to the SpriteImage, stored
        # against the appropriate state
        self._textureLists[state] = textureList

        # set the state if this is the only one
        if len(self._textureLists) == 1:
            self._currentState = state

    def reset(self):

        '''
        Clear object states and textures, and reset
        the object to default values.
        '''

        self.visible = True
        self.alpha = 255
        # maps a state to a list of textures
        self._textureLists = {}
        self._currentState = None
        # keeps track of current animation frame and progress
        self._animationIndex = 0
        self._animationTimer = 0
        self.pause = False

    def _resetState(self):

        '''
        Reset the current sprite animation.
        '''

        self._animationIndex = 0
        self._animationTimer = 0
    
    #
    # properties
    #

    # state

    @property
    def state(self):
        return self._currentState
    
    @state.setter
    def state(self, value):
        # only change state if the new state is different
        if value == self._currentState:
            return
        # set the new state
        self._currentState = value
        # reset index and timer for the new state
        self._resetState()

    # alpha transparency

    @property
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        if value < 0 or value > 255:
            raise ValueError('alpha must be between 0 and 255')
        self._alpha = value
    
    # current texture center

    @property
    def center(self):
        if self._currentState is None:
            return (0, 0)
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        return (currentTexture.get_width() / 2, currentTexture.get_height() / 2)