#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3
from PySide import QtCore
from PySide import QtGui

class HSTradesWidget(QtGui.QWidget):
    def __init__(self):
        super(HSTradesWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
        
        self.tvAsserts = QtGui.QTableView()
        self.smAsserts = QtGui.QStandardItemModel(self.tvAsserts)
        self.smAsserts.setColumnCount(7)
        self.smAsserts.setHorizontalHeaderLabels(['Tdate', 'Code', 'Name', 'Operate', 'No', 'Price', 'Vollum'])
        self.tvAsserts.setModel(self.smAsserts)        

        queryBtn = QtGui.QPushButton(self.tr("Query")) 
        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttonBox.addButton(queryBtn, QtGui.QDialogButtonBox.ActionRole)
        
        layout =  QtGui.QVBoxLayout()        
        self.tvAsserts.setSizePolicy( QtGui.QSizePolicy.Policy.Expanding, QtGui.QSizePolicy.Policy.Expanding )
        layout.addWidget(self.tvAsserts)
        
        hlayout = QtGui.QHBoxLayout()
        self.cbType = QtGui.QComboBox()
        self.cbSecurity = QtGui.QComboBox() 
        self.cbAccount = QtGui.QComboBox() 
        hlayout.addWidget( self.cbType  )
        hlayout.addWidget( self.cbSecurity  )
        hlayout.addWidget( self.cbAccount  )
        hlayout.addWidget( buttonBox )
        layout.addLayout( hlayout )
        self.setLayout(layout) 
        
        self.initComboBoxes()
        
        
        queryBtn.clicked.connect(self.queryData)
        self.cbType.activated.connect(self.loadSecurity)
    @QtCore.Slot()
    def queryData(self):
        
        if( self.smAsserts.rowCount() >0 ):
            self.smAsserts.removeRows(0, self.smAsserts.rowCount() )
            
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor() 
        sql = "select t.TDate, t.Code, c.Name , t.Type, t.TIndex, t.Price, t.Volume from d_trade t , b_code c \
        where t.code = c.code and c.code ='{0}' and t.Account='{1}' \
        order by t.TDate DESC".format( self.cbSecurity.itemData( self.cbSecurity.currentIndex() ) , self.cbAccount.currentText() )   
        
        volList =[]
        tdateList = []
        for row in  cursor.execute(sql):
            itemrow =[]
            itemrow.append( QtGui.QStandardItem(row[0]) ) # TDate                
            itemrow.append( QtGui.QStandardItem(row[1]) ) # Code
            itemrow.append( QtGui.QStandardItem(row[2]) ) # Name
            itemrow.append( QtGui.QStandardItem(row[3]) ) # Type
            itemrow.append( QtGui.QStandardItem(str(row[4])) ) # TIndex
            itemrow.append( QtGui.QStandardItem('{0:.3f}'.format(row[5])) ) # Price
            itemrow.append( QtGui.QStandardItem(str(row[6] ))) # Volume
            self.smAsserts.appendRow( itemrow )
            volList.append(row[6])
            tdateList.append(row[0])
        itemrow =[]
        itemrow.append( QtGui.QStandardItem() ) # TDate                
        itemrow.append( QtGui.QStandardItem() ) # Code
        itemrow.append( QtGui.QStandardItem() ) # Name
        itemrow.append( QtGui.QStandardItem() ) # Type
        itemrow.append( QtGui.QStandardItem() ) # TIndex
        itemrow.append( QtGui.QStandardItem())  # Price
        itemrow.append( QtGui.QStandardItem(str( sum(volList ))) ) # Volume
        self.smAsserts.insertRow(0, itemrow )             
        
        for i in range(0, len(volList)-1):      # 合并同一天的交易
            if tdateList[i] == tdateList[i+1] :
                volList[i+1] = volList[i+1] + volList[i]
                volList[i] = 0
                
        totalSell=0.0                           # 累计卖出量
        for v in volList:
            if v<0 :
                totalSell = totalSell+v
                
        for i in range( len(volList)-1, -1, -1):
            if volList[i] > 0 :
                totalSell = totalSell + volList[i]
                if totalSell > 0  :            # 累计买入超过累计卖出
                    self.smAsserts.item(i+1,0).setBackground( QtGui.QBrush(QtGui.QColor(255, 0, 0, 127)) )
                    self.smAsserts.item(0,0).setText( str( totalSell ) )
                    break
        conn.close()
    @QtCore.Slot()
    def loadSecurity(self,index):
        self.cbSecurity.clear()
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor() 
        sql = "select DISTINCT t.code, c.Name from d_trade t , b_code c where t.code = c.code and c.type ='{0}'".format( self.cbType.itemText(index) )
        for row in  cursor.execute(sql):
            self.cbSecurity.addItem(row[1],row[0])        
        
        conn.close()
        
    def initComboBoxes(self):
        self.cbType.clear()
        self.cbAccount.clear()
        
        conn = sqlite3.connect('HSAsserts.db')
        cursor = conn.cursor() 
        initeType=0
        for row in  cursor.execute('select DISTINCT b.type from d_trade t , b_code b where t.code = b.code'):
            if row[0] == u'股票':
                initeType = self.cbType.count()
            self.cbType.addItem(row[0])
        self.cbType.setCurrentIndex(initeType)
                
        for row in  cursor.execute('select DISTINCT account from d_trade'):
            self.cbAccount.addItem(row[0])
        conn.close()
        self.loadSecurity(initeType)
