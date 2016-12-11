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

    def initUI(self):
        # generate the plot
             
        self.canvas = MyMplCanvas(self, width=5, height=4) 
        self.ax1 = self.canvas.fig.add_axes( [0.0, 0.04, 0.95, 0.95], axis_bgcolor=(.94,.94,.94))
        self.ax1.tick_params('y', labelright = True ,labelleft = False )
        
        hlayout = QHBoxLayout()
        self.cbFund = QComboBox()
        self._loadComBoxes()
        self.sdate = QDateEdit( QDate(2014,12,31) )
        self.edate = QDateEdit(QDate.currentDate())
        
        
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
        hnav = SinaQuote.GetHNav(secID)
        hnav.sort_values(by='fbrq',inplace=True)
        #hnav.set_index('fbrq', inplace=True)
        
        hnav['FADJ_Nav']=SinaQuote.FundAdjNaV(hnav['jjjz'].values,hnav['ljjz'].values) 
        #print(hnav)
        npNav = hnav.values        
        #npNav.dtype.names = ('fbrq','jjjz','ljjz','FADJ_Nav')

        stsdate = pd.Timestamp( self.sdate.date().toPython() )
        etsdate =  pd.Timestamp( self.edate.date().toPython() )   

        npNav = npNav[ npNav[:,0] >= stsdate  ]
        npNav = npNav[ npNav[:,0] <= etsdate  ]
        npNav[:,3] = npNav[:,3] / npNav[0,3] *100
        
        self.ax1.plot( npNav[:,0], npNav[:,3] , label=self.cbFund.currentText() )
        leg = self.ax1.legend(loc=0,fontsize=10,frameon=False)
        leg.get_frame().set_facecolor((.94,.94,.94))
        self.canvas.draw_idle()
        self._funds.append(secID)
       
    @Slot()    
    def clearFunds(self) :
        self._funds.clear()
        self.ax1.clear()
        self.canvas.draw_idle()
        pass