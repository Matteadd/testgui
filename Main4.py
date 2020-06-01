import multiprocessing
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
# Modalità in cui la lettra dei dati è qui nel main e tramite il metodo update grafico avviene ad ogni iterazione la creazione di un thread
# from ThreadGrafici import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d
# Modalita in cui la lettura è all'intedno dei thread e anche i metodi per l'aggiornamento del grafico
# from ThreadGrafici2 import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d
# Modalita in cui la lettura è allinterno dei thread ma non lacoro più sul axes ma sul line contenuto in esso, tramite l'aggiornamento dei singoli dati
# from ThreadGrafici3 import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d
# Modalita in cui la lettura è è qui nel main e tramite il metodo update grafico avviene ad ogni iterazione la creazione di un thread ma non lavoro più sul axes ma sul line contenuto in esso, tramite l'aggiornamento dei singoli dati
from ThreadGrafici4 import ThAxesAcc2d, ThAxesGyro2d, ThAxesAcc3d


class Gui:

    mpu = mpu6050(0x68) if mpu6050 is not None else ""

    def __init__(self, window):

        self.play = False
        self.dataX = list(reversed([i for i in range(50)]))
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
        accAxes.plot(self.dataX, self.dataY[0], label=accLegends[0])
        accAxes.plot(self.dataX, self.dataY[1], label=accLegends[1])
        accAxes.plot(self.dataX, self.dataY[2], label=accLegends[2])

        gyroAxes = fig.add_subplot(312)
        gyroAxes.set_xticklabels([])
        gyroAxes.set_xlim(50, 0)
        gyroAxes.set_ylim([-300, 300])
        gyroAxes.plot(self.dataX, self.dataY[0], label=gyroLegends[0])
        gyroAxes.plot(self.dataX, self.dataY[1], label=gyroLegends[1])
        gyroAxes.plot(self.dataX, self.dataY[2], label=gyroLegends[2])

        accAxes3d = fig.add_subplot(313, projection="3d", elev=45, azim=45)
        accAxes3d.set_xticklabels([])
        accAxes3d.set_yticklabels([])
        accAxes3d.set_zticklabels([])
        accAxes3d.set_xlim(-10, 10)
        accAxes3d.set_ylim(-10, 10)
        accAxes3d.set_zlim(-10, 10)
        accAxes3d.plot([0, 0], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        accAxes3d.plot([0, 0], [0, 0], [0, 0], color="blue", marker="o", markevery=[-1])
        accAxes3d.plot([0, 0], [0, 0], [0, 0], color="green", marker="o", markevery=[-1])

        # accAxes.plot(self.dataX, self.dataY[2], label=accLegends[2])
        # gyroAxes.plot(self.dataX, self.dataY[2], label=gyroLegends[2])

        accAxes.legend(loc='upper right', fancybox=True, shadow=True)
        gyroAxes.legend(loc='upper right', fancybox=True, shadow=True)

        widgetTkFigure = canvasGrafico.get_tk_widget()
        widgetTkFigure.place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.9)

        # print("canvasGrafico: ", type(canvasGrafico), canvasGrafico)
        # print("widgetTkFigure: ", type(widgetTkFigure), widgetTkFigure)

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
                # self.updateFigure(topLevel, (accAxes, gyroAxes, accAxes3d), canvasGrafico, widgetTkFigure,)
                # self.updateFigure(topLevel, fig, canvasGrafico, widgetTkFigure,)
                # thUpdateAxesAcc3d = ThAxesAcc3d(accAxes3d, canvasGrafico, widgetTkFigure, [self.play])
                # thUpdateAxesGyro2d = ThAxesGyro2d(accAxes3d, canvasGrafico, widgetTkFigure)
                # thUpdateAxesAcc2d = ThAxesAcc2d(accAxes3d, canvasGrafico, widgetTkFigure)
                thUpdateAxesAcc3d = multiprocessing.Process(target=self.updateAcc3d, args=(accAxes3d, canvasGrafico, widgetTkFigure))
                # thUpdateAxesAcc2d = multiprocessing.Process(target=self.updateAcc2d, args=(accAxes, canvasGrafico, widgetTkFigure))
                thUpdateAxesAcc3d.start()
                thUpdateAxesAcc3d.join()
                # thUpdateAxesAcc2d.start()
                topLevel.after(0, self.updateFrame(topLevel, canvasGrafico, widgetTkFigure))
                # thUpdateAxesGyro2d.start()
                # thUpdateAxesGyro2d.join()
                # thUpdateAxesAcc2d.join()
                # canvasGrafico.draw()
                # widgetTkFigure.update()

            else:
                self.play = val

    def updateFrame(self, toplevel, canvasGrafico, widgetTkFigure):
        if self.play:
            canvasGrafico.draw()
            widgetTkFigure.update()
            toplevel.after(0, self.updateFrame(toplevel, canvasGrafico, widgetTkFigure))

    def updateFigure(self, topLevel, axes, canvasGrafico, widgetTkGrafico2d):
        axes2dAcc = axes[0]
        axes2dGyro = axes[1]
        axes3dAcc = axes[2]
        print(axes2dAcc.get_lines())
        print(axes2dGyro.get_lines())
        print(axes3dAcc.get_lines())

        while self.play:
            startTime = time.time()

            # dataAccFromMpu = self.mpu.get_accel_data()
            # dataGyroFromMpu = self.mpu.get_gyro_data()
            # x = dataAccFromMpu["x"]
            # y = dataAccFromMpu["y"]
            # z = dataAccFromMpu["z"]

            x = round(random.uniform(-5, 5), 1)
            y = round(random.uniform(-5, 5), 1)
            z = round(random.uniform(-5, 5), 1)

            del self.dataY[0][0]
            del self.dataY[1][0]
            del self.dataY[2][0]

            self.dataY[0].append(x)
            self.dataY[1].append(y)
            self.dataY[2].append(z)

            thUpdateAxesAcc2d = ThAxesAcc2d(axes2dAcc, self.dataY, canvasGrafico)
            thUpdateAxesGyro2d = ThAxesGyro2d(axes2dGyro, self.dataY, canvasGrafico)
            thUpdateAxesAcc3d = ThAxesAcc3d(axes3dAcc, (x, y, z), canvasGrafico)

            thUpdateAxesAcc2d.start()
            thUpdateAxesGyro2d.start()
            thUpdateAxesAcc3d.start()

            thUpdateAxesAcc2d.join()
            thUpdateAxesGyro2d.join()
            thUpdateAxesAcc3d.join()

            canvasGrafico.draw()
            canvasGrafico.flush_events()

            widgetTkGrafico2d.update()

            nowTime = time.time()
            print(round(nowTime - startTime, 3), "seconds")

    def updateAcc3d(self, axes, canvasGrafico, widgetTkFigure):
        linex = axes.get_lines()[0]
        liney = axes.get_lines()[1]
        linez = axes.get_lines()[2]

        while self.play:
            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            linex.set_xdata([0, x])
            linex.set_ydata([0, 0])
            linex.set_3d_properties([0, 0])

            liney.set_xdata([0, 0])
            liney.set_ydata([0, y])
            liney.set_3d_properties([0, 0])

            linez.set_xdata([0, 0])
            linez.set_ydata([0, 0])
            linez.set_3d_properties([0, z])

    def updateAcc2d(self, axes, canvasGrafico, widgetTkFigure):
        linex = axes.get_lines()[0]
        liney = axes.get_lines()[1]
        linez = axes.get_lines()[2]
        dataX = list(reversed([i for i in range(50)]))
        dataY = [[0] * 50, [0] * 50, [0] * 50]

        while self.play:
            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            del dataY[0][0]
            del dataY[1][0]
            del dataY[2][0]

            dataY[0].append(x)
            dataY[1].append(y)
            dataY[2].append(z)

            linex.set_xdata(dataX)
            linex.set_ydata(dataY[0])
            liney.set_xdata(dataX)
            liney.set_ydata(dataY[1])
            linez.set_xdata(dataX)
            linez.set_ydata(dataY[2])


if __name__ == '__main__':
    root = tk.Tk()
    top = Gui(root)
    root.mainloop()
