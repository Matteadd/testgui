import threading
import traceback
import random
threadLock = threading.Lock()


class ThAxesAcc2d(threading.Thread):

    def __init__(self, axes, canvasGrafico, widgetTkFigure):
        threading.Thread.__init__(self)
        self.axes = axes
        self.dataX = [i for i in range(50)]
        self.dataY = [[0] * 50, [0] * 50, [0] * 50]
        self.canvasGrafico = canvasGrafico
        self.widgetTkFigure = widgetTkFigure

    def run(self):
        while True:
            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            del self.dataY[0][0]
            del self.dataY[1][0]
            del self.dataY[2][0]

            self.dataY[0].append(x)
            self.dataY[1].append(y)
            self.dataY[2].append(z)

            self.axes.clear()
            self.axes.set_xticklabels([])
            self.axes.plot(self.dataX, self.dataY[0])
            self.axes.plot(self.dataX, self.dataY[1])
            self.axes.plot(self.dataX, self.dataY[2])
            self.canvasGrafico.draw()
            self.widgetTkFigure.update()


class ThAxesGyro2d(threading.Thread):

    def __init__(self, axes, canvasGrafico, widgetTkFigure):
        threading.Thread.__init__(self)
        self.axes = axes
        self.dataX = [i for i in range(50)]
        self.dataY = [[0] * 50, [0] * 50, [0] * 50]
        self.canvasGrafico = canvasGrafico
        self.widgetTkFigure = widgetTkFigure

    def run(self):
        while True:
            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            del self.dataY[0][0]
            del self.dataY[1][0]
            del self.dataY[2][0]

            self.dataY[0].append(x)
            self.dataY[1].append(y)
            self.dataY[2].append(z)

            self.axes.clear()
            self.axes.set_xticklabels([])
            self.axes.plot(self.dataX, self.dataY[0])
            self.axes.plot(self.dataX, self.dataY[1])
            self.axes.plot(self.dataX, self.dataY[2])
            self.canvasGrafico.draw()
            self.widgetTkFigure.update()


class ThAxesAcc3d(threading.Thread):

    def __init__(self, axes, canvasGrafico, widgetTkFigure, play):
        threading.Thread.__init__(self)
        self.line = axes.get_lines()[0]
        self.canvasGrafico = canvasGrafico
        self.widgetTkFigure = widgetTkFigure
        self.play = play

        print("canvasGrafico", id(canvasGrafico), type(canvasGrafico))
        print("widgetTkFigure", id(widgetTkFigure), type(widgetTkFigure))

    def run(self):
        # pass
        print(self.line)
        # self.canvasGrafico.draw()
        # self.widgetTkFigure.update()

        while self.play[0]:
            x = round(random.uniform(-1, 1), 1)
            y = round(random.uniform(-1, 1), 1)
            z = round(random.uniform(-1, 1), 1)

            self.line.set_xdata([0, x])
            self.line.set_ydata([0, y])
            self.line.set_3d_properties([0, z])

            # self.axes.clear()
            # self.axes.set_xticklabels([])
            # self.axes.set_yticklabels([])
            # self.axes.set_zticklabels([])
            # self.axes.set_xlim(-2, 2)
            # self.axes.set_ylim(-2, 2)
            # self.axes.set_zlim(-2, 2)
            # self.axes.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
            # self.axes.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
            # self.axes.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])
            # self.canvasGrafico.draw()
            # self.widgetTkFigure.update()
