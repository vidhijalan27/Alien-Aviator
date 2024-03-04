import tkinter as tk
from tkinter import *
from random import *
import subprocess
from tkinter import font

def onClick():  
    with open("data.txt", "a") as file:
        file.write(e.get()+" ")

    username.destroy()
    e.destroy()
    startButton.destroy()

    loading=tk.Label(canvasStart, text="Loading...", background="black", fg="white", font=("Georgia", 22))
    width_loading=loading.winfo_reqwidth()
    height_loading=loading.winfo_reqheight()
    centerX_loading=(1280-width_loading)/2
    centerY_loading=(720-height_loading)/2
    canvasStart.create_window(centerX_loading, centerY_loading, window=loading, anchor=NW)

    canvasStart.after(1500, start.withdraw)
    canvasStart.after(1500, lambda: subprocess.run(["python", "gameplay.py"]))

start=tk.Tk()
start.resizable(width=False, height=False)
start.title("Alien Aviator")
start.iconbitmap(r"C:\Users\Vidhi Jalan\Downloads\favicon.ico")
canvasStart=Canvas(start, width=1280, height=720)
canvasStart.pack()
canvasStart.config(background="black")



username=tk.Label(start, text="Username: ", background="black", fg="white", font=("Georgia", 18))
e=tk.Entry(start,width=25, font=("Georgia",14), bg="black", borderwidth=2.5, fg="#cfd3d2")

width_username=username.winfo_reqwidth()
height_username=username.winfo_reqheight()

width_e=e.winfo_reqwidth()
height_e=e.winfo_reqheight()

centerX_username=(1280-width_username-width_e)/2
centerY_username=(720-height_username+100)/2
canvasStart.create_window(centerX_username, centerY_username, window=username, anchor=NW)

centerX_e=centerX_username+(width_e/2)-30
centerY_e=(720-height_username+100)/2
canvasStart.create_window(centerX_e, centerY_e, window=e, anchor=NW)


font.nametofont("TkDefaultFont").configure(size=16)
customFont=font.Font(family="Black Ops One Regular", size=24)

startButton=Button(start, text="START", font=(customFont), bg="black", fg="#cfd3d2", bd=3.5, padx=15, command=onClick)
startButton.pack()
width_startButton=startButton.winfo_reqwidth()
height_startButton=startButton.winfo_reqheight()
centerX_startButton=(1280-width_startButton)/2
centerY_startButton=centerY_e+height_e+30
canvasStart.create_window(centerX_startButton, centerY_startButton, window=startButton, anchor=NW)


start.mainloop()