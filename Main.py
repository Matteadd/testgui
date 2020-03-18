import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

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

mpu = mpu6050(0x68) if mpu6050 is not None else ""

import random


class Gui():

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

        fig = Figure(facecolor="red", frameon=False, constrained_layout=True)
        grafico2d = FigureCanvasTkAgg(fig, topLevel)
        accAxes = fig.add_subplot(211)
        accAxes.set_xticklabels([])
        accAxes.set_xlim(50, 0)
        accAxes.set_ylim([-30, 30])

        gyroAxes = fig.add_subplot(212)
        gyroAxes.set_xticklabels([])
        gyroAxes.set_xlim(50, 0)
        gyroAxes.set_ylim([-300, 300])

        fig3d = Figure(facecolor="red", frameon=True, constrained_layout=True)
        fig3d.set_constrained_layout_pads(w_pad=0, h_pad=0, wspace=0, hspace=0)
        grafico3d = FigureCanvasTkAgg(fig3d, topLevel)
        ax3d = fig3d.add_subplot(111, projection="3d", elev=45, azim=45)
        ax3d.set_xticklabels([])
        ax3d.set_yticklabels([])
        ax3d.set_zticklabels([])
        ax3d.set_xlim(-2, 2)
        ax3d.set_ylim(-2, 2)
        ax3d.set_zlim(-2, 2)
        # ax3d.plot([0, 0], [0, 0], [0, 0], color="blue", marker="o", markevery=[-1])
        # ax3d.plot([0, 0], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        ax3d.plot([0, 0], [0, 0], [0, 0], color="green", marker="o", markevery=[-1])

        accPlots = []
        gyroPlots = []

        # accAxes.plot(self.dataX, self.dataY[0], label=accLegends[0])
        # accAxes.plot(self.dataX, self.dataY[1], label=accLegends[1])
        accAxes.plot(self.dataX, self.dataY[2], label=accLegends[2])
        # gyroAxes.plot(self.dataX, self.dataY[0], label=gyroLegends[0])
        # gyroAxes.plot(self.dataX, self.dataY[1], label=gyroLegends[1])
        gyroAxes.plot(self.dataX, self.dataY[2], label=gyroLegends[2])

        accGyroPlotsList = [accPlots, gyroPlots]

        accAxes.legend(loc='upper right', fancybox=True, shadow=True)
        gyroAxes.legend(loc='upper right', fancybox=True, shadow=True)

        grafico2d.get_tk_widget().place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.5)
        grafico3d.get_tk_widget().place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.4)

        # imgGrafico3d = tk.Button(topLevel)
        # imgGrafico3d.place(relx=0.05, rely=0.15)
        # imgResized = GraphicUtility.ridimensionaImage("img/grafico3D.gif", 400, 300)
        # imgGrafico3d.configure(image=imgResized, borderwidth=0, command=lambda: creaPlotter3d())
        # imgGrafico3d.image = imgResized
        #
        # # --------------------------------------------------------------------
        #
        # titoloProgresX = tk.Label(topLevel)
        # titoloProgresX.configure(text=labelFromFile['labelassex'])
        # titoloProgresX.configure(background="#ffffff")
        # titoloProgresX.place(relx=0.40, rely=0.5)
        #
        # progressX = ttk.Progressbar(topLevel, orient="horizontal", length=200, mode='determinate', )
        # progressX.place(relx=0.40, rely=0.55)
        #
        # triangoloXLabel = ttk.Label(topLevel)
        # triangoloXLabel.place(relx=0.55, rely=0.50, anchor="e", height=40, width=40)
        # triangoloXLabel.configure(relief="flat")
        # triangoloXLabel.configure(background="#ffffff")
        # triangoloXLabel.configure(borderwidth=0)
        #
        # # --------------------------------------------------------------------
        #
        # titoloProgresY = tk.Label(topLevel)
        # titoloProgresY.configure(text=labelFromFile['labelassey'])
        # titoloProgresY.configure(background="#ffffff")
        # titoloProgresY.place(relx=0.605, rely=0.5)
        #
        # progressY = ttk.Progressbar(topLevel, orient="horizontal", length=200, mode='determinate', )
        # progressY.place(relx=0.605, rely=0.55)
        #
        # triangoloYLabel = ttk.Label(topLevel)
        # triangoloYLabel.place(relx=0.755, rely=0.50, anchor="e", height=40, width=40)
        # triangoloYLabel.configure(relief="flat")
        # triangoloYLabel.configure(background="#ffffff")
        # triangoloYLabel.configure(borderwidth=0)
        #
        # # --------------------------------------------------------------------
        #
        # titoloProgresZ = tk.Label(topLevel)
        # titoloProgresZ.configure(text=labelFromFile['labelassez'])
        # titoloProgresZ.configure(background="#ffffff")
        # titoloProgresZ.place(relx=0.81, rely=0.5)
        #
        # progressZ = ttk.Progressbar(topLevel, orient="horizontal", length=200, mode='determinate', )
        # progressZ.place(relx=0.81, rely=0.55)
        #
        # triangoloZLabel = ttk.Label(topLevel)
        # triangoloZLabel.place(relx=0.96, rely=0.50, anchor="e", height=40, width=40)
        # triangoloZLabel.configure(relief="flat")
        # triangoloZLabel.configure(background="#ffffff")
        # triangoloZLabel.configure(borderwidth=0)
        #
        # # ----------------------------------------------------------------------

        # codIntervento = tk.Label(topLevel)
        # codIntervento.place(relx=0.6, rely=0.01, )
        # codIntervento.configure(background="#d9d9d9")
        # codIntervento.configure(font="-family {Roboto} -size 11")
        # codIntervento.configure(text=f"Cod. Intervento : {self.codIntervento}")
        #
        # indicatoreTemp = tk.Label(topLevel)
        # indicatoreTemp.place(relx=0.6, rely=0.04, )
        # indicatoreTemp.configure(textvariable=valueLabelTemp)
        # indicatoreTemp.configure(background="#d9d9d9")
        # indicatoreTemp.configure(font="-family {Roboto} -size 11")
        #
        # timerLabel = tk.Label(topLevel)
        # timerLabel.place(relx=0.6, rely=0.07, )
        # timerLabel.configure(textvariable=valueTimer)
        # timerLabel.configure(background="#d9d9d9")
        # timerLabel.configure(font="-family {Roboto} -size 11")
        #
        # # Deve prendere l'immagine perchè non è a sfondo trasparente
        # # print(self.kitChirurgicoSelezionato)
        # nomeLogo = tk.Label(topLevel)
        # nomeLogo.place(relx=0.8, rely=0.01, )
        # nomeLogo.configure(text=f"Kit chirugico : {self.kitChirurgicoSelezionato}")
        # nomeLogo.configure(background="#d9d9d9")
        # nomeLogo.configure(font="-family {Roboto} -size 11")
        #
        # downloadReport = tk.Label(topLevel)
        # downloadReport.place(relx=0.8, rely=0.04, )
        # logoImg = GraphicUtility.ridimensionaImage(f"img/imgReport.png", 216, 50)
        # downloadReport.configure(image=logoImg, borderwidth=0)
        # downloadReport.image = logoImg
        #
        # # kitChirurgicoLabel = tk.Label(topLevel)
        # # # kitChirurgicoLabel.place(relx=0.02, rely=0.1, )
        # # logoImg = GraphicUtility.ridimensionaImage(f"./imgkitchir/{self.kitChirurgicoSelezionato}.jpg", 150, 40)
        # # kitChirurgicoLabel.configure(image=logoImg, borderwidth=0)
        # # kitChirurgicoLabel.image = logoImg
        #
        # if self.pathZipProgetto != "":
        #     srcImg = unzipImgProgetto()
        #
        #     img1 = tk.Label(topLevel)
        #     img1.place(relx=0.1, rely=0.6)
        #     imgResized = GraphicUtility.ridimensionaImage(srcImg[0], 284, 200)
        #     img1.configure(image=imgResized, borderwidth=0)
        #     img1.image = imgResized
        #
        #     img2 = tk.Label(topLevel)
        #     img2.place(relx=0.4, rely=0.6)
        #     imgResized = GraphicUtility.ridimensionaImage(srcImg[1], 488, 200)
        #     img2.configure(image=imgResized, borderwidth=0)
        #     img2.image = imgResized
        #
        avviaButton = tk.Button(topLevel)
        # avviaButton.config(text="Avvia Lettura", command=lambda: self.aggiornaGrafici(True, fig, fig3d, accGyroPlotsList, topLevel, grafico2d, grafico3d))
        avviaButton.config(text="Avvia Lettura", command=lambda: setPlay(True))
        avviaButton.place(relx=0.05, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        stopButton = tk.Button(topLevel)
        # stopButton.config(text="Ferma Lettura", command=lambda: self.aggiornaGrafici(False, fig, fig3d, accGyroPlotsList, topLevel, grafico2d, grafico3d))
        stopButton.config(text="Ferma Lettura", command=lambda: setPlay(False))
        stopButton.place(relx=0.26, rely=0.9, relwidth=0.2, relheight=0.1, bordermode='ignore')

        def disabilitaRotazione(event):
            ax3d.view_init(elev=45, azim=45)

        fig3d.canvas.mpl_connect('motion_notify_event', disabilitaRotazione)

        def setPlay(val):
            if val:
                self.play = val
                self.aggiornaGrafici(fig, fig3d, accGyroPlotsList, topLevel, grafico2d, grafico3d)
            else:
                self.play = val
                # stop = val

    def aggiornaGrafici(self, figure2d, figure3d, accGyroPlotsList, topLevel, grafico2d, grafico3d):

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
            axes3dAcc.plot([0, 0], [0, y





                                    ], [0, 0], color="blue", marker="o", markevery=[-1])
            axes3dAcc.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])
            grafico3d.draw()

            nowTime = time.time()
            print(round(nowTime - startTime, 3), "seconds")

            topLevel.update()
            topLevel.after(1, self.aggiornaGrafici(figure2d, figure3d, accGyroPlotsList, topLevel, grafico2d, grafico3d))


if __name__ == '__main__':
    root = tk.Tk()
    top = Gui(root)
    root.mainloop()
