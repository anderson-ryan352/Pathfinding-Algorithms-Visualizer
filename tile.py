import pygame

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
