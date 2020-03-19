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
from ThreadGrafici import ThGrafico2d, ThGrafico3d


class Gui:

    mpu = mpu6050(0x68) if mpu6050 is not None else ""

    def __init__(self, window):

        self.play = False
        self.dataX = [i for i in range(0, 50, )]
        self.dataY = [[0] * 50, [0] * 50, [0] * 50]

        topLevel = root
        topLevel.title("Chirurgia Guidata OS")
        topLevel.geometry(f"1000x1000+0+0")
        topLevel.configure(bg="#ffffff")

        accLegends = ['Acc_x', 'Acc_y', 'Acc_z']
        gyroLegends = ['Gyro_x', 'Gyro_y', 'Gyro_z']

        fig = Figure(facecolor="red", frameon=False, constrained_layout=False)
        grafico2d = FigureCanvasTkAgg(fig, topLevel)

        accAxes = fig.add_subplot(211)
        # accAxes.set_xticklabels([])
        # accAxes.set_xlim(50, 0)
        # accAxes.set_ylim([-5, 5])

        gyroAxes = fig.add_subplot(212)
        # gyroAxes.set_xticklabels([])
        # gyroAxes.set_xlim(50, 0)
        # gyroAxes.set_ylim([-300, 300])

        fig3d = Figure(facecolor="red", frameon=True, constrained_layout=False)
        fig3d.set_constrained_layout_pads(w_pad=0, h_pad=0, wspace=0, hspace=0)
        grafico3d = FigureCanvasTkAgg(fig3d, topLevel)
        ax3d = fig3d.add_subplot(111, projection="3d", elev=45, azim=45)
        ax3d.set_xticklabels([])
        ax3d.set_yticklabels([])
        ax3d.set_zticklabels([])
        ax3d.set_xlim(-2, 2)
        ax3d.set_ylim(-2, 2)
        ax3d.set_zlim(-2, 2)
        ax3d.plot([0, 0], [0, 0], [0, 0], color="green", marker="o", markevery=[-1])

        accPlots = []
        gyroPlots = []

        accAxes.plot(self.dataX, self.dataY[2], label=accLegends[2])
        gyroAxes.plot(self.dataX, self.dataY[2], label=gyroLegends[2])

        accGyroPlotsList = [accPlots, gyroPlots]

        accAxes.legend(loc='upper right', fancybox=True, shadow=True)
        gyroAxes.legend(loc='upper right', fancybox=True, shadow=True)

        grafico2d.get_tk_widget().place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.5)
        grafico3d.get_tk_widget().place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.4)

        avviaButton = tk.Button(topLevel)
        avviaButton.config(text="Avvia Lettura", command=lambda: setPlay(True))
        avviaButton.place(relx=0.05, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        stopButton = tk.Button(topLevel)
        stopButton.config(text="Ferma Lettura", command=lambda: setPlay(False))
        stopButton.place(relx=0.26, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        def disabilitaRotazione(event):
            ax3d.view_init(elev=45, azim=45)

        fig3d.canvas.mpl_connect('motion_notify_event', disabilitaRotazione)

        def setPlay(val):
            if val:
                self.play = val
                self.updateGrafici(topLevel, fig, fig3d, grafico2d, grafico3d)
                # self.aggiornaGrafici(topLevel, fig, fig3d, grafico2d, grafico3d)
            else:
                self.play = val

    def updateGrafici(self, topLevel, figure2d, figure3d, grafico2d, grafico3d):

        axes2dAcc = figure2d.axes[0]
        axes2dGyro = figure2d.axes[1]
        axes3dAcc = figure3d.axes[0]

        while self.play:
            startTime = time.time()

            dataAccFromMpu = self.mpu.get_accel_data()
            dataGyroFromMpu = self.mpu.get_gyro_data()

            # x = round(random.uniform(-1, 1), 1)
            # y = round(random.uniform(-1, 1), 1)
            # z = round(random.uniform(-1, 1), 1)

            x = dataAccFromMpu["x"]
            y = dataAccFromMpu["y"]
            z = dataAccFromMpu["z"]

            del self.dataY[0][0]
            del self.dataY[1][0]
            del self.dataY[2][0]

            self.dataY[0].append(x)
            self.dataY[1].append(y)
            self.dataY[2].append(z)

            # threadUpdategrafico2d = threading.Thread(target=self.aggiornaGrafico2d, args=(axes2dAcc, axes2dGyro, grafico2d, self.dataX, self.dataY, self.dataX, self.dataY))
            # threadUpdategrafico3d = threading.Thread(target=self.aggiornaGrafico3d, args=(axes3dAcc, grafico3d, (x, y, z)))

            threadUpdategrafico2d = ThGrafico2d(grafico2d, axes2dAcc, axes2dGyro, self.dataX, self.dataY, self.dataX, self.dataY)
            threadUpdategrafico3d = ThGrafico3d(axes3dAcc, grafico3d, (x, y, z))

            threadUpdategrafico2d.start()
            threadUpdategrafico3d.start()

            threadUpdategrafico2d.join()
            threadUpdategrafico3d.join()

            grafico2d.draw()
            grafico3d.draw()
            topLevel.update()

            nowTime = time.time()
            print(round(nowTime - startTime, 3), "seconds")
            # topLevel.after(1, self.updateGrafici(topLevel, figure2d, figure3d, grafico2d, grafico3d))

    # vecchio metodo da 0.3 secondi di esecuzioni
    def aggiornaGrafici(self, topLevel, figure2d, figure3d, grafico2d, grafico3d):

        startTime = time.time()
        axes2dAcc = figure2d.axes[0]
        axes2dGyro = figure2d.axes[1]
        axes3dAcc = figure3d.axes[0]

        if self.play:

            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            del self.dataY[0][0]
            del self.dataY[1][0]
            del self.dataY[2][0]

            self.dataY[0].append(x)
            self.dataY[1].append(y)
            self.dataY[2].append(z)

            axes2dAcc.clear()
            axes2dAcc.plot(self.dataX, self.dataY[0])
            axes2dAcc.plot(self.dataX, self.dataY[1])
            axes2dAcc.plot(self.dataX, self.dataY[2])
            grafico2d.draw()

            axes2dGyro.clear()
            axes2dGyro.plot(self.dataX, self.dataY[0])
            axes2dGyro.plot(self.dataX, self.dataY[1])
            axes2dGyro.plot(self.dataX, self.dataY[2])
            grafico2d.draw()

            axes3dAcc.clear()
            axes3dAcc.set_xticklabels([])
            axes3dAcc.set_yticklabels([])
            axes3dAcc.set_zticklabels([])
            axes3dAcc.set_xlim(-2, 2)
            axes3dAcc.set_ylim(-2, 2)
            axes3dAcc.set_zlim(-2, 2)
            axes3dAcc.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
            axes3dAcc.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
            axes3dAcc.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])
            grafico3d.draw()

            nowTime = time.time()
            print(round(nowTime - startTime, 3), "seconds")

            topLevel.update()
            topLevel.after(1, self.aggiornaGrafici(topLevel, figure2d, figure3d, grafico2d, grafico3d))


    @staticmethod
    def aggiornaGrafico2d(grafico2d, axes2dAcc, axes2dGyro, accDataX, accDataY, gyroDataX, gyroDataY):

            logging.info("Aggiornamento grafico 2d avviato")

            axes2dAcc.clear()
            axes2dGyro.clear()

            axes2dAcc.plot(accDataX, accDataY[0])
            axes2dAcc.plot(accDataX, accDataY[1])
            axes2dAcc.plot(accDataX, accDataY[2])
            axes2dGyro.plot(gyroDataX, gyroDataY[0])
            axes2dGyro.plot(gyroDataX, gyroDataY[1])
            axes2dGyro.plot(gyroDataX, gyroDataY[2])

            grafico2d.draw()
            logging.info("Aggiornamento grafico 2d terminato")


    @staticmethod
    def aggiornaGrafico3d(axes3dAcc, grafico3d, accValue):

        logging.info("Aggiornamento grafico 3d avviato")

        x = accValue[0]
        y = accValue[1]
        z = accValue[2]

        axes3dAcc.clear()
        axes3dAcc.set_xticklabels([])
        axes3dAcc.set_yticklabels([])
        axes3dAcc.set_zticklabels([])
        axes3dAcc.set_xlim(-2, 2)
        axes3dAcc.set_ylim(-2, 2)
        axes3dAcc.set_zlim(-2, 2)
        axes3dAcc.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        axes3dAcc.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
        axes3dAcc.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])
        grafico3d.draw()

        logging.info("Aggiornamento grafico 3d terminato")


if __name__ == '__main__':
    root = tk.Tk()
    top = Gui(root)
    root.mainloop()
