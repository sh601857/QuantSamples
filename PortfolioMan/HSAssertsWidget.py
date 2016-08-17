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
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Import trades"), "", ("csv Files (*.csv)") ) [0]
    
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor()        
        
        
        pass
    
    
    @QtCore.Slot()
    def quotes(self):
        pass