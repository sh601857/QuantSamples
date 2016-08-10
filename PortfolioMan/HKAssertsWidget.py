#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
from PySide import QtCore
from PySide import QtGui
import csv
import SinaQuote

class HKAssertsWidget(QtGui.QWidget):

    def __init__(self):
        super(HKAssertsWidget, self).__init__()     
        self.initUI()

    def initUI(self): 

        self.tvAsserts = QtGui.QTableView()
        self.smAsserts = QtGui.QStandardItemModel(self.tvAsserts)
        self.smAsserts.setColumnCount(8)
        self.smAsserts.setHorizontalHeaderLabels(['Name','Code','Tdate','Price','SumVollum','cvalue','Cost','Gain'])
        self.tvAsserts.setModel(self.smAsserts)

        importBtn = QtGui.QPushButton(self.tr("Import"))
        quoteBtn = QtGui.QPushButton(self.tr("Quotes"))
        updateBtn = QtGui.QPushButton(self.tr("Update"))      
        saveBtn = QtGui.QPushButton(self.tr("Save"))

        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)

        buttonBox.addButton(importBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quoteBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(saveBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(updateBtn, QtGui.QDialogButtonBox.ActionRole) 

        layout =  QtGui.QVBoxLayout()        
        self.tvAsserts.setSizePolicy( QtGui.QSizePolicy.Policy.Expanding, QtGui.QSizePolicy.Policy.Expanding )
        layout.addWidget(self.tvAsserts)
        #layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)      
        updateBtn.clicked.connect(self.loadData)
        saveBtn.clicked.connect(self.save)
        importBtn.clicked.connect(self.importT)
        quoteBtn.clicked.connect(self.quotes)
        
        self.loadData()
        
    @QtCore.Slot()
    def loadData(self):

        if( self.smAsserts.rowCount() >0 ):
            self.smAsserts.removeRows(0, self.smAsserts.rowCount() )

        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()
        hkd2rmb = 0.85773
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
                    cvalue = row[5] * hkd2rmb
                else:
                    cvalue = row[5]
                totalCV = totalCV + cvalue
                totalCost = totalCost + row[6]
                itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(cvalue)) ) # cvalue
                itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(row[6])) ) # Cost
                itemrow.append( QtGui.QStandardItem('{0:.2f}'.format(cvalue + row[6])) ) # Gain
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
            self.smAsserts.insertRow(0, itemrow )  
            
        except:
            pass       
        conn.close() 
        
    @QtCore.Slot()
    def importT(self):
        
        
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Import trades"), "", ("csv Files (*.csv)") ) [0]
        
        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()
        sql = "INSERT OR REPLACE INTO D_Trade VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        
        with open(fileName, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            i=0
            for row in reader:
                if i == 0 : 
                    i=i+1
                    continue
                if len(row)< 15 :
                    continue
                sqllist = ( row[1],row[0],row[15],row[3],row[5],row[4],row[14],row[7] )
                cursor.execute(sql,sqllist)
            conn.commit()
        conn.close()                
        pass
    
    @QtCore.Slot()
    def quotes(self):
        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()        
        stocks=''
        for row in cursor.execute("select Code,TradeMarket from b_code where Enable=1"):
            if( stocks == ''):
                stocks = row[1]+row[0]
            else:
                stocks = stocks + ',' + row[1]+row[0]
            
            
        qd = SinaQuote.GetQuote( stocks )
        sql = "INSERT OR REPLACE INTO D_LatestQuote VALUES (?, ?, ?)"
        for i in range( len(qd) ):
            sqltuple = (qd.iloc[i]['code'][2:] , qd.iloc[i]['datetime'].strftime('%Y-%m-%d%H:%M:%S'), str(qd.iloc[i]['C']) )
            cursor.execute(sql,sqltuple)
        conn.commit()                
        conn.close()  
        
    @QtCore.Slot()
    def save(self):

        pass