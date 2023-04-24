import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


class liveGraph:

    def __init__(self, InputItems=[1], TkinterScale=False, Ylimits=[0, 10]):
        """

        :param float Input: Input that gets passed to graph as Y value on new point
        :param bool TkinterScale: chooses to create and render a tk scale object to override/test input
        :param list Ylimits: The range of values of the graphs Y axis or
        """
        self.TkTrue = TkinterScale

        if self.TkTrue == True:
            self.window = tk.Tk()
            self.window.geometry("300x50")

            self.window.rowconfigure([0, 1, 2, 3], minsize=25)
            self.window.columnconfigure([0, 1, 2], minsize=100)

            scaleVal = tk.DoubleVar()
            self.scaleVal = scaleVal
            scale = tk.Scale(from_=Ylimits[0], to=Ylimits[1], orient=tk.HORIZONTAL, length=300, resolution=.1,
                             variable=scaleVal)

            scale.pack()

        fig, ax = plt.subplots()

        lnNames = []

        for x in range(len(InputItems)):
            lnNames.append(f"line{x}")
        print(InputItems)

        xs = np.linspace(0, Ylimits[1], 200)
        # 200 empty list entry's?

        self.yValList = []
        for x in range(len(InputItems)):
            ys = [0] * 200
            self.yValList.append(ys)
        print(len(self.yValList))

        self.lineList = []

        for x in lnNames:
            x, = ax.plot(xs, ys, animated=True)
            self.lineList.append((x,))
        print(self.lineList)

        ax.set_ylim(Ylimits[0], Ylimits[1])

        plt.show(block=False)
        plt.pause(0.1)
        bg = fig.canvas.copy_from_bbox(fig.bbox)

        for x in self.lineList:
            ax.draw_artist(x[0])

        fig.canvas.blit(fig.bbox)

        self.figTup = fig, ax
        self.ys = ys
        self.bg = bg

    def update(self, Input=None):
        fig = self.figTup[0]
        ax = self.figTup[1]
        ys = self.ys
        bg = self.bg

        # Ik i can refactor every self val but i dont want to :)
        # because i can just copy and paste my old code

        if self.TkTrue:
            scaleVal = self.scaleVal
            window = self.window
            self.yValList[0].append(float(scaleVal.get()))
            window.update()
            window.update_idletasks()
        else:
            index = 0
            for ln in self.lineList:
                print(index)
                self.yValList[index].append(Input[index])


                self.yValList[index] = self.yValList[index][len(self.yValList[index]) - 200:]
                print(len(self.yValList[index]))
                ln[0].set_ydata(self.yValList[index])

                index += 1
        # adding the input value to the list of Y positions
        # TODO: add Serial input function
        #       or when passing str to input just Read from SM
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports

        # setting the graphs position and removing old values

        fig.canvas.restore_region(bg)
        for ln in self.lineList:
            ax.draw_artist(ln[0])
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()

        # bliting the canvas of the graph matplotlib docs:
        # https://matplotlib.org/stable/tutorials/advanced/blitting.html#sphx-glr-tutorials-advanced-blitting-py



