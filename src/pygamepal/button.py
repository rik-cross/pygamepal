#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from .drawText import drawText

class Button:

    '''
    Used to provide input, and can be controlled by mouse and/or keypress.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/buttonExample.gif?raw=true

    `Example Button code`_.

    .. _Example Button code: https://github.com/rik-cross/pygamepal/blob/main/examples/buttonExample.py

    :param pygamepal.Input input: The input object used to control the button.
    :param (int, int) position: The (x, y) position of the button on the drawn surface (default = (0, 0)).
    :param str text: Text to display on the button (default = None).
    :param pygame.Color foregroundColor: Foreground color, used to draw the button text and border (default = 'white).
    :param pygame.Color backgroundColor: Background color, used to draw the button background (default = 'black).
    :param int borderWidth: Width of the button border (default = 1).
    :param pygame.Color borderColor: Color of the button border (default = 'white').
    :param pygame.Texture image: Button background image (default = None).
    :param function(pygamepal.Button) onHighlighted: A function called when the mouse position intersects with the button position (default = None).
    :param function(pygamepal.Button) onSelected: A function called when the button is clicked, or the relevant button pressed (default = None).
    :param function(pygamepal.Button) updateMethod: Used to override the default update method of a button (default = None).
    :param function(pygamepal.Button, pygame.Surface) drawMethod: Used to override the default draw method of a button (default = None).
    :param pygame.Key keyCode: The keypress associated with selecting the button (default = None).
    '''

    def __init__(self,
        # input is not optional
        input,
        position = (0, 0), size = (100, 50),
        text = None,
        foregroundColor = 'white', backgroundColor = 'black',
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
        self.text = text
        
        if image is not None:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image

        self.foregroundColor = foregroundColor
        self.backgroundColor = backgroundColor
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

        '''
        Must be called once per frame if the button is not used as part of a pygamepal.Scene.
        '''

        if self.input is None:
            return

        if self.updateMethod is not None:
            self.updateMethod(self)
            return

        self.setHighlighted()
        self.setSelected()

    def draw(self, surface):

        '''
        Must be called once per frame if the button is not being used as part of a pygamepal.Scene.

        :param pygame.Surface surface: The surface to draw to.
        '''

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

        '''
        Should be called within a custom button.updateMethod in order to update the button 'highlighted' status.
        A button is highlighted if the mouse is within the button bounds.
        '''
        
        self._isHighlighted = False
        cursor = self.input.getMouseCursorPosition()
        if self._isWithinBounds(cursor, (self.position[0], self.position[1], self.size[0], self.size[1])):
            self._isHighlighted = True
            if self.onHighlighted is not None:
                self.onHighlighted(self)

    def setSelected(self):

        '''
        Should be called within a custom button.updateMethod in order to update the button 'selected' status.
        A button is selected if either the keyCode is pressed, or if the mouse button is pressed within the button bounds.
        '''

        self._isSelected = False
        cursor = self.input.getMouseCursorPosition()
        if (self.keyCode is not None and self.input.isKeyPressed(self.keyCode)) or \
            (self._isWithinBounds(cursor, (self.position[0], self.position[1], self.size[0], self.size[1])) and \
            self.input.isMouseButtonPressed(0)):
            self._isSelected = True
            if self.onSelected is not None:
                self.onSelected(self)

    def _isWithinBounds(self, position, rect):
        
        '''
        returns True if an (x, y) 'position' (usually the mouse position) is inside the (x, y, w, h) 'rect' (usually the button).
        
        :param (int, int) position: The (x, y) position to test.
        :param (int, int, int, int): The (x, y, w, h) rectangle to test against the position.
        '''
        
        return position[0] >= rect[0] and position[0] <= rect[0] + rect[2] and \
            position[1] >= rect[1] and position[1] <= rect[1] + rect[3]
    
    def drawBackground(self, surface):

        '''
        Draws the button background. Can be called from a custom button.drawMethod function.

        :param pygame.Surface surface: The surface to draw to.
        '''
        
        pygame.draw.rect(surface,
                         self.backgroundColor,
                         (self.position[0], self.position[1], self.size[0], self.size[1]))
    
    def drawImage(self, surface):

        '''
        Draws the button image. Can be called from a custom button.drawMethod function.

        :param pygame.Surface surface: The surface to draw to.
        '''
        
        if self.image is not None:
            surface.blit(self.image, self.position)

    def drawText(self, surface):
        

        '''
        Draws the button text. Can be called from a custom button.drawMethod function.

        :param pygame.Surface surface: The surface to draw to.
        '''

        drawText(surface, text = self.text,
                 position = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2),
                 color = self.foregroundColor, centerX = True, centerY = True)

    def drawBorder(self, surface):

        '''
        Draws the button border. Can be called from a custom button.drawMethod function.

        :param pygame.Surface surface: The surface to draw to.
        '''
        
        if self.borderWidth > 0:
            pygame.draw.rect(surface,
                             self.foregroundColor,
                             (self.position[0], self.position[1], self.size[0], self.size[1]),
                             width = 1)
    
    #
    # properties
    #

    # True when the button is hoghlighted
    @property
    def isHighlighted(self):
        '''
        Returns True is the mouse position intersents with the button.
        '''
        return self._isHighlighted
    
    # True when the button is selected
    @property
    def isSelected(self):
        '''
        Returns True is the button keyCode is pressed, or if the button is clicked.
        '''
        return self._isSelected   
