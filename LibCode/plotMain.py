import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk



class plotLive:

    def __init__(self, Input=1, Interval=100, TkinterScale = False):
        self.In = Input
        self.Interval = Interval
        self.TkTrue = TkinterScale

        if self.TkTrue == True:
            window = tk.Tk()
            window.geometry("300x50")

            window.rowconfigure([0, 1, 2, 3], minsize=25)
            window.columnconfigure([0, 1, 2], minsize=100)
            self.window = window

            scaleVal = tk.DoubleVar()
            self.scaleVal = scaleVal
            scale = tk.Scale(from_=0, to=10, orient=tk.HORIZONTAL, length=300, resolution=.1, variable=scaleVal)

            scale.pack()

        x = np.linspace(0, 10, 200)

        fig, ax = plt.subplots()

        ys = [0] * 200

        # 200 empty list entry's?

        (ln,) = ax.plot(x, ys, animated=True)

        ax.set_ylim([0, 10])

        plt.show(block=False)
        plt.pause(0.1)
        bg = fig.canvas.copy_from_bbox(fig.bbox)
        ax.draw_artist(ln)
        fig.canvas.blit(fig.bbox)

        self.figTup = fig, ax
        self.ys = ys
        self.ln = ln
        self.bg = bg

    def update(self, Input= None):
        self.In = Input
        fig = self.figTup[0]
        ax = self.figTup[1]
        ys = self.ys
        ln = self.ln
        bg = self.bg

        # Ik i can refactor every self val but i dont want to :)
        # because i can just copy and paste my old code

        if self.TkTrue == True:
            scaleVal = self.scaleVal
            window = self.window
            ys.append(float(scaleVal.get()))
            window.update()
            window.update_idletasks()
        else:
            ys.append(self.In)

        # TODO: add Serial input function
        #       or when passing str to input just Read from SM
        fig.canvas.restore_region(bg)
        ys = ys[len(ys) - 200:]

        ln.set_ydata(ys)

        ax.draw_artist(ln)
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()




obj = plotLive(TkinterScale=True)


while True:
    obj.update()
