#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from .drawText import drawText

class Button:

    def __init__(self,
                 # input is not optional
                 input,
                 position = (0, 0), size = (100, 50),
                 label = None,
                 fgColor = 'white', bgColor = 'black',
                 borderWidth = 1,
                 borderColor = 'white',
                 image = None,
                 # this method called when highlighted
                 onHighlighted = None,
                 # this method is called when selected
                 onSelected = None,
                 # updateMethod and drawMethod give the ability
                 # to override default button befaviour
                 updateMethod = None,
                 drawMethod = None,
                 # a keycode can also be associated with a button
                 # (only works if pygamepal.input is specified)
                 keyCode = None
                 ):
        
        self._scene = None

        self.input = input
        self.position = position
        self.size = size
        self.label = label
        if image is not None:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image
        self.fgColor = fgColor
        self.bgColor = bgColor
        self.borderWidth = borderWidth
        self.borderColor = borderColor
        self.onHighlighted = onHighlighted
        self.onSelected = onSelected
        self.updateMethod = updateMethod
        self.drawMethod = drawMethod
        self.keyCode = keyCode

        self._isHighlighted = False
        self._isSelected = False
    
    def update(self):

        if self.input is None:
            return

        if self.updateMethod is not None:
            self.updateMethod(self)
            return

        self.setHighlighted()
        self.setSelected()

    def draw(self, surface):

        if self.drawMethod is not None:
            self.drawMethod(self, surface)
            return

        self.drawBackground(surface)
        self.drawImage(surface)
        self.drawText(surface)
        self.drawBorder(surface)

    #
    # draw helper methods
    # (useful for when providing a draw callback)
    #

    def setHighlighted(self):
        # button is highlighted if mouse is within button bounds
        self._isHighlighted = False
        cursor = self.input.getMouseCursorPosition()
        if self._isWithinBounds(cursor, (self.position[0], self.position[1], self.size[0], self.size[1])):
            self._isHighlighted = True
            if self.onHighlighted is not None:
                self.onHighlighted(self)

    def setSelected(self):
        # button is selected if either
        # -- key is pressed, or
        # -- mouse button is pressed and within bounds
        self._isSelected = False
        cursor = self.input.getMouseCursorPosition()
        if (self.keyCode is not None and self.input.isKeyPressed(self.keyCode)) or \
            (self._isWithinBounds(cursor, (self.position[0], self.position[1], self.size[0], self.size[1])) and \
            self.input.isMouseButtonPressed(0)):
            self._isSelected = True
            if self.onSelected is not None:
                self.onSelected(self)

    def _isWithinBounds(self, position, rect):
        # returns True if 'position' is inside 'rect'
        return position[0] >= rect[0] and position[0] <= rect[0] + rect[2] and \
            position[1] >= rect[1] and position[1] <= rect[1] + rect[3]
    
    def drawBackground(self, screen):
        # draw background
        pygame.draw.rect(screen,
                         self.bgColor,
                         (self.position[0], self.position[1], self.size[0], self.size[1]))
    
    def drawImage(self, screen):
        # draw image
        if self.image is not None:
            screen.blit(self.image, self.position)

    def drawText(self, screen):
        # draw text
        drawText(screen, text = self.label,
                 position = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2),
                 color = self.fgColor, centerX = True, centerY = True)

    def drawBorder(self, screen):
        # draw border
        if self.borderWidth > 0:
            pygame.draw.rect(screen,
                             self.fgColor,
                             (self.position[0], self.position[1], self.size[0], self.size[1]),
                             width = 1)
    
    #
    # properties
    #

    # True when the button is hoghlighted
    @property
    def isHighlighted(self):
        return self._isHighlighted
    
    # True when the button is selected
    @property
    def isSelected(self):
        return self._isSelected   
