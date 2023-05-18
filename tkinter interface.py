import time
import tkinter as tk
import math

root = tk.Tk()
root.geometry("300x100")

scaleVal = tk.DoubleVar()
scale = tk.Scale(from_=-10, to=10, orient=tk.HORIZONTAL, length=300, resolution=1, variable=scaleVal)

scale.pack()

textVar = tk.Variable()
text = tk.Label(text="innit", textvariable=textVar)
text.pack()

mainList = ["PID on", " PID off", "setPoint"]
mainMenu = 1

PidState = False

setPoint =0



def setButtonVar(*args):
    global buttonVar, PidState, mainMenu,setPoint
    if int(scaleVal.get()) % 3 == 2 and ( mainMenu == 1 or mainMenu ==2):

        mainMenu =3

    else:
        if mainMenu == 3:
            mainMenu =2
            setPoint = abs(scaleVal.get())
        else:
            mainMenu =1

    print(mainMenu)


btnVar = tk.IntVar()
button = tk.Button(text="enter")
button.bind("<ButtonPress>", setButtonVar)

button.pack()

while True:
    if mainMenu == 1 or mainMenu ==2:
        textVar.set(mainList[int(scaleVal.get() % 3)])
    else:
        textVar.set(f"press to exit setpoint = {abs(scaleVal.get())}")
    print(setPoint)
    time.sleep(.01)
    root.update()
