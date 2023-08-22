#
# pygame_utils -- SpriteImage Example
#
# instructions:
#  -- space to toggle pause middle sprite
#  -- arrow keys to control bottom sprite
#
# Image credit - Cup Nooble
#  --  cupnooble.itch.io/sprout-lands-asset-pack
#

# import modules
import pygame
import pygame_utils
import os

# initialise Pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode((680, 460))
pygame.display.set_caption('SpriteImage Example')
clock = pygame.time.Clock() 

# add input, to easily query keys
input = pygame_utils.Input()

# load a texture
texture = pygame.image.load(os.path.join('images','character.png'))
# double the texture size
texture = pygame.transform.scale(texture, (texture.get_width()*2,texture.get_height()*2))
# split texture into a 2D list of sub-textures
splitTextures = pygame_utils.splitTexture(texture, 96, 96)

# a sprite with a single texture
sprite1 = pygame_utils.SpriteImage()
sprite1.addTextures('default', splitTextures[0][0])

# an animated sprite with multiple textures
sprite2 = pygame_utils.SpriteImage()
sprite2.addTextures('walk_right', splitTextures[3][1], splitTextures[3][2], splitTextures[3][1], splitTextures[3][3])

# a controllable sprite with multiple animation states
sprite3 = pygame_utils.SpriteImage()
sprite3.addTextures('idle', splitTextures[0][0], splitTextures[0][1])
sprite3.addTextures('walk_down', splitTextures[0][1], splitTextures[0][2], splitTextures[0][1], splitTextures[0][3])
sprite3.addTextures('walk_up', splitTextures[1][1], splitTextures[1][2], splitTextures[1][1], splitTextures[1][3])
sprite3.addTextures('walk_left', splitTextures[2][1], splitTextures[2][2], splitTextures[2][1], splitTextures[2][3])
sprite3.addTextures('walk_right', splitTextures[3][1], splitTextures[3][2], splitTextures[3][1], splitTextures[3][3])

# for easily getting key presses
input = pygame_utils.Input()

# game loop
running = True
while running:

    # clear screen
    screen.fill((0, 0, 0))

    # advance clock
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # input
    #

    # space to toggle pause s2 sprite
    if input.isKeyPressed(pygame.K_SPACE):
        sprite2.pause = not sprite2.pause

    # arrow keys to change state of s3 sprite
    if input.isKeyDown(pygame.K_UP):
        sprite3.setState('walk_up')
    elif input.isKeyDown(pygame.K_DOWN):
        sprite3.setState('walk_down')
    elif input.isKeyDown(pygame.K_LEFT):
        sprite3.setState('walk_left')
    elif input.isKeyDown(pygame.K_RIGHT):
        sprite3.setState('walk_right')
    # idle state is the default
    else:
        sprite3.setState('idle')

    #
    # update
    #

    input.update()
    sprite1.update()
    sprite2.update()
    sprite3.update()

    #
    # draw
    #

    # draw split texture
    for col in range(len(splitTextures)):
        for row in range(len(splitTextures[0])):
            pygame.draw.rect(screen, (50, 50, 50), (col * 100, row * 100, 96, 96), False)
            screen.blit(splitTextures[row][col], (col * 100, row * 100, 96, 96))

    # draw sprites and accompanying text
    pygame_utils.drawText(screen, 'Sprite 1 (single texture)', 420, 40)
    sprite1.draw(screen, 500, 50)
    pygame_utils.drawText(screen, 'Sprite 2 (space to pause/play)', 420, 140)
    sprite2.draw(screen, 500, 150)
    pygame_utils.drawText(screen, 'Sprite 3 (arrow keys to change)', 420, 240)
    sprite3.draw(screen, 500, 250)
    # draw to screen
    pygame.display.flip()

# quit Pygame
pygame.quit()
