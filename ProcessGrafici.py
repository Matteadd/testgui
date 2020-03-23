import multiprocessing


class PrAxesAcc2d(multiprocessing.Process):

    def __init__(self, axes, dataY):
        multiprocessing.Process.__init__(self)
        self.axes = axes
        self.dataX = [i for i in range(50)]
        self.dataY = dataY

    def run(self):
        self.axes.clear()
        self.axes.set_xticklabels([])
        self.axes.plot(self.dataX, self.dataY[0])
        self.axes.plot(self.dataX, self.dataY[1])
        self.axes.plot(self.dataX, self.dataY[2])


class PrAxesGyro2d(multiprocessing.Process):

    def __init__(self, axes, dataY):
        multiprocessing.Process.__init__(self)
        self.axes = axes
        self.dataX = [i for i in range(50)]
        self.dataY = dataY

    def run(self):
        print("Sono qui")
        self.axes.clear()
        self.axes.set_xticklabels([])
        self.axes.plot(self.dataX, self.dataY[0])
        self.axes.plot(self.dataX, self.dataY[1])
        self.axes.plot(self.dataX, self.dataY[2])


class PrAxesAcc3d(multiprocessing.Process):

    def __init__(self, axes, values):
        multiprocessing.Process.__init__(self)
        self.axes = axes
        self.values = values

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
