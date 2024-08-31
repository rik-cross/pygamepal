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
    Maps string states to a pygamepal.SpriteTextureList object containing textures and associated information.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/spriteImageExample.gif?raw=true

    `Example SpriteImage code`_.

    .. _Example SpriteImage code: https://github.com/rik-cross/pygamepal/blob/main/examples/spriteImageExample.py

    Parameters for the first provided state:

    :param pygame.texture textures: 0 or more textures to add to the first SpriteTextureList. Note that if more than 1 texture is added, the spriteImage becomes an animation.
    :param str state: The state name to associate with added textures (default = None).
    :param int animationDelay: The amount of time to display each texture (default = 8).
    :param bool loop: Loop animation (ignored if only one image provided for a state, default = True).
    :param bool hFlip: Horizontally flip images (default = False).
    :param bool vFlip: Vertically flip textures (default = False).
    :param (int, int) offset: Used to ignore part of the image when specifying a drawing position. Useful for sprites with whitespace or characters holding tools, etc. (default = (0, 0)).
    
    Parameters for all states:
    
    :param bool visible: Show image (default = True).
    :param int alpha: The transparency value (between 0 and 255, default = 255).
    :param bool pause: Stops animation (ignored for states with only one image, default = False).
    '''

    def __init__(self,

        *textures,
        state = None,
        animationDelay = 8,
        loop = True,
        hFlip = False,
        vFlip = False,
        offset = (0, 0),

        visible = True,
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

    def update(self, deltaTime = 1):

        '''
        Updates the current sprite animation. Must be called once per frame.

        :param float deltaTime: Time elapsed since last call (default = 1).
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

    def draw(self, surface, position):

        '''
        Draws the current frame of the current state's animation. Must be called once per frame.
        
        :param pygame.surface surface: The surface to draw to.
        :param (int, int) position: The (x, y) position to draw to (default = (0, 0)).
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
                    (position[0] - self._textureLists[self._currentState]._offset[0],
                     position[1] - self._textureLists[self._currentState]._offset[1],
                     currentTexture.get_width(),
                     currentTexture.get_height()))

    def addTextures(self, *textures, state = None, animationDelay = 8, loop = True, hFlip = False, vFlip = False, offset = (0, 0)):

        '''
        Add one or more textures to a (new or existing) state.

        :param pygame.texture textures: 0 or more textures to add to the first SpriteTextureList. Note that if more than 1 texture is added, the spriteImage becomes an animation.
        :param str state: The state name to associate with added textures (default = None).
        :param int animationDelay: The amount of time to display each texture (default = 8).
        :param bool loop: Loop animation (ignored if only one image provided for a state, default = True).
        :param bool hFlip: Horizontally flip images (default = False).
        :param bool vFlip: Vertically flip textures (default = False).
        :param (int, int) offset: Used to ignore part of the image when specifying a drawing position. Useful for sprites with whitespace or characters holding tools, etc. (default = (0, 0)).
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
        Clear object states and textures, and reset the object to default values.
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
        '''
        Get / set the current state.
        '''
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
        '''
        Get / set the current alpha value.
        '''
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        if value < 0 or value > 255:
            raise ValueError('alpha must be between 0 and 255')
        self._alpha = value
    
    # current texture center

    @property
    def center(self):
        '''
        Get the center positon for the current texture.
        '''
        if self._currentState is None:
            return (0, 0)
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        return (currentTexture.get_width() / 2, currentTexture.get_height() / 2)