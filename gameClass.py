import pygame
import sys

from settings import *
from buttonClass import *
from database import *
from main import *


# -------------------------------------------------------------------------------------------------
# Game Class
# -------------------------------------------------------------------------------------------------

class Game():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT)) # Pygame window
        self.running = True
        self.grid = grid # default grid
        self.splitString = [] # variables for split
        self.newGrid = []  # variables for split
        self.selected = None # indicates if cell is selected
        self.mousePosition = None # returns position of mouse
        self.state = "playing" # default state
        self.finished = False
        self.cellChanged = False
        self.playingButtons = [] # list that holds all buttons for playing state
        self.lockedCells = [] # list that holds all locked cells
        self.incorrectCells = [] # list that holds all incorrectly played cells
        self.font = pygame.font.SysFont("arial", cellSize // 2) # font to be used
        self.load() # initialises the game
        self.puzzles() # creates a fresh new board every time

    def run(self):
        # the game loop
        while self.running == True:
            if self.state == "playing":
                # calls the following functions which allows gameplay to work
                self.playingEvents()
                self.playingUpdate()
                self.playingDraw()
        # when game is no longer running
        pygame.quit()
        sys.exit()

# -------------------------------------------------------------------------------------------------
# Playing State Functions
# -------------------------------------------------------------------------------------------------

    def playingEvents(self):
        # contains code which is in charge of general user gameplay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # if the user clicks the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = (selected)  # returns position of mouse
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            # indicates that mouse is hovering over button
                            button.click()

            # if the user types a key
            if event.type == pygame.KEYDOWN:
                if self.selected != None and list(self.selected) not in self.lockedCells:
                    if self.checkInt(event.unicode):
                        # changes the cell
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        # indexes are in the self.selected attribute
                        self.cellChanged = True

    def playingUpdate(self):
        # contains code which updates the board during the user's gameplay
        self.mousePosition = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePosition)

        if self.cellChanged:
            # when a player makes a move
            self.incorrectCells = []
            if self.allCellsFilled():
                # checks if board is correct
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    print("Congratulations! \nYou've completed this sudoku!")

    def playingDraw(self):
        # contains which sets up the GUI
        self.window.fill(WHITE)

        # adding buttons
        for button in self.playingButtons:
            button.draw(self.window)

        # when the user selects
        if self.selected:
            self.drawSelection(self.window, self.selected)

        # shading cells
        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)

        # drawing the GUI
        self.drawNumbers(self.window)
        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

# -------------------------------------------------------------------------------------------------
# Board Checking Functions
# -------------------------------------------------------------------------------------------------

    def allCellsFilled(self):
        # used to check to see if all cells in the grid have been filled
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def checkAllCells(self):
        # used to check the grid
        self.checkRows()
        self.checkColumns()
        self.checkSubGrid()

    def checkRows(self):  # used to check each row
        for yindex, row in enumerate(self.grid):
            possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # the list of possible numbers that can be inputted
            for xindex in range(9):
                if self.grid[yindex][xindex] in possibleNumbers:
                    possibleNumbers.remove(self.grid[yindex][xindex])
                    # if a number already appears in the grid, it removes it from the list
                else:
                    if [xindex, yindex] not in self.lockedCells and [xindex, yindex] not in self.incorrectCells:
                        self.incorrectCells.append([xindex, yindex])
                        # if the user makes an incorrect move, it's added to the incorrectCells list
                    if [xindex, yindex] in self.lockedCells:
                        for i in range(9):
                            if self.grid[yindex][i] == self.grid[yindex][xindex]:
                                self.incorrectCells.append([i, yindex])
                                # if the user enters a locked cell, it's added to the incorrectCells list

    def checkColumns(self):  # used to check each column
        for xindex in range(9):
            possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # the list of possible numbers that can be inputted
            for yindex, row in enumerate(self.grid):
                if self.grid[yindex][xindex] in possibleNumbers:
                    possibleNumbers.remove(self.grid[yindex][xindex])
                    # if a number already appears in the grid, it removes it from the list
                else:
                    if [xindex, yindex] not in self.lockedCells and [xindex, yindex] not in self.incorrectCells:
                        self.incorrectCells.append([xindex, yindex])
                        # if the user makes an incorrect move, it's added to the incorrectCells list
                    if [xindex, yindex] in self.lockedCells:
                        for i, row in enumerate(self.grid):
                            if self.grid[i][xindex] == self.grid[yindex][xindex]:
                                self.incorrectCells.append([xindex, i])
                                # if the user enters a locked cell, it's added to the incorrectCells list

    def checkSubGrid(self):  # used to check each subgrid in the board
        for x in range(3):
            for y in range(3):
                possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                # the list of possible numbers that can be inputted
                for i in range(3):
                    for j in range(3):
                        # used to check each cell in each subgrid
                        xindex = x * 3 + i
                        yindex = y * 3 + j
                        if self.grid[yindex][xindex] in possibleNumbers:
                            possibleNumbers.remove(self.grid[yindex][xindex])
                            # if a number already appears in the grid, it removes it from the list
                        else:
                            if [xindex, yindex] not in self.incorrectCells and [xindex, yindex] not in self.lockedCells:
                                self.incorrectCells.append([xindex, yindex])
                                # if the user makes an incorrect move, it's added to the incorrectCells list
                            if [xindex, yindex] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xindex2 = (x * 3) + k
                                        yindex2 = (y * 3) + l
                                        if self.grid[yindex2][xindex2] == self.grid[yindex][xindex]:
                                            # extra measures caused by bug which wouldn't register some locked cells
                                            self.incorrectCells.append([xindex2, yindex2])
                                            # if the user enters a locked cell, it's added to the incorrectCells list

# -------------------------------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------------------------------

    def shadeIncorrectCells(self, window, incorrect):
        # draws a coloured square to indicate the cell is incorrect
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR, (
            cell[0] * cellSize + gridPosition[0], cell[1] * cellSize + gridPosition[1], cellSize, cellSize))

    def shadeLockedCells(self, window, locked):
        # draws a coloured square to indicate the cell is locked
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOUR, (
            cell[0] * cellSize + gridPosition[0], cell[1] * cellSize + gridPosition[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for yindex, row in enumerate(self.grid):  # for each row in the grid
            for xindex, num in enumerate(row):  # for each cell in each row
                if num != 0:  # while cell is not blank
                    position = [(xindex * cellSize) + gridPosition[0], (yindex * cellSize) + gridPosition[1]]
                    # draws the numbers in relation to position of grid on the window
                    self.textOnScreen(window, str(num), position)
                    # calls textOnScreen to output numbers

    def drawSelection(self, window, position):
        # draws a coloured square to indicate the cell has been selected
        pygame.draw.rect(window, TEAL, (
        (position[0] * cellSize) + gridPosition[0], (position[1] * cellSize) + gridPosition[1], cellSize, cellSize))

    def drawGrid(self, window):
        # draws border square
        pygame.draw.rect(window, BLACK, (gridPosition[0], gridPosition[1], WIDTH - 150, HEIGHT - 150), 2)
        for x in range(9):
            if x % 3 != 0:  # for every line it draws lines, thickness 1
                # vertical lines
                pygame.draw.line(window, BLACK, (gridPosition[0] + (x * cellSize), gridPosition[1]),
                                 (gridPosition[0] + (x * cellSize), gridPosition[1] + 450))
                # horizontal lines
                pygame.draw.line(window, BLACK, (gridPosition[0], gridPosition[1] + (x * cellSize)),
                                 (gridPosition[0] + 450, gridPosition[1] + +(x * cellSize)))
            else: # for every third line it draws lines, thickness 2
                # vertical lines
                pygame.draw.line(window, BLACK, (gridPosition[0] + (x * cellSize), gridPosition[1]),
                                 (gridPosition[0] + (x * cellSize), gridPosition[1] + 450), 2)
                # horizontal lines
                pygame.draw.line(window, BLACK, (gridPosition[0], gridPosition[1] + (x * cellSize)),
                                 (gridPosition[0] + 450, gridPosition[1] + +(x * cellSize)), 2)

    def mouseOnGrid(self):
        # if we click off the grid, it returns false
        if self.mousePosition[0] < gridPosition[0] or self.mousePosition[1] < gridPosition[1]:
            return False
        if self.mousePosition[0] > gridPosition[0] + gridSize or self.mousePosition[1] > gridPosition[1] + gridSize:
            return False

        # if we click on the grid, it returns the position of the mouse
        return (
        (self.mousePosition[0] - gridPosition[0]) // cellSize, (self.mousePosition[1] - gridPosition[1]) // cellSize)

    def loadButtons(self):
        # initialising buttons for the GUI
        self.playingButtons.append(Button(75, 40, WIDTH // 8, 40, function=self.checkAllCells, colour=(210, 140, 220),
                                          text="Check"))  # check button

        self.playingButtons.append(
            Button(170, 40, WIDTH // 8, 40, function=self.easyDiff, colour=(100, 230, 110),
                   text="Easy"))  # easy button

        self.playingButtons.append(
            Button(264, 40, WIDTH // 8, 40, function=self.mediumDiff, colour=(255, 180, 50),
                   text="Medium"))  # medium button

        self.playingButtons.append(
            Button(356, 40, WIDTH // 8, 40, function=self.hardDiff, colour=(240, 130, 130),
                   text="Hard"))  # hard button

        self.playingButtons.append(
            Button(450, 40, WIDTH // 8, 40, function=self.solver, colour=(110, 200, 250),
                   text="Solve"))  # solve button

    def textOnScreen(self, window, text, position):
        label = self.font.render(text, False, BLACK)
        fontWidth = label.get_width()  # gets the width of the label object
        fontHeight = label.get_height()  # gets the height of the label object
        position[0] += (cellSize - fontWidth) // 2  # finds the centre of the cell width
        position[1] += (cellSize - fontHeight) // 2  # finds the centre of the cell height
        window.blit(label, position)  # outputs onto screen

    def load(self):
        # contains code to setup a new game
        # sets lists empty to initialise board
        self.playingButtons = []
        self.loadButtons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finished = False

        # setting up locked cells from original board
        for yindex, row in enumerate(self.grid):
            for xindex, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xindex, yindex])

    def checkInt(self, string):
        # contains code to stop users passing in non-numeric values into cells
        try:
            int(string)  # tries to convert value in variable string into an integer
            return True
        except:
            return False  # if a non-numeric string is entered, it returns False and returns an error

    def changeGrid(self, puzzle):
        # contains code in charge of changing the grid
        self.grid = puzzle
        self.load()

    def split(self, var):
        # used by database functions to restore grid into 2D array format
        # sets lists empty each time to stop duplication of data
        self.splitString = []
        self.newGrid = []

        # appending numbers as 1-D array
        for char in range(len(var)):
            self.splitString.append(int(var[char]))
        # appending numbers as 2-D array
        for index in range(0, 81, 9):
            self.newGrid.append(self.splitString[index:index + 9])

# -------------------------------------------------------------------------------------------------
# Solver Functions
# -------------------------------------------------------------------------------------------------

    def updateSolved(self, window):
        # updating solved board
        self.drawNumbers(self.window)
        pygame.display.update()

    def possible(self, y, x, n):
        # checking to see if it's possible to solve the board
        for i in range(0, 9):
            if self.grid[y][i] == n:
                return False
        for i in range(0, 9):
            if self.grid[i][x] == n:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0 + i][x0 + j] == n:
                    return False
        return True

    def solver(self):
        for yindex, row in enumerate(self.grid):  # for each row in the grid
            for xindex, num in enumerate(row):  # for each cell in each row
                if self.grid[yindex][xindex] == 0:
                    for n in range(1, 10):  # counts to n-1, so 10 is never reached
                        if self.possible(yindex, xindex, n) and self.finished == False:
                            self.grid[yindex][xindex] = n
                            self.solver()  # recursion
                            self.grid[yindex][xindex] = 0  # backtrack if not possible so make space empty again
                    return

        # updating the solved board
        self.updateSolved(self.window)

        # freezing the screen and getting an input
        input("Enter to continue: ")

