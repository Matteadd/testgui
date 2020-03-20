import threading
import traceback


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

