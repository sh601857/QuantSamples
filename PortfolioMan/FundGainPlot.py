#coding=utf-8
import pandas as pd
import numpy as np
from MyMplCanvas import MyMplCanvas
import SinaQuote
from PySide.QtCore import *
from PySide.QtGui import *
import sqlite3
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

class FundGainPlotWgt(QWidget):
    def __init__(self):
        super(FundGainPlotWgt, self).__init__()     
        self.initUI()
        self._funds=[]
        self._ylim = [100.0,110.0]

    def initUI(self):
        # generate the plot
             
        self.canvas = MyMplCanvas(self, width=5, height=4) 
        self.ax1 = self.canvas.fig.add_axes( [0.0, 0.04, 0.95, 0.95], facecolor=(.94,.94,.94))
        self.ax1.tick_params('y', labelright = True ,labelleft = False )
        
        hlayout = QHBoxLayout()
        self.cbFund = QComboBox()
        self.cbFund.setMaxVisibleItems(60)
        self._loadComBoxes()
        self.sdate = QDateEdit( QDate(2016,12,30) )
        self.sdate.setDisplayFormat('yyyy-MM-dd')
        self.edate = QDateEdit(QDate.currentDate())
        self.edate.setDisplayFormat('yyyy-MM-dd')
        
        addBtn = QPushButton('Add')
        addBtn.clicked.connect( self.addFund )
        clearBtn = QPushButton('Clear')
        clearBtn.clicked.connect( self.clearFunds) 
        importBtn = QPushButton('Import')
        importBtn.clicked.connect( self.importFundCodes) 
        
        hlayout.addStretch()
        hlayout.addWidget(importBtn)
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
        ysticks = [100]
        ys = 110
        while ys < self._ylim[1]: 
            ysticks.append(ys)
            ys=ys*1.1
        ys = 90	
        while ys > self._ylim[0]: 
            ysticks.append(ys)
            ys=ys*0.9
        ysticks.sort()
        self.ax1.set_yscale(u'log')
        self.ax1.set_ylim(self._ylim[0],self._ylim[1])
        self.ax1.yaxis.set_ticks(ysticks) 
        self.ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
        self.ax1.yaxis.grid(True,color='0.6', linestyle='-', linewidth=0.5)
        self.ax1.set_xlim(xlim[0],xlim[1])
       
        #self.canvas.fig.autofmt_xdate()
        self.canvas.draw_idle()
        self._funds.append(secID)
        
       
    @Slot()    
    def clearFunds(self) :
        self._funds.clear()
        self.ax1.clear()
        self._ylim = [100.0,110.0]
        self.canvas.draw_idle()
        pass
    
    @Slot()                
    def importFundCodes(self) :
        fileName = QFileDialog.getOpenFileName( self, self.tr("Import csv"), "", ("csv Files (*.csv)") ) [0]
        if fileName == '' :
            return        
        conn = sqlite3.connect('FundDB.db')
        cursor = conn.cursor()  
        
        with open(fileName, newline='', encoding='gb2312') as f:
            reader = csv.reader(f)
            i=int(0)
            records=int(0)
            tableName = ''
            sql=''
            for row in reader:
                if i==0 : # row[0]   table name
                    tableName = row[0]
                    i = i+1
                    if tableName == 'b_fund':     
                        sql = "INSERT OR REPLACE INTO b_fund VALUES  (?, ?, ?, ?, ?, ?,?)"
                    else:
                        return

                    continue
                if i==1 : # row[1]   table header
                    i = i+1
                    continue
                if len(row) < 2:
                    continue                                

                if tableName == 'b_fund':     
                    sqltuple = ( row[0], row[1], row[2] if row[2] !='' else None , row[3] if row[3] !='' else None , row[4], row[5] , row[6])
                    cursor.execute(sql,sqltuple)
                    records=records+1                      
                else:
                    return                

            conn.commit()
            QMessageBox.information(self,self.tr('Import csv'), self.tr('[{0}] records imported to [{1}].'.format(records,tableName)) , QMessageBox.Ok)
        conn.close()             
               
        