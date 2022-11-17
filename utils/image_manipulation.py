from .settings import *
from .imagedata import *
from math import floor

class ImageManipulation:

    def __init__(self) -> None:
        pass

    def expandMagicRows(image_data: ImageData):

        image_data.printMaxMin()

        # Calculate factor by which the image must be resized
        factor = ROWS / (image_data.getMaxY() - image_data.getMinY() + 1)

        # If image do not need to be resized
        if factor == 1:

            # Finish
            return image_data

        # Calculate step (if step = 0.5, then line 0 will appear twice since it has to count two steps until increase to another line)
        step = 1/factor
        debug_msg('step: ' + str(step))

        '''
        Suppose a image like this:
        [ 0  0  0  0  0
          1  0  0  0  1 -> Image starts at row 1
          0  1  1  1  0 -> Image ends at row 2
          0  0  0  0  0
        ]

        But the grid has 4 rows, 

        The expansion array will be: (contains data of the old grid expanded to new grid)
        [
            1  -> Put row 1 from the old grid in row 0 of the new grid 
            1  -> Put row 1 from the old grid in row 1 of the new grid
            2  -> Put row 2 from the old grid in row 2 of the new grid
            2  -> Put row 2 from the old grid in row 3 of the new grid
        ]

        The expanded image will be:
        [ 1  0  0  0  1 -> Image starts at row 0
          1  0  0  0  1
          0  1  1  1  0
          0  1  1  1  0 -> Image ends at row 3
        ]
        '''
        
        # Create expansion array
        expansion_array = []

        # Indicates current grid row
        new_row = 0

        # Create new array with the lines that must be populated
        while(new_row <= ROWS):
            expansion_array.append(floor(new_row*step))
            new_row += 1

        # New grid that wil be populated
        duplicate_top = []

        # Load old grid
        grid = image_data.getGrid()

        # Populate new grid with information from the old grid
        for i, row in enumerate(grid):
            duplicate_top.append([])
            for j, pixel in enumerate(row):
                if i >= len(expansion_array):
                    duplicate_top[i].append(grid[i][j])
                    continue
                duplicate_top[i].append(grid[expansion_array[i]][j])

        # Set current working grid to new expanded one
        image_data.setGrid(duplicate_top)

        # Set new boundaries
        image_data.setMaxY(49)
        image_data.setMinY(0)

        debug_msg('Fator: ' + str(factor))

        return image_data

    def expandMagicCols(image_data: ImageData):

        image_data.printMaxMin()

        # Calculate factor by which the image must be resized
        factor = COLS / (image_data.getMaxX() - image_data.getMinX() + 1)

        # If image do not need to be resized
        if factor == 1:

            # Finish
            return image_data

        # Calculate step (if step = 0.5, then line 0 will appear twice since it has to count two steps until increase to another line)
        step = 1/factor
        debug_msg('step: ' + str(step))

        '''
        Suppose a image like this:
        [ 0  1  0  0
          0  0  1  0
          0  1  0  0
          0  0  1  0
             |  |-> Image ends at column 2
             |-> Image starts at column 1
        ]

        But the grid has 4 columns, 

        The expansion array will be: (contains data of the old grid expanded to new grid)
        [
            1  -> Put column 1 from the old grid in column 0 of the new grid 
            1  -> Put column 1 from the old grid in column 1 of the new grid
            2  -> Put column 2 from the old grid in column 2 of the new grid
            2  -> Put column 2 from the old grid in column 3 of the new grid
        ]

        The expanded image will be:
        [ 1  1  0  0
          0  0  1  1
          1  1  0  0
          0  0  1  1
          |        |-> Image ends at column 3
          |-> Image starts at column 0
        ]
        '''
        
        # Create expansion array
        expansion_array = []

        # Indicates current grid row
        new_row = 0

        # Create new array with the lines that must be populated
        while(new_row <= COLS):
            expansion_array.append(floor(new_row*step))
            new_row += 1

        # New grid that wil be populated
        duplicate_top = []

        # Load old grid
        grid = image_data.getGrid()

        # Populate new grid with information from the old grid
        for i, row in enumerate(grid):
            duplicate_top.append([])
            for j, pixel in enumerate(row):
                if i >= len(expansion_array):
                    duplicate_top[i].append(grid[i][j])
                    continue
                duplicate_top[i].append(grid[i][expansion_array[j]])

        # Set current working grid to new expanded one
        image_data.setGrid(duplicate_top)

        # Set new boundaries
        image_data.setMaxX(49)
        image_data.setMinX(0)

        debug_msg('Fator: ' + str(factor))

        return image_data

    # Aligns image to top left
    def align_top_left(image_data: ImageData):
        
        top_grid = []
        left_grid = []

        grid = image_data.getGrid()

        # Because both X and Y start at 0 and ends in 49, the size needs to be added 1
        y_size = image_data.getMaxY()+1
        x_size = image_data.getMaxX()+1

        # If image is not aligned to the top
        if image_data.getMinY() > 0:
            for i, row in enumerate(grid):
                top_grid.append([])
                for j, pixel in enumerate(row):
                    # If inside old grid
                    if (image_data.getMinY() + i) < y_size:
                        # Copy what`s needed
                        top_grid[i].append(grid[image_data.getMinY()+i][j])
                        image_data.setMaxY(i)
                    # If out of boundaries of old grid
                    else:
                        # Complete the remaining with white spots
                        top_grid[i].append(WHITE)
            
            image_data.setGrid(top_grid)
            image_data.setMinY(0)
            

        # If image is not aligned to the left
        if image_data.getMinX() > 0:
            for i, row in enumerate(grid):
                left_grid.append([])
                for j, pixel in enumerate(row):
                    if (image_data.getMinX() + j) < x_size:
                        left_grid[i].append(top_grid[i][image_data.getMinX()+j])
                        image_data.setMaxX(j)
                    else:
                        left_grid[i].append(WHITE)
            image_data.setGrid(left_grid)
            image_data.setMinX(0)

        return image_data