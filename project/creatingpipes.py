import tkinter as Tk
from tkinter import *
from random import *

frameSpeed=10
score=-1
alienX=200
alienY=200
pipeX=1280
pipeHole=290
flag, paused=False, False
ctr=0
endObstacle, endBestScore, endScore = None, None, None
cheatcode=""
bosscode=""


window=Tk()
window.resizable(width=False, height=False)
window.title("Alien Aviator")
window.iconbitmap(r"C:\Users\Vidhi Jalan\Downloads\favicon.ico")
canvas=Canvas(window, width=1280, height=720)
canvas.pack()
canvas.config(background="black")



star=[]
starsCoords=[]
c=["white", "#fefefe", "#dfdfdf", "#f5f5f5", "#fffafa", "#f8f8ff", "#f0ffff"]

for i in range(500):
    x=randint(1,1279)
    y=randint(1,719)
    size=randint(1,2)
    colour=randint(0,6)
    xy=(x, y, x+size, y+size)
    star.append(canvas.create_oval(xy, fill=c[colour], outline=c[colour]))
    starsCoords.append((x, y))

def twinkling_stars():
    colours = ["white", "#ffffed", "#fefefe", "#dfdfdf", "#f5f5f5", "#fffafa", "#f8f8ff", "#f0ffff"]
    for i, s in enumerate(star):  # Loop through all stars to change their color and size
        starColour = colours[randint(0, 7)]
        size = randint(1, 2)
        canvas.itemconfig(s, fill=starColour, outline=starColour)
        canvas.coords(s, starsCoords[i][0], starsCoords[i][1], starsCoords[i][0] + size, starsCoords[i][1] + size)
    window.after(700, twinkling_stars)
    
twinkling_stars()


try:
    alien_image=PhotoImage(file=r"C:\Users\Vidhi Jalan\Downloads\alien.png")
    alien=canvas.create_image(250, alienY, image=alien_image)
except TclError as error:
    print("Error loading the image:", error)

pipeUp=canvas.create_rectangle(pipeX, 0, pipeX + 120, pipeHole, fill="#73c2fb", outline="#74BF2E")
pipeDown=canvas.create_rectangle(pipeX, pipeHole + 250, pipeX + 120, 700, fill="#73c2fb", outline="#74BF2E")
scoreScreen=canvas.create_text(30, 50, text="0", font=("Impact", 50), fill="#cfd3d2", anchor=W)


def createPipeHole():
    global pipeHole, score, frameSpeed
    score=score+1
    canvas.itemconfig(scoreScreen, text="Score: "+str(score))
    pipeHole=randint(100, 500)
    if(score+1%6==0 and score!=0):
        frameSpeed=frameSpeed-1
    elif(score==0):
        frameSpeed=10


def movingPipe():
    global pipeX, pipeHole, flag
    if not flag and not paused:
        pipeX=pipeX-5
        canvas.coords(pipeUp, pipeX, 0, pipeX+120, pipeHole)
        canvas.coords(pipeDown, pipeX, pipeHole+200, pipeX+120, 720)

        if(pipeX<-120):
            pipeX=1280
            createPipeHole()
        window.after(frameSpeed, movingPipe)

createPipeHole()
window.after(frameSpeed, movingPipe)
window.mainloop()