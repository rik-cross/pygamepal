#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Trigger:

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

                        # calculate distance between trigger centers
                        

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
        return self._rect.x
    
    @x.setter
    def x(self, value):
        self._rect.x = value

    @property
    def y(self):
        return self._rect.y
    
    @y.setter
    def y(self, value):
        self._rect.y = value

    @property
    def w(self):
        return self._rect.w
    
    @w.setter
    def w(self, value):
        self._rect.w = value

    @property
    def h(self):
        return self._rect.h
    
    @h.setter
    def h(self, value):
        self._rect.h = value