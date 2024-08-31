#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

# create a default 'system' font
pygame.font.init()
sysFont = pygame.font.SysFont(None, 24)
smallFont = pygame.font.SysFont(None, 14)

def drawText(surface, text,
             position = [0, 0],
             font = None,
             antialias = True,
             color = 'white', backgroundColor = None,
             centerX = False, centerY = False):
    
    '''
    Draw text.

    :param pygame.Surface surface: The surface to draw to.
    :param str text: The text to draw.
    :param (int, int) position: The (x, y) position to draw on the specified surface (default = (0, 0)).
    :param pygame.Font font: The font to draw the text in (default = pygamepal.sysFont).
    :param bool antialias: Antialias text (default = True).
    :param pygame.Color color: Text color (default = 'white').
    :param pygame.Color backgroundColor: Background text color (default = None).
    :param bool centerX: Center horizontally (default = False).
    :param bool centerY: Center vertically (default = False).
    '''

    # use the default 'system' font if none specified
    if font is None:
        font = sysFont

    # create text surface
    textSurface = font.render(text, antialias, color, backgroundColor)

    # center
    if centerX == True:
        position = (position[0] - textSurface.get_rect().width // 2, position[1])
    if centerY == True:
        position = (position[0], position[1] - textSurface.get_rect().height // 2)

    # draw text to surface
    surface.blit(textSurface, position)