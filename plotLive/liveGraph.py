import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


class liveGraph:

    def __init__(self, Input=1, TkinterScale=False,Ylimits=[0,10]):
        """

        :param float Input: Input that gets passed to graph as Y value on new point
        :param bool TkinterScale: chooses to create and render a tk scale object to override/test input
        :param list Ylimits: The range of values of the graphs Y axis or
        """
        self.In = Input
        self.TkTrue = TkinterScale

        if self.TkTrue == True:
            self.window = tk.Tk()
            self.window.geometry("300x50")

            self.window.rowconfigure([0, 1, 2, 3], minsize=25)
            self.window.columnconfigure([0, 1, 2], minsize=100)


            scaleVal = tk.DoubleVar()
            self.scaleVal = scaleVal
            scale = tk.Scale(from_=Ylimits[0], to=Ylimits[1], orient=tk.HORIZONTAL, length=300, resolution=.1, variable=scaleVal)

            scale.pack()

        x = np.linspace(0, Ylimits[1], 200)

        fig, ax = plt.subplots()

        ys = [0] * 200

        # 200 empty list entry's?

        (ln,) = ax.plot(x, ys, animated=True)

        ax.set_ylim(Ylimits[0],Ylimits[1])

        plt.show(block=False)
        plt.pause(0.1)
        bg = fig.canvas.copy_from_bbox(fig.bbox)
        ax.draw_artist(ln)
        fig.canvas.blit(fig.bbox)

        self.figTup = fig, ax
        self.ys = ys
        self.ln = ln
        self.bg = bg

    def update(self, Input=None):
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
        # adding the input value to the list of Y positions
        # TODO: add Serial input function
        #       or when passing str to input just Read from SM
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports

        ys = ys[len(ys) - 200:]
        ln.set_ydata(ys)

        # setting the graphs position and removing old values

        fig.canvas.restore_region(bg)
        ax.draw_artist(ln)
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()

        # bliting the canvas of the graph matplotlib docs:
        # https://matplotlib.org/stable/tutorials/advanced/blitting.html#sphx-glr-tutorials-advanced-blitting-py
