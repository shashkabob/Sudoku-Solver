import csv
import sqlite3
from settings import *

# establishing a connection to the database
connection = sqlite3.connect('database.sqlite')
cursor = connection.cursor()

# opening the csv file which stores the puzzles
with open('SudokuData.csv', 'r') as csvfile:
    # reading the csv file
    reader = csv.reader(csvfile)
    puzzles = []
    for line in reader:
        puzzles.append(line)

puzzles = puzzles[2:] # data for puzzles table
easy = puzzles[0:10] # data for easy table
medium = puzzles[10:20] # data for medium table
hard = puzzles[20: 30] # data for hard table

# -------------------------------------------------------------------------------------------------
# Database Functions - Creating Tables
# -------------------------------------------------------------------------------------------------

def createPuzzles():
    # creating the puzzles table
    try:
        cursor.execute('''
            CREATE TABLE Puzzles (
                ID int NOT NULL,
                Level STRING,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        # runs exception if table already exists
        print("Puzzles has already been created")
        return

def createEasy():
    # creating the easy table
    try:
        cursor.execute('''
            CREATE TABLE Easy (
                ID int NOT NULL,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        # runs exception if table already exists
        print("Easy has already been created")
        return

def createMedium():
    # creating the medium table
    try:
        cursor.execute('''
            CREATE TABLE Medium (
                ID int NOT NULL,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        # runs exception if table already exists
        print("Medium has already been created")
        return

def createHard():
    # creating the hard table
    try:
        cursor.execute('''
            CREATE TABLE Hard (
                ID int NOT NULL,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        # runs exception if table already exists
        print("Hard has already been created")
        return

# -------------------------------------------------------------------------------------------------
# Database Functions - Inserting Into Tables
# -------------------------------------------------------------------------------------------------

def addPuzzles():
    # adding data into the puzzles table
    for puzzle in puzzles:
        # setting values to insert
        id = int(puzzle[0])
        level = str(puzzle[1])
        data = str(puzzle[2])
        # executing command in SQl
        cursor.execute(f'''
            INSERT INTO Puzzles (ID, Level, Data) 
            VALUES ('{id}', '{level}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def addEasy():
    # dding data into the easy table
    for puzzle in easy:
        # setting values to insert
        id = int(puzzle[0])
        data = str(puzzle[2])
        # executing command in SQL
        cursor.execute(f'''
            INSERT INTO Easy (ID, Data) 
            VALUES ('{id}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def addMedium():
    # adding data into the medium table
    for puzzle in medium:
        # setting values to insert
        id = int(puzzle[0])
        data = str(puzzle[2])
        # executing command in SQL
        cursor.execute(f'''
            INSERT INTO Medium (ID, Data) 
            VALUES ('{id}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def addHard():
    # adding data into the hard table
    for puzzle in hard:
        # setting values to insert
        id = int(puzzle[0])
        data = str(puzzle[2])
        # executing command in SQL
        cursor.execute(f'''
            INSERT INTO Hard (ID, Data) 
            VALUES ('{id}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

