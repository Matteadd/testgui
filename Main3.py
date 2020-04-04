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
# from ThreadGrafici import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d
from ThreadGrafici2 import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d


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
        canvasGrafico = FigureCanvasTkAgg(fig, topLevel)

        accAxes = fig.add_subplot(311)
        accAxes.set_xticklabels([])
        accAxes.set_xlim(50, 0)
        accAxes.set_ylim([-5, 5])

        gyroAxes = fig.add_subplot(312)
        gyroAxes.set_xticklabels([])
        gyroAxes.set_xlim(50, 0)
        gyroAxes.set_ylim([-300, 300])

        accAxes3d = fig.add_subplot(313, projection="3d", elev=45, azim=45)
        accAxes3d.set_xticklabels([])
        accAxes3d.set_yticklabels([])
        accAxes3d.set_zticklabels([])
        accAxes3d.set_xlim(-10, 10)
        accAxes3d.set_ylim(-10, 10)
        accAxes3d.set_zlim(-10, 10)
        accAxes3d.plot([0, 0], [0, 0], [0, 0], color="green", marker="o", markevery=[-1])

        accAxes.plot(self.dataX, self.dataY[2], label=accLegends[2])
        gyroAxes.plot(self.dataX, self.dataY[2], label=gyroLegends[2])

        accAxes.legend(loc='upper right', fancybox=True, shadow=True)
        gyroAxes.legend(loc='upper right', fancybox=True, shadow=True)

        widgetTkFigure = canvasGrafico.get_tk_widget()
        widgetTkFigure.place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.9)

        print("canvasGrafico: ", type(canvasGrafico), canvasGrafico)
        print("widgetTkFigure: ", type(widgetTkFigure), widgetTkFigure)

        avviaButton = tk.Button(topLevel)
        avviaButton.config(text="Avvia Lettura", command=lambda: setPlay(True))
        avviaButton.place(relx=0.05, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        stopButton = tk.Button(topLevel)
        stopButton.config(text="Ferma Lettura", command=lambda: setPlay(False))
        stopButton.place(relx=0.26, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        def disabilitaRotazione(event):
            accAxes3d.view_init(elev=45, azim=45)
        fig.canvas.mpl_connect('motion_notify_event', disabilitaRotazione)

        def setPlay(val):
            if val:
                self.play = val
                # self.updateFigure(topLevel, fig, canvasGrafico, widgetTkFigure,)
                thUpdateAxesAcc3d = ThAxesAcc3d(accAxes3d, canvasGrafico, widgetTkFigure, [self.play])
                print("canvasGraficoid", id(canvasGrafico))
                print("widgetTkFigureid", id(widgetTkFigure))

                # thUpdateAxesGyro2d = ThAxesGyro2d(accAxes3d, canvasGrafico, widgetTkFigure)
                # thUpdateAxesAcc2d = ThAxesAcc2d(accAxes3d, canvasGrafico, widgetTkFigure)
                thUpdateAxesAcc3d.start()
                # thUpdateAxesGyro2d.start()
                # thUpdateAxesAcc2d.start()
                # thUpdateAxesAcc3d.join()
                # thUpdateAxesGyro2d.join()
                # thUpdateAxesAcc2d.join()

            else:
                self.play = val

    def updateFigure(self, topLevel, figure2d, canvasGrafico, widgetTkGrafico2d):
        axes2dAcc = figure2d.axes[0]
        axes2dGyro = figure2d.axes[1]
        axes3dAcc = figure2d.axes[2]

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

            thUpdateAxesAcc2d = ThAxesAcc2d(axes2dAcc, self.dataY, canvasGrafico)
            thUpdateAxesGyro2d = ThAxesGyro2d(axes2dGyro, self.dataY, canvasGrafico)
            thUpdateAxesAcc3d = ThAxesAcc3d(axes3dAcc, (x, y, z), canvasGrafico)

            # thUpdateAxesAcc2d.start()
            # thUpdateAxesGyro2d.start()
            thUpdateAxesAcc3d.start()

            # thUpdateAxesAcc2d.join()
            # thUpdateAxesGyro2d.join()
            thUpdateAxesAcc3d.join()

            canvasGrafico.draw()
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
