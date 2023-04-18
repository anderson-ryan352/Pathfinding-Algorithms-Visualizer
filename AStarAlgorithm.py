import math
import pygame
import button
from queue import PriorityQueue


WIN_WIDTH = 800
WIN = pygame.display.set_mode((WIN_WIDTH+200, WIN_WIDTH))
pygame.display.set_caption("A* Algorithm")

#Tile Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
LAPIS = (48, 103, 158)
DBLUE = (38, 132, 255)

aStarDiagonalButtonImg = pygame.image.load('res/aStarDiag.png').convert_alpha()
aStarNonDiagonalButtonImg = pygame.image.load('res/aStarNonDiag.png').convert_alpha()


class Tile:
    def __init__(self, row, col, width, totalRows):
        self.width = width
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = LAPIS
        self.totalRows = totalRows
        self.neighbors = []

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #Getters and Setters
    def setStart(self):
        self.color = BLUE

    def isStart(self):
        return self.color == BLUE
    
    def setEnd(self):
        self.color = PURPLE

    def isEnd(self):
        return self.color == PURPLE

    def setWall(self):
        self.color = BLACK

    def isWall(self):
        return self.color == BLACK

    def setOpen(self):
        self.color = ORANGE

    def isOpen(self):
        return self.color == ORANGE

    def setClosed(self):
        self.color=GRAY

    def isClosed(self):
        return self.color == GRAY

    def getPos(self):
        return self.row,self.col

    def setPath(self):
        self.color = GREEN

    def reset(self):
        self.color = LAPIS

    #Checking neighbors and appending if neighbor tile is not a border tile/a wall
    def updateNeighbors(self, grid, allowDiagonal):
        self.neighbors = []

        #Top check
        if (self.row > 0    #Not a top border tile
                and not grid[self.row-1][self.col].isWall()):   #[-1][0] isn't a wall
            self.neighbors.append(grid[self.row-1][self.col])   #Add target to neighbors

        #Bottom check
        if (self.row<self.totalRows-1   #Not a bottom border tile
                and not grid[self.row+1][self.col].isWall()):   #[+1][0] isn't a wall
            self.neighbors.append(grid[self.row+1][self.col])  #Add target to neighbors

        #Left check
        if (self.col > 0    #Not a left border tile
                and not grid[self.row][self.col-1].isWall()):   #[0][-1] isn't a wall
            self.neighbors.append(grid[self.row][self.col-1])   #Add target to neighbors

        #Right check
        if (self.col < self.totalRows-1  #Not a right border tile
                and not grid[self.row][self.col+1].isWall()):   #[0][+1] isn't a wall
            self.neighbors.append(grid[self.row][self.col+1])   #Add target to neighbors

        if allowDiagonal:
            #Top left check
            if (self.row > 0    #Not a top border tile
                    and self.col > 0    #Not a left border tile
                    and not grid[self.row-1][self.col-1].isWall()): #[-1][-1] isn't a wall
                self.neighbors.append(grid[self.row-1][self.col-1]) #Add target to neighbors

            #Top right check
            if (self.col < self.totalRows-1 #Not a right border tile
                    and self.row > 0    #Not a top border tile
                    and not grid[self.row-1][self.col+1].isWall()): #[-1][+1] isn't a wall
                self.neighbors.append(grid[self.row-1][self.col+1]) #Add target to neighbors

            #Bottom right check
            if (self.row < self.totalRows -1    #Not a bottom border tile
                    and self.col < self.totalRows-1     #Not a right border tile
                    and not grid[self.row+1][self.col+1].isWall()): #[+1][+1] isn't a wall
                self.neighbors.append(grid[self.row+1][self.col+1]) #Add target to neighbors

            #Bottom left check
            if (self.col > 0    #Not a left border tile
                    and self.row < self.totalRows-1     #Not a right border tile
                    and not grid[self.row+1][self.col-1].isWall()):   #[+1][-1] isn't a wall
                self.neighbors.append(grid[self.row+1][self.col-1]) #Add target to neighbors



def newGrid(rows, width):
    grid = []
    gap = width//rows
    for x in range(rows):
        grid.append([])
        for y in range(rows):
            tile = Tile(x, y, gap, rows)
            grid[x].append(tile)
    return grid


def drawWindow(win, grid, rows, width, buttons):
    win.fill(LAPIS)

    for row in grid:
        for tile in row:
            tile.draw(win)
    drawGridLines(win, rows, width)
    for button in buttons:
        button.draw(win)
    pygame.display.update()


def drawGridLines(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, DBLUE, (0, i*gap), (width, i*gap), width=2)
    for j in range(rows):
        pygame.draw.line(win, DBLUE, (j*gap, 0), (j*gap, width), width=2)


def getClickPos(pos, rows, width):
    gap = width//rows
    y,x = pos
    row = y//gap
    col = x//gap

    return row, col


def algorithm(draw, grid, start, end):
    openSet = PriorityQueue()
    count = 0
    openSet.put((0, count, start))
    cameFrom = {}

    gScore = {tile: float("inf") for row in grid for tile in row}
    gScore[start] = 0
    fScore = {tile: float("inf") for row in grid for tile in row}
    fScore[start] = heuristic(start.getPos(), end.getPos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                #Pressing space or return during algorithm will end pathfinding
                if (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                    return None
            
        curTile = openSet.get()[2]
        openSetHash.remove(curTile)

        if curTile == end:
            genPath(cameFrom, end, draw)
            end.setEnd()
            start.setStart()
            return True
        for neighbor in curTile.neighbors:
            tempGScore = gScore[curTile] + 1
                
            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = curTile
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + heuristic(neighbor.getPos(), end.getPos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.setOpen()
        draw()
        if curTile!=start:
            curTile.setClosed()
    return False


#Calculates absolute distance between two points using their coordinates
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1-x2) + abs(y1-y2)


def genPath(cameFrom, curTile, draw):
    while curTile in cameFrom:
        curTile = cameFrom[curTile]
        curTile.setPath()
        draw()

def validBoundsCheck(row, col, totalRows):
    if (row >= totalRows or row < 0 
        or col >= totalRows or col < 0):
        return False
    return True

def main(win, width):
    rows = 40
    grid = newGrid(rows, width)

    start = None
    end = None
    isRunning = True

    aStarDiagonalButton = button.Button(850, 100, aStarDiagonalButtonImg)
    aStarNonDiagonalButton = button.Button(850, 200, aStarNonDiagonalButtonImg)

    UIButtons = [aStarDiagonalButton,
                aStarNonDiagonalButton]


    while isRunning:

        drawWindow(win, grid, rows, width, UIButtons)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            #Setting Start, End, and Wall tiles
            if pygame.mouse.get_pressed()[0]:#Left Click
                pos = pygame.mouse.get_pos()
                row, col = getClickPos(pos, rows, width)
                if validBoundsCheck(row, col, rows):
                    tile = grid[row][col]
                    if not start and tile != end:
                        start = tile
                        start.setStart()
                    elif not end and tile != start:
                        end = tile
                        end.setEnd()
                    elif tile != start and tile != end:
                        tile.setWall()
                elif(aStarDiagonalButton.isActivated()
                      and start and end):
                    for row in grid:
                        for tile in row:
                            tile.updateNeighbors(grid, True)
                    algorithm(lambda: drawWindow(win, grid, rows, width, UIButtons), grid, start, end)
                elif(aStarNonDiagonalButton.isActivated()
                        and start and end):
                    for row in grid:
                        for tile in row:
                            tile.updateNeighbors(grid, False)
                    algorithm(lambda: drawWindow(win, grid, rows, width, UIButtons), grid, start, end)
                

            #Deleting tiles
            if pygame.mouse.get_pressed()[2]:#Right Click
                pos = pygame.mouse.get_pos()
                row, col = getClickPos(pos, rows, width)
                if validBoundsCheck(row, col, rows):
                    tile = grid[row][col]
                    tile.reset()
                    if tile == start:
                        start = None
                    elif tile == end:
                        end = None
            if event.type == pygame.KEYDOWN:
                #Reset entire grid with Backspace
                if event.key == pygame.K_BACKSPACE:
                    grid = newGrid(rows, width)
                    start = None
                    end = None

    pygame.quit()
main(WIN, WIN_WIDTH)

