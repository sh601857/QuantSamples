#coding=utf-8

from PySide.QtCore import *
from PySide.QtGui import *
import xlwings as xw
import pandas as pd
import numpy as np

import XueQiuQuote

d = { 'Code':['02601','01336'] ,
      'Name':[u'中国太保',u'新华保险'],
      'Price':[None,None],'Pct':[None,None],'PE_TTM':[None,None],'PB':[None,None],'TShares':[None,None],'HShares':[None,None],
      }

_headers = ['Code','Name','Price','Pct','PE_TTM','PB','TShares','HShares']
class AHQuoteModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(AHQuoteModel, self).__init__(parent)
        self._dfData = pd.DataFrame()
        
    def rowCount(self, parent = QModelIndex()):
        return len(self._dfData)

    def columnCount(self, parent = QModelIndex()):
        return len(_headers)

    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() == False:
            return None #QVariant()
        if role == Qt.DisplayRole:
            return str( self._dfData.iloc[index.row(),index.column()] )
        elif role == Qt.EditRole:
            return None #QVariant()
        elif role == Qt.TextAlignmentRole:
            if index.column() > 1:
                return Qt.AlignRight 
            else:
                return Qt.AlignLeft 
        elif role == Qt.ForegroundRole:
            if self.flags(index) & Qt.ItemIsEditable :             
                return QBrush( QColor('#0000FF') )           
        else:
            return None #QVariant()

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole :
            pass
        return True

    def flags(self, index):
        flag = Qt.ItemIsSelectable | Qt.ItemIsEnabled 
        return flag

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal :
            if role == Qt.DisplayRole :
                return _headers[section]
        else:
            if role == Qt.DisplayRole :
                return section+1
        return None

    def loadData(self, data ):
        self.beginResetModel()
        self._dfData = data      
        self.endResetModel()  
        
    @Slot()
    def Quotes(self): 
        tickers=''
        for i in range( len( self._dfData) ):
            if i==0 :
                tickers = self._dfData['Code'][i]
            else:
                tickers = tickers + ',' + self._dfData['Code'][i]
        if tickers != '' :
            qdf = XueQiuQuote.GetHKQuote(tickers) 
            #print(qdf)
            self.beginResetModel()
            for i in range(len( self._dfData)):
                self._dfData.loc[i,'Price'] = qdf.loc[self._dfData.loc[i,'Code'], 'close' ]
                self._dfData.loc[i,'Pct'] = qdf.loc[self._dfData.loc[i,'Code'], 'percentage' ]
                
            self.endResetModel()
            #print (self._dfData )    
        
class AHQuotesWidget(QWidget):
    def __init__(self, parent=None):
        super(AHQuotesWidget, self).__init__(parent)     
        self.initUI()

    def initUI(self): 
        self.tvStocks = QTableView()
        self.tmStocks = AHQuoteModel(self.tvStocks)
        self.tmStocks.loadData( pd.DataFrame(d, columns= _headers) )
        
        self.tvStocks.setModel(self.tmStocks) 
        
        quoteBtn = QPushButton(self.tr("Quotes"))
        quoteBtn.clicked.connect(self.tmStocks.Quotes)
        
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(quoteBtn)
        #hlayout.setContentsMargins(1,1,1,1)
        
        layout =  QVBoxLayout()        
        self.tvStocks.setSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding )
        layout.addWidget(self.tvStocks)           
        layout.addLayout( hlayout )
        self.setLayout(layout) 
        layout.setContentsMargins(1,1,1,1)
        
