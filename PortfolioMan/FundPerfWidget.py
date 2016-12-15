from PySide.QtCore import *
from PySide.QtGui import *
import pandas as pd
import numpy as np
import sqlite3
import SinaQuote


def FundPerfModel(QAbstractTableModel):
    def __init__(self):
        super(FundPerfModel, self).__init__()
        self._dfData = PD.DataFrame()
        
    def rowCount(self, parent = QModelIndex()):
        return len(self._dfData)

    def columnCount(self, parent = QModelIndex()):
        return 8

    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() == False:
            return None #QVariant()
        if role == Qt.DisplayRole:
            return None #QVariant()
        elif role == Qt.EditRole:
            return None #QVariant()
        elif role == Qt.TextAlignmentRole:
            if index.column() > 0:
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
                return return None #QVariant()
        else:
            if role == Qt.DisplayRole :
                return section+1
        return None

    def loadData(self, data ):
        self.beginResetModel()
        self._dfData = data      
        self.endResetModel()    



def FundPerfWidget(QWidget):
    def __init__(self):
        super(FundPerfWidget, self).__init__()     
        self.initUI()


    def initUI(self):
        # generate the plot    