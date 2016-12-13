#coding=utf-8
import pandas as pd
import numpy as np
from MyMplCanvas import MyMplCanvas
import SinaQuote
from PySide.QtCore import *
from PySide.QtGui import *
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

class FundGainPlotWgt(QWidget):
    def __init__(self):
        super(FundGainPlotWgt, self).__init__()     
        self.initUI()
        self._funds=[]
        self._ylim = [100.0,200.0]

    def initUI(self):
        # generate the plot
             
        self.canvas = MyMplCanvas(self, width=5, height=4) 
        self.ax1 = self.canvas.fig.add_axes( [0.0, 0.04, 0.95, 0.95], axis_bgcolor=(.94,.94,.94))
        self.ax1.tick_params('y', labelright = True ,labelleft = False )
        
        hlayout = QHBoxLayout()
        self.cbFund = QComboBox()
        self._loadComBoxes()
        self.sdate = QDateEdit( QDate(2014,12,31) )
        self.sdate.setDisplayFormat('yyyy-MM-dd')
        self.edate = QDateEdit(QDate.currentDate())
        self.edate.setDisplayFormat('yyyy-MM-dd')
        
        addBtn = QPushButton('Add')
        addBtn.clicked.connect( self.addFund )
        clearBtn = QPushButton('Clear')
        clearBtn.clicked.connect( self.clearFunds)        
        hlayout.addStretch()
        hlayout.addWidget(self.cbFund)
        hlayout.addWidget(self.sdate)
        hlayout.addWidget(self.edate)
        hlayout.addWidget(addBtn)
        hlayout.addWidget(clearBtn)
        layout =  QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout( hlayout )
        self.setLayout(layout)  
        
    def _loadComBoxes(self)  :
        
        self.cbFund.clear()
        conn = sqlite3.connect('FundDB.db')
        cursor = conn.cursor()         
        for row in  cursor.execute('select SecID, Name, SNo from B_Fund order by SNo'):
            self.cbFund.addItem(row[1], row[0])
        conn.close()        
        self.cbFund.setCurrentIndex(0)
        
    @Slot()    
    def addFund(self) :
        
        secID = self.cbFund.itemData( self.cbFund.currentIndex() )
        if secID in self._funds:
            return        
        npNav = SinaQuote.GetHNav(secID)
        #stsdate = pd.to_datetime( self.sdate.date().toPython() )
        #etsdate =  pd.to_datetime( self.edate.date().toPython() ) 
        stsdate = self.sdate.text()
        etsdate = self.edate.text()        
        npNav = npNav[ npNav.fbrq >=stsdate ]
        npNav = npNav[ npNav.fbrq <=etsdate ]

        npNav.adjNav =  npNav.adjNav / npNav.adjNav[0] *100
        
        self.ax1.plot( pd.to_datetime( npNav.fbrq ), npNav.adjNav , label=self.cbFund.currentText() )
        
        leg = self.ax1.legend(loc=0,fontsize=10,frameon=False)
        leg.get_frame().set_facecolor((.94,.94,.94))
        import matplotlib.dates
        import datetime
        xlim = matplotlib.dates.date2num( [self.sdate.date().toPython(), self.edate.date().toPython()+datetime.timedelta(days=2) ] )
        if np.min( npNav.adjNav ) - 5.0 < self._ylim[0] :
            self._ylim[0] = np.min( npNav.adjNav ) - 5.0 
        if np.max( npNav.adjNav ) + 5.0 > self._ylim[1] :
            self._ylim[1] = np.max( npNav.adjNav ) + 5.0 
            
        self.ax1.set_xlim(xlim[0],xlim[1])
        self.ax1.set_ylim(self._ylim[0],self._ylim[1])
        self.ax1.set_yscale(u'log')
        #self.canvas.fig.autofmt_xdate()
        self.canvas.draw_idle()
        self._funds.append(secID)
        
        
       
    @Slot()    
    def clearFunds(self) :
        self._funds.clear()
        self.ax1.clear()
        self.canvas.draw_idle()
        pass