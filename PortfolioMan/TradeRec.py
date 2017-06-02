#coding=utf-8

import pandas as pd
import numpy as np
import xlwings as xw

# wb = xw.Book(r'C:\Users\Administrator\Documents\table.xls')
# sht = wb.sheets['table']
# print( sht.range("D2").value )

rec = pd.read_csv(r'C:\Users\Administrator\Documents\table.xls',sep='\t',header=0, index_col=None, encoding='gbk')
res = rec[ [u'成交日期',u'证券代码',u'证券名称',u'摘要',u'合同编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东帐户'] ]
res.to_csv(r'C:\Users\Administrator\Documents\table.xls', sep=',', index=False, encoding='gbk')
print(res)