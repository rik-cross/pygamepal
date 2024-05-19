#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Sprite(pygame.sprite.Sprite):

    # add trigger to constructor
    def __init__(self,
                 imageName = None, texture = None,
                 position = (0, 0), size = (0, 0), z = 0,
                 scaleImage = False,
                 collider = None,
                 trigger = None,
                 drawColor = 'white'):

        # importing here to avoid a circular dependency
        from pygamepal import SpriteImage

        self.position = position

        self.collider = collider
        self.trigger = trigger
        
        self.spriteImage = None
        

        # use image name to create a texture if defined
        if imageName is not None:
            texture = pygame.image.load(imageName)
            texture = texture.convert_alpha()
        
        # create a spriteImage if a texture is specified
        if texture is not None:
            texture = texture.convert_alpha()
            # set the texture size to the sprite size if specified
            if scaleImage == True and size is not None:
                texture = pygame.transform.scale(texture, size)
            # create the spriteImage
            self.spriteImage = SpriteImage(texture)

        # use the texture size if no size is specified
        if size == (0, 0):
            if texture is not None:
                self.size = texture.get_size()
        else:
            self.size = size
        
        self.z = z

        self.currentScene = None

        self.drawColor = drawColor

        # call the user-defined init() method
        self.init()
        
    def _update(self):

        from pygamepal import Trigger, Collider

        # 
        # update the sprite of colliders
        #

        if self.collider is not None:
            self.collider._sprite = self
            self.collider.update()

        # 
        # update the sprite of triggers
        #

        if self.trigger is not None:
            self.trigger._sprite = self
            self.trigger.update()

        if self.spriteImage is not None:
            self.spriteImage.update()
       
        self.update()
    
    def _draw(self, surface):

        from pygamepal import Game, drawText, smallFont, DEBUG

        if self.spriteImage is not None:
            self.spriteImage.draw(surface, self.position[0], self.position[1])

        if DEBUG is True:
            
            # draw sprite size box
            if hasattr(self, 'position') is True and self.position is not None and hasattr(self, 'size') is True and self.size is not None:
                # draw bounding box
                pygame.draw.rect(surface, 'white', (self.position[0], self.position[1], self.size[0], self.size[1]), 1)
                # draw position and size info
                drawText(
                    surface,
                    '[' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.size[0]) + ', ' + str(self.size[1])  + ']',
                    (self.x + self.size[0] + 2, self.y + self.size[1] / 2 - 5),
                    font = smallFont,
                    color = self.drawColor)
            
            # draw sprite collider
            if self.collider is not None:
                self.collider.draw(surface)

            # draw sprite trigger
            if self.trigger is not None:
                self.trigger.draw(surface)
    
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
    # properties
    #

    # position, x and y

    @property
    def position(self):
        return self._position
    
    # setting the position checks colliders
    @position.setter
    def position(self, value):

        from pygamepal import Collider
    
        if hasattr(self, 'collider') is False or self.collider is None:
            # convert the new position to a Vector2
            self._position = pygame.math.Vector2(value[0], value[1])
        
        else:
        
            #
            # check x
            #

            # calculate the travel distance to get the direction
            direction = [value[0] - self._position[0], 0]
            # only check the x movement
            newXPos = [value[0], self.position[1]]
            # get a list of colliding sprites
            collisionList = self.collider._getCollisions(newXPos)
            # find the closes collided sprite
            closestX = None
            for c in collisionList:
                d = c._rect.x - self.collider._rect.x
                if closestX is None or d < closestX:
                    closestX = d
            # move towards the closest collider if one exists
            if closestX is not None:
                if direction[0] > 0:
                    self._position[0] = self._position[0] + closestX - self.collider.size[0]
                elif direction[0] < 0:
                    self._position[0] = self._position[0] + closestX + c._rect[2]
            else:
                self._position[0] = value[0]
            
            #
            # check y
            #
            
            # calculate the travel distance to get the direction
            direction = [0, value[1] - self._position[1]]
            # only check the x movement
            newYPos = [self.position[0], value[1]]
            # get a list of colliding sprites
            collisionList = self.collider._getCollisions(newYPos)
            # find the closes collided sprite
            closestY = None
            for c in collisionList:
                d = c._rect.y - self.collider._rect.y
                if closestY is None or d < closestY:
                    closestY = d
            # move towards the closest collider if one exists
            if closestY is not None:
                if direction[1] > 0:
                    self._position[1] = self._position[1] + closestY - self.collider.size[1]
                elif direction[1] < 0:
                    self._position[1] = self._position[1] + closestY + c._rect[3]
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