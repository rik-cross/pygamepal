#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Trigger:

    '''
    A trigger defines an area that executes callback functions when colliding with other triggers.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/triggerExample.gif?raw=true
    
    `Example Trigger code`_.

    .. _Example Trigger code: https://github.com/rik-cross/pygamepal/blob/main/examples/triggerExample.py

    :param (int, int) position: The (x, y) top-left position of the trigger (default = (0, 0)).
    :param (int, int) size: The (w, h) size of the trigger, in pixels (default = (10, 10)).
    :param (int, int) offset: The (x, y) offset from the parent pygamepal.Sprite position (default = (0, 0)).
    :param func onEnter: A function called once when two triggers first collide (default = None).
    :param func onCollide: A function called on every frame that two triggers collide (default = None).
    :param func onExit: A function called once when two triggers no longer collide (default = None).
    :param pygame.Color drawColor: The color to draw the trigger (default = 'yellow').
    '''
    
    # a static list of all triggers created, to facilitate
    # collision detection for all triggers including those
    # that don't belong to a scene or sprite
    _allTriggers = []

    def __init__(
        self,
        position = (0, 0),
        size = (10, 10),
        offset = (0, 0),
        onEnter = None,
        onCollide = None,
        onExit = None,
        drawColor = 'yellow'):
        
        # add the trigger to the static list
        Trigger._allTriggers.append(self)

        # stores other triggers currently colliding with this one
        self._collidedTriggers = []
        
        # parent scene and sprite
        self._scene = None
        self._sprite = None
        
        # the trigger size and position are stored as a pygame.Rect
        self.offset = offset
        # position is adjusted and offset from the parent sprite if appropriate
        self._rect = pygame.rect.Rect(position[0], position[1], size[0], size[1])
        
        # set trigger collision callbacks
        self.onCollide = onCollide
        self.onEnter = onEnter
        self.onExit = onExit
        
        self.drawColor = drawColor
        # the color changes if a trigger is activated
        self._currentColor = drawColor

    def update(self, deltaTime = 1):

        '''
        Update must be called once per frame if used independently.
        (Note: does not need to be called if used as part of a pygamepal.Game or pygamepal.Scene)

        :param float deltaTime: Time elapsed since last game tick (default = 1).
        '''

        #
        # update trigger position if attached to a parent sprite
        #

        if self._sprite is not None and self._sprite.position is not None:
            self.x = self._sprite.x + self.offset[0]
            self.y = self._sprite.y + self.offset[1]

        #
        # process this trigger with respect to all other triggers
        #

        # check against every created trigger
        for t in Trigger._allTriggers:
            # don't collide trigger with itself
            if t is not self:
                # only collide triggers in the same scene
                if self._scene == t._scene:
                    # if triggers collide
                    if self._rect.colliderect(t._rect):

                        if t not in self._collidedTriggers:
                            # onEnter
                            if self.onEnter is not None:
                                self.onEnter(self, t)
                            self._collidedTriggers.append(t)
                        # onCollide
                        if self.onCollide is not None:
                            self.onCollide(self, t)
                            
                    # if no trigger collision
                    else:
                        if t in self._collidedTriggers:
                            # onExit
                            if self.onExit is not None:
                                self.onExit(self, t)
                            self._collidedTriggers.remove(t)
        
        # change the trigger color if it has been activated
        if len(self._collidedTriggers) > 0:
            self._currentColor = 'green'
        else:
            self._currentColor = self.drawColor
                
    def draw(self, surface):

        '''
        Draw can be called to draw a trigger when used independently.
        (Note: this method is called automatically when pygamepal.DEBUG is True,
        when used as part of a pygamepal.Game or pygamepal.Scene)

        :param pygame.Surface surface: The surface to draw to.
        '''

        from pygamepal import drawText, smallFont
        
        # draw trigger bouding box
        pygame.draw.rect(surface, self._currentColor, self._rect, 1)
        # draw size and position info
        drawText(
            surface,
            '[' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.w) + ', ' + str(self.h)  + ']',
            (self.x, self.y - 12),
            font = smallFont,
            color = self._currentColor)
        
    #
    # properties
    #

    @property
    def x(self):
        '''
        Get / set the trigger x position.
        '''
        return self._rect.x
    
    @x.setter
    def x(self, value):
        self._rect.x = value

    @property
    def y(self):
        '''
        Get / set the trigger y position.
        '''
        return self._rect.y
    
    @y.setter
    def y(self, value):
        self._rect.y = value

    @property
    def w(self):
        '''
        Get / set the trigger width.
        '''
        return self._rect.w
    
    @w.setter
    def w(self, value):
        self._rect.w = value

    @property
    def h(self):
        '''
        Get / set the trigger height.
        '''
        return self._rect.h
    
    @h.setter
    def h(self, value):
        self._rect.h = value