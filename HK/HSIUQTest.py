# -*- coding: utf-8 -*-

import urllib.request 
import shutil
import csv
import codecs
from datetime import date
import datetime
import sqlite3
import numpy as np
import pandas as pd
import sys

from uqer import Client

kd = pd.read_csv('HKI.csv', index_col=0)
#kd['closeIndexR'] = kd['closeIndex']

kd_HSI = kd.loc[ kd.index[ kd.ticker=='HSI'], :]
kd_HSCEI = kd.loc[ kd.index[ kd.ticker=='HSCEI'],:]


conn = sqlite3.connect(u'D:\\yun\百度云\\PortfolioMan\\dat\\HKI.db')
cursor = conn.cursor()

kd['closeIndexR'] = np.NaN

sql = "select secid, tradedate, closeprice from HKITRI where tradedate>='{0}' order by tradedate".format(  kd.iloc[0,1].replace("-", "") )
hsitri = pd.read_sql( sql, conn )
conn.close()

for i in range(0,len(hsitri)):
    iday = hsitri.loc[i,'tradedate']
    sday = '{0}-{1}-{2}'.format( iday[0:4], iday[4:6] , iday[6:8] )
    if hsitri.loc[i,'secid'] == 'HSI':
        kd_HSI.loc[kd_HSI.tradeDate==sday,'closeIndexR'] = hsitri.loc[i,'closeprice']
    elif hsitri.loc[i,'secid'] == 'HSCEI':
        kd_HSCEI.loc[kd_HSCEI.tradeDate==sday,'closeIndexR'] = hsitri.loc[i,'closeprice']
        
kd_HSI.dropna(subset=['closeIndexR'], inplace=True)
kd_HSCEI.dropna(subset=['closeIndexR'], inplace=True)




mlt = kd_HSCEI.loc[:,'closeIndexR'] / kd_HSCEI.loc[:,'closeIndex']
kd_HSCEI.loc[:,'openIndex'] = kd_HSCEI.loc[:,'openIndex'] * mlt
kd_HSCEI.loc[:,'highestIndex'] = kd_HSCEI.loc[:,'highestIndex'] * mlt   
kd_HSCEI.loc[:,'lowestIndex'] = kd_HSCEI.loc[:,'lowestIndex'] * mlt 
kd_HSCEI.loc[:,'closeIndex'] = kd_HSCEI.loc[:,'closeIndexR'] 

mlt = kd_HSI['closeIndexR'] / kd_HSI.loc[:,'closeIndex']
kd_HSI.loc[:,'openIndex'] = kd_HSI.loc[:,'openIndex'] * mlt
kd_HSI.loc[:,'highestIndex'] = kd_HSI.loc[:,'highestIndex'] * mlt    
kd_HSI.loc[:,'lowestIndex'] = kd_HSI.loc[:,'lowestIndex'] * mlt 
kd_HSI.loc[:,'closeIndex'] = kd_HSI.loc[:,'closeIndexR'] 

#rd = pd.concat([kd_HSCEI, kd_HSI] )
#rd = rd.drop('closeIndexR',axis=1)
#rd.replace({'ticker':'HSI'}, 'SH900998',inplace=True)
#rd.replace({'ticker':'HSCEI'}, 'SH900999',inplace=True)
kd_HSI.drop(['closeIndexR','ticker'],axis=1,inplace=True)
kd_HSCEI.drop(['closeIndexR','ticker'],axis=1,inplace=True)

kd_HSI.to_csv("day/SH900998.txt", header=False, index=False, na_rep='0' , sep= ',',float_format ="%.3f")
kd_HSCEI.to_csv("day/SH900999.txt", header=False, index=False, na_rep='0' , sep= ',',float_format ="%.3f")





