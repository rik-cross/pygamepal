import pygame

class Trigger:

    _allTriggers = []

    def __init__(self, position = (0, 0), size = (10, 10), sprite = None, spriteOffset = (0, 0), onEnter = None, onCollide = None, onExit = None):
        Trigger._allTriggers.append(self)
        self._triggers = []
        # associated sprite
        self.sprite = sprite
        self.spriteOffset = spriteOffset
        if self.sprite is not None and hasattr(self.sprite, 'position') is True and self.sprite.position is not None:
            self._rect = pygame.rect.Rect(self.sprite.x + self.spriteOffset[0], self.sprite.y + self.spriteOffset[1], size[0], size[1])
        else:
            self._rect = pygame.rect.Rect(position[0], position[1], size[0], size[1])
        # onCollide is called every frame that another
        # trigger collides with this one
        self.onCollide = onCollide
        # onEnter is called once when another
        # trigger collider with this one
        self.onEnter = onEnter
        # onExit is called once when another
        # trigger stops colliding with this one
        self.onExit = onExit
        self._drawColor = 'gray80'
        # stores other triggers currently colliding
        # with this one
        self._collidedTriggers = []

    def update(self, deltaTime = 1):
        # update position if attached to a sprite
        if self.sprite is not None and self.sprite.position is not None:
            self.x = self.sprite.x + self.spriteOffset[0]
            self.y = self.sprite.y + self.spriteOffset[1]
        # for other triggers
        for t in Trigger._allTriggers:
            if t is not self:
                # if triggers collide
                if self._rect.colliderect(t._rect):
                    # there is a collision
                    if t not in self._collidedTriggers:
                        # onEnter
                        if self.onEnter is not None:
                            self.onEnter(self, t)
                        self._collidedTriggers.append(t)
                    # onCollide
                    if self.onCollide is not None:
                        self.onCollide(self, t)
                    self._drawColor = 'white'
                # no collision
                else:
                    if t in self._collidedTriggers:
                        # onExit
                        if self.onExit is not None:
                            self.onExit(self, t)
                        self._collidedTriggers.remove(t)
                    self._drawColor = 'gray80'
                
    def draw(self, surface):
        pygame.draw.rect(surface, self._drawColor, self._rect, 2)
    
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