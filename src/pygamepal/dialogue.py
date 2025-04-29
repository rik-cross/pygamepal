#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from .drawText import drawText, splitText, sysFont
from .dialoguePage import DialoguePage

class Dialogue:

    '''
    Displays one or more pages of dialogue.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/dialogueExample.gif?raw=true

    `Example Dialogue code`_.

    .. _Example Dialogue code: https://github.com/rik-cross/pygamepal/blob/main/examples/dialogueExample.py

    :param (int, int) position: The (x, y) top-left position of the box (default = (0, 0)).
    :param (int, int) size: The (width, height) size of the box (default = (50, 50)).
    :param pygame.Font font: The text font (default = None, which uses pygamepal.sysFont).
    :param pygame.Color backgroundColor: Dialogue box background color (default = None).
    :param pygame.Color textColor: Text color (default = 'black').
    :param pygame.Color borderColor: Box and texture border color (default = 'black').
    :param int borderWidth: The width of the border, in pixels (default = 0).
    :param int paddingWidth: The space in pixels between elements (default = 10).
    :param str textEffect: Either 'none' or 'tick' (default = 'none').
    :param int tickSpeed: The delay between showing each character (if textEffect == 'tick' only, default = 4).
    :param str advanceTextSymbol: The string to show at the end of pages 0 to n-1 of dialogue (default = '>').
    :param pygame.Sound tickSound: Sound to play when advancing the text (if textEffect == 'tick' only, default = None).
    :param int borderRadius: Bevel on the edges of the borders (default = 0).
    :param bool visible: Vibisility of the dialogue box (default = True).
    :param function customDrawMethod: Provide an alternative draw() method (default = None).
    '''

    def __init__(self,
        position = (0, 0),
        size = (200, 100),
        font = None,
        backgroundColor = None,
        textColor = 'black',
        borderColor = 'black',
        borderWidth = 0,
        padding = 10,
        textEffect = 'none',
        tickSpeed = 4,
        advanceTextSymbol = '>',
        tickSound = None,
        borderRadius = 0,
        visible = True,
        custonDrawMethod = None
    ):

        self.position = position
        self.size = size
        
        if font is None:
            self.font = sysFont
        else:
            self.font = font

        if backgroundColor is None:
            self.backgroundColor = (255, 255, 255, 0)
        else:
            self.backgroundColor = backgroundColor

        self.textColor = textColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.padding = padding        
        self.textEffect = textEffect
        self.tickSpeed = tickSpeed
        self.advanceTextSymbol = advanceTextSymbol
        self._tickSound = tickSound
        self.borderRadius = borderRadius
        self.visible = visible
        self.customDrawMethod = custonDrawMethod

        self.pages = []
        self._pageIndex = 0
        self._characterIndex = 0
        self._tickTimer = 0
        self.complete = False

        # create a main dialogue box surface
        self._surface = pygame.Surface(self.size, pygame.SRCALPHA)

        # calculate the text position
        

    def update(self, deltaTime = 1):

        '''
        Updates the dialogue box, once per frame.

        :param float deltaTime: the game time elapsed since the last frame (default = 1).
        '''

        # only update if:
        # - there is at least one dialogue page
        # - the dialogue is not yet complete
        # - the text has a 'tick' effect 
        # - there are characters of text left to tick

        if not self.pages:
            return

        self._currentPage = self.pages[self._pageIndex]
        self._textPosition = self._currentPage.textOffset 

        if self.complete is False and self.textEffect == 'tick' and self._characterIndex < len(self.pages[self._pageIndex].text):
            self._tickTimer += deltaTime
            # advance the tick effect
            if self._tickTimer >= self.tickSpeed:
                self._tickTimer = 0
                self._characterIndex += 1
                # play a sound if one has been specified
                if self._tickSound is not None:
                    pygame.mixer.Sound.play(self._tickSound)

    def draw(self, surface):

        '''
        Draws the dialogue box, along with the current page of text.

        :param float deltaTime: the game time elapsed since the last frame (default = 1).
        '''

        # only draw if visible
        if self.visible is False:
            return
    
        # only draw if pages exist
        if not self.pages:
            return
        
        # use custom draw method instead, if one if specified
        if self.customDrawMethod is not None:
            self.customDrawMethod(surface)
            return

        # clear the main surface
        self._surface.fill((0, 0, 0, 0), (0, 0, *self.size))

        # draw background
        pygame.draw.rect(
            self._surface,
            self.backgroundColor,
            (0, 0, *self.size),
            border_radius=self.borderRadius
        )
        
        # draw border
        if self.borderWidth > 0 and self.borderColor is not None:
            pygame.draw.rect(
                self._surface,
                self.borderColor,
                (0, 0, *self.size),
                width = self.borderWidth,
                border_radius=self.borderRadius
            )   

        #
        # draw texture and border, etc.
        #

        # if a texture exists for the current dialogue page
        if self._currentPage.texture is not None:

            # draw a background for the texture if one is specified
            if self._currentPage.textureBackgroundColor is not None:

                # draw texture background
                pygame.draw.rect(self._surface, self._currentPage.textureBackgroundColor,
                                 (*self._currentPage.texturePosition,
                                  self.size[1] - 2 * self.borderWidth - 2 * self.padding,
                                  self.size[1] - 2 * self.borderWidth - 2 * self.padding),
                                  border_radius=self.borderRadius
                )

                # draw texture
                self._surface.blit(
                    pygame.transform.scale(self._currentPage.texture, self._currentPage.textureSize),
                    (self._currentPage.texturePosition[0] + self.borderWidth + self.padding + self._currentPage.texturePadding[0],
                     2 * self.borderWidth + 2 * self.padding + self._currentPage.texturePadding[1])
                )

                # draw texture border
                if self.borderWidth > 0 and self.borderColor is not None:
                    pygame.draw.rect(self._surface, self.borderColor,
                                    (*self._currentPage.texturePosition,
                                    self.size[1] - 2 * self.borderWidth - 2 * self.padding,
                                    self.size[1] - 2 * self.borderWidth - 2 * self.padding),
                                    width = self.borderWidth,
                                    border_radius=self.borderRadius
                    )

        #
        # draw each split line of text
        #

        if self.textEffect == 'none':

            heightOffset = 0
            for line in self._currentPage.splitText:

                drawText(
                    self._surface,
                    line,
                    (self._textPosition[0], self._textPosition[1] + heightOffset),
                    self.font,
                    color = self.textColor
                )

                heightOffset += self.font.get_height() + self.padding // 2
        
        # if 'tick', only draw currently visible characters
        if self.textEffect == 'tick':

            charsLeft = self._characterIndex

            heightOffset = 0
            for line in self._currentPage.splitText:

                if charsLeft > 0:

                    drawText(
                        self._surface,
                        line[0:charsLeft],
                        (self._textPosition[0], self._textPosition[1] + heightOffset),
                        self.font,
                        color = self.textColor
                    )

                    charsLeft -= len(line)

                heightOffset += self.font.get_height() + self.padding // 2 

        # draw the dialogue surface to the surface passed
        surface.blit(self._surface, (self.position[0], self.position[1]))     
    
    def addPage(
        self,
        text,
        texture = None,
        textureAlignment = 'left',
        textureBackgroundColor = None
    ):

        '''
        Adds a page of dialogue to the dialogue box.

        :param str text: The text to display.
        :param pygame.texture texture: The texture to display with the text (default = None).
        :param str textureAlignment: Position of the texture ('left' or 'right', default = 'left').
        :param pygame.Color textureBackgroundColor: The texture background color (default = None).
        '''

        # create and add a new DialoguePage, setting this object as the 'parent'
        self.pages.append(
            DialoguePage(
                self,
                text,
                texture,
                textureAlignment,
                textureBackgroundColor
            )
        )

        # add the text advance symbol to all but the last pages,
        # and remove from the final page
        if self.advanceTextSymbol is not None:

            # add the symbol to all but the last page, if it hasn't been added already
            for i in range(0, len(self.pages) - 1):
                if self.pages[i].text[-len(self.advanceTextSymbol):] != self.advanceTextSymbol:
                    self.pages[i].text = self.pages[i].text + ' ' + self.advanceTextSymbol

            # remove the symbol from the final page, but only if it needs adding
            if self.pages[-1].text[-len(self.advanceTextSymbol):] == self.advanceTextSymbol:
                self.pages[-1].text = self.pages[-1].text[:-len(self.advanceTextSymbol)-1]
        
    def advance(self):
    
        '''
        Advances the dialogue. This means firstly showing all text for the current page, and then
        moving to the next page of dialogue.
        '''

        if not self.pages:
            return

        self._tickTimer = 0

        # if there is still more text to display on the current page
        # then advance to the end of that page's text
        if self.textEffect == 'tick' and self._characterIndex < len(self._currentPage.text):
            self._characterIndex = len(self._currentPage.text)
        # otherwise, move to the next page of text and move to the first character
        else:
            self._pageIndex += 1
            self._characterIndex = 0
            
            # if at the last page then hide the box and mark as completed
            if self._pageIndex > len(self.pages) - 1:
                self._pageIndex = len(self.pages) - 1
                self.visible = False
                self.complete = True

    def getText(self, split = True):

        '''
        Get the current page of text. If the text has a 'tick' effect,
        only the currently visible text is returned.

        :param bool split: Returns a list of text, split according to the available
        text width (default = True).
        '''

        if split == True:

            if self.textEffect == 'tick':

                charsLeft = self._characterIndex
                textLines = []

                for line in self._currentPage.splitText:
                    if charsLeft > 0:
                        textLines.append(line[0:charsLeft])
                        charsLeft -= len(line)
                
                return textLines

            else:
                return self._currentPage.splitText

        else:

            if self.textEffect == 'tick':
                return self._currentPage.text[:self._characterIndex]
            else:
                return self._currentPage.text            

