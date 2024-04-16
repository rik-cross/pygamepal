#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

# import modules
import pygame
import pygamepal

# initialise Pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Particles Example')
clock = pygame.time.Clock()

#
# snow particles
#

snow = pygamepal.Particles(
    # positioned at the top of the screen
    emitterPosition = (0, 0),
    # the particle emitter is the width of the screen
    emitterSize = (680, 0),
    # particle emitter never expires
    emitterLifetime = -1,
    emitterParticleDelay = 5,
    particleLifetime = 250,
    particleVelocityMin = (0, 3),
    particleVelocityMax = (0, 3.5),
    particleSize = 2,
    particleSizeDecay= 0 ,
    particleColors = ['white']
)

#
# confetti particles
#

confetti = pygamepal.Particles(
    emitterPosition = (340, 460),
    # particle emitter never expires
    emitterLifetime = -1,
    emitterParticleDelay = 2,
    particleLifetime = 150,
    # particles have downwawrd acceleration (gravity)
    particleAccelerationMin = (0, 0.2),
    particleAccelerationMax = (0, 0.2),
    # particles have upwards velocity, and some horizontal variance
    particleVelocityMin = (-3, -10),
    particleVelocityMax = (3, -10),
    particleSize = 5,
    particleSizeDecay = 0,
    # particles can be any valid pygame colour
    particleColors= [c for c in pygame.color.THECOLORS.keys()]
)

#
# dust particles
#

dust = pygamepal.Particles(
    emitterPosition = (340, 100),
    emitterLifetime = -1,
    emitterParticleDelay = 5,
    particleLifetime = 50,
    # particles have a small amount of random velocity
    particleVelocityMin = (-2, -2),
    particleVelocityMax = (2, 2),
    particleSize = 15,
    particleSizeDecay = 0.4,
    particleColors = ['gray60', 'gray70', 'gray80']
)

# game loop
running = True
while running:

    # advance clock
    clock.tick(60)

    deltaTime = clock.get_time()

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # update
    #

    for p in [snow, confetti, dust]:
        p.update()

    #
    # draw
    #

    # clear screen
    screen.fill('cornflowerblue')

    for p in [snow, confetti, dust]:
        p.draw(screen)

    # draw to screen
    pygame.display.flip()

# quit Pygame
pygame.quit()