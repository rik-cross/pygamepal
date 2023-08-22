#
# pygame_utils -- Input Example
#

# import modules
import pygame
import pygame_utils

# initialise Pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('Input Test')
clock = pygame.time.Clock() 

input = pygame_utils.Input()

# game loop
running = True
while running:

    # clear screen
    screen.fill((0, 0, 0))

    # advance clock (10 FPS so that text is easier to read)
    clock.tick(10)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # input
    #

    # none

    #
    # update
    #

    # update input manager
    input.update()

    #
    # draw
    #

    # input text
    text =  "Return key -- down: " + str(input.isKeyDown(pygame.K_RETURN)) + \
            ", pressed: " + str(input.isKeyPressed(pygame.K_RETURN)) + \
            ", released: " + str(input.isKeyReleased(pygame.K_RETURN)) + \
            ", duration: " + str(input.getKeyDownDuration(pygame.K_RETURN)) + \
            ", long down: " + str(input.isKeyLongDown(pygame.K_RETURN)) + \
            ", long press: " + str(input.isKeyLongPressed(pygame.K_RETURN)) + \
            ", long%: " + str(input.GetKeyLongPressPercentage(pygame.K_RETURN))

    print(text)

    # draw to screen
    pygame.display.flip()

# quit Pygame
pygame.quit()
