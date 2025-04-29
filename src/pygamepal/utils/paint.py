#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from ..game import Game
from ..input import Input
from ..button import Button
from ..camera import Camera
from ..drawText import drawText

class PaintApp(Game):

    def zoomOut(self, button=None):
        self.camera.zoom -= 8
    def zoomIn(self, button=None):
        self.camera.zoom += 8
    def firstImage(self, button):
        self.currentImageIndex = 0
    def prevImage(self, button):
        self.currentImageIndex -= 1
        if self.currentImageIndex < 0:
            self.currentImageIndex = len(self.spriteSurfaces) - 1
    def nextImage(self, button):
        self.currentImageIndex += 1
        if self.currentImageIndex >= len(self.spriteSurfaces):
            self.currentImageIndex = 0
    def lastImage(self, button):
        self.currentImageIndex = len(self.spriteSurfaces) - 1
    def addImage(self, button):
        self.spriteSurfaces.append(pygame.surface.Surface((self.imgW, self.imgH), pygame.SRCALPHA))
        self.currentImageIndex = len(self.spriteSurfaces) - 1
    def clearImage(self, button):
        for i in range(self.spriteSurfaces[self.currentImageIndex].get_size()[0]):
            for j in range(self.spriteSurfaces[self.currentImageIndex].get_size()[1]):
                self.spriteSurfaces[self.currentImageIndex].set_at((i, j), (0,0,0,0))
    def deleteImage(self, button):
        if len(self.spriteSurfaces) == 1:
            return
        self.spriteSurfaces.remove(self.spriteSurfaces[self.currentImageIndex])
        if self.currentImageIndex >= len(self.spriteSurfaces):
            self.currentImageIndex = len(self.spriteSurfaces) - 1
    def saveImage(self, button):
        saveSurf = pygame.surface.Surface((self.imgW * self.saveZoom * len(self.spriteSurfaces), self.imgH * self.saveZoom))
        
        for s in range(len(self.spriteSurfaces)):
            
            fromSurf = self.spriteSurfaces[s]
            
            for i in range(fromSurf.get_size()[0]):
                for j in range(fromSurf.get_size()[1]):

                    for a in range(0, self.saveZoom):
                        for b in range(0, self.saveZoom):
                            saveSurf.set_at(((self.imgW * self.saveZoom * s) + i*self.saveZoom+a, j*self.saveZoom+b),fromSurf.get_at((i, j)))

        pygame.image.save(saveSurf, "test.png")
    def lowerImageZoom(self, button):
        self.saveZoom -= 1
        if self.saveZoom < 1:
            self.saveZoom = 1
    def raiseImageZoom(self, button):
        self.saveZoom += 1
    def setC(self, button, c):
        self.c = self.cl[c]
    def undo(self, button):
        if self.h == 0:
            return
        data = self.history[self.h-1]
        pos = data[0]
        old = data[1]
        self.spriteSurfaces[self.currentImageIndex].set_at(pos, old)
        self.h-= 1
    def redo(self, button):
        if self.h >= len(self.history):
            return
        self.h += 1
        data = self.history[self.h-1]
        pos = data[0]
        new = data[2]
        self.spriteSurfaces[self.currentImageIndex].set_at(pos, new)
    def togglePlay(self, button):
        self.playing = not self.playing
    def reset(self, button):
        self.currentImageIndex = 0
        self.spriteSurfaces = self.spriteSurfaces[:1]
        self.clearImage()
    def setTool(self, button, tool):
        self.tool = self.tools.index(tool)

    def init(self):

        # mouse images
        self.mouse_draw = pygame.image.load('pen.png')
        self.cursor = self.mouse_draw
        #pygame.mouse.set_visible(False)

        self.startDrag = None
        self.endDrag = None

        #self.size = (1500, 800)
        #self.caption = 'PygamePal Paint'
        
        self.imgW = 16
        self.imgH = 16
        self.cameraS = 16 * 32
        self.camZ = (self.cameraS / max(self.imgW, self.imgH)) - 128/max(self.imgW, self.imgH)

        self.c = pygame.color.THECOLORS['snow1']
        self.px = self.cameraS
        self.py = 0
        self.pw = 5
        self.ph = 5

        self.saveZoom = 1

        self.currentImageIndex = 0
        self.spriteSurfaces = [pygame.surface.Surface((self.imgW,self.imgH), pygame.SRCALPHA)]

        self.transSurface = pygame.surface.Surface((self.imgW,self.imgH), pygame.SRCALPHA)
        for d in range(0, self.imgW):
            for f in range(0, self.imgH):
                if (d%2 == 0 and f%2 == 1) or (d%2 == 1 and f%2 == 0):
                    self.transSurface.set_at((d, f), 'gray60')
                else:
                    self.transSurface.set_at((d, f), 'gray30')
        self.outputSurface = pygame.surface.Surface((self.imgW,self.imgH), pygame.SRCALPHA)
        
        self.input = Input()
        self.camera = Camera((0, 0), (self.cameraS, self.cameraS), target=(self.imgW//2, self.imgH//2), zoom=self.camZ, minZoom=1, maxZoom=1000, borderThickness=0, backgroundColor='black')

        # buttons
        self.buttonZoomOut = Button(self.input, (0, self.cameraS), (32, 32), '-', onSelected=self.zoomOut)
        self.buttonZoomIn = Button(self.input, (40, self.cameraS), (32, 32), '+', onSelected=self.zoomIn)
        
        self.buttonPrevImage = Button(self.input, (120, self.cameraS), (32, 32), '<', onSelected=self.prevImage)
        self.buttonNextImage = Button(self.input, (160, self.cameraS), (32, 32), '>',  onSelected=self.nextImage)
        self.buttonFirstImage = Button(self.input, (80, self.cameraS), (32, 32), '<<', onSelected=self.firstImage)
        self.buttonLastImage = Button(self.input, (200, self.cameraS), (32, 32), '>>', onSelected=self.lastImage)
        self.buttonAddImage = Button(self.input, (240, self.cameraS), (32, 32), 'New', onSelected=self.addImage)
        self.buttonDeleteImage = Button(self.input, (280, self.cameraS), (32, 32), 'Del', onSelected=self.deleteImage)

        self.buttonClearImage = Button(self.input, (320, self.cameraS), (32, 32), 'Clear', onSelected=self.clearImage)

        self.buttonSaveImage = Button(self.input, (600, 300), (32, 32), 'S', onSelected=self.saveImage)
        self.buttonLowerImageZoom = Button(self.input, (640, 300), (32, 32), '-', onSelected=self.lowerImageZoom)
        self.buttonRaiseImageZoom = Button(self.input, (680, 300), (32, 32), '+', onSelected=self.raiseImageZoom)

        self.buttonUndo = Button(self.input, (0, self.cameraS+40), (32, 32), 'U', onSelected=self.undo)
        self.buttonRedo = Button(self.input, (40, self.cameraS+40), (32, 32), 'R', onSelected=self.redo)

        self.buttonPlay = Button(self.input, (520, 200), (32, 32), 'Pl', onSelected=self.togglePlay)

        self.buttonReset = Button(self.input, (360, self.cameraS), (32, 32), 'Reset', onSelected=self.reset)

        self.cl = pygame.color.THECOLORS
        self.cl['transparent'] = (0, 0, 0, 0)
        self.crv = {v:k for k,v in self.cl.items()}

        self.cs = [
            'snow1','lavenderblush2','mistyrose3','mistyrose4', 'gray25',
            'lightgoldenrod1','gold1','tan1','yellowgreen','olivedrab',
            'thistle','lightpink2','hotpink1','mediumpurple2','mediumorchid4',
            
            'aquamarine3','darkturquoise','deepskyblue3','royalblue3','darkslategray',
            'coral2','orangered2','saddlebrown','gray10', 'transparent'
            ]
        
        self.buttons = []
        xx = self.cameraS
        yy = 0
        for z in range(len(self.cs)):
            bg = self.cs[z]
            if self.cl[self.cs[z]] == self.cl['transparent']:
                bg = 'transparent'
            self.buttons.append(
                Button(
                    self.input, (xx, yy), (32, 32), backgroundColor = bg, onSelected = lambda b=self, c = self.cs[z] : self.setC(b, c)
                )
            )
            xx += 32
            if xx >= self.cameraS + 32 * self.pw:
                yy += 32
                xx = self.cameraS
        
        self.buttons[-1].image = pygame.image.load('transparent.png')


        self.history = []
        self.h = 0

        self.playing = False
        self.animationTimer = 0
        self.animationDelay = 4

        self.prevWorldMousePos = self.getWorldPosFromMousePos()
        self.currWorldMousePos = self.getWorldPosFromMousePos()
        self.prevMouse1 = self.input.isMouseButtonDown(0)
        self.currMouse1 = self.input.isMouseButtonDown(0)

        #
        # tools
        #

        self.tools = ['pen', 'fill', 'move', 'select']
        self.tool = 0

        self.buttonPen = Button(self.input, (self.cameraS, 32*5), (32, 32), 'Pen', 'white', 'black', onSelected=lambda b=self, t='pen' : self.setTool(b, t), keyCode=pygame.K_p)
        self.buttonFill = Button(self.input, (self.cameraS +32*1 , 32*5), (32, 32), 'Fill', 'white', 'black', onSelected=lambda b=self, t='fill' : self.setTool(b, t))
        self.buttonMove = Button(self.input, (self.cameraS +32*2, 32*5), (32, 32), 'Move', 'white', 'black', onSelected=lambda b=self, t='move' : self.setTool(b, t))
        self.buttonSelect = Button(self.input, (self.cameraS +32*3, 32*5), (32, 32), 'Sel', 'white', 'black', onSelected=lambda b=self, t='select' : self.setTool(b, t))

        self.cx = self.px
        self.cy = self.py

        

    def update(self, deltaTime=1):

        self.input.update()
        self.camera.update()

        self.buttonZoomOut.update()
        self.buttonZoomIn.update()

        self.buttonFirstImage.update()
        self.buttonPrevImage.update()
        self.buttonNextImage.update()
        self.buttonLastImage.update()
        self.buttonAddImage.update()

        self.buttonClearImage.update()
        self.buttonDeleteImage.update()

        self.buttonSaveImage.update()
        self.buttonLowerImageZoom.update()
        self.buttonRaiseImageZoom.update()

        self.buttonUndo.update()
        self.buttonRedo.update()

        self.buttonPlay.update()

        self.buttonReset.update()


        self.buttonPen.update()
        self.buttonFill.update()
        self.buttonMove.update()
        self.buttonSelect.update()

        for b in self.buttons:
            b.update()

        self.prevWorldMousePos = self.currWorldMousePos
        self.currWorldMousePos = self.getWorldPosFromMousePos()
        self.prevMouse1 = self.currMouse1
        self.currMouse1 = self.input.isMouseButtonDown(0)

        self.dragging = False
        if self.currMouse1 and self.prevWorldMousePos != self.currWorldMousePos:
            self.dragging = True




        #else:
        #    self.startDrag = None
        #   self.endDrag = None

        #print (self.startDrag, '  ', self.endDrag)

        if self.dragging and self.tools[self.tool] == 'move':

            #self.camera.target = self.currWorldMousePos
            dx = self.prevWorldMousePos[0] - self.currWorldMousePos[0]
            dy = self.prevWorldMousePos[1] - self.currWorldMousePos[1]
            
            # this causes the mouse position to move
            self.camera.target = (self.camera.target[0] + dx, self.camera.target[1] + dy)
            self.currWorldMousePos = (self.currWorldMousePos[0] + dx, self.currWorldMousePos[1] + dy)
    
        #print(self.startDrag, '  ', self.endDrag)

        currentMousePos = self.input.getMouseCursorPosition()
        cameraPos = self.camera.position
        cameraSize = self.camera.size

        if self.tools[self.tool] == 'pen' and self.input.isMouseButtonDown(0):
            if currentMousePos[0] >= cameraPos[0] and currentMousePos[0] <= cameraPos[0] + cameraSize[0] and currentMousePos[1] >= cameraPos[1] and currentMousePos[1] <= cameraPos[1] + cameraSize[1]:
                worldP = self.getWorldPosFromMousePos()         
                if worldP[0] >= 0 and worldP[0] < self.imgW and worldP[1] >= 0 and worldP[1] < self.imgH:

                    if self.spriteSurfaces[self.currentImageIndex].get_at(worldP) != self.c:

                        # improve to cope with multiple sheets
                        self.history = self.history[0:self.h]

                        # image, p, c_undo, c_redo
                        # make an object 'historyData'
                        self.history.append([worldP, self.spriteSurfaces[self.currentImageIndex].get_at(worldP), self.c])
                        self.h += 1

                        self.spriteSurfaces[self.currentImageIndex].set_at(worldP, self.c)

        # select tool
        #print(self.tools[self.tool])
        if self.tools[self.tool] == 'select' and self.input.getMouseCursorPosition()[0] < (self.camera.position[0] + self.camera.size[0]) and self.input.getMouseCursorPosition()[1] < (self.camera.position[1] + self.camera.size[1]):

            # calculate world pos from mouse pos

            if self.input.isMouseButtonPressed(0):
                # start
                self.startDrag = self.currWorldMousePos
                self.endDrag = None

            elif self.dragging and (self.prevWorldMousePos != self.currWorldMousePos):
                # end
                self.endDrag = self.currWorldMousePos

        #print(self.startDrag, self.endDrag)

        for z in self.buttons:
                
            if self.cl[z.backgroundColor] == self.c:
                self.cx = self.px + (self.cs.index(z.backgroundColor) % self.pw) * 32
                self.cy = self.py + (self.cs.index(z.backgroundColor) // self.ph) * 32
        
        if self.playing:
            self.animationTimer += 1
            if self.animationTimer >= self.animationDelay:
                self.animationTimer = 0
                self.currentImageIndex += 1
                if self.currentImageIndex >= len(self.spriteSurfaces):
                    self.currentImageIndex = 0
        
        if self.input.isMouseButtonPressed(2):
            m = self.input.getMouseCursorPosition()
            if m[0] >= 0 and m[0] <= self.cameraS and m[1] >= 0 and m[1] <= self.cameraS:
                self.camera.target = self.getWorldPosFromMousePos()
        
        for event in self.events:
            if event.type == pygame.MOUSEWHEEL:
                m = self.input.getMouseCursorPosition()
                if m[0] >= 0 and m[0] <= self.cameraS and m[1] >= 0 and m[1] <= self.cameraS:
                    if event.y > 0:
                        self.zoomIn()
                    elif event.y < 0:
                        self.zoomOut()

    def draw(self):

        self.screen.fill('cornflowerblue')

        self.outputSurface.blit(self.transSurface, (0, 0))
        self.outputSurface.blit(self.spriteSurfaces[self.currentImageIndex], (0, 0))
        self.camera.draw(self.outputSurface, self.screen)

        if self.startDrag is not None and self.endDrag is not None:
            
            # get screen pos from world pos
            spixelOffset = (self.startDrag[0] - self.camera.target[0],
                            self.startDrag[1] - self.camera.target[1])
            sres = (self.camera.position[0] + self.camera.size[0]/2 + spixelOffset[0] * self.camera.zoom,
                   self.camera.position[1] + self.camera.size[1]/2 + spixelOffset[1] * self.camera.zoom)
            #print(spixelOffset)

            epixelOffset = (self.endDrag[0] - self.camera.target[0],
                            self.endDrag[1] - self.camera.target[1])
            eres = (self.camera.position[0] + self.camera.size[0]/2 + epixelOffset[0] * self.camera.zoom,
                   self.camera.position[1] + self.camera.size[1]/2 + epixelOffset[1] * self.camera.zoom)

            #print(spixelOffset)
            #print(self.startDrag, ' ', sres, '    ', self.endDrag, ' ', eres)
            pygame.draw.rect(self.screen, 'white', (
                min(sres[0], eres[0]),
                min(sres[1], eres[1]),
                max(sres[0], eres[0])-min(sres[0], eres[0]), 
                max(sres[1], eres[1])-min(sres[1], eres[1])),
                2)


        self.buttonZoomOut.draw(self.screen)
        self.buttonZoomIn.draw(self.screen)

        self.buttonFirstImage.draw(self.screen)
        self.buttonPrevImage.draw(self.screen)
        self.buttonNextImage.draw(self.screen)
        self.buttonLastImage.draw(self.screen)
        self.buttonAddImage.draw(self.screen)

        self.buttonClearImage.draw(self.screen)
        self.buttonDeleteImage.draw(self.screen)

        self.buttonSaveImage.draw(self.screen)
        self.buttonLowerImageZoom.draw(self.screen)
        self.buttonRaiseImageZoom.draw(self.screen)

        self.buttonUndo.draw(self.screen)
        self.buttonRedo.draw(self.screen)

        self.buttonPlay.draw(self.screen)

        self.buttonReset.draw(self.screen)

        self.buttonPen.draw(self.screen)
        self.buttonFill.draw(self.screen)
        self.buttonMove.draw(self.screen)
        self.buttonSelect.draw(self.screen)


        for b in self.buttons:
            b.draw(self.screen)

        # draw tool select
        pygame.draw.rect(self.screen, 'white', (self.cameraS - 2 + 32*(self.tools.index(self.tools[self.tool])), 32*5 - 2, 36, 36), 2)
        pygame.draw.rect(self.screen, 'black', (self.cameraS + 32*(self.tools.index(self.tools[self.tool])), 32*5, 32, 32), 2)
        


        # draw colour select
        pygame.draw.rect(self.screen, 'white', (self.cx - 2 , self.cy -2 , 36, 36), 2)
        pygame.draw.rect(self.screen, 'black', (self.cx, self.cy, 32, 32), 2)

        drawText(self.screen, str(self.saveZoom) + ', image size= ' + str(self.imgW*self.saveZoom) + 'x' + str(self.imgH*self.saveZoom) , (600, 350))
        
        for g in range(8):
            if g == self.currentImageIndex:
                ccc = 'white'
                w = 5
            elif g <= len(self.spriteSurfaces) -1:
                ccc = 'gray60'
                w = 5
            else:
                ccc = 'gray60'
                w = 1
            pygame.draw.circle(self.screen, ccc, (self.cameraS/2 - 4*15 + g*15, self.cameraS - 20), 5, w)
            pygame.draw.circle(self.screen, 'white', (self.cameraS/2 - 4*15 + g*15, self.cameraS - 20), 5, 1)

        
        drawText(self.screen, str(self.animationDelay), (650, 250))

        cp = (self.input.getMouseCursorPosition()[0],
              self.input.getMouseCursorPosition()[1] - self.cursor.get_size()[1])
        self.screen.blit(self.cursor, cp)

    
    def getWorldPosFromMousePos(self):

        currentMousePos = self.input.getMouseCursorPosition()
        cameraPos = self.camera.position
        cameraSize = self.camera.size

        offset = ((currentMousePos[0] - cameraPos[0]),
                    (currentMousePos[1] - cameraPos[1]))

        diff = ((cameraSize[0] - 8*self.camera.zoom) / 2,
                (cameraSize[0] - 8*self.camera.zoom) / 2)
    
        t = (4-self.camera.target[0],
             4-self.camera.target[1])

        worldPos = (int((currentMousePos[0] - cameraPos[0] - diff[0] - t[0]*self.camera.zoom) / self.camera.zoom),
                    int((currentMousePos[1] - cameraPos[1] - diff[1] - t[1]*self.camera.zoom) / self.camera.zoom))
        
        return worldPos

#
# create a new app instance
#

paintApp = PaintApp(size=(1000, 600), caption='PygamePal Paint')
paintApp.run()