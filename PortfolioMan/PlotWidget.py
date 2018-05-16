import sys
import os
os.environ['QT_API'] = 'pyside2'
import matplotlib
#import pylab

matplotlib.use('Qt4Agg')
#matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

class PlotWidget(QtGui.QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()     
        self.initUI()

    def initUI(self):
        # generate the plot
        fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        ax.plot([0,1])
        
        # generate the canvas to display the plot
        canvas = FigureCanvas(fig)
        layout =  QtGui.QVBoxLayout()
        layout.addWidget(canvas)
        
        self.setLayout(layout)  