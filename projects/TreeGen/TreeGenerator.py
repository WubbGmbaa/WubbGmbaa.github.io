from turtle import *
from tkinter.colorchooser import askcolor
import tkinter
import string
import random
import threading
import logging
import sys
print("TreeGen by Bryan Gratz")
print("https://bryan.project.zone/projects/TreeGen/treegen.html\n")
print("This work is licensed under a Creative Commons\nAttribution-ShareAlike 4.0 International License")
print("http://creativecommons.org/licenses/by-sa/4.0/\n\n")
startingPenSize = 10
clcount = 0
turtleBale = [] #collective noun for a group of turtles
treeColor = ('#008800')
statusString = ""
interBranchAngle = 30
mainTurtle = Turtle()
mainTurtle.screen.clear()
mainTurtle.screen.title("TreeGen")
interBranchAngleSlider = 15
startingPenSizeSlider = 10
startCoordX = 0
startCoordY = -100
increment = 1
coordX = 0
coordY = -100
i = 0

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

def branchDraw(theTurtleInQuestion):
    
    global turtleBale
    global increment
    global interBranchAngle
    global i
    i = i + 1;
    #sys.stdout.write("\r" + str(i) + " branch segments generated")
    statusBar.config(text=str(i) + " branch segments generated")
    controlWindow.update_idletasks() #makes status bar message actually update. Side effect: tree is now visible while rendering, huzzah!
    #theTurtleInQuestion.pencolor(incrementHex(theTurtleInQuestion.pencolor(),increment)) #not yet debugged
    if theTurtleInQuestion.pensize() != 1:
        theTurtleInQuestion.pensize(theTurtleInQuestion.pensize()-1)
        randDirection = random.randint(1,2)
        if randDirection == 1:
            theTurtleInQuestion.left(interBranchAngle)
        elif randDirection == 2:
            theTurtleInQuestion.right(interBranchAngle)
        for justALoop in range(10):
            theTurtleInQuestion.forward(3)
            randClone = random.randint(1,15)
            if randClone == 1:
                turtleBale.append(theTurtleInQuestion.clone())
                branchDraw(turtleBale[-1])
        turtleBale.append(theTurtleInQuestion.clone())
        branchDraw(turtleBale[-1])
    #theTurtleInQuestion.reset() #disabled to fix "floating" branches
    theTurtleInQuestion.ht()
    #theTurtleInQuestion.screen.update() #not needed, since turtle pens already show once the tree is done. This is a useful bug.
    

def incrementHex(hex_str, increment): #with hex_str in format "#FFFFFF" or any colour
        red = int(hex_str[1:3],16) #specifies base for integer conversion
        green = int(hex_str[3:5],16)
        blue = int(hex_str[5:],16)
        red += increment #increment can be negative
        green += increment
        blue += increment
        new_hex_str = "#" + str(hex(red)) + str(hex(blue)) + str(hex(green))
        return new_hex_str

def treeThread():
    threading.Thread(target=startTree).start() #needs to be debugged

def startTree():
    global statusBar
    global treeColor
    global mainTurtle
    global i
    #randColor = "#"+("%06x"%random.randint(0,16777215))
    logging.info("Generating tree...")
    mainTurtle.screen.tracer(0, 0)
    mainTurtle.pu()
    mainTurtle.setheading(90)
    mainTurtle.setpos(startCoordX,startCoordY)
    mainTurtle.pencolor(treeColor)
    mainTurtle.pensize(startingPenSize)
    mainTurtle.speed(0)
    mainTurtle.pd()
    nextTurtle = mainTurtle.clone()
    branchDraw(nextTurtle)
    logging.info("Done.")
    i = 0
    statusBar.config(text="Ready.")

def canvasClear():
    global turtleBale
    global mainTurtle
    mainTurtle.screen.clear()
    turtleBale.clear()
    logging.debug("Canvas cleared.")

def getColor():
    global treeColor
    painColor = askcolor()
    treeColor = painColor[1]
    logging.debug("Tree color set to " + treeColor)

def setStartingPenSize(n):
    global startingPenSize
    startingPenSize = int(n)
    logging.debug("Tree size set to " + n)

def setScaleBranchAngle(n):
    global interBranchAngle
    interBranchAngle = int(n)
    logging.debug("Tree angle set to " + n)

def setCoordStart():
    global startCoordX
    global startCoordY
    startCoordX = coordXIn.get()
    startCoordY = coordYIn.get()
    logging.debug("Coordinates changed.")

controlWindow  = tkinter.Tk()
controlWindow.title("TreeGen")

clCountScale = tkinter.Scale(controlWindow, variable = startingPenSizeSlider, label="Size", length=300, from_=2, to=50, orient=tkinter.HORIZONTAL, command = setStartingPenSize)
clCountScale.set(10)
clCountScale.pack()
angleScale = tkinter.Scale(controlWindow, variable = interBranchAngleSlider, label="Branch Angle", length=300, from_=0, to=90, orient=tkinter.HORIZONTAL, command = setScaleBranchAngle)
angleScale.set(15)
angleScale.pack()

#coordsFrame = tkinter.Frame(controlWindow, width = 300)
#coordsFrame.pack()
#coordsLabel = tkinter.Label(coordsFrame, text="Starting Point")
#coordsLabel.pack(side = tkinter.LEFT)
#coordXLabel = tkinter.Label(coordsFrame, text="X:")
#coordXLabel.pack(side = tkinter.LEFT)
#coordXIn = tkinter.Spinbox(coordsFrame, width = 5)
#coordXIn.pack(side = tkinter.LEFT)
#coordYLabel = tkinter.Label(coordsFrame, text="Y:")
#coordYLabel.pack(side = tkinter.LEFT)
#coordYIn = tkinter.Spinbox(coordsFrame, width = 5)
#coordYIn.pack(side = tkinter.LEFT)
#coordSetButton = tkinter.Button(coordsFrame, text = "Set", command = setCoordStart)
#coordSetButton.pack(side = tkinter.LEFT)

bottomButtonContainer = tkinter.Frame(controlWindow,width = 300)
bottomButtonContainer.pack()
colorButton = tkinter.Button(bottomButtonContainer, text="Tree Color...", command = getColor)
colorButton.pack(side = tkinter.LEFT)
genButton = tkinter.Button(bottomButtonContainer, text="Generate!", command = startTree)
genButton.pack(side = tkinter.RIGHT)
clearButton = tkinter.Button(bottomButtonContainer, text="Clear Canvas", command = canvasClear)
clearButton.pack(side = tkinter.RIGHT)

statusBar=tkinter.Label(controlWindow, bd=1,relief=tkinter.SUNKEN, anchor=tkinter.W, textvariable=statusString)
statusBar.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH)
statusBar.config(text='Ready.')

controlWindow.mainloop()

