import math
import pygame
import button
import tile
from queue import PriorityQueue


WIN_WIDTH = 800
WIN = pygame.display.set_mode((WIN_WIDTH+200, WIN_WIDTH+50))
pygame.display.set_caption("Algorithm Vizualization")


aStarDiagonalButtonImg = pygame.image.load('res/aStarDiag.png').convert_alpha()
aStarNonDiagonalButtonImg = pygame.image.load('res/aStarNonDiag.png').convert_alpha()
resetButtonImg = pygame.image.load('res/reset.png').convert_alpha()
clearSearchButtonImg = pygame.image.load('res/clearSearch.png').convert_alpha()
spaceInfoImg = pygame.image.load('res/spaceInfo.png').convert_alpha()

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



def newGrid(rows, width):
    grid = []
    gap = width//rows
    for x in range(rows):
        grid.append([])
        for y in range(rows):
            curTile = tile.Tile(x, y, gap, rows)
            grid[x].append(curTile)
    return grid


def drawWindow(win, grid, rows, width, buttons, UIText):
    win.fill(LAPIS)

    for row in grid:
        for square in row:
            square.draw(win)
    drawGridLines(win, rows, width)
    for button in buttons:
        button.draw(win)
    for text in UIText:
        win.blit(text, (400, 800))
    
    pygame.display.update()


def drawGridLines(win, rows, width):
    gap = width//rows
    for i in range(rows+1):
        pygame.draw.line(win, DBLUE, (0, i*gap), (width, i*gap), width=2)
    for j in range(rows+1):
        pygame.draw.line(win, DBLUE, (j*gap, 0), (j*gap, width), width=2)


def getClickPos(pos, rows, width):
    gap = width//rows
    y,x = pos
    row = y//gap
    col = x//gap

    return row, col


def aStarAlgorithm(draw, grid, start, end):
    openSet = PriorityQueue()
    count = 0
    openSet.put((0, count, start))
    cameFrom = {}

    gScore = {square: float("inf") for row in grid for square in row}
    gScore[start] = 0
    fScore = {square: float("inf") for row in grid for square in row}
    fScore[start] = heuristic(start.getPos(), end.getPos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                #Pressing space during algorithm will end pathfinding
                if (event.key == pygame.K_SPACE):
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

def clearSearch(grid):
    for row in grid:
        for square in row:
            if (square.color == ORANGE
                or square.color == GREEN
                or square.color == GRAY):
                square.color = LAPIS
    return grid




def main(win, width):
    rows = 40
    grid = newGrid(rows, width)

    start = None
    end = None
    isRunning = True

    aStarDiagonalButton = button.Button(850, 100, aStarDiagonalButtonImg)
    aStarNonDiagonalButton = button.Button(850, 200, aStarNonDiagonalButtonImg)
    resetButton = button.Button(850, 700, resetButtonImg)
    clearSearchButton = button.Button(850, 600, clearSearchButtonImg)

    UIButtons = [aStarDiagonalButton,
                aStarNonDiagonalButton,
                resetButton,
                clearSearchButton]
    

    UIText = [spaceInfoImg]


    while isRunning:

        drawWindow(win, grid, rows, width, UIButtons, UIText)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            #Setting Start, End, and Wall tiles
            if pygame.mouse.get_pressed()[0]:#Left Click
                pos = pygame.mouse.get_pos()
                row, col = getClickPos(pos, rows, width)
                if validBoundsCheck(row, col, rows):
                    curTile = grid[row][col]
                    if not start and curTile != end:
                        start = curTile
                        start.setStart()
                    elif not end and curTile != start:
                        end = curTile
                        end.setEnd()
                    elif curTile != start and curTile != end:
                        curTile.setWall()
                elif(aStarDiagonalButton.isActivated()
                      and start and end):
                    for row in grid:
                        for square in row:
                            square.updateNeighbors(grid, True)
                    aStarAlgorithm(lambda: drawWindow(win, grid, rows, width, UIButtons, UIText), grid, start, end)
                elif(aStarNonDiagonalButton.isActivated()
                        and start and end):
                    for row in grid:
                        for square in row:
                            square.updateNeighbors(grid, False)
                    aStarAlgorithm(lambda: drawWindow(win, grid, rows, width, UIButtons, UIText), grid, start, end)
                elif(resetButton.isActivated()):
                    grid = newGrid(rows, width)
                    start = None
                    end = None
                elif(clearSearchButton.isActivated()):
                    grid = clearSearch(grid)
                

            #Deleting tiles
            if pygame.mouse.get_pressed()[2]:#Right Click
                pos = pygame.mouse.get_pos()
                row, col = getClickPos(pos, rows, width)
                if validBoundsCheck(row, col, rows):
                    curTile = grid[row][col]
                    curTile.reset()
                    if curTile == start:
                        start = None
                    elif curTile == end:
                        end = None
            if event.type == pygame.KEYDOWN:
                #Reset entire grid with Backspace
                if event.key == pygame.K_BACKSPACE:
                    grid = newGrid(rows, width)
                    start = None
                    end = None

    pygame.quit()
main(WIN, WIN_WIDTH)

