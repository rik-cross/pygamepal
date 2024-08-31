#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from pygamepal import Game

class Collider:

    '''
    A collider is an area for which other colliders should not enter.
    A collider can be used independently, or as part of a sprite.

    `Example Collider code`_.

    .. _Example Collider code: https://github.com/rik-cross/pygamepal/blob/main/examples/colliderExample.py

    `Example Sprite Collider code`_.

    .. _Example Sprite Collider code: https://github.com/rik-cross/pygamepal/blob/main/examples/spriteExample.py

    :param:
    '''

    # a static list of all colliders created, to facilitate
    # collision detection for all colliders including those
    # that don't belong to a scene or sprite
    _allColliders = []

    def __init__(self, position = (0, 0),  size = (0, 0), offset = (0, 0), drawColor = 'red'):
        Collider._allColliders.append(self)
        self._scene = None
        self._sprite = None
        self.offset = offset
        self.size = size
        self._rect = pygame.rect.Rect(position[0], position[1], size[0], size[1])
        self.drawColor = drawColor
    
    def update(self):

        '''
        Update method needs to be called for a collider if used independently (i.e. if not as part of a pygamepal.Scene or pygamepal.Sprite).
        '''

        # update position if attached to a sprite
        if self._sprite is not None and self._sprite.position is not None:
            self.x = self._sprite.x + self.offset[0]
            self.y = self._sprite.y + self.offset[1]

    def draw(self, surface):

        '''
        Draw method doesn't need to be called, unless the collider is being used independently and needs to be seen.
        (Note: to see colliders used as part of a pygamepal.Scene or pygamepal.Sprite, set pygamepal.DEGUG = True.)
        '''
        
        from pygamepal import drawText, smallFont
        
        # draw collider bouding box
        pygame.draw.rect(surface, self.drawColor, self._rect, 1)
        # draw size and position info
        drawText(
            surface,
            '[' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.w) + ', ' + str(self.h)  + ']',
            (self.x, self.y + self.h + 2),
            font = smallFont,
            color = self.drawColor)

    def _getCollisions(self, newPosition):

        '''
        Returns a list of all colliders intersecting with newPosition, and using all existing offset and size data.

        :param (int, int) newPosition: The new (x, y) position to check collisions against.
        '''

        # build the list of collisions to return
        collisionList = []

        # return all other colliders...
        for collider in Collider._allColliders:
            if collider is not self:
                # ... in the same scene
                if collider._scene is self._scene:
                    # construct a pygame.Rect object for the new position
                    newPosRect = pygame.Rect(newPosition[0] + self.offset[0], newPosition[1] + self.offset[1], self.size[0], self.size[1])
                    # add collider to list if they would intersect
                    if collider._rect.colliderect(newPosRect):
                        collisionList.append(collider)

        return collisionList

    #
    # properties
    #

    @property
    def x(self):
        '''
        Get / set the x position.
        '''
        return self._rect.x
    
    @x.setter
    def x(self, value):
        # handle collision directly if not part of a scene
        if self._sprite is None:
            newPosition = (value, self.y)
            if len(self._getCollisions(newPosition)) == 0:
                self._rect.x = value
        else:
            self._rect.x = value

    @property
    def y(self):
        '''
        Get / set the y position.
        '''
        return self._rect.y
    
    @y.setter
    def y(self, value):
        # handle collision directly if not part of a scene
        if self._sprite is None:
            newPosition = (self.x, value)
            if len(self._getCollisions(newPosition)) == 0:
                self._rect.y = value
        else:
            self._rect.y = value

    @property
    def w(self):
        '''
        Get / set the width.
        '''
        return self._rect.w
    
    @w.setter
    def w(self, value):
        self._rect.w = value

    @property
    def h(self):
        '''
        Get / set the height.
        '''
        return self._rect.h
    
    @h.setter
    def h(self, value):
        self._rect.h = value