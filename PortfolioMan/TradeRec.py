#coding=utf-8

import pandas as pd
import numpy as np
import xlwings as xw

# wb = xw.Book(r'C:\Users\SFF\Documents\table.xls')  Administrator
# sht = wb.sheets['table']
# print( sht.range("D2").value )

account = {'A764440052':'HHXHT','0162754560':'HHXHT', 'A760709852':'SFFHT','0162391596':'SFFHT','A103762289':'HYJHT','0124806514':'HYJHT',
'A733917349':'HTSWP','0221666359':'HTSWP','A733919236':'JAXHT','0221666518':'JAXHT','C115038475':'HYJHB','2010504448':'HYJHB'}

rec = pd.read_csv(r'C:\Users\Administrator\Documents\table.xls',sep='\t',header=0, index_col=None, dtype={u'股东帐户':str,u'证券代码':str}, encoding='gbk',
      usecols=[u'成交日期',u'证券代码',u'证券名称',u'摘要',u'合同编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东帐户'])
rec = rec[ [u'成交日期',u'证券代码',u'证券名称',u'摘要',u'合同编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东帐户'] ]
rec[u'合同编号'] = rec.index + 1
rec[u'股东帐户'] = rec[u'股东帐户'].map( lambda x: account[x] )
rec.to_csv(r'C:\Users\Administrator\Documents\table.xls', sep=',', index=False, encoding='gbk')
print(rec)