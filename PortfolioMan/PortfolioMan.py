#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
from PySide import QtCore
from PySide import QtGui
import HKAssertsWidget
import HSAssertsWidget
import HSTradesWidget
import PlotWidget
import FundGainPlot

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
            
        self._createDockCMDTree()
        self._createCentralWgt()

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
        
    def _createDockCMDTree(self):
        # create commonds tree 
        def createItem( itemData ):
            item = QtGui.QStandardItem( itemData['text'] )
            item.setData(itemData['ID'], QtCore.Qt.UserRole+1)
            item.setFlags( itemData['Flags'] )
            return item
        
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()
        
        item = createItem({'text':'1.HS Stock','ID':10,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, })
        item.appendRow( createItem({'text':'Asserts','ID':10,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'Trades','ID':11,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        parentItem.appendRow(item)        

        item = createItem({'text':'2.HK Stock','ID':20,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, })
        item.appendRow( createItem({'text':'Asserts','ID':20,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'AH','ID':22,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'Plot','ID':21,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        parentItem.appendRow(item)  

        item = createItem({'text':'3.Fund','ID':30,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, })
        item.appendRow( createItem({'text':'Performance','ID':30,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
        item.appendRow( createItem({'text':'Plot','ID':31,'Flags': QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled, }) )
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
        
    
    def _createCentralWgt(self):
        #Create central widget			
        self.HKWgt =  HKAssertsWidget.HKAssertsWidget()
        self.plotWgt = PlotWidget.PlotWidget()  # QtGui.QWidget()
        self.HSAWgt = HSAssertsWidget.HSAssertsWidget()
        self.HSTradeWgt = HSTradesWidget.HSTradesWidget()
        self.thirdPageWidget =  QtGui.QWidget()
        self.fundGainPlotWidget = FundGainPlot.FundGainPlotWgt()
    
        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.HSAWgt)
        self.censw.addWidget(self.HSTradeWgt)
        self.censw.addWidget(self.HKWgt)
        self.censw.addWidget(self.plotWgt)
        self.censw.addWidget(self.fundGainPlotWidget)
        
        self.censw.addWidget(self.thirdPageWidget)
        self.censw.setCurrentIndex(0)
        self._curWgtID = 10
        self.setCentralWidget(self.censw)        
    
    def setCensWgt(self,wgtID):
        if wgtID == 20:
            self.censw.setCurrentWidget(self.HKWgt)
        elif wgtID==21:
            self.censw.setCurrentWidget(self.plotWgt)
        elif wgtID == 10:
            self.censw.setCurrentWidget(self.HSAWgt)
        elif wgtID == 11:
            self.censw.setCurrentWidget(self.HSTradeWgt)
        elif wgtID == 31:
            self.censw.setCurrentWidget(self.fundGainPlotWidget)    
        else:
            self.censw.setCurrentWidget(self.thirdPageWidget)
            
        self._curWgtID = wgtID    
    
    @QtCore.Slot()
    def setWidget(self,index):
        wgtID = self.cmdmodel.itemFromIndex(index).data(QtCore.Qt.UserRole+1)
        if( self._curWgtID != wgtID):        
            self.setCensWgt(wgtID)
            
    @QtCore.Slot()
    def resetDockWidth(self):
        self.cmdTree.setMinimumWidth(10)
    
def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
