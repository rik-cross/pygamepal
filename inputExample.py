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
pygame.display.set_caption('Input Example')
clock = pygame.time.Clock()

input = pygame_utils.Input()

# game loop
running = True
while running:

    # clear screen
    screen.fill(pygame_utils.Colour.CORNFLOWER_BLUE)

    # advance clock (10 FPS so that text is easier to read)
    clock.tick(10)

    deltaTime = clock.get_time()

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
    input.update(deltaTime)

    #
    # draw
    #

    # input text
    key = pygame.K_RETURN
    text = "Return key -- down: " + str(input.isKeyDown(key)) + \
        ", pressed: " + str(input.isKeyPressed(key)) + \
        ", released: " + str(input.isKeyReleased(key)) + \
        ", duration: " + str(input.getKeyDownDuration(key)) + \
        ", long down: " + str(input.isKeyLongDown(key)) + \
        ", long press: " + str(input.isKeyLongPressed(key)) + \
        ", long%: " + \
        "{:.2f}".format(input.GetKeyLongPressPercentage(key))

    print(text)

    # draw to screen
    pygame.display.flip()

#  quit Pygame
pygame.quit()
