from .settings import *

class ImageData:
    def __init__(self):
        self.min_y = 49
        self.min_x = 49
        self.max_y = 0
        self.max_x = 0
        self.grid = []
    
    def setMinY(self, min_y):
        self.min_y = min_y

    def setMinX(self, min_x):
        self.min_x = min_x

    def setMaxY(self, max_y):
        self.max_y = max_y
        
    def setMaxX(self, max_x):
        self.max_x = max_x

    def receiveNewXandY(self, newX, newY):
        if newX > self.max_x:
            self.max_x = newX
        if newX < self.min_x:
            self.min_x = newX
        
        if newY > self.max_y:
            self.max_y = newY
        if newY < self.min_y:
            self.min_y = newY

    def getMinX(self):
        return self.min_x

    def getMinY(self):
        return self.min_y

    def getMaxX(self):
        return self.max_x

    def getMaxY(self):
        return self.max_y

    def printMaxMin(self):
        if True == DEBUG_ACTIVE:
            print('Max X: '+ str(self.max_x) + '  Min X: '+ str(self.min_x) + '  Max Y: '+ str(self.max_y) + '  Min Y: '+ str(self.min_y))

    def setGrid(self,grid):
        self.grid = grid

    def getGrid(self):
        return self.grid

    def setPixelColor(self, x, y, color):
        self.grid[x][y] = color