# -------------------------------------------------------------------------------------------------
# Database Functions - Accessing Tables
# -------------------------------------------------------------------------------------------------

    def easyDiff(self):
        try:
            # fetches a puzzle from easy table
            cursor.execute(f'''
            SELECT Data FROM 'Easy' 
            ORDER BY RANDOM()
            LIMIT 1
            ''')
        except sqlite3.OperationalError:
            print("Error occurred selecting data")
            return
        data = cursor.fetchall() # assigns this data to a variable
        string = str(data)[4:85] # gets the appropriate string
        self.split(string) # reverts it back into a 2D array
        self.changeGrid(self.newGrid)

    def mediumDiff(self):
        try:
            # fetches a puzzle from medium table
            cursor.execute(f'''
            SELECT Data FROM 'Medium' 
            ORDER BY RANDOM()
            LIMIT 1
            ''')
        except sqlite3.OperationalError:
            print("Error occurred selecting data")
            return
        data = cursor.fetchall()  # assigns this data to a variable
        string = str(data)[4:85]  # gets the appropriate string
        self.split(string)  # reverts it back into a 2D array
        self.changeGrid(self.newGrid)

    def hardDiff(self):
        try:
            # fetches a puzzle from hard table
            cursor.execute(f'''
            SELECT Data FROM 'Hard' 
            ORDER BY RANDOM()
            LIMIT 1
            ''')
        except sqlite3.OperationalError:
            print("Error occurred selecting data")
            return
        data = cursor.fetchall()  # assigns this data to a variable
        string = str(data)[4:85]  # gets the appropriate string
        self.split(string)  # reverts it back into a 2D array
        self.changeGrid(self.newGrid)

    def puzzles(self):
        try:
            # fetches a puzzle from Puzzles table
            cursor.execute(f'''
            SELECT Data FROM 'Puzzles' 
            ORDER BY RANDOM()
            LIMIT 1
            ''')
        except sqlite3.OperationalError:
            print("Error occurred selecting data")
            return
        data = cursor.fetchall()  # assigns this data to a variable
        string = str(data)[4:85]  # gets the appropriate string
        self.split(string)  # reverts it back into a 2D array
        self.changeGrid(self.newGrid)
