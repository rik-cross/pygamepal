#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

from .drawText import splitText

class DialoguePage:

    '''
    Pages for the Dialogue class
    (Users of the PygamePal library should not need to use this class directly. Instead, it is used by pygamepal.Dialogue).

    :param pygamepal.Dialogue parent: The Dialogue object in which the DialoguePage exists.
    :param str text: The page of text.
    :param pygame.Texture texture: The texture to display with the text (default = None).
    :param string alignment: The alignment of the texture (either 'left' or 'right', default = 'left').
    :param pygamepal.Color textureBackgroundColor: The color to disply behind the texture (default = None).
    '''

    def __init__(
        self,
        parent,
        text,
        texture = None,
        textureAlignment = 'left',
        textureBackgroundColor = None
    ):
        
        self.parent = parent
        self.texture = texture
        self.textureAlignment = textureAlignment
        self.textureBackgroundColor = textureBackgroundColor
        self.text = text

        self.calculateTextOffset()
        self.calculateTextureSize()
        self.calculateTexturePosition()
    
    def calculateTextOffset(self):
        self.textOffset = (self.parent.borderWidth + self.parent.padding, self.parent.borderWidth + self.parent.padding)
        if self.texture is not None and self.textureAlignment == 'left':
            self.textOffset = (
                self.textOffset[0] + (self.parent.size[1] - 2*self.parent.borderWidth - self.parent.padding),
                self.textOffset[1])
    
    def calculateTextureSize(self):
        
        '''
        Calculates the (w, h) size of the texture, based on the available space.
        '''
        
        if self.texture is None:
            return
        
        textureSpaceAvailable = self.parent.size[1] - 4 * self.parent.padding - 4 * self.parent.borderWidth
        _, _, w, h = self.texture.get_rect()
        factor = textureSpaceAvailable / max(w, h)
        self.textureSize = (w * factor, h * factor)
        self.texturePadding = (
            (textureSpaceAvailable - self.textureSize[0]) / 2,
            (textureSpaceAvailable - self.textureSize[1])
        )
    
    def calculateTexturePosition(self):

        '''
        Calculates the (x, y) position of the texture.
        '''

        if self.texture is None:
            return
        
        # calculate position from left
        leftPos = self.parent.borderWidth + self.parent.padding
        if self.textureAlignment == 'right':
            leftPos = self.parent.size[0] - self.parent.size[1] + self.parent.padding + self.parent.borderWidth

        # calculate position from top
        topPos = self.parent.borderWidth + self.parent.padding

        self.texturePosition = (leftPos, topPos)

    def calculateTextWidth(self):

        '''
        Calculates the available width for the text.
        '''

        # width available = parent Dialogue box size - parent Dialogue borders and padding
        self.textWidthAvailable = self.parent.size[0] - 2 * self.parent.borderWidth - 2 * self.parent.padding

        # subtract texture width (if texture exists), including borders and padding
        if self.texture is not None:
            self.textWidthAvailable -= (self.parent.size[1]) - (2 * self.parent.padding) - (2 * self.parent.borderWidth)

    @property
    def text(self):
        '''
        Get / set the page text.
        '''
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.calculateTextWidth()
        self.splitText = splitText(self.text, font = self.parent.font, width = self.textWidthAvailable)