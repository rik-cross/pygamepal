import pygame

# create a default 'system' font
pygame.font.init()
sysFont = pygame.font.SysFont(None, 24)

def drawText(screen, text, x = 0, y = 0, font = None, antialias = True, color = (255, 255, 255), background = None):
    
    # use the default 'system' font if none specified
    if font is None:
        font = sysFont

    # create text surface
    textSurface = font.render(text, antialias, color, background)
    # draw text to screen
    screen.blit(textSurface, (x, y))