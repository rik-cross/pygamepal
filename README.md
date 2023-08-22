(Note: I'm also developing the [Gamma](https://github.com/rik-cross/gamma) Pygame ECS engine!)

# Pygame Utils
A library of classes and functions to support game development in Pygame

### Usage
Simply add the `pygame_utils.py` file to your project and import the module using `import pygame_utils` to use!

### Contents

- [Input](#input)
- [SpriteImage](#spriteImage)
- [Utility Functions](#functions)

<a name="input"></a>Input -- [Example](./inputExample.py)

```
# create new instance
input = pygame_utils.Input()

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
<a name="spriteImage"></a>SpriteImage -- [Example](./spriteImageExample)

```
# create new instance
spriteImage = pygame_utils.spriteImage()

# add one or more sprites, associated with a state
spriteImage.addTextures(state, firstTexture, *moreTextures)

# update() must be called once per frame
spriteImage.update()

# draw the current image/animation frame
spriteImage.draw()

# change the current image/animation state
# (does not need to be called for sprite with single state)
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

<a name="functions"></a>Utility functions

```
# draws text with minimal required parameters
drawText(screen, text, x, y, font=None, antialias=True, colour=White, background=None)
# minimal example:
drawText(screen, 'Hello, world!')

# returns a list of sub-textures from a large spritesheet/texture
# the list has the same dimensions as the original texture, but
# can be flattened using flatten(2dList).
splitTexture(texture, newTextureWidth, newTextureHeight)
# simple example, splitting a single 96x32 spritesheet into 4 separate textures:
textureList = splitTexture(texture, 32, 32)
firstTexture = textureList[0][0] # or firstTexture = flatten(textureList)[0]

# flattens a 2d list into a single list
flatten(2dList)
# see above for example
```
