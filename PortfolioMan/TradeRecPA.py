#coding=utf-8

import pandas as pd
import numpy as np
import xlwings as xw

# wb = xw.Book(r'C:\Users\SFF\Documents\table.xls')  Administrator
# sht = wb.sheets['table']
# print( sht.range("D2").value )

fpath = 'C:\\Users\\Administrator\\Documents\\'

with open( fpath+'wt.xls', 'r', encoding='gbk') as fpr: 
    content = fpr.read() 
content = content.replace('=', '') 
with open(fpath+'wt1.xls', 'w', encoding='gbk') as fpw: 
    fpw.write(content)

account = {'A455111089':'HYJPA','0124806514':'HYJPA','A106398983':'SFFPA','0162391596':'SFFPA'}

rec = pd.read_csv(fpath+'wt1.xls',sep='\t',header=0, index_col=None,  encoding='gbk', dtype={u'股东代码':str,u'证券代码':str},
       usecols=[u'发生日期',u'证券代码',u'证券名称',u'业务名称',u'委托编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东代码'])
rec = rec[ [u'发生日期',u'证券代码',u'证券名称',u'业务名称',u'委托编号',u'成交均价',u'成交数量',u'成交金额',u'发生金额',u'股东代码'] ]
rec.dropna(subset=[u'股东代码'],inplace=True)

for i in range( len(rec) ):
    if u'卖出' in rec.iloc[i,3]:
        rec.iloc[i,6] = - rec.iloc[i,6] 
    rec.iloc[i,4] = i+10001 		
rec[u'股东代码'] = rec[u'股东代码'].map( lambda x: account[x] )
rec[u'发生日期'] = rec[u'发生日期'].map( lambda x: x.replace(u'-', '')  )
rec[u'业务名称'] = rec[u'业务名称'].map( lambda x: x.replace(u'清算', '')  )

rec.to_csv(fpath+'table.xls', sep=',', index=False, encoding='gbk')
print(rec)