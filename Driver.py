import tkinter as tk
from tkinter import *
import tkinter.font as tkFont

data = []
for x in range(9):
    row = []
    data.append(row)

def readInData(fileName):
    f = open(fileName, "r")
    for x in range(9):
        line = f.readline().strip()
        nums = line.split(" ")
        for z in range(9):
            data[x].append(int(nums[z]))

def makeString():
    myStr = ""
    for x in range(9):
        for z in range(9):
            myStr += str(data[x][z]) + " "
            if z == 2 or z == 5:
                myStr += "| "
        myStr+= "\n"
        if x == 2 or x == 5:
            myStr += "------------------\n"
    return myStr

def printy():
    print("ahh")

def getRow(rowNum):
    row = []
    for x in range(9):
        row.append(data[rowNum][x])
    return row

def getCol(colNum):
    col = []
    for x in range(9):
        col.append(data[x][colNum])
    return col

def getSquare(squareY, squareX):
    myList = []
    
    myList.append(data[0+squareY*3][0+squareX*3])
    myList.append(data[0+squareY*3][1+squareX*3])
    myList.append(data[0+squareY*3][2+squareX*3])
    myList.append(data[1+squareY*3][0+squareX*3])
    myList.append(data[1+squareY*3][1+squareX*3])
    myList.append(data[1+squareY*3][2+squareX*3])
    myList.append(data[2+squareY*3][0+squareX*3])
    myList.append(data[2+squareY*3][1+squareX*3])
    myList.append(data[2+squareY*3][2+squareX*3])

    return myList

def getRemainingOptions(posY, posX):
    if data[posY][posX] != 0:
        return []
    choices = [1,2,3,4,5,6,7,8,9]
    for x in getSquare(int(posY/3), int(posX/3)):
        if int(x) in choices:
            choices.remove(int(x))
    for x in getRow(posY):
        if int(x) in choices:
            choices.remove(int(x))
    for x in getCol(posX):
        if int(x) in choices:
            choices.remove(int(x))
    return choices

def fillGuaranteed(posY, posX):
    choices = getRemainingOptions(posY, posX)
    if len(choices) == 1:
        data[posY][posX] = choices[0]
        return True
    return False

window = tk.Tk()
board = tk.StringVar()

def fillAllGuaranteed():
    done = False
    for x in range(9):
        for y in range(9):
            if data[y][x] == 0:
                done = done or fillGuaranteed(y,x)
    board.set(makeString())
    return done

def soloOptionRow(rowNum):
    options = []
    for col in range(9):
        if data[rowNum][col] == 0:
            options.append(getRemainingOptions(rowNum, col))
    for y in range(len(options)):
        subList = options[y]
        unionList = []
        for x in range(len(options)):
            if x!=y:
                unionList = list(set(unionList + options[x]))
        soloList = list(set(subList) - set(unionList))
        if len(soloList) == 1:
            for colCounter in range(9):
                if int(soloList[0]) in getRemainingOptions(rowNum,colCounter):
                    data[rowNum][colCounter] = soloList[0]
                

def soloOptionCol(colNum):
    options = []
    for row in range(9):
        if data[row][colNum] == 0:
            options.append(getRemainingOptions(row, colNum))
    for y in range(len(options)):
        subList = options[y]
        unionList = []
        for x in range(len(options)):
            if x!=y:
                unionList = list(set(unionList + options[x]))
        soloList = list(set(subList) - set(unionList))
        if len(soloList) == 1:
            for rowCounter in range(9):
                if int(soloList[0]) in getRemainingOptions(rowCounter,colNum):
                    data[rowCounter][colNum] = soloList[0]

def soloOptionSquare(squareY, squareX):
    options = []
    for y in range(3):
        for x in range(3):
            if data[squareY*3 + y][squareX*3 + x] == 0:
                options.append(getRemainingOptions(squareY*3 + y, squareX*3 + x))
    
    for y in range(len(options)):
        subList = options[y]
        unionList = []
        for x in range(len(options)):
            if x!=y:
                unionList = list(set(unionList + options[x]))
        soloList = list(set(subList) - set(unionList))
        if len(soloList) == 1:
            for y in range(3):
                for x in range(3):
                    if int(soloList[0]) in getRemainingOptions(squareY*3 + y, squareX*3 + x):
                        data[squareY*3 + y][squareX*3 + x] = soloList[0]

readInData("hard.txt")

def setValue(row, column, val):
    if int(val) in getRemainingOptions(row, column):
        data[row][column] = val
        board.set(makeString())
        return True
    return False

def solveThePuzzle():

    for a in range(15):
        while fillAllGuaranteed():
            ao = 1
        
        for x in range(9):
            soloOptionCol(x)
            soloOptionRow(x)
        
        for y in range(3):
            for x in range(3):
                soloOptionSquare(y,x)
    
    board.set(makeString())
    
board.set(makeString())
fontObj = tkFont.Font(size=28)

myLabel = tk.Label(window, textvariable = board, font = fontObj)
solveButton = tk.Button(text = "Solve", command = solveThePuzzle)
solveButton.pack()

myLabel.pack()


window.mainloop()