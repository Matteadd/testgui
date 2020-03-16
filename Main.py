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


class Gui():

    def __init__(self, window):

        # def unzipImgProgetto():
        #     from zipfile import is_zipfile, ZipFile
        #     srcImg = []
        #     if is_zipfile(self.pathZipProgetto):
        #         archiveMembers = ZipFile(self.pathZipProgetto).namelist()
        #         for archiveMember in archiveMembers:
        #             if ".jpg" in str(archiveMember) or ".png" in str(archiveMember):
        #                 fileUnzipped = ZipFile(self.pathZipProgetto).open(archiveMember)
        #                 srcImg.append(fileUnzipped)
        #     return srcImg
        #
        # labelFromFile = ChirurgiaGuidataOsProperties.ChirurgiaGuidataOsProperties.getLabelViews()["Plotter"]
        #
        # valueLabelTemp = tk.StringVar()
        # valueLabelTemp.set(f"{labelFromFile['labeltitolotemperatura']} 0.0 C°")
        #
        # valueTimer = tk.StringVar()
        # valueTimer.set(f"{labelFromFile['labeltitolotimer']} 00:00:00")
        #
        # valueLabelAlert = tk.StringVar()
        # valueLabelAlert.set(f"Status: Ok")
        #
        # valueProgressX = tk.IntVar()
        # valueProgressX.set(0)
        #
        # valueProgressY = tk.IntVar()
        # valueProgressY.set(0)
        #
        # valueProgressZ = tk.IntVar()
        # valueProgressZ.set(0)
        #
        topLevel = root
        # topLevel.transient(self.top)
        # topLevel.grab_set()
        #
        topLevel.title("Chirurgia Guidata OS")
        topLevel.geometry(f"1000x1000+0+0")
        # topLevel.resizable(0, 0)
        # topLevel.protocol("WM_DELETE_WINDOW", lambda: self.closeTopLevelPlotter(topLevel))
        # topLevel.configure(bg="#ffffff")
        #
        # headerFrame = ttk.Frame(topLevel)
        # headerFrame.place(relx=0.0, rely=0.0, height=90, relwidth=1.0)
        # headerFrame.configure(relief='flat')
        # headerFrame.configure(borderwidth="2")
        #
        # imgTitoloLabel = ttk.Label(headerFrame)
        # imgTitoloLabel.place(relx=0.15, rely=0.05, height=70, width=505)
        # imgTitoloLabel.configure(relief="flat")
        # testoHeader = GraphicUtility.ridimensionaImage("img/TestoHeader.png", GraphicUtility.getWidth(imgTitoloLabel),
        #                                                GraphicUtility.getHeight(imgTitoloLabel))
        # imgTitoloLabel.configure(image=testoHeader)
        # imgTitoloLabel.image = testoHeader
        #
        # logoLabel = ttk.Label(headerFrame)
        # logoLabel.place(relx=0.01, rely=0.0, height=70, width=150)
        # logoLabel.configure(relief="flat")
        # logo = GraphicUtility.ridimensionaImage("img/Logo.png", GraphicUtility.getWidth(logoLabel),
        #                                         GraphicUtility.getHeight(logoLabel))
        # logoLabel.configure(image=logo)
        # logoLabel.image = logo
        #
        fig = Figure(facecolor="white", frameon=False, constrained_layout=True, linewidth=2)
        accAxes = fig.add_subplot(211)
        accAxes.set_xticklabels([])
        accAxes.set_xlim(50, 0)
        accAxes.set_ylim([-30, 30])
        #
        gyroAxes = fig.add_subplot(212)
        gyroAxes.set_xticklabels([])
        gyroAxes.set_xlim(50, 0)
        gyroAxes.set_ylim([-300, 300])

        accLegends = ['Acc_x', 'Acc_y', 'Acc_z']
        gyroLegends = ['Gyro_x', 'Gyro_y', 'Gyro_z']

        timeValues = [i for i in range(0, 50, )]
        accValues = [[0] * 50, [0] * 50, [0] * 50]
        gyroValues = [[0] * 50, [0] * 50, [0] * 50]

        # fig3d = Figure(facecolor="white", frameon=True, constrained_layout=True, linewidth=10, edgecolor="#04253a")
        fig3d = Figure()
        grafico3d = FigureCanvasTkAgg(fig3d, topLevel)
        grafico3d.draw()
        ax3d = fig3d.add_subplot(111, projection="3d")
        ax3d.set_xticklabels([])
        ax3d.set_yticklabels([])
        ax3d.set_zticklabels([])

        # plt.cla()
        ax3d.set_xlim(-2, 2)
        ax3d.set_ylim(-2, 2)
        ax3d.set_zlim(-2, 2)
        ax3d.plot([0, 0], [0, 0], [0, 0], color="blue", marker="o", markevery=[-1])
        ax3d.plot([0, 0], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        ax3d.plot([0, 0], [0, 0], [0, 0], color="green", marker="o", markevery=[-1])

        # plot gyro per x, y, z
        accPlotAllowed = [1, 1, 1]
        # plot acc per x, y, z
        gyroPlotAllowed = [1, 1, 1]

        accPlots = []
        gyroPlots = []

        for i, createLine in enumerate(accPlotAllowed):
            if createLine == 1:
                accPlots.append(accAxes.plot(timeValues, accValues[i], label=accLegends[i])[0])

        for i, createLine in enumerate(gyroPlotAllowed):
            if createLine == 1:
                gyroPlots.append(gyroAxes.plot(timeValues, gyroValues[i], label=gyroLegends[i])[0])

        accGyroPlotsList = [accPlots, gyroPlots]

        accAxes.legend(loc='upper right', fancybox=True, shadow=True)
        gyroAxes.legend(loc='upper right', fancybox=True, shadow=True)

        grafico = FigureCanvasTkAgg(fig, topLevel)
        # grafico.draw()
        #
        grafico.get_tk_widget().place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.5)
        grafico3d.get_tk_widget().place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.5)

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
        #
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
        # avviaButton = tk.Button(topLevel)
        # avviaButton.config(text=labelFromFile['buttonavviaintervento'], command=lambda: actionAvviaButton())
        # avviaButton.place(relx=0.85, rely=0.6, height=50, width=150, bordermode='ignore')
        #
        # fermaButton = tk.Button(topLevel)
        # fermaButton.config(text=labelFromFile['buttonsospendiintervento'], command=lambda: actionFermaButton())
        # fermaButton.place(relx=0.85, rely=0.7, height=50, width=150, bordermode='ignore')
        #
        # chiudiFinestraButton = tk.Button(topLevel)
        # chiudiFinestraButton.config(text=labelFromFile['buttonteminaintervento'], command=lambda: actionchiudiButton())
        # chiudiFinestraButton.place(relx=0.85, rely=0.8, height=50, width=150, bordermode='ignore')
        #
        # fig3d, ax3d = plt.subplots(subplot_kw={'projection': '3d'})
        # ax3d.set_xticklabels([])
        # ax3d.set_yticklabels([])
        # ax3d.set_zticklabels([])
        #
        # plt.gcf().canvas.set_window_title('Chirurgia Guidata Os')
        #
        # def creaPlotter3d():
        #     plt.show()
        #
        # def actionAvviaButton():
        #     if avviaButton["text"] == labelFromFile['buttonavviaintervento']:
        #         avviaButton["text"] = labelFromFile['buttonriprendiintervento']
        #     else:
        #         self.calibrazioneSensore()
        #         # showinfo("Chirurgia Guidata OS", labelFromFile["messaggioconfermacalibrazione"])
        #     self.playGrafico = True
        #     avviaButton.configure(state="disable")
        #     fermaButton.configure(state="normal")
        #     chiudiFinestraButton.configure(state="disable")
        #     self.updateGrafico(accGyroPlotsList, grafico, valueLabelTemp, labelFromFile['labeltitolotemperatura'],
        #                        [progressX, progressY, progressZ], [triangoloXLabel, triangoloYLabel, triangoloZLabel], ax3d)
        #     # self.updateGrafico3d(ax3d, grafico3D)
        #     # self.updateGrafico3d(ax3d2, grafico3D)
        #     self.updateTimer(valueTimer, labelFromFile['labeltitolotimer'])
        #
        # def actionFermaButton():
        #     self.playGrafico = False
        #     avviaButton.configure(state="normal")
        #     fermaButton.configure(state="disable")
        #     chiudiFinestraButton.configure(state="normal")
        #
        # def actionchiudiButton():
        #     avviaButton.configure(state="normal")
        #     fermaButton.configure(state="normal")
        #     plt.close(fig3d)
        #     self.closeTopLevelPlotter(topLevel)


if __name__ == '__main__':
    root = tk.Tk()
    top = Gui(root)
    root.mainloop()