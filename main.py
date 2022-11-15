from utils import *
import pandas as pd
from math import floor

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Drawing Program")

def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid

def draw_grid(win, grid):
    # Gives the element (row) and index of the element (i)
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        # Because our count starts at 0, we need to add one more line and column so
        # we have lines in the end of each row and column
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))

        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))

BUTTON_HEIGHT = 50

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - BUTTON_HEIGHT/2

buttons = [
    Button(10, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, BLACK),
    Button(70, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, RED),
    Button(130, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, GREEN),
    Button(190, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, BLUE),
    Button(250, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Erase", BLACK),
    Button(310, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Clear", BLACK),
    Button(370, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Import", BLACK),
    Button(430, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Denoise", BLACK),
    Button(490, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Expand", BLACK),
]

def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)
    for button in buttons:
        button.draw(win)
    pygame.display.update()



def get_row_col_from_pos(pos):
    
    x,y = pos

    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    
    return row, col

# Exports whatever is in the grid to excel file
def export_data(grid, old_df):
    vetor = []
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if grid[i][j] != WHITE:
                vetor.append(1)
            else:
                vetor.append(0)

    df = pd.DataFrame(vetor).T

    old_df = pd.concat([old_df, df])

    try:
        old_df.to_excel(r'C:\Users\Caio\Downloads\_test.xlsx', index=False)
    except PermissionError:
        print('Deu Ruim')

    return old_df

# imports and turns excel file into grid
def import_data():
    loaded = pd.read_excel(r'C:\Users\Caio\Downloads\_test.xlsx')
    grid_loaded = []
    for i in range(0,ROWS):
        grid_loaded.append([])
        for j in range(0, COLS):
            if loaded.iloc[0][(i*COLS)+j] == 1:
                grid_loaded[i].append(BLACK)
            else:
                grid_loaded[i].append(WHITE)

    return grid_loaded



run = True

clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)

data_frame = pd.DataFrame()

drawing_color = BLACK

class ImageData:
    def __init__(self):
        self.min_y = 49
        self.min_x = 49
        self.max_y = 0
        self.max_x = 0
    
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
        print('Max X: '+ str(self.max_x) + '  Min X: '+ str(self.min_x) + '  Max Y: '+ str(self.max_y) + '  Min Y: '+ str(self.min_y))
    

# Function to remove lost pixels in the grid
def clear_grid(grid):
    found = False
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            for k in range (-2,3):
                for l in range (-2,3):
                    if k == 0 and l == 0:
                        continue

                    index_row = i + k

                    index_col = j + l

                    # if any of the indexes are negative
                    if index_row < 0 or index_col < 0:
                        # go for the next step
                        continue

                    # if any of the indexes are greater than the grid size
                    if index_row >= ROWS or index_col >= COLS:
                        # go for the next step
                        continue

                    if grid[index_row][index_col] != WHITE:
                        found = True
                        break
                
                # If found a neighbour pixel, then move on to the next pixel
                if found == True:
                    break

            # If found a neighbour pixel, then move on to the next pixel
            if found == True:
                found = False
            # Otherwise (there are no neighbour pixels)
            elif grid[i][j] != WHITE:
                # Clear current pixel
                grid[i][j] = WHITE
                print('Erasing pixel '+ str(i)+' '+str(j))
    
    return grid

# Align letter to top left
def align_top_left(grid, image_data: ImageData):
    
    top_grid = []
    left_grid = []

    print(image_data.getMinY())

    y_size = image_data.getMaxY()+1
    x_size = image_data.getMaxX()+1

    run = False

    # If image is not aligned to the top
    if image_data.getMinY() > 0:
        for i, row in enumerate(grid):
            top_grid.append([])
            for j, pixel in enumerate(row):
                if (image_data.getMinY() + i) < y_size:
                    top_grid[i].append(grid[image_data.getMinY()+i][j])
                    image_data.setMaxY(i)
                else:
                    top_grid[i].append(WHITE)
        image_data.setMinY(0)

        run = True
        

    # If image is not aligned to the left
    if image_data.getMinX() > 0:
        for i, row in enumerate(grid):
            left_grid.append([])
            for j, pixel in enumerate(row):
                if (image_data.getMinX() + j) < x_size:
                    left_grid[i].append(top_grid[i][image_data.getMinX()+j])
                    image_data.setMaxX(j)
                    #print('Resizing X: ' + str(j))
                    #image_data.printMaxMin()
                else:
                    left_grid[i].append(WHITE)
        image_data.setMinX(0)

        run = True

    if run:
        return left_grid, image_data
    else:
        return grid, image_data

def expandMagic(grid, image_data: ImageData):

    image_data.printMaxMin()

    factor = ROWS / (image_data.getMaxY() - image_data.getMinY() + 1)

    expand_array = []

    #for i in range(1, image_data.getMaxY(), 1/factor):
    #    if round(i*factor) < 49:
    #        expand_array.append(round(i*factor))
    #    else:
    #        break

    do_loop = True
    step = 1/factor
    iteration = 0;

    print('step: ' + str(step))

    while(do_loop):
        expand_array.append(floor(iteration*step))
        if (iteration >= 50):
            do_loop = False

        iteration += 1

    print('Expand array len: ' + str(len(expand_array)))

    print('Expand Array: ')
    print(expand_array)

    duplicate_top = []

    for i, row in enumerate(grid):
        duplicate_top.append([])
        for j, pixel in enumerate(row):
            if i >= len(expand_array):
                duplicate_top[i].append(grid[i][j])
                continue
            duplicate_top[i].append(grid[expand_array[i]][j])

    print('Fator: ' + str(factor))

    return duplicate_top, image_data

def expandMagicCols(grid, image_data: ImageData):

    image_data.printMaxMin()

    factor = COLS / (image_data.getMaxX() - image_data.getMinX() + 1)

    expand_array = []

    #for i in range(1, image_data.getMaxY(), 1/factor):
    #    if round(i*factor) < 49:
    #        expand_array.append(round(i*factor))
    #    else:
    #        break

    do_loop = True
    step = 1/factor
    iteration = 0;

    print('step: ' + str(step))

    while(do_loop):
        expand_array.append(floor(iteration*step))
        if (iteration >= 50):
            do_loop = False

        iteration += 1

    print('Expand array len: ' + str(len(expand_array)))

    print('Expand Array: ')
    print(expand_array)

    duplicate_top = []

    for i, row in enumerate(grid):
        duplicate_top.append([])
        for j, pixel in enumerate(row):
            if i >= len(expand_array):
                duplicate_top[i].append(grid[i][j])
                continue
            duplicate_top[i].append(grid[i][expand_array[j]])

    print('Fator: ' + str(factor))

    return duplicate_top, image_data

image_data = ImageData()

expand_ran = False

while run:
    
    # From pygame, limit the FPS
    clock.tick(FPS)

    # Get events
    for event in pygame.event.get():
        
        # If user clicked the "x" in the window
        if event.type == pygame.QUIT:
            run = False

        # If left click pressed
        if pygame.mouse.get_pressed()[LEFT_CLICK]:

            # Get the click position
            pos = pygame.mouse.get_pos()

            try:
                # Get the coordinates from click position (if coordinates out of grid, IndexError will be raised)
                row, col = get_row_col_from_pos(pos)

                # Set clicked pixel to the current drawing color
                grid[row][col] = drawing_color

                image_data.receiveNewXandY(col, row)

            # In the case that the click happenned outside grid
            except IndexError:

                # Look for a button press
                for button in buttons:

                    # If button was not clicked
                    if not button.clicked(pos):

                        # Continue loop
                        continue

                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        expand_ran = False
                        image_data = ImageData()
                    elif button.text == "Erase":
                        data_frame = export_data(grid, data_frame)
                        print(image_data.getMaxX(), image_data.getMaxY(), image_data.getMinX(), image_data.getMinY())
                    elif button.text == "Import":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        grid = import_data()
                    elif button.text == "Expand":
                        if not expand_ran:
                            expand_ran = True
                            grid, image_data = expandMagic(grid, image_data)
                            grid, image_data = expandMagicCols(grid, image_data)
                    elif button.text == "Denoise":
                        try:
                            grid = clear_grid(grid)
                            grid, image_data = align_top_left(grid, image_data)
                        except IndexError:
                            pass
                    else:
                        drawing_color = button.color

                    break


    draw(WIN, grid, buttons)
        
pygame.quit()