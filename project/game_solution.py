#resolution: 1280x720

#importing modules
import tkinter as tk
from tkinter import *
from random import *
import subprocess
from tkinter import font

def twinkling_stars():
    colours = ["white", "#ffffed", "#fefefe", "#dfdfdf", "#f5f5f5", "#fffafa", "#f8f8ff", "#f0ffff"]
    for i, s in enumerate(star):    #looping through all stars to change their color and size to give a twinkling-effect
        starColour = colours[randint(0, 7)]
        size = randint(1, 2)
        canvasStart.itemconfig(s, fill=starColour, outline=starColour)
        canvasStart.coords(s, starsCoords[i][0], starsCoords[i][1], starsCoords[i][0] + size, starsCoords[i][1] + size)
    start.after(700, twinkling_stars)


def onClick():  
    with open("data.txt", "a") as file:
        file.write(e.get()+" ")

    #destroying the widgets present on the screen to give the loading effect
    username.destroy()
    e.destroy()
    startButton.destroy()

    loading=tk.Label(canvasStart, text="Loading...", background="black", fg="white", font=("Georgia", 22))
    width_loading=loading.winfo_reqwidth()
    height_loading=loading.winfo_reqheight()
    centerX_loading=(1280-width_loading)/2
    centerY_loading=(720-height_loading)/2
    canvasStart.create_window(centerX_loading, centerY_loading, window=loading, anchor=NW)

    canvasStart.after(1500, start.withdraw) #removing the current window from the screen
    canvasStart.after(1500, lambda: subprocess.run(["python", "gameplay.py"])) #opening the gameplay window

#creating the homepage window
start=tk.Tk()
start.resizable(width=False, height=False)
start.title("Alien Aviator")
start.iconbitmap("favicon.ico")
canvasStart=Canvas(start, width=1280, height=720)
canvasStart.pack()
canvasStart.config(background="black")

#creating stars on the canvas for the background
star=[]
starsCoords = []
c = ["white", "#fefefe", "#dfdfdf", "#f5f5f5", "#fffafa", "#f8f8ff", "#f0ffff"]

for i in range(500):
    x = randint(1,1279)
    y = randint(1,719)
    size = randint(1,2)
    colour = randint(0,6)
    xy = (x, y, x+size, y+size)
    star.append(canvasStart.create_oval(xy, fill=c[colour], outline=c[colour]))
    starsCoords.append((x, y))
    
twinkling_stars()

#adding images to the background
try:
    ufo_image = PhotoImage(file="ufo.png")
    canvasStart.create_image(395, 380, image=ufo_image)
    left_image = PhotoImage(file="left.png")
    canvasStart.create_image(130, 300, image=left_image)
    right_image = PhotoImage(file="right.png")
    canvasStart.create_image(1150, 350, image=right_image)
except TclError as error:
    print("Error loading the image: ", error)

#creating a custom font for the title
font.nametofont("TkDefaultFont").configure(size=16)
customFont2=font.Font(family="Rubik Moonrocks Regular", size=70)

#creating a label for the title "Alien Aviator" and placing it at the specified coordinates 
title=tk.Label(start, text="Alien Aviator", background="black", fg="white", font=customFont2)
width_title=title.winfo_reqwidth()
centerX_title=(1280-width_title)/2
canvasStart.create_window(centerX_title, 120, window=title, anchor=NW)

#creating a label and an entry for username input
username=tk.Label(start, text="Username: ", background="black", fg="white", font=("Georgia", 18))
e=tk.Entry(start,width=25, font=("Georgia",14), bg="black", borderwidth=2.5, fg="#cfd3d2")
#getting the width and height of username label and entry
width_username=username.winfo_reqwidth()
height_username=username.winfo_reqheight()
width_e=e.winfo_reqwidth()
height_e=e.winfo_reqheight()
#calculating the center positions for the username label and entry
centerX_username=(1280-width_username-width_e)/2
centerY_username=(720-height_username+100)/2
centerX_e=centerX_username+(width_e/2)-30
centerY_e=(720-height_username+100)/2
#creating a window for the username label and entry
canvasStart.create_window(centerX_username, centerY_username, window=username, anchor=NW)
canvasStart.create_window(centerX_e, centerY_e, window=e, anchor=NW)

#creating a custom font for the start button
font.nametofont("TkDefaultFont").configure(size=16)
customFont=font.Font(family="Black Ops One Regular", size=24)
#creating the start button, getting the width of the widget, and placing it at the specified coordinates
startButton=Button(start, text="START", font=(customFont), bg="black", fg="#cfd3d2", bd=3.5, padx=15, command=onClick)
startButton.pack()
width_startButton=startButton.winfo_reqwidth()
height_startButton=startButton.winfo_reqheight()
centerX_startButton=(1280-width_startButton)/2
centerY_startButton=centerY_e+height_e+30
canvasStart.create_window(centerX_startButton, centerY_startButton, window=startButton, anchor=NW)


start.mainloop()