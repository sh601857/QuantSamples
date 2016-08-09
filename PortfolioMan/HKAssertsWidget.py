#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
from PySide import QtCore
from PySide import QtGui

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

        layout.addWidget(self.tvAsserts)
        layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)      

        saveBtn.clicked.connect(self.save)
        self.loadData()

    def loadData(self):

        if( self.smAsserts.rowCount() >0 ):
            self.smAsserts.removeRows( self.smAsserts.rowCount() )

        conn = sqlite3.connect('HKAsserts.db')
        cursor = conn.cursor()
        try:
            for row in cursor.execute('SELECT Name,Code,tdate,price,SumVollum,cvalue,Cost,Gain FROM v_AssetsOverview ORDER BY cvalue'):
                itemrow =[]
                itemrow.append( QtGui.QStandardItem(row[0]) ) # name
                itemrow.append( QtGui.QStandardItem(row[1]) ) # code
                itemrow.append( QtGui.QStandardItem(row[2]) ) # tdate
                itemrow.append( QtGui.QStandardItem(str(row[3])) ) # price
                itemrow.append( QtGui.QStandardItem(str(row[4])) ) # SumVollum
                itemrow.append( QtGui.QStandardItem(str(row[5])) ) # cvalue
                itemrow.append( QtGui.QStandardItem(str(row[6])) ) # Cost
                itemrow.append( QtGui.QStandardItem(str(row[7])) ) # Gain
                self.smAsserts.appendRow( itemrow )
        except:
            pass       
        conn.close() 

    @QtCore.Slot()
    def save(self):

        pass