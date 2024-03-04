#resolution: 1280x720

#importing modules
import tkinter as Tk
from tkinter import *
from random import *
from tkinter import font
import subprocess


def twinkling_stars():
    colours = ["white", "#ffffed", "#fefefe", "#dfdfdf", "#f5f5f5", "#fffafa", "#f8f8ff", "#f0ffff"]
    for i, s in enumerate(star):  # Loop through all stars to change their color and size
        starColour = colours[randint(0, 7)]
        size = randint(1, 2)
        canvasOver.itemconfig(s, fill=starColour, outline=starColour)
        canvasOver.coords(s, starsCoords[i][0], starsCoords[i][1], starsCoords[i][0] + size, starsCoords[i][1] + size)
    over.after(700, twinkling_stars)


def displayText():
    #extracting and processing the data
    try:    
        with open("data.txt", "r") as file:
            lines = file.readlines()
            data = {}
            
            for line in lines:
                n, sc = line.strip().split(" ")
                sc = int(sc)
                if n in data:   #keeping track of the highest score for each player
                    data[n] = max(data[n], sc)
                else:
                    data[n] = sc

            #sorting scores in descending order and displaying the top 10 scores
            sortedScores = sorted(data.items(), key=lambda x: x[1], reverse=True)
            s=""
            ctr=0
            for n, sc in sortedScores:
                if(ctr<10):
                    s=s+f"{n}\t \t{sc}\n"
                ctr=ctr+1

            #configuring the label to display the leaderboard
            label.config(text=s)
            label.place(relx=0.4, rely=0.3, anchor=NW)

    except FileNotFoundError:
        label.config(text="File not Found")
        label.place(relx=0.5, rely=0.2, anchor=CENTER)


over=Tk()
over.resizable(width=False, height=False)
over.title("Alien Aviator")
over.iconbitmap(r"C:\Users\Vidhi Jalan\Downloads\favicon.ico")
canvasOver=Canvas(over, width=1280, height=720)
canvasOver.pack()
canvasOver.config(background="black")


star=[]
starsCoords=[]
c=["white", "#fefefe", "#dfdfdf", "#f5f5f5", "#fffafa", "#f8f8ff", "#f0ffff"]

for i in range(500):
    x=randint(1,1279)
    y=randint(1,719)
    size=randint(1,2)
    colour=randint(0,6)
    xy=(x, y, x+size, y+size)
    star.append(canvasOver.create_oval(xy, fill=c[colour], outline=c[colour]))
    starsCoords.append((x, y))
    
twinkling_stars()

#restart function
def onClick():
    canvasOver.after(500, over.withdraw)    #removing the gameover window from the screen
    canvasOver.after(500, lambda: subprocess.run(["python", "game_solution.py"]))    #opening the homepage window

font.nametofont("TkDefaultFont").configure(size=16)
customFont=font.Font(family="Emulogic", size=40)
#creating "GAME OVER" label and positioning it at the top
gameOver=Label(canvasOver, text="GAME OVER", background="black", fg="white", font=(customFont))
width_loading=gameOver.winfo_reqwidth()
height_loading=gameOver.winfo_reqheight()
centerX_loading=(1280-width_loading)/2
canvasOver.create_window(centerX_loading, 100, window=gameOver, anchor=NW)


label=Label(over, text="", bg="black", fg="white", font=("Georgia", 18))    #creating a label to display the scores
displayText()   #calling the function to display scores

customFont2=font.Font(family="Black Ops One Regular", size=18)

#creating the "HOME" button and centering it horizontally
home=Button(canvasOver, text="HOME", background="black", fg="white", font=customFont2, bd=3, padx=13, command=onClick)
width_home=home.winfo_reqwidth()
centerX_home=(1280-width_home)/2
canvasOver.create_window(centerX_home, 550, window=home, anchor=NW)


over.mainloop()