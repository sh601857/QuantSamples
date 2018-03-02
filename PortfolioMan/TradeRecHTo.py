#coding=utf-8

import pandas as pd
import numpy as np
import xlwings as xw

# wb = xw.Book(r'C:\Users\SFF\Documents\table.xls')  Administrator
# sht = wb.sheets['table']
# print( sht.range("D2").value )

fpath = 'C:\\Users\\Administrator\\Documents\\'

account = {'A242096229':'LLFHTo','0243781523':'LLFHTo',}

rec = pd.read_csv(fpath+'table.xls',sep='\t',header=0, index_col=None, dtype={u'股东帐户':str,u'证券代码':str}, encoding='gbk',
      usecols=[u'成交日期',u'证券代码',u'证券名称',u'操作',u'合同编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东帐户'])
rec = rec[ [u'成交日期',u'证券代码',u'证券名称',u'操作',u'合同编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东帐户'] ]
rec[u'合同编号'] = rec.index + 1
rec[u'股东帐户'] = rec[u'股东帐户'].map( lambda x: account[x] )
rec.to_csv(fpath+'table.xls', sep=',', index=False, encoding='gbk')
print(rec)