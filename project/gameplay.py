#resolution: 1280x720

#importing modules
import tkinter as Tk
from tkinter import *
from random import *
import subprocess
from tkinter import font

#declaring variables
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

#creating the gameplay window
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

#displaying the alien image on the canvas
try:
    alien_image=PhotoImage(file=r"C:\Users\Vidhi Jalan\Downloads\alien.png")
    alien=canvas.create_image(250, alienY, image=alien_image)
except TclError as error:
    print("Error loading the image:", error)

#creating the pipes
pipeUp=canvas.create_rectangle(pipeX, 0, pipeX + 120, pipeHole, fill="#73c2fb", outline="#74BF2E")
pipeDown=canvas.create_rectangle(pipeX, pipeHole + 250, pipeX + 120, 700, fill="#73c2fb", outline="#74BF2E")
scoreScreen=canvas.create_text(30, 50, text="0", font=("Impact", 50), fill="#cfd3d2", anchor=W)

#creating a label to prompt users to press space to start playing
font.nametofont("TkDefaultFont").configure(size=16)
customFont=font.Font(family="Black Ops One Regular", size=28)
pressSpace=Label(window, text="PRESS SPACE TO PLAY", bg="black", fg="white", font=customFont)
width_pressSpace=pressSpace.winfo_reqwidth()
centerX_pressSpace=(1280-width_pressSpace)/2
canvas.create_window(centerX_pressSpace, 350, window=pressSpace, anchor=NW)
window.after(1750, pressSpace.destroy)    #destroying the label after a certain time


def createPipeHole():
    global pipeHole, score, frameSpeed
    #incrementing the score and updating it on the canvas
    score=score+1
    canvas.itemconfig(scoreScreen, text="Score: "+str(score))
    pipeHole=randint(100, 500)   #randomizing the pipe hole position
    if(score+1%6==0 and score!=0):
        frameSpeed=frameSpeed-1
    elif(score==0):
        frameSpeed=10


def movingPipe():
    global pipeX, pipeHole, flag
    #moving the pipe horizontally across the canvas
    if not flag and not paused:
        pipeX=pipeX-5
        canvas.coords(pipeUp, pipeX, 0, pipeX+120, pipeHole)
        canvas.coords(pipeDown, pipeX, pipeHole+200, pipeX+120, 720)
        #resetting the pipe position once it moves out of the canvas
        if(pipeX<-120):
            pipeX=1280
            createPipeHole()   #creating a new pipe hole position
        window.after(frameSpeed, movingPipe)   #recursive call to continue moving the pipe


def movingUp(event=None):
    global alienY, ctr, flag
    #moving the alien upwards if the game is active and not paused
    if not flag and not paused:
        alienY=alienY-10
        if(alienY<=40):   #ensuring that the alien stays within the bounds of the canvas
            alienY=40
        canvas.coords(alien, 250, alienY)   #updating the alien's position on the canvas
        #controlling the speed of the upward movement by recursively calling itself
        if(ctr<4):
            ctr=ctr+1
            window.after(frameSpeed, movingUp)
        else:
            ctr=0


def movingDown():
    global alienY, flag
    #moving the alien downwards if the game is active and not paused
    if not flag and not paused:
        alienY=alienY+3
        if(alienY>=(650)):   #ensuring that the alien stays within the bounds of the canvas
            alienY=650
        canvas.coords(alien, 250, alienY)   #updating the alien's position on the canvas
        window.after(frameSpeed, movingDown)   #recursive call for continuous movement


def collision():
    global flag
    #check for collision between the alien and the pipe
    if((pipeX<320 and pipeX+120>=128) and (alienY<pipeHole+40 or alienY>pipeHole+160)):
        flag=True
        #getting the score and adding it to the data.txt file when collision occurs
        with open("data.txt", "a") as file:
            file.write(str(score)+"\n")
        canvas.after(500, window.withdraw)   #when collision occurs, the game is over. therefore, removing the gameplay window from the screen
        canvas.after(500, lambda: subprocess.run(["python", "gameOver.py"]))    #opening the gameover window
    #if no collision occurs, schedule the collision check again after a frame
    if not flag:
        window.after(frameSpeed, collision)


def onClickingSpace(event):
    if(event.keysym=="space"):
        onPause()

def onPause():
    global paused, alienY, pipeX
    paused = not paused
    #unbind cheatcode keys when paused
    window.unbind("<Down>")
    window.unbind("<Left>")
    window.unbind("<Right>")
    #resume game movements when unpaused
    if not paused:
        movingDown()
        movingPipe()
        window.bind("<Down>", cheatCodesAdd)
        window.bind("<Left>", cheatCodesMultiply)
        window.bind("<Right>", cheatCodesMultiply)   

onPause()
movingDown()

#creating a pause button on the canvas
pause=PhotoImage(file=r"C:\Users\Vidhi Jalan\Downloads\pause.png")
pauseButton= Button(window, image=pause, bd=0, bg="black", command=onPause)
canvas.create_window(1200, 20, anchor=NE, window=pauseButton)


def save(event):
    global score, alienX, alienY, pipeX, pipeHole
    with open("state.txt", "w") as fl:
        fl.write(f"{score},{alienX},{alienY},{pipeX},{pipeHole}")
    with open("data.txt", "a") as file:
        file.write(str(score)+"\n")
    canvas.after(500, window.withdraw)   #when the game is saved, removing the gameplay window from the screen
    canvas.after(500, lambda: subprocess.run(["python", "gameOver.py"]))    #opening the gameover window
    

def load(event):
    global score, alienX, alienY, pipeX, pipeHole
    with open("state.txt", "r") as file:
        data = file.readline().split(",")
        score = int(data[0])
        alienX = int(data[1])
        alienY = int(data[2])
        pipeX = int(data[3])
        pipeHole = int(data[4])
        subprocess.run(["python", "gameplay.py"])

def cheatCodesAdd(event):
    global cheatcode
    #appending "D" to cheatcode if the "Down" key is pressed
    if(event.keysym=="Down"):
        cheatcode+="D"
    onActivation()

def cheatCodesMultiply(event):
    global cheatcode
    #appending "L" if "Left" key is pressed and "R" if "Right" key is pressed
    if(event.keysym=="Left"):
        cheatcode+="L"
    elif(event.keysym=="Right"):
        cheatcode+="R"
    onActivation()


def onActivation():
    global cheatcode, bosscode, score
    #checking if cheatcode ends with specific strings and taking actions accordingly
    if(cheatcode.endswith("DDD")):
        score+=5
        cheatcode=""
    elif(cheatcode.endswith("LRLR")):
        score*=2
        cheatcode=""
    #updating the score display on the canvas
    canvas.itemconfig(scoreScreen, text="Score: "+str(score))
    

def bossKey(event=None):
    global canvasend, canvas, paused, spreadsheet, bg
    paused=True    #pausing the game
    #creating a canvas to display the spreadsheet
    canvasend=Canvas(window, width=1280, height=720)
    canvas.create_window(640, 360, anchor=CENTER, window=canvasend)
    spreadsheet=PhotoImage(file=r"C:\Users\Vidhi Jalan\Desktop\project\work.gif")
    bg=canvasend.create_image(640, 360, anchor=CENTER, image=spreadsheet)
    canvasend.tkraise(canvasend._name)   
    #unbinding keys to prevent any actions while boss key is active
    window.unbind("<space>")
    window.unbind("<Down>")
    window.unbind("<Left>")
    window.unbind("<Right>")


    def exitt(event='None'):
        global paused, canvasend
        paused=False    #resuming the game upon exiting the boss key screen
        canvasend.destroy()
        #rebinding keys for game functionality
        window.bind("<space>", onClickingSpace)
        window.bind("<Down>", cheatCodesAdd)
        window.bind("<Left>", cheatCodesMultiply)
        window.bind("<Right>", cheatCodesMultiply)   
    window.bind("<Escape>", exitt)

     
createPipeHole()
window.after(frameSpeed, movingDown)
window.after(frameSpeed, movingPipe)
window.after(frameSpeed, collision)
#key binds
window.bind("<Up>", movingUp)
window.bind("<space>", onClickingSpace)
window.bind("<Down>", cheatCodesAdd)
window.bind("<Left>", cheatCodesMultiply)
window.bind("<Right>", cheatCodesMultiply)
window.bind("<Insert>", bossKey)
window.bind("<s>", save)
window.bind("<l>", load)
window.mainloop()