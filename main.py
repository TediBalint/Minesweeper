import random
import pygame

#Constants
X = 800
Y = 900
DISPLAY = (X,Y)
SIZE = 20
BOMBS = 40
FLAGICON = pygame.transform.scale(pygame.image.load("flag-ico.png"), (80*2.5*SIZE/100,80*2.5*SIZE/100))
UITEXTSIZE = 40

white = (255,255,255)


#Colors
bggreen = (74,117,4)
blue = (0,0,255)
red = (255,0,0)
grey = (128,128,128)
green = (124,200,0)
lightergreen = (174, 250, 50)
darkgreen = (1, 100, 32)
lighdarkgreen = (51, 150, 82)
brown = (216, 184, 152)
lighterbrown = (226, 194, 162)
darkbrown = (166, 134, 102)
lighterdarkbrown = (176, 144, 112)

#tiles
mouseOnTiles = False
tiles = []
lastTile = None
flags = BOMBS

class tile:
    def __init__(self, xIndex, yIndex, size, color) -> None:
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.isMine = False
        self.number = None
        self.size = size
        self.color = color
        self.clicked = False
        self.xPos = self.xIndex * self.size
        self.yPos = self.yIndex * self.size
        self.randColor = (random.randint(50,255), random.randint(50, 255), random.randint(50,255))
        self.flagged = False


    def draw(self):        
        
        
        if not self.clicked:
            pygame.draw.rect(win, self.color,(self.xPos, self.yPos, self.size, self.size))
            if self.flagged:
                win.blit(FLAGICON,(self.xPos, self.yPos))
            return
        if not self.isMine:
            pygame.draw.rect(win, self.color,(self.xPos, self.yPos, self.size, self.size))
            num = pygame.font.Font('freesansbold.ttf', int(self.size/1.25)).render(str(self.number), True, self.getNumberColor())
            win.blit(num,(self.xPos + self.size/3.4, self.yPos + self.size/6))
        else: 
            
            pygame.draw.rect(win, self.randColor,(self.xPos, self.yPos, self.size, self.size))
            pygame.draw.circle(win,(self.randColor[0]-50, self.randColor[1]-50, self.randColor[2]-50),(self.xPos + self.size/2, self.yPos + self.size/2), self.size/3 )
        

    def setNumber(self):
        if not self.isMine:
            number = 0
            for x in range(-1, 2):
                for y in range(-1,2):
                    if len(tiles)-1 >= self.xIndex + x >= 0 and len(tiles)-1 >= self.yIndex + y >= 0 and tiles[self.xIndex + x][self.yIndex + y].isMine:
                        number += 1
            self.number = number
                    
        
    
    def getNumberColor(self):
        color = 0
        if self.number == 0:
            color = grey
        elif self.number == 1:
            color = blue
        elif self.number == 2:
            color = green
        elif self.number == 3:
            color = red
        elif self.number == 4:
            color = brown
        return color
    def onClick(self):
        
        if len(getActive_ClickedMines()[0]) == 0 and len(getActive_ClickedMines()[1]) == 0:
            generateBombs(BOMBS, self.xIndex, self.yIndex)
        self.getAllTilesNextToZero()
        self.color = getColor(self)
        

        
        self.draw()
        

    def getAllTilesNextToZero(self):
        if not self.clicked:
            self.clicked = True
            if self.number == 0:
                for x in range(-1,2):
                    for y in range(-1,2):
                        if not(y == 0 and x == 0):
                            if len(tiles) > self.xIndex + x > -1 and len(tiles) > self.yIndex + y > -1:
                                tiles[self.xIndex + x][self.yIndex + y].onClick()
                            


def showAll():
    for x in range(len(tiles)):
        for y in range(len(tiles)):
            tiles[x][y].onClick()
def getActive_ClickedMines():
    active_mines = []
    clicked_mines = []
    for x in range(len(tiles)):
        for y in range(len(tiles)):
            if tiles[x][y].isMine:
                active_mines.append(tiles[x][y])
            if tiles[x][y].clicked:
                clicked_mines.append(tiles[x][y])

    return active_mines, clicked_mines
def makeMatrix(Size: int):
    for x in range(Size):
        tmp_listX = []
        for y in range(Size):
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                color = green
            else:
                color = darkgreen
            tmp_listX.append(tile(x, y, (DISPLAY[0])/Size, color))
        tiles.append(tmp_listX)
def getColor(tile: tile):
    x = tile.xIndex
    y = tile.yIndex
    if not tile.clicked:
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
            color = green
        else:
            color = darkgreen
    else:
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
            color = brown
        else:
            color = darkbrown
    return color


def generateBombs(amount, clickedX, clickedY):
    nums = []
    for i in range(amount):
        
        num1 = random.randint(0, len(tiles)-1)
        num2 = random.randint(0, len(tiles)-1)
        sumNum = f"{num1};{num2}"
        while sumNum in nums or sumNum == f"{clickedX};{clickedY}":
            num1 = random.randint(0, len(tiles)-1)
            num2 = random.randint(0, len(tiles)-1)
            sumNum = f"{num1};{num2}"
        nums.append(sumNum)


    for number in nums:
        x = int(number.split(';')[0])
        y = int(number.split(';')[1])
        tiles[x][y].isMine = True

    for x in range(len(tiles)):
        for y in range(len(tiles)):
            tiles[x][y].setNumber()

    

def updateUI():
    pygame.draw.rect(win, bggreen, (0, Y-(Y-X), X, Y-X))
    win.blit(FLAGICON, (X/2-(Y-X)/2, Y-(Y-X)/1.5))
    FO = pygame.font.Font('freesansbold.ttf', UITEXTSIZE)
    win.blit(FO.render(str(flags), True, white), (X/2, Y-(Y-X)/1.5))

    # num = pygame.font.Font('freesansbold.ttf', int(self.size/1.25)).render(str(self.number), True, self.getNumberColor())
    # win.blit(num,(self.xPos + self.size/3.4, self.yPos + self.size/6))

def main():
    pass

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption('MineSweeper')
    makeMatrix(SIZE)
    run = True
    for x in tiles:
        for y in range(len(tiles)):
            x[y].draw()
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not mouseOverTile.clicked and not mouseOverTile.flagged:
                        mouseOverTile.onClick()
                if event.button == 2:
                    showAll()
                if event.button == 3:
                    if not mouseOverTile.flagged:
                        mouseOverTile.flagged = True
                        flags -= 1
                        
                    else:
                        mouseOverTile.flagged = False
                        flags += 1
                    mouseOverTile.draw()
       


        mouseX, mouseY = pygame.mouse.get_pos()
        size = tiles[0][0].size
        
        x = int(mouseX/size)
        y = int(mouseY/size)
        
        
        try:
            mouseOverTile = tiles[x][y]
            mouseOnTiles = True
        except IndexError:
            mouseOnTiles = False
        if lastTile != mouseOverTile:
            
            try:
                color = getColor(lastTile)
                mouseOverTile.color = (mouseOverTile.color[0]+20, mouseOverTile.color[1]+20, mouseOverTile.color[2]+20)
                lastTile.color = color
                lastTile.draw()
                mouseOverTile.draw()
            except AttributeError:
                pass
            
        lastTile = mouseOverTile
        updateUI()
        pygame.display.update()
        clock.tick(60)

        
            


    