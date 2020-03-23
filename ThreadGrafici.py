import threading
import traceback

threadLock = threading.Lock()


class ThGrafico2d(threading.Thread):

    def __init__(self, grafico2d, axes2dAcc, axes2dGyro, accDataX, accDataY, gyroDataX, gyroDataY, topLevel):
        threading.Thread.__init__(self)
        self.grafico2d = grafico2d
        self.axes2dAcc = axes2dAcc
        self.axes2dGyro = axes2dGyro
        self.accDataX = accDataX
        self.accDataY = accDataY
        self.gyroDataX = gyroDataX
        self.gyroDataY = gyroDataY
        self.topLevel = topLevel

    def run(self):
        print("grafico2d: ", type(self.grafico2d), self.grafico2d)

        self.axes2dAcc.clear()
        self.axes2dGyro.clear()
        self.axes2dAcc.set_xticklabels([])
        self.axes2dGyro.set_xticklabels([])

        self.axes2dAcc.plot(self.accDataX, self.accDataY[0])
        self.axes2dAcc.plot(self.accDataX, self.accDataY[1])
        self.axes2dAcc.plot(self.accDataX, self.accDataY[2])
        self.axes2dGyro.plot(self.gyroDataX, self.gyroDataY[0])
        self.axes2dGyro.plot(self.gyroDataX, self.gyroDataY[1])
        self.axes2dGyro.plot(self.gyroDataX, self.gyroDataY[2])

        # self.grafico2d.draw()
        # self.topLevel.update()


class ThGrafico3d(threading.Thread):

    def __init__(self, axes3dAcc, grafico3d, accValue):
        threading.Thread.__init__(self)
        self.axes3dAcc = axes3dAcc
        self.grafico3d = grafico3d
        self.accValue = accValue

    def run(self):

        x = self.accValue[0]
        y = self.accValue[1]
        z = self.accValue[2]

        self.axes3dAcc.clear()
        self.axes3dAcc.set_xticklabels([])
        self.axes3dAcc.set_yticklabels([])
        self.axes3dAcc.set_zticklabels([])
        self.axes3dAcc.set_xlim(-2, 2)
        self.axes3dAcc.set_ylim(-2, 2)
        self.axes3dAcc.set_zlim(-2, 2)
        self.axes3dAcc.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        self.axes3dAcc.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
        self.axes3dAcc.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])


class ThGrafico2d3d(threading.Thread):
    def __init__(self, grafico2d, axes2dAcc, axes2dGyro, axes3dAcc, accDataY, gyroDataY, topLevel, accValue):
        threading.Thread.__init__(self)
        self.grafico2d = grafico2d
        self.axes2dAcc = axes2dAcc
        self.axes2dGyro = axes2dGyro
        self.axes3dAcc = axes3dAcc
        self.accDataX = [i for i in range(50)]
        self.accDataY = accDataY
        self.gyroDataX = [i for i in range(50)]
        self.gyroDataY = gyroDataY
        self.topLevel = topLevel
        self.accValue = accValue

    def run(self):
        print("grafico2d: ", type(self.grafico2d), self.grafico2d)

        x = self.accValue[0]
        y = self.accValue[1]
        z = self.accValue[2]

        self.axes2dAcc.clear()
        self.axes2dAcc.set_xticklabels([])

        self.axes2dGyro.clear()
        self.axes2dGyro.set_xticklabels([])

        self.axes3dAcc.clear()
        self.axes3dAcc.set_xticklabels([])
        self.axes3dAcc.set_yticklabels([])
        self.axes3dAcc.set_zticklabels([])
        self.axes3dAcc.set_xlim(-2, 2)
        self.axes3dAcc.set_ylim(-2, 2)
        self.axes3dAcc.set_zlim(-2, 2)

        self.axes3dAcc.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        self.axes3dAcc.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
        self.axes3dAcc.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])

        self.axes2dAcc.plot(self.accDataX, self.accDataY[0])
        self.axes2dAcc.plot(self.accDataX, self.accDataY[1])
        self.axes2dAcc.plot(self.accDataX, self.accDataY[2])

        self.axes2dGyro.plot(self.gyroDataX, self.gyroDataY[0])
        self.axes2dGyro.plot(self.gyroDataX, self.gyroDataY[1])
        self.axes2dGyro.plot(self.gyroDataX, self.gyroDataY[2])

        # self.grafico2d.draw()
        # self.topLevel.update()


class ThAxesAcc2d(threading.Thread):

    def __init__(self, axes, dataY, grafico):
        threading.Thread.__init__(self)
        self.axes = axes
        self.dataX = [i for i in range(50)]
        self.dataY = dataY
        self.grafico = grafico

    def run(self):
        self.axes.clear()
        self.axes.set_xticklabels([])
        self.axes.plot(self.dataX, self.dataY[0])
        self.axes.plot(self.dataX, self.dataY[1])
        self.axes.plot(self.dataX, self.dataY[2])
        threadLock.acquire()
        self.grafico.draw()
        threadLock.release()


class ThAxesGyro2d(threading.Thread):

    def __init__(self, axes, dataY, grafico):
        threading.Thread.__init__(self)
        self.axes = axes
        self.dataX = [i for i in range(50)]
        self.dataY = dataY
        self.grafico = grafico

    def run(self):
        self.axes.clear()
        self.axes.set_xticklabels([])
        self.axes.plot(self.dataX, self.dataY[0])
        self.axes.plot(self.dataX, self.dataY[1])
        self.axes.plot(self.dataX, self.dataY[2])
        threadLock.acquire()
        self.grafico.draw()
        threadLock.release()


class ThAxesAcc3d(threading.Thread):

    def __init__(self, axes, values, grafico):
        threading.Thread.__init__(self)
        self.axes = axes
        self.values = values
        self.grafico = grafico

    def run(self):
        x = self.values[0]
        y = self.values[1]
        z = self.values[2]

        self.axes.clear()
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.set_zticklabels([])
        self.axes.set_xlim(-2, 2)
        self.axes.set_ylim(-2, 2)
        self.axes.set_zlim(-2, 2)
        self.axes.plot([0, x], [0, 0], [0, 0], color="red", marker="o", markevery=[-1])
        self.axes.plot([0, 0], [0, y], [0, 0], color="blue", marker="o", markevery=[-1])
        self.axes.plot([0, 0], [0, 0], [0, z], color="green", marker="o", markevery=[-1])
        threadLock.acquire()
        self.grafico.draw()
        threadLock.release()