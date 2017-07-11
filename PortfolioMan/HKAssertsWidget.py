#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
import urllib.request
from PySide import QtCore
from PySide import QtGui
import csv
import SinaQuote
import gtimg

class HKAssertsWidget(QtGui.QWidget):

    def __init__(self):
        super(HKAssertsWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
        
        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()
        cursor.execute('select HKD2RMB from d_param' )
        self.hkd2rmb =cursor.fetchone()[0]
        conn.close() 
        #self.hkd2rmb = 0.85773
        self.tvAsserts = QtGui.QTableView()
        self.smAsserts = QtGui.QStandardItemModel(self.tvAsserts)
        self.smAsserts.setColumnCount(8)
        self.smAsserts.setHorizontalHeaderLabels(['Name','Code','Tdate','Price','SumVollum','CValue','Cost','Gain'])
        self.tvAsserts.setModel(self.smAsserts)

        importBtn = QtGui.QPushButton(self.tr("Import"))
        quoteBtn = QtGui.QPushButton(self.tr("Quotes"))
        updateBtn = QtGui.QPushButton(self.tr("Update"))      
        hkd2rmbBtn = QtGui.QPushButton(self.tr("HKD2RMB"))

        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)

        buttonBox.addButton(importBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quoteBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(hkd2rmbBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(updateBtn, QtGui.QDialogButtonBox.ActionRole) 

        layout =  QtGui.QVBoxLayout()        
        self.tvAsserts.setSizePolicy( QtGui.QSizePolicy.Policy.Expanding, QtGui.QSizePolicy.Policy.Expanding )
        layout.addWidget(self.tvAsserts)
        #layout.addStretch()
        hlayout = QtGui.QHBoxLayout()
        self.teHKD = QtGui.QLineEdit()
        self.teHKD.setText( str( self.hkd2rmb ) )
        #self.teHKD.setEnabled( False )

        hlayout.addWidget( QtGui.QLabel('HKD2RMB:') )
        hlayout.addWidget( self.teHKD )
        hlayout.addWidget( buttonBox )

        layout.addLayout( hlayout )
        self.setLayout(layout)      
        updateBtn.clicked.connect(self.loadData)
        hkd2rmbBtn.clicked.connect(self.updatehkd2rmb)
        importBtn.clicked.connect(self.importT)
        quoteBtn.clicked.connect(self.quotes)
        
        self.loadData()
        
    @QtCore.Slot()
    def loadData(self):

        if( self.smAsserts.rowCount() >0 ):
            self.smAsserts.removeRows(0, self.smAsserts.rowCount() )

        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()
        
        totalCV = 0.0
        totalCost =0.0
        try:
            for row in cursor.execute('SELECT Name,Code,tdate,price,SumVollum,cvalue,Cost,Gain FROM v_AssetsOverview ORDER BY cvalue DESC'):
                itemrow =[]
                itemrow.append( QtGui.QStandardItem(row[0]) ) # name
                itemrow.append( QtGui.QStandardItem(row[1]) ) # code
                itemrow.append( QtGui.QStandardItem(row[2]) ) # tdate
                itemrow.append( QtGui.QStandardItem(str(row[3])) ) # price
                itemrow.append( QtGui.QStandardItem(str(row[4])) ) # SumVollum
                if(len(row[1])==5):
                    cvalue = row[5] * self.hkd2rmb
                else:
                    cvalue = row[5]
                totalCV = totalCV + cvalue
                totalCost = totalCost + row[6]
                itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(cvalue)) ) # cvalue
                itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(row[6])) ) # Cost
                itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(cvalue + row[6])) ) # Gain
                for i in range(3,8):
                    itemrow[i].setTextAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter )                
                self.smAsserts.appendRow( itemrow )
            itemrow =[]
            itemrow.append( QtGui.QStandardItem('Total') ) # name                
            itemrow.append( QtGui.QStandardItem() ) # code
            itemrow.append( QtGui.QStandardItem() ) # tdate
            itemrow.append( QtGui.QStandardItem() ) # price
            itemrow.append( QtGui.QStandardItem() ) # SumVollum
            itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(totalCV)) ) # cvalue
            itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(totalCost)) ) # Cost
            itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(totalCV + totalCost)) ) # Gain
            for i in range(3,8):
                itemrow[i].setTextAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter )
            self.smAsserts.insertRow(0, itemrow )  
            self.tvAsserts.resizeColumnToContents( 2 )
        except:
            pass       
        conn.close() 
        
    @QtCore.Slot()
    def importT(self):      
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Import csv"), "", ("csv Files (*.csv)") ) [0]
        if fileName == '' :
            return        
        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()
        
        with open(fileName, newline='', encoding='gb2312') as f:
            reader = csv.reader(f)
            i=int(0)
            records=int(0)
            tableName = ''
            sql=''
            for row in reader:
                if i == 0 : 
                    tableName = row[0]
                    i = i+1
                    if tableName == 'D_Trade':
                        sql = "INSERT OR REPLACE INTO D_Trade VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    elif tableName == 'B_Code':     
                        sql = "INSERT OR REPLACE INTO B_Code VALUES  (?, ?, ?, ?, ?, ?, ?)"
                    else:
                        return
                    continue
                if i==1 : # row[1]   table header
                    i = i+1
                    continue                               
                if tableName == 'D_Trade':
                    if len(row)< 17 :
                        continue                    
                    sqllist = ( row[0],row[1],row[15],row[3],row[4],row[5],row[14],row[7],row[16] )
                    cursor.execute(sql,sqllist)
                    records=records+1
                elif tableName == 'B_Code': 
                    if len(row)< 7 :
                        continue                    
                    sqltuple = ( row[0],row[1],row[2],row[3] if row[3] !='' else None ,row[4]  if row[4] !='' else None ,row[5]  if row[5] !='' else None ,row[6] )
                    cursor.execute(sql,sqltuple)
                    records=records+1                      
                else:
                    return 
                
            conn.commit()
            QtGui.QMessageBox.information(self,self.tr('Import csv'), self.tr('[{0}] records imported to [{1}]'.format(records,tableName)) , QtGui.QMessageBox.Ok)
        conn.close()                
        pass
    
    @QtCore.Slot()
    def quotes(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        
        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()        
        stocks=''
        #for row in cursor.execute("select Code,TradeMarket from b_code where Enable=1"):
            #if( stocks == ''):
                #stocks = row[1]+row[0]
            #else:
                #stocks = stocks + ',' + row[1]+row[0]            
        #qd = SinaQuote.GetQuote( stocks )
        #sql = "INSERT OR REPLACE INTO D_LatestQuote VALUES (?, ?, ?)"
        #for i in range( len(qd) ):
            #sqltuple = (qd.iloc[i]['code'][2:] , qd.iloc[i]['datetime'].strftime('%Y-%m-%d %H:%M:%S'), str(qd.iloc[i]['C']) )
            #cursor.execute(sql,sqltuple)
			
        for row in cursor.execute("select c.Code,TradeMarket from b_code c,v_assets a where c.Enable=1 and c.TradeMarket notnull and a.code= c.code and a.sumvollum !=0 "):
            if( stocks == ''):
                stocks = 'r_' + row[1] + row[0]
            else:
                stocks = stocks + ',r_' + row[1]+row[0]  
                
        qd = gtimg.GetLatestQuoteStock(stocks)
        sql = "INSERT OR REPLACE INTO D_LatestQuote VALUES (?, ?, ?)"
        for i in range( len(qd) ):
            sqltuple = (qd.iloc[i]['code'][2:] , qd.iloc[i]['datetime'].strftime('%Y-%m-%d %H:%M:%S'), str(qd.iloc[i]['C']) )
            cursor.execute(sql,sqltuple)
						
        conn.commit()
        conn.close() 
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.information(self,self.tr('Get Quotes'), self.tr('[{0}] records updated.'.format(i+1)) , QtGui.QMessageBox.Ok)
        
        
    @QtCore.Slot()
    def updatehkd2rmb(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        url = "http://www.sse.com.cn/services/hkexsc/home/"
        urllib.request.urlretrieve(url,'local_filename.html')
        
        f = open('local_filename.html', 'rt', encoding= 'utf-8')      
        for line in f:
            if 'var SELL_PRICE_clear =' in line:
                idoc = line.find('.',10)
                iend = line.find("'",idoc)
                #print( line[idoc-1:iend] )
                self.hkd2rmb = float(line[idoc-1:iend])
                self.teHKD.setText( str( self.hkd2rmb ) )
                conn = sqlite3.connect('HKAsserts.db')
                cursor = conn.cursor()
                cursor.execute('update d_param set HKD2RMB=?' , (self.hkd2rmb,))
                conn.commit()
                conn.close()                 
                QtGui.QApplication.restoreOverrideCursor()
                QtGui.QMessageBox.information(self,self.tr('Update HKD2RMB'), self.tr('HKD2RMB = [{0}].'.format(self.hkd2rmb)) , QtGui.QMessageBox.Ok)
        else:
            QtGui.QApplication.restoreOverrideCursor()