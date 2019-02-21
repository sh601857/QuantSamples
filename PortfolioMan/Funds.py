#coding=utf-8
# tpomcuvnmu 
# 501038 166024 501049 （即将上市交易） 封闭2年的创新型杠杆封基163417
import pandas as pd
import numpy as np
import xlwings as xw
import SinaQuote
import fundEM
import time
wb = xw.Book(u'D:\\yun\\百度云\\FinExcels\\Funds.xlsm')
sht = wb.sheets['Nav']

src = 0  #0  4 

for i in range(3,1000):    
    code=sht.range('A{0}'.format(i)).value

    if code != None:
        print(code)
        if src == 0:
            tpNav = SinaQuote.GetNav( code[2:] )
        else:
            if i%3 == 1:
                time.sleep(0.5)
            tpNav = fundEM.GetNav( code[2:] )
            sht.range((i,6+src)).value = tpNav[4]
        if tpNav != None:
            sht.range((i,3+src)).value = tpNav[1]
            sht.range((i,4+src)).value = tpNav[2]
            sht.range((i,5+src)).value = tpNav[3]

    else:
        break
        
        

#wb.save()     
#wb.close()  

