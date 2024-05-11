import pygame

# each sprite can optionally have a collider
class Collider:
    def __init__(self, offset, size):
        self.offset = offset
        self.size = size

class Sprite(pygame.sprite.Sprite):

    def __init__(self, imageName = None, texture = None, position = (0, 0), size = (0, 0), z = 0, collider = None, scaleImage = False):

        # importing here to avoid a circular dependency
        from pygamepal import SpriteImage

        self.trigger = None

        self.spriteImage = None
        self.position = position

        # use image name to create a texture if defined
        if imageName is not None:
            texture = pygame.image.load(imageName).convert_alpha()
        
        # create a spriteImage if a texture is specified
        if texture is not None:
            # set the texture size to the sprite size if specified
            if scaleImage == True and size is not None:
                texture = pygame.transform.scale(texture, size)
            # create the spriteImage
            self.spriteImage = SpriteImage(firstTexture=texture)

        # use the texture size if no size is specified
        if size == (0, 0):
            if texture is not None:
                self.size = texture.get_size()
        else:
            self.size = size
        
        self.z = z
        self.collider = collider
        self.currentScene = None

        # call the user-defined init() method
        self.init()
        
    def _update(self):
        if self.spriteImage is not None:
            self.spriteImage.update()
        if self.trigger is not None:
            self.trigger.update()
        self.update()
    
    def _draw(self, screen):

        from pygamepal import Game

        if self.spriteImage is not None:
            self.spriteImage.draw(screen, self.position[0], self.position[1])
        if Game.DEBUG is True:
            # DEBUG draw sprite size box
            if hasattr(self, 'position') is True and self.position is not None and hasattr(self, 'size') is True and self.size is not None:
                pygame.draw.rect(screen, 'white', (self.position[0], self.position[1], self.size[0], self.size[1]), 1)
            # DEBUG draw sprite collider box
            if self.collider is not None and self.position is not None:
                pygame.draw.rect(screen, 'red', (self.position[0] + self.collider.offset[0], self.position[1] + self.collider.offset[1], self.collider.size[0], self.collider.size[1]), 1)
            # DEBUG draw trigger
            if self.trigger is not None:
                self.trigger.draw(screen)

    #
    # user-defined methods
    #

    def init(self):
        pass

    def update(self):
        pass

    # method runs once when sprite added to scene
    def onAddedToScene(self):
        pass
    
    # method runs once when sprite removed from scene
    def onRemovedFromScene(self):
        pass

    # returns True if this sprite overlaps another
    # (using the size)
    def touching(self, otherSprite):
        thisRect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        otherRect = pygame.Rect(otherSprite.position[0], otherSprite.position[1], otherSprite.size[0], otherSprite.size[1])
        return thisRect.colliderect(otherRect)
    
    # uses the position and size to return the center
    def getCenter(self):
        return (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
    
    #
    # helper methods
    #

    # returns a list of sprite whose colliders are
    # colliding with this sprite's collider
    # newPosition is used to check sprite before moving
    def getCollidingSprites(self, newPosition):
        # list of colliding sprites
        cs = []
        # don't check if this sprite doesn't have a collider
        if hasattr(self, 'collider') is False or self.collider is None:
            return cs
        # create a collider rect object to test
        thisRect = pygame.Rect(newPosition[0] + self.collider.offset[0], newPosition[1] + self.collider.offset[1], self.collider.size[0], self.collider.size[1])
        # check against all other sprites...
        for sprite in self.currentScene.sprites:
            # ...that aren't this sprite...
            if sprite is not self:
                # ...that have a collider
                if hasattr(sprite, 'collider') is True and sprite.collider is not None:
                    # create a collider rect object to test against
                    otherRect = pygame.Rect(sprite.position[0] + sprite.collider.offset[0], sprite.position[1] + sprite.collider.offset[1], sprite.collider.size[0], sprite.collider.size[1])
                    # add sptite to the list if colliders are colliding
                    if thisRect.colliderect(otherRect):
                        cs.append(sprite)
        # returh the list of colliding sprites
        return cs

    #
    # properties
    #

    # position, x and y

    @property
    def position(self):
        return self._position
    
    # setting the position checks colliders
    @position.setter
    def position(self, value):
        
        # allow movement if there's no collider to check 
        if hasattr(self, 'collider') is False or self.collider is None:
            self._position = pygame.math.Vector2(value[0], value[1])
            return    
        
        #
        # check x
        #

        # calculate the travel distance to get the direction
        direction = [value[0] - self._position[0], 0]
        # only check the x movement
        newXPos = [value[0], self.position[1]]
        # get a list of colliding sprites
        collisionList = self.getCollidingSprites(newXPos)
        # find the closes collided sprite
        closestX = None
        closestS = None
        for c in collisionList:
            d = ((c.position[0] + c.collider.offset[0]) - (self.position[0] + self.collider.offset[0]))
            if closestX is None or d < closestX:
                closestX = d
                closestS = c
        # move towards the closest collider if one exists
        if closestX is not None:
            if direction[0] > 0:
                self._position[0] = self._position[0] + closestX - self.collider.size[0]
            elif direction[0] < 0:
                self._position[0] = self._position[0] + closestX + c.collider.size[0]
        else:
            self._position[0] = value[0]
        
        #
        # check y
        #

        # calculate the travel distance to get the direction
        direction = [0, value[1] - self._position[1]]
        # only check the y movement
        newYPos = [self.position[0], value[1]]
        # get a list of colliding sprites
        collisionList = self.getCollidingSprites(newYPos)
        # find the closes collided sprite
        closestY = None
        closestS = None
        for c in collisionList:
            d = ((c.position[1] + c.collider.offset[1]) - (self.position[1] + self.collider.offset[1]))
            if closestY is None or d < closestY:
                closestY = d
                closestS = c
        # move towards the closest collider if one exists
        if closestY is not None:
            if direction[1] > 0:
                self._position[1] = self._position[1] + closestY - self.collider.size[1]
            elif direction[1] < 0:
                self._position[1] = self._position[1] + closestY + c.collider.size[1]
        else:
            self._position[1] = value[1]
        
        # convert the new position to a Vector2
        self._position = pygame.math.Vector2(self._position[0], self._position[1])

    @property
    def x(self):
        return self._position[0]
    
    @x.setter
    def x(self, value):
        self.position = (value, self._position[1])

    @property
    def y(self):
        return self._position[1]
    
    @y.setter
    def y(self, value):
        self.position = (self._position[0], value)