#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from .easingFunctions import easeLinear

class Transition:

    '''
    The base class for transitions between 2 surfaces. This class does not need to be used directly.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/transitionExample.gif?raw=true

    `Example Transition code`_.

    .. _Example Transition code: https://github.com/rik-cross/pygamepal/blob/main/transitionExample.py
    
    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):

        self.fromSurface = fromSurface
        self.toSurface = toSurface
        self.duration = duration
        self.easingFunction = easingFunction

        self.easeValue = 0
        self.currentPercentage = 0
        self.finished = False

        # allows adjusting for different durations
        self.durationCoefficient = 100 / self.duration

    def update(self, deltaTime=1):
        perc = self.currentPercentage + (deltaTime * self.durationCoefficient)
        self.currentPercentage = min(perc, 100)
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.currentPercentage == 100:
            self.finished = True

    def draw(self, surface):
        if self.drawMethod is not None:
            self.drawMethod

    def reset(self):
        self.currentPercentage = 0
        self.easeValue = 0
        self.durationCoefficient = 100 / self.duration

class TransitionFade(Transition):

    '''
    Fade between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = easeLinear):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            self.fromSurface.set_alpha((100 - self.easeValue) * 2.55)
            surface.blit(self.fromSurface, (0, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(self.easeValue * 2.55)
            surface.blit(self.toSurface, (0, 0))

    def __repr__(self):
        return 'Transition: Fade between'

class TransitionFadeToBlack(Transition):

    '''
    Fade to black between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)
        self.blacksurface = pygame.Surface((self.fromSurface.get_width(), self.fromSurface.get_height()), pygame.SRCALPHA, 32)
        self.blacksurface.fill('black')

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None and self.easeValue < 50:
            surface.blit(self.fromSurface, (0, 0))
        if self.toSurface is not None and self.easeValue > 50:
            surface.blit(self.toSurface, (0, 0))
        distanceFromMidPoint = abs(50 - self.easeValue)
        percentageToAlpha = 255 - (distanceFromMidPoint * 2.55 * 2)
        self.blacksurface.set_alpha(percentageToAlpha)
        surface.blit(self.blacksurface, (0, 0))

    def __repr__(self):
        return 'Transition: Fade to black'

class TransitionWipeLeft(Transition):

    '''
    Wipe left between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            surface.blit(self.fromSurface, (0, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = (surface.get_width()) - (surface.get_width() / 100 * self.easeValue)
            surface.blit(self.toSurface, (r, 0))

    def __repr__(self):
        return 'Transition: Wipe left'

class TransitionWipeRight(Transition):

    '''
    Wipe right between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            surface.blit(self.fromSurface, (0, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = ((surface.get_width() * -1)) + (surface.get_width() / 100 * self.easeValue)
            surface.blit(self.toSurface, (r, 0))

    def __repr__(self):
        return 'Transition: Wipe right'

class TransitionWipeUp(Transition):

    '''
    Wipe up between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            surface.blit(self.fromSurface, (0, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = (surface.get_height()) - (surface.get_height() / 100 * self.easeValue)
            surface.blit(self.toSurface, (0, r))

    def __repr__(self):
        return 'Transition: Wipe up'

class TransitionWipeDown(Transition):

    '''
    Wipe down between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            surface.blit(self.fromSurface, (0, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = ((surface.get_height() * -1)) + (surface.get_height() / 100 * self.easeValue)
            surface.blit(self.toSurface, (0, r))

    def __repr__(self):
        return 'Transition: Wipe down'

class TransitionMoveLeft(Transition):

    '''
    Move left between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            self.fromSurface.set_alpha(255)
            r = 0 - (surface.get_width() / 100 * self.easeValue)
            surface.blit(self.fromSurface, (r, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = (surface.get_width()) - (surface.get_width() / 100 * self.easeValue)
            surface.blit(self.toSurface, (r, 0))

    def __repr__(self):
        return 'Transition: Move left'

class TransitionMoveRight(Transition):

    '''
    Move right between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            self.fromSurface.set_alpha(255)
            r = (surface.get_width() / 100 * self.easeValue)
            surface.blit(self.fromSurface, (r, 0))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = ((surface.get_width() * -1)) + (surface.get_width() / 100 * self.easeValue)
            surface.blit(self.toSurface, (r, 0))

    def __repr__(self):
        return 'Transition: Move right'

class TransitionMoveUp(Transition):

    '''
    Move up between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            self.fromSurface.set_alpha(255)
            r = 0 - (surface.get_height() / 100 * self.easeValue)
            surface.blit(self.fromSurface, (0, r))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = (surface.get_height()) - (surface.get_height() / 100 * self.easeValue)
            surface.blit(self.toSurface, (0, r))

    def __repr__(self):
        return 'Transition: Move up'

class TransitionMoveDown(Transition):

    '''
    Move down between 2 surfaces.

    :param pygame.Surface from Surface: The surface to transition from.
    :param pygame.Surface toSurface: The surface to transition to.
    :param float duration: The time over which to transition between surfaces.
    :param func easingFunction: The easing function to apply to the transition (default = pygamepal.easeLinear).
    '''

    def __init__(self, fromSurface = None, toSurface = None, duration = 100, easingFunction = None):
        super().__init__(fromSurface, toSurface, duration, easingFunction)

    def draw(self, surface):
        self.easeValue = self.easingFunction(self.currentPercentage)
        if self.fromSurface is not None:
            self.fromSurface.set_alpha(255)
            r = (surface.get_height() / 100 * self.easeValue)
            surface.blit(self.fromSurface, (0, r))
        if self.toSurface is not None:
            self.toSurface.set_alpha(255)
            r = ((surface.get_height() * -1)) + (surface.get_height() / 100 * self.easeValue)
            surface.blit(self.toSurface, (0, r))

    def __repr__(self):
        return 'Transition: Move down'