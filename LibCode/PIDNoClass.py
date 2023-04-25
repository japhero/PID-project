import math
import time
from plotLive import liveGraph
import tkinter as tk



window = tk.Tk()
window.geometry("300x50")

window.rowconfigure([0, 1, 2, 3], minsize=25)
window.columnconfigure([0, 1, 2], minsize=100)


scaleVal = tk.DoubleVar()
scaleVal = scaleVal
scale = tk.Scale(from_ =0, to=100, orient=tk.HORIZONTAL, length=300, resolution=.1, variable=scaleVal)

scale.pack()

graph = liveGraph(Ylimits=[0,100],TkinterScale=False)

kp = .5
ki = .02
kd = .02
prevPoint =0
input = 0
setPoint = 50
output = 0
integral =0
lastError =0
dt =.01

val=0

scaleVal.set(50)


for val in range(1,4):
    setPoint = 50
    # if val == 1:
    #     setPoint = 50
    # elif val == 2:
    #     setPoint = 20
    # elif val == 3:
    #     setPoint = 80
    while True:
        window.update()

        time.sleep(.01)

        #print(f'KP: {(kp * (setPoint - input))} = {kp}* {setPoint} - {input}')
        print(f"{output} {setPoint} ")

        output += (kp * (setPoint - input))
        integral += (setPoint - input) * time.process_time()
        output += (ki * integral)
        output += kd * ((setPoint - input) - lastError / time.process_time())



        lastError = setPoint - input
        input += output
        graph.update(input)
        pass



