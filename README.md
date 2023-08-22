(Note: I'm also developing the [Gamma](https://github.com/rik-cross/gamma) Pygame ECS engine!)

# Pygame Utils
A library of classes and functions to support game development in Pygame

### Usage
Simply add the `pygame_utils.py` file to your project and import the module using `import pygame_utils` to use!

### Contents

Input -- [Example](./inputExample.py)

```
# update() must be called once per frame
input.update()
input.isKeyDown(keycode)
input.isKeyPressed(keycode)
input.isKeyReleased(keycode)
input.getKeyDownDuration(keycode)
input.isKeyLongDown(keycode)
input.isKeyLongPressed(keycode)
input.getKeyLongPressPercentage(keycode)
```
SpriteImage -- [Example](./spriteImageExample)

```

# update() must be called once per frame
spriteImage.update()

# draw the current image/animation frame
spriteImage.draw()

# add one or more sprites, associated with a state
spriteImage.addTextures(state, firstTexture, *moreTextures)

# change the current image/animation state
spriteImage.setState(state)

# resets the current animation
spriteImage.reset()

# spriteImage parameters
spriteImage.loop
spriteImage.hFlip
spriteImage.vFlip
# number of game frames per animation frame
spriteImage.animationDelay
# start (x,y) position of texture, to remove padding
spriteImage.offset
spriteImage.pause
```

Utility functions

```
# draws text with minimal required parameters
drawText(screen, text, x, y, font=None, antialias=True, colour=White, background=None)

# returns a list of sub-textures from a large spritesheet/texture
# the list has the same dimensions as the original texture, but
# can be flattened using flatten(2dList).
splitTexture(texture, newTextureWidth, newTextureHeight)

# flattens a 2d list into a single list
flatten(2dList)
```
