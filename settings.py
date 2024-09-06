# colours used in program
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
TEAL = (174, 227, 245)
LOCKEDCELLCOLOUR = (245, 245, 245)
INCORRECTCELLCOLOUR = (255, 150, 150)

# default board
grid = [[0,0,0,0,0,0,0,0,0],
        [9,0,1,2,5,0,8,4,0],
        [0,4,7,3,8,0,2,9,0],
        [0,0,5,8,3,0,0,2,0],
        [4,0,2,0,0,0,6,0,0],
        [3,8,0,0,0,0,1,5,9],
        [6,1,0,9,7,3,0,0,0],
        [0,0,3,0,2,0,9,6,0],
        [0,2,9,4,0,0,0,0,0]]

# positions and sizes for creating the board
WIDTH = 600
HEIGHT = 600
gridPosition = (75, 100)  # the top left of the grid
cellSize = 50
gridSize = cellSize * 9

# join function joins numbers in a 2-D array format into a string
def join(string):
    string = ""
    for listNumber in range(9):
        for index in range(9):
            string = string + str(grid[listNumber][index])
    print(string)
    # used when adding numbers into csv file
