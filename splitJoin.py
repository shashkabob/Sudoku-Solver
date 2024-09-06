puzzle = [[0,0,0,0,0,0,0,0,0],
 [2,8,0,0,0,0,0,5,9],
 [4,0,9,0,0,0,1,0,3],
 [0,0,0,0,0,0,0,0,0],
 [0,0,0,1,2,0,7,0,8],
 [0,0,0,0,7,8,4,1,0],
 [0,0,6,5,0,0,0,3,0],
 [0,0,2,7,6,0,0,0,0],
 [7,0,1,4,0,0,0,0,0]]

string = "$540060078306180020092004500609000705710496000408003100000030900180000257950027000"
test = (string[1:])

def join():
    string = ""
    for listNumber in range(9):
        for index in range(9):
            string = string + str(puzzle[listNumber][index])
    print(string)


splitString = []
newPuzzle = []

def split(var):
    for char in range(len(var)):
        splitString.append(int(var[char]))

    for index in range(0,81,9):
        newPuzzle.append(splitString[index:index + 9])
    print(newPuzzle)

split(test)



