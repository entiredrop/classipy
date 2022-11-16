from utils import *
import pandas as pd
from math import floor
from sklearn.neural_network import MLPClassifier
import pickle

alphabet_obj = Alphabet()

mlp_clf = MLPClassifier()

def train_mlp():
    mlp_clf = MLPClassifier(hidden_layer_sizes=(600,400,200),
                        max_iter = 50000,activation = 'relu',
                        solver = 'adam')

    loaded = pd.read_excel(r'data\\train_dataset.xlsx')

    X_data = loaded
    X_data = X_data.drop(columns='Name')
    loaded.drop(loaded.iloc[:, 1:len(loaded.columns)], inplace=True, axis=1)

    print(loaded)

    mlp_clf.fit(X_data, loaded)

    return mlp_clf

alphabet_current_index = 0
alphabet_current_repetition = 0

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

prediction_button = \
    Button(490, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "???", BLACK)

buttons = [
    Button(10, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, BLACK),
    Button(70, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, RED),
    Button(130, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Load ML", BLACK),
    Button(190, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Predict", BLACK),
    Button(250, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Export", BLACK),
    Button(310, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Clear", BLACK),
    Button(370, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Import", BLACK),
    Button(430, button_y, BUTTON_HEIGHT, BUTTON_HEIGHT, WHITE, "Denoise", BLACK),
    prediction_button,
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

def create_array_to_predict(grid, button: Button, mlp_clf: MLPClassifier):
    array_to_export = []

    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if grid[i][j] != WHITE:
                array_to_export.append(1)
            else:
                array_to_export.append(0)

    df = pd.DataFrame(array_to_export).T

    pred = mlp_clf.predict(df)

    for i in pred:
        print('Neural: '+ alphabet_obj.get_letter_for_index(i))

        button.text = alphabet_obj.get_letter_for_index(i)


# Exports whatever is in the grid to excel file
def export_data(grid, old_df, alphabet_current_index, alphabet_current_repetition):
    array_to_export = []

    if alphabet_current_index >= ALPHABET_SIZE:
        return old_df

    array_to_export.append(alphabet_current_index)

    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if grid[i][j] != WHITE:
                array_to_export.append(1)
            else:
                array_to_export.append(0)

    df = pd.DataFrame(array_to_export).T

    old_df = pd.concat([old_df, df])

    alphabet_current_repetition += 1

    if alphabet_current_repetition >= ALPHABET_REPETITIONS:
        alphabet_current_index += 1
        alphabet_current_repetition = 0

    try:
        old_df.to_excel(r'data\\new_data.xlsx', index=False)
    except PermissionError:
        print('Deu Ruim')

    return old_df, alphabet_current_repetition, alphabet_current_index

# imports and turns excel file into grid
def import_data():
    loaded = pd.read_excel(r'C:\Caio\VSCode\Dataset\data_set_3.xlsx')
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

data_frame = pd.DataFrame()

drawing_color = BLACK
    

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
def align_top_left(image_data: ImageData):
    
    top_grid = []
    left_grid = []

    grid = image_data.getGrid()

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
        image_data.setGrid(left_grid)
        return image_data
    else:
        return image_data

def expandMagicRows(image_data: ImageData):

    image_data.printMaxMin()

    factor = ROWS / (image_data.getMaxY() - image_data.getMinY() + 1)

    if factor == 1:
        return image_data

    expand_array = []

    grid = image_data.getGrid()
    
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

    image_data.setGrid(duplicate_top)

    image_data.setMaxY(49)
    image_data.setMinY(0)

    print('Fator: ' + str(factor))

    return image_data

def expandMagicCols(image_data: ImageData):

    image_data.printMaxMin()

    factor = COLS / (image_data.getMaxX() - image_data.getMinX() + 1)

    expand_array = []

    if factor == 1:
        return image_data

    grid = image_data.getGrid()

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

    image_data.setGrid(duplicate_top)

    image_data.setMaxX(49)
    image_data.setMinX(0)

    print('Fator: ' + str(factor))

    return image_data

# Perform pre-processing
def condition_grid_to_process(image_data: ImageData):

    image_data = align_top_left(image_data)
    image_data = expandMagicRows(image_data)
    image_data = expandMagicCols(image_data)

    return image_data

image_data = ImageData()
image_data.setGrid(init_grid(ROWS, COLS, BG_COLOR))

expand_ran = False
button_clicked = False
predicted = False
while run:
    
    # From pygame, limit the FPS
    clock.tick(120)

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
                image_data.setPixelColor(row, col, drawing_color)

                image_data.receiveNewXandY(col, row)

            # In the case that the click happenned outside grid
            except IndexError:

                # Look for a button press
                for button in buttons:

                    # If button was not clicked
                    if not button.clicked(pos):
                        button_clicked = False
                        # Continue loop
                        continue
                    
                    if button_clicked:
                        continue

                    button_clicked = True

                    if button.text == "Clear":
                        if alphabet_current_index < ALPHABET_SIZE:
                            print('Write the letter ' + alphabet_obj.get_letter_for_index(alphabet_current_index))

                        image_data = ImageData()
                        image_data.setGrid(init_grid(ROWS, COLS, BG_COLOR))
                        expand_ran = False
                        predicted = False

                    elif button.text == "Export":
                        if not expand_ran:
                            expand_ran = True
                            image_data.setGrid(clear_grid(image_data.getGrid()))
                            image_data = condition_grid_to_process(image_data)
                            data_frame, alphabet_current_repetition, alphabet_current_index = export_data(image_data.getGrid(), data_frame, alphabet_current_index, alphabet_current_repetition)
                        print(image_data.getMaxX(), image_data.getMaxY(), image_data.getMinX(), image_data.getMinY())
                    elif button.text == "Import":
                        image_data.setGrid(init_grid(ROWS, COLS, BG_COLOR))
                        image_data.setGrid(import_data())
                    elif button.text == "Expand":
                        if not expand_ran:
                            expand_ran = True
                            mlp_clf = train_mlp()
                    elif button.text == "Predict":
                        if not predicted:
                            predicted = True
                            image_data = condition_grid_to_process(image_data)
                            create_array_to_predict(image_data.getGrid(), prediction_button, mlp_clf)

                    elif button.text == "Load ML":
                        filename = 'data\\ml_model.sav'
                        mlp_clf = pickle.load(open(filename, 'rb'))
                    elif button.text == "Denoise":
                        try:
                            #image_data.setGrid(clear_grid(image_data.getGrid()))
                            #image_data = align_top_left(image_data)
                            mlp_clf = train_mlp()
                            filename = 'data\\ml_model.sav'
                            pickle.dump(mlp_clf, open(filename, 'wb'))
                            print('Network trained!')
                        except IndexError:
                            pass
                    else:
                        drawing_color = button.color

                    break


    draw(WIN, image_data.getGrid(), buttons)
        
pygame.quit()