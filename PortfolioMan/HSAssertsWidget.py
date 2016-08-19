#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
import urllib.request
from PySide import QtCore
from PySide import QtGui
import csv
import SinaQuote


class HSAssertsWidget(QtGui.QWidget):
    def __init__(self):
        super(HSAssertsWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
        self.tvAsserts = QtGui.QTableView()
        self.smAsserts = QtGui.QStandardItemModel(self.tvAsserts)
        self.smAsserts.setColumnCount(8)
        self.smAsserts.setHorizontalHeaderLabels(['Name','Code','Tdate','Price','SumVollum','CValue','Cost','Gain'])
        self.tvAsserts.setModel(self.smAsserts)
    
        importBtn = QtGui.QPushButton(self.tr("Import"))
        quoteBtn = QtGui.QPushButton(self.tr("Quotes"))
        navBtn = QtGui.QPushButton(self.tr("NetValue"))
        updateBtn = QtGui.QPushButton(self.tr("Update"))      
    
        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
    
        buttonBox.addButton(importBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quoteBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(navBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(updateBtn, QtGui.QDialogButtonBox.ActionRole) 
    
        layout =  QtGui.QVBoxLayout()        
        self.tvAsserts.setSizePolicy( QtGui.QSizePolicy.Policy.Expanding, QtGui.QSizePolicy.Policy.Expanding )
        layout.addWidget(self.tvAsserts)
        hlayout = QtGui.QHBoxLayout()  
        hlayout.addWidget( buttonBox )   
        layout.addLayout( hlayout )
        self.setLayout(layout)      
        updateBtn.clicked.connect(self.loadData)
        importBtn.clicked.connect(self.importT)
        quoteBtn.clicked.connect(self.quotes)        
        navBtn.clicked.connect(self.getNAV)   
        
        self.loadData()
        
    @QtCore.Slot()
    def loadData(self):
        if( self.smAsserts.rowCount() >0 ):
            self.smAsserts.removeRows(0, self.smAsserts.rowCount() )
            
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor()            
        totalCV = 0.0
        totalCost =0.0
        try:
            for row in cursor.execute('SELECT Name,Code,tdate,price,SumVollum,cvalue,Cost,Gain FROM v_AssetsOverview ORDER BY cvalue DESC'):
                itemrow =[]
                itemrow.append( QtGui.QStandardItem(row[0]) ) # name
                itemrow.append( QtGui.QStandardItem(row[1]) ) # code
                itemrow.append( QtGui.QStandardItem(row[2] if row[2] != None else '') ) # tdate
                itemrow.append( QtGui.QStandardItem(str(row[3]) if row[3] != None else '' ) ) # price
                itemrow.append( QtGui.QStandardItem(str(row[4])) ) # SumVollum
                cvalue = row[5] if row[5] != None else 0.0
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
        conn = sqlite3.connect('HSAsserts.db')
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
                if len(row) < 2:
                    continue                
                if tableName == 'D_Trade':

                    sqltuple = ( row[0],row[1],row[4],row[3],row[5],row[6],row[8], abs(abs(float(row[8]))-abs(float(row[7]))) if float(row[7])>0 else 0.0 , row[9] )                       
                    cursor.execute(sql,sqltuple)
                    records=records+1                    
                    
                elif tableName == 'B_Code':     
                    sqltuple = ( row[0],row[1],row[2],row[3] if row[3] !='' else None ,row[4]  if row[4] !='' else None ,row[5]  if row[5] !='' else None ,row[6] )
                    cursor.execute(sql,sqltuple)
                    records=records+1                      
                else:
                    return                
                
            conn.commit()
            QtGui.QMessageBox.information(self,self.tr('Import csv'), self.tr('[{0}] records imported to [{1}].'.format(records,tableName)) , QtGui.QMessageBox.Ok)
        conn.close()             
    
    @QtCore.Slot()
    def quotes(self):
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor()        
        stocks=''                 #select c.Code,TradeMarket from b_code c,v_assets a where c.Enable=1 and c.TradeMarket notnull and a.code= c.code and a.sumvollum !=0  
        for row in cursor.execute("select c.Code,TradeMarket from b_code c where c.Enable=1 and c.TradeMarket notnull "):
            if( stocks == ''):
                stocks = row[1].lower() + row[0]
            else:
                stocks = stocks + ',' + row[1].lower()+row[0]
                
        qd = SinaQuote.GetQuote( stocks )
        #print(qd)
        sql = "INSERT OR REPLACE INTO D_LatestQuote VALUES (?, ?, ?)"
        for i in range( len(qd) ):
            CValue = qd.iloc[i]['C']
            if CValue == 0:
                CValue = qd.iloc[i]['PC']
            sqltuple = (qd.iloc[i]['code'][2:] , qd.iloc[i]['datetime'].strftime('%Y-%m-%d %H:%M:%S'), str(CValue) )
            cursor.execute(sql,sqltuple)
        conn.commit()
        QtGui.QMessageBox.information(self,self.tr('Get Quotes'), self.tr('[{0}] records updated.'.format(i)) , QtGui.QMessageBox.Ok)
        conn.close()  
        
    @QtCore.Slot()    
    def getNAV(self):
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor() 
        navs = []
                                  #select c.Code,TradeMarket from b_code c,v_assets a where c.Enable=1 and c.NetvalueMarket ='OF' and a.code= c.code and a.sumvollum !=0  
        cursor.execute("select c.Code from b_code c where c.Enable=1 and c.NetvalueMarket ='OF'")
        codes = cursor.fetchall() # select c.Code from b_code c where c.Enable=1 and c.NetvalueMarket ='OF'
        progress = QtGui.QProgressDialog("Get Navs...", "Abort", 0, len(codes), self)
        progress.setWindowTitle('PortfoliMan')
        progress.setWindowModality(QtCore.Qt.WindowModal)
        for r in range(len(codes)):              
            fundCode = codes[r][0]
            nav = SinaQuote.GetNav(fundCode)
            if nav != None :
                navs.append( nav )
            progress.setValue(r)
            QtCore.QCoreApplication.processEvents()
            import time
            time.sleep(1)
            if progress.wasCanceled() :
                return
        progress.setValue(len(codes)) 
        
        sql = "INSERT OR REPLACE INTO D_LatestNetvalue VALUES (?, ?, ?, ?)"
        cursor.executemany(sql,navs)
        conn.commit()
        QtGui.QMessageBox.information(self,self.tr('Get Navs'), self.tr('[{0}] records updated.'.format(len(navs))) , QtGui.QMessageBox.Ok)
        conn.close()          
        with open('D_LatestNetvalue.csv', 'w', newline='') as csvfile:
            fieldnames = ['Code', 'Tdate', 'Netvalue','SumNetvalue']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow( dict( Code ='D_LatestNetvalue', Tdate='',Netvalue='',SumNetvalue='' ) )
            writer.writeheader()
            for nav in navs:
                writer.writerow(dict( Code =nav[0], Tdate=nav[1],Netvalue=nav[2],SumNetvalue=nav[3] ))
                

        
