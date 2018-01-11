#coding=utf-8
# tpomcuvnmu 
# 501038 166024 501049 （即将上市交易） 封闭2年的创新型杠杆封基163417
import pandas as pd
import numpy as np
import xlwings as xw
import SinaQuote

wb = xw.Book('Funds.xlsx')
sht = wb.sheets['FundPerf']

for i in range(2,1000):    
    code=sht.range('B{0}'.format(i)).value
    if code != None:
        npNav = SinaQuote.GetHNav( code[2:] )
        if len(npNav) > 1:
            sht.range((i,4)).value = npNav.fbrq[-1]
            sht.range((i,5)).value = npNav.adjNav[-1] / npNav.adjNav[-2] - 1.0
        for j in range(6,20):
            bdate = sht.range((1,j)).value
            if bdate != None:
                begNav = npNav[ npNav.fbrq ==bdate ]
                if len(begNav) > 0:
                    sht.range((i,j)).value = npNav.adjNav[-1] / begNav.adjNav[0] - 1.0
                pass
            else:
                break
    else:
        break    
#wb.save()     
#wb.close()  

