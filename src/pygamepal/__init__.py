__version__ = "1.1.0"
__author__ = 'Rik Cross'
__license__ = 'MIT'

import pygame

from .globals import *

from .game import *
from .scene import *
from .sprite import *

from .input import *
from .camera import *
from .spriteImage import *
from .collider import *
from .trigger import *
from .button import *
from .particle import *
from .particleEmitter import *
from .transition import *
from .animator import *
from .animation import *
from .lighting import *
from .dialogue import *
from .dialoguePage import *

from .drawText import *
from .spriteTextureList import *
from .splitTexture import *
from .flatten import *
from .easingFunctions import *

pygame.init()

DEBUG = False