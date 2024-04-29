import pygame

# create a default 'system' font
pygame.font.init()
sysFont = pygame.font.SysFont(None, 24)

def drawText(screen, text, x = 0, y = 0, font = None, antialias = True, color = (255, 255, 255), background = None, centerX = False, centerY = False):
    
    # use the default 'system' font if none specified
    if font is None:
        font = sysFont

    # create text surface
    textSurface = font.render(text, antialias, color, background)

    # center
    if centerX == True:
        x -= textSurface.get_rect().width // 2
    if centerY == True:
        y -= textSurface.get_rect().height // 2

    # draw text to screen
    screen.blit(textSurface, (x, y))