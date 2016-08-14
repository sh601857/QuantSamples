#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
from PySide import QtCore
from PySide import QtGui
import HKAssertsWidget
import PlotWidget

class MainW(QtGui.QMainWindow):

    def __init__(self):
        super(MainW, self).__init__()

        self.initUI()

    def initUI(self): 
        
        self.setWindowIcon(QtGui.QIcon('PortfolioMan.ico'))
        if (os.name == 'nt'):
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            myappid = 'PortfolioManHK.1.0.0' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)        
        # create commonds tree        
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()
        item = QtGui.QStandardItem(self.tr("1.HK"))
        item.setData(0,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("Asserts")
        subitem.setData( 0, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("Plot")
        subitem.setData( 1, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem(self.tr("2.HS"))
        item.appendRow(QtGui.QStandardItem("Asserts"))
        item.appendRow(QtGui.QStandardItem("Plot"))
        parentItem.appendRow(item)
   
        self.cmdTree = QtGui.QTreeView(self)
        self.cmdTree.setModel(self.cmdmodel)
        self.cmdTree.setHeaderHidden(True)
        self.cmdTree.expandToDepth(2)
        self.cmdTree.setMinimumWidth(150)
        dockWidget = QtGui.QDockWidget((""), self)
        dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dockWidget.setWidget(self.cmdTree)
        dockWidget.setTitleBarWidget(QtGui.QWidget(dockWidget))
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)#hide the titlebar

        #Create central widget			
        self.HKWgt =  HKAssertsWidget.HKAssertsWidget()
        self.plotWgt = PlotWidget.PlotWidget()  # QtGui.QWidget()
        self.thirdPageWidget =  QtGui.QWidget()

        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.HKWgt)
        self.censw.addWidget(self.plotWgt)
        self.censw.addWidget(self.thirdPageWidget)
        self.censw.setCurrentIndex(0)

        self.setCentralWidget(self.censw)

        # Actions
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()
        # menus
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('PorfolioMan')    
        self.showMaximized()

        self.cmdTree.clicked.connect(self.setWidget)
        
        QtCore.QTimer.singleShot(200, self.resetDockWidth)
        
    @QtCore.Slot()
    def setWidget(self,index):
        wgtID = self.cmdmodel.itemFromIndex(index).data(QtCore.Qt.UserRole+1)
        if wgtID == 0:
            self.censw.setCurrentWidget(self.HKWgt)
        elif wgtID==1:
            self.censw.setCurrentWidget(self.plotWgt)
        else:
            self.censw.setCurrentWidget(self.thirdPageWidget)
            
    @QtCore.Slot()
    def resetDockWidth(self):
        self.cmdTree.setMinimumWidth(10)
    
def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
