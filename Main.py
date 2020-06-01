import threading
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import logging

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    from tkinter.messagebox import showinfo

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

try:
    from mpu6050 import mpu6050
except ImportError:
    mpu6050 = None



import random
from ThreadGrafici import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d
import multiprocessing

# from ProcessGrafici import PrAxesAcc2d, PrAxesGyro2d, PrAxesAcc3d


class Gui:

    mpu = mpu6050(0x68) if mpu6050 is not None else ""

    def __init__(self, window):

        self.play = False
        self.dataX = [i for i in range(0, 50, )]
        self.dataY = [[0] * 50, [0] * 50, [0] * 50]

        topLevel = root
        topLevel.title("Chirurgia Guidata OS")
        topLevel.geometry(f"700x700+500+100")
        topLevel.configure(bg="#ffffff")

        accLegends = ['Acc_x', 'Acc_y', 'Acc_z']
        gyroLegends = ['Gyro_x', 'Gyro_y', 'Gyro_z']

        fig = Figure(facecolor="red", frameon=False, constrained_layout=True)
        grafico2d = FigureCanvasTkAgg(fig, topLevel)

        accAxes = fig.add_subplot(311)
        accAxes.set_xticklabels([])
        accAxes.set_xlim(50, 0)
        accAxes.set_ylim([-5, 5])

        gyroAxes = fig.add_subplot(312)
        gyroAxes.set_xticklabels([])
        gyroAxes.set_xlim(50, 0)
        gyroAxes.set_ylim([-300, 300])

        ax3d = fig.add_subplot(313, projection="3d", elev=45, azim=45)
        ax3d.set_xticklabels([])
        ax3d.set_yticklabels([])
        ax3d.set_zticklabels([])
        ax3d.set_xlim(-10, 10)
        ax3d.set_ylim(-10, 10)
        ax3d.set_zlim(-10, 10)
        ax3d.plot([0, 0], [0, 0], [0, 0], color="green", marker="o", markevery=[-1])

        accPlots = []
        gyroPlots = []

        accAxes.plot(self.dataX, self.dataY[2], label=accLegends[2])
        gyroAxes.plot(self.dataX, self.dataY[2], label=gyroLegends[2])

        accGyroPlotsList = [accPlots, gyroPlots]

        accAxes.legend(loc='upper right', fancybox=True, shadow=True)
        gyroAxes.legend(loc='upper right', fancybox=True, shadow=True)

        widgetTkGrafico2d = grafico2d.get_tk_widget()

        print("canvasGrafico: ", type(grafico2d), grafico2d)
        print("widgetTkGrafico2d: ", type(widgetTkGrafico2d), widgetTkGrafico2d)

        widgetTkGrafico2d.place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.9)

        avviaButton = tk.Button(topLevel)
        avviaButton.config(text="Avvia Lettura", command=lambda: setPlay(True))
        avviaButton.place(relx=0.05, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        stopButton = tk.Button(topLevel)
        stopButton.config(text="Ferma Lettura", command=lambda: setPlay(False))
        stopButton.place(relx=0.26, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        def disabilitaRotazione(event):
            ax3d.view_init(elev=45, azim=45)

        fig.canvas.mpl_connect('motion_notify_event', disabilitaRotazione)

        def setPlay(val):
            if val:
                self.play = val
                self.updateFigure(topLevel, fig, grafico2d, widgetTkGrafico2d,)
            else:
                self.play = val

    def updateFigure(self, topLevel, figure2d, grafico2d, widgetTkGrafico2d):
        axes2dAcc = figure2d.axes[0]
        axes2dGyro = figure2d.axes[1]
        axes3dAcc = figure2d.axes[2]
        print(figure2d.axes)

        while self.play:
            startTime = time.time()

            # dataAccFromMpu = self.mpu.get_accel_data()
            # dataGyroFromMpu = self.mpu.get_gyro_data()
            # x = dataAccFromMpu["x"]
            # y = dataAccFromMpu["y"]
            # z = dataAccFromMpu["z"]

            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            del self.dataY[0][0]
            del self.dataY[1][0]
            del self.dataY[2][0]

            self.dataY[0].append(x)
            self.dataY[1].append(y)
            self.dataY[2].append(z)

            # threadUpdategrafico2d3d = ThGrafico2d3d(canvasGrafico, axes2dAcc, axes2dGyro, axes3dAcc, self.dataY, self.dataY, topLevel, (x, y, z))
            # threadUpdategrafico2d3d.start()
            # threadUpdategrafico2d3d.join()

            thUpdateAxesAcc2d = ThAxesAcc2d(axes2dAcc, self.dataY, grafico2d)
            thUpdateAxesGyro2d = ThAxesGyro2d(axes2dGyro, self.dataY, grafico2d)
            thUpdateAxesAcc3d = ThAxesAcc3d(axes3dAcc, (x, y, z), grafico2d)

            thUpdateAxesAcc2d.start()
            thUpdateAxesGyro2d.start()
            thUpdateAxesAcc3d.start()

            thUpdateAxesAcc2d.join()
            thUpdateAxesGyro2d.join()
            thUpdateAxesAcc3d.join()

            # prUpdateAxesAcc2d = PrAxesAcc2d(axes2dAcc, self.dataY)
            # prUpdateAxesGyro2d = PrAxesGyro2d(axes2dGyro, self.dataY)
            # prUpdateAxesGyro2d = PrAxesGyro2d(axes2dGyro, self.dataY)
            # prUpdateAxesAcc3d = multiprocessing.Process(target=self.update3dpr, args=(axes3dAcc, (x, y, z), canvasGrafico))
            #
            # prUpdateAxesAcc2d.start()
            # prUpdateAxesGyro2d.start()
            # prUpdateAxesAcc3d.start()
            #
            # prUpdateAxesAcc2d.join()
            # prUpdateAxesGyro2d.join()
            # prUpdateAxesAcc3d.join()

            grafico2d.draw()
            widgetTkGrafico2d.update()

            nowTime = time.time()
            print(round(nowTime - startTime, 3), "seconds")

    @staticmethod
    def update3dpr(axes, values, grafico):
        x = values[0]
        y = values[1]
        z = values[2]

        axes.clear()
        axes.set_xticklabels([])
        axes.set_yticklabels([])
        axes.set_zticklabels([])
        axes.set_xlim(-2, 2)
        axes.set_ylim(-2, 2)
        axes.set_zlim(-2, 2)
        axes.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        axes.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
        axes.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])

        # canvasGrafico.draw()


if __name__ == '__main__':
    root = tk.Tk()
    top = Gui(root)
    root.mainloop()
