#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

#
# draw utils
#

# easily draw text

def drawText(screen, text, x = 0, y = 0, font = None, antialias = True, color = (255, 255, 255), background = None):
    # use 'standard' font if none specified
    if font is None:
        font = pygame.font.SysFont(None, 24)
    # create text surface
    textSurface = font.render(text, antialias, color, background)
    # draw text to screen
    screen.blit(textSurface, (x, y))
