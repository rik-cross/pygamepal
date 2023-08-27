#
# Pygame simple camera example
# part of the pygame_utils library
#  -- github.com/rik-cross/pygame_utils
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack

import pygame

# initialise Pygame
pygame.init()

screen_size = (680, 460)

# setup screen to required size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Simple camera example')
clock = pygame.time.Clock()

character = pygame.sprite.Sprite()
character.image = pygame.image.load('character.png')
character.position = (100, 100)
character.size = (36, 48)

# game loop
running = True
while running:

    # clear screen to Cornflower Blue
    screen.fill('cornflowerblue')

    # advance clock at 60 FPS
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # camera is focused on the center of the player
    cameraCenter = (character.position[0] + character.size[0]/2,
                    character.position[1] + character.size[1]/2)

    # camera offset = screen center - camera center
    cameraOffset = (screen_size[0]/2 - cameraCenter[0],
                    screen_size[1]/2 - cameraCenter[1])

    # player position doesn't change, instead the offset is added to the position
    screen.blit(character.image, (character.position[0] + cameraOffset[0], 
                                  character.position[1] + cameraOffset[1]))

    # draw to the screen
    pygame.display.flip()

# quit Pygame on exit
pygame.quit()
