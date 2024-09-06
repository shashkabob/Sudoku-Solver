import csv
import sqlite3
#from splitJoin import *

connection = sqlite3.connect('database.sqlite')
cursor = connection.cursor()

with open('SudokuData.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    puzzles = []
    for line in reader:
        puzzles.append(line)

puzzles = puzzles[2:]
easy = puzzles[0:10]
medium = puzzles[10:20]
hard = puzzles[20: 30]

def createPuzzles():
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
        print("Puzzles has already been created")
        return

def createEasy():
    try:
        cursor.execute('''
            CREATE TABLE Easy (
                ID int NOT NULL,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        print("Easy has already been created")
        return

def createMedium():
    try:
        cursor.execute('''
            CREATE TABLE Medium (
                ID int NOT NULL,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        print("Medium has already been created")
        return

def createHard():
    try:
        cursor.execute('''
            CREATE TABLE Hard (
                ID int NOT NULL,
                Data STRING
            )
        ''')
        connection.commit()
    except sqlite3.OperationalError:
        print("Hard has already been created")
        return

def addPuzzles():
    for puzzle in puzzles:
        id = int(puzzle[0])
        level = str(puzzle[1])
        data = str(puzzle[2])
        cursor.execute(f'''
            INSERT INTO Puzzles (ID, Level, Data) 
            VALUES ('{id}', '{level}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def addEasy():
    for puzzle in easy:
        id = int(puzzle[0])
        data = str(puzzle[2])
        cursor.execute(f'''
            INSERT INTO Easy (ID, Data) 
            VALUES ('{id}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def addMedium():
    for puzzle in medium:
        id = int(puzzle[0])
        data = str(puzzle[2])
        cursor.execute(f'''
            INSERT INTO Medium (ID, Data) 
            VALUES ('{id}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def addHard():
    for puzzle in hard:
        id = int(puzzle[0])
        data = str(puzzle[2])
        cursor.execute(f'''
            INSERT INTO Hard (ID, Data) 
            VALUES ('{id}', '${data}');
        ''')
        connection.commit()
    cursor.close()
    connection.close()

def easyDiff():
    try:
        cursor.execute(f'''
        SELECT Data FROM 'Easy' 
        ORDER BY RANDOM()
        LIMIT 1
        ''')
    except sqlite3.OperationalError:
        print("Error occurred selecting data")
        return
    data = cursor.fetchall()
    string = str(data)[4:85]
    split(string)

def mediumDiff():
    try:
        cursor.execute(f'''
        SELECT Data FROM 'Medium' 
        ORDER BY RANDOM()
        LIMIT 1
        ''')
    except sqlite3.OperationalError:
        print("Error occurred selecting data")
        return
    data = cursor.fetchall()
    string = str(data)[4:85]
    split(string)

def hardDiff():
    try:
        cursor.execute(f'''
        SELECT Data FROM 'Hard' 
        ORDER BY RANDOM()
        LIMIT 1
        ''')
    except sqlite3.OperationalError:
        print("Error occurred selecting data")
        return
    data = cursor.fetchall()
    string = str(data)[4:85]
    split(string)


