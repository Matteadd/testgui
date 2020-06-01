import threading
import traceback


class ThAxesAcc2d(threading.Thread):

    def __init__(self, axes, dataY, grafico):
        threading.Thread.__init__(self)
        print(axes.get_lines())
        self.linex = axes.get_lines()[0]
        self.liney = axes.get_lines()[1]
        self.linez = axes.get_lines()[2]
        self.dataX = list(reversed([i for i in range(50)]))
        self.dataY = dataY
        self.grafico = grafico

    def run(self):
        self.linex.set_xdata(self.dataX)
        self.linex.set_ydata(self.dataY[0])
        self.liney.set_xdata(self.dataX)
        self.liney.set_ydata(self.dataY[1])
        self.linez.set_xdata(self.dataX)
        self.linez.set_ydata(self.dataY[2])


class ThAxesGyro2d(threading.Thread):

    def __init__(self, axes, dataY, grafico):
        threading.Thread.__init__(self)
        self.linex = axes.get_lines()[0]
        self.liney = axes.get_lines()[1]
        self.linez = axes.get_lines()[2]
        self.dataX = list(reversed([i for i in range(50)]))
        self.dataY = dataY
        self.grafico = grafico

    def run(self):
        self.linex.set_xdata(self.dataX)
        self.linex.set_ydata(self.dataY[0])
        self.liney.set_xdata(self.dataX)
        self.liney.set_ydata(self.dataY[1])
        self.linez.set_xdata(self.dataX)
        self.linez.set_ydata(self.dataY[2])


class ThAxesAcc3d(threading.Thread):

    def __init__(self, axes, values, grafico):
        threading.Thread.__init__(self)
        self.linex = axes.get_lines()[0]
        self.liney = axes.get_lines()[1]
        self.linez = axes.get_lines()[2]
        self.values = values
        self.grafico = grafico

    def run(self):
        x = self.values[0]
        y = self.values[1]
        z = self.values[2]

        # x = round(random.uniform(-1, 1), 1)
        # y = round(random.uniform(-1, 1), 1)
        # z = round(random.uniform(-1, 1), 1)
        self.linex.set_xdata([0, x])
        self.linex.set_ydata([0, 0])
        self.linex.set_3d_properties([0, 0])

        self.liney.set_xdata([0, 0])
        self.liney.set_ydata([0, y])
        self.liney.set_3d_properties([0, 0])

        self.linez.set_xdata([0, 0])
        self.linez.set_ydata([0, 0])
        self.linez.set_3d_properties([0, z])
