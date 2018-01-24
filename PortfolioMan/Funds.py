#coding=utf-8
# tpomcuvnmu 
# 501038 166024 501049 （即将上市交易） 封闭2年的创新型杠杆封基163417
import pandas as pd
import numpy as np
import xlwings as xw
import SinaQuote

wb = xw.Book(u'D:\\yun\\百度云\\FinExcels\\Funds.xlsm')
sht = wb.sheets['Nav']

for i in range(3,1000):    
    code=sht.range('A{0}'.format(i)).value
    if code != None:
        tpNav = SinaQuote.GetNav( code[2:] )
        if tpNav != None:
            sht.range((i,3)).value = tpNav[1]
            sht.range((i,4)).value = tpNav[2]
            sht.range((i,5)).value = tpNav[3]
    else:
        break    
#wb.save()     
#wb.close()  

