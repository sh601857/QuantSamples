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
        updateBtn = QtGui.QPushButton(self.tr("Update"))      
    
        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
    
        buttonBox.addButton(importBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quoteBtn, QtGui.QDialogButtonBox.ActionRole)
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
        
        self.loadData()
        
    @QtCore.Slot()
    def loadData(self):
        pass
    
    
    @QtCore.Slot()
    def importT(self):    
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Import csv"), "", ("csv Files (*.csv)") ) [0]
    
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
                    sqltuple = ( row[0],row[1],row[2],row[3],row[4],row[5],row[6] )
                    cursor.execute(sql,sqltuple)
                    records=records+1                      
                else:
                    return                
                
            conn.commit()
            QtGui.QMessageBox.information(self,self.tr('Import csv'), self.tr('[{0}] records imported to [{1}].'.format(records,tableName)) , QtGui.QMessageBox.Ok)
        conn.close()             
    
    @QtCore.Slot()
    def quotes(self):
        pass