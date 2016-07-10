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

kd = pd.read_csv('HKI.csv', index_col=0)
kd['closeIndexR'] = kd['closeIndex']
kd_HSI = kd[kd.ticker=='HSI']
kd_HSCEI = kd[kd.ticker=='HSCEI']


conn = sqlite3.connect('HKI.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS HKITRI (
    secid text NOT NULL,
    tradedate text,
    closeprice real,
    PRIMARY KEY (secid,tradedate)
    )
""")

sql = "INSERT OR IGNORE INTO HKITRI VALUES (?, ?, ?)"

for sday in kd_HSI.tradeDate.values: #r.date :
    tday = datetime.datetime.strptime(sday, '%Y-%m-%d')
    file = 'idx_{0}{1}.csv'.format(tday.day, tday.strftime('%b%y'))
    cash ='temp.csv'
    url = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hstri/' + file
    print ('downloading {0} with urllib'.format(tday.strftime('%d%b%y')))
    try:    
        with urllib.request.urlopen(url) as response, open(cash, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        continue
    
    with codecs.open(cash, encoding='utf-16-le') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_ALL)
        inserted=0
        for row in spamreader:
            if( len(row) > 4 and u'Hang Seng Index Total Return Index' in row[1] ):
                sqllist=[]
                sqllist.append(u'HSI')
                sqllist.append(tday.strftime('%Y%m%d'))
                sqllist.append(float(row[3]))
                sqltuple=tuple(sqllist)
                cursor.execute(sql,sqltuple)
                kd_HSI.loc[kd_HSI.tradeDate==sday,'closeIndexR'] = sqllist[2]
                inserted=inserted+1
            if( len(row) > 4 and u'Hang Seng China Enterprises Index Total Return Index' in row[1] ):
                sqllist=[]
                sqllist.append(u'HSCEI')
                sqllist.append(tday.strftime('%Y%m%d'))
                sqllist.append(float(row[3]))
                sqltuple=tuple(sqllist)
                cursor.execute(sql,sqltuple)
                kd_HSCEI.loc[kd_HSCEI.tradeDate==sday,'closeIndexR'] = sqllist[2]
                inserted=inserted+1
            if( inserted>=2 ):
                break

conn.commit()			
conn.close()
mlt = kd_HSCEI['closeIndexR'] / kd_HSCEI['closeIndex']
kd_HSCEI['openIndex'] = kd_HSCEI['openIndex'] * mlt
kd_HSCEI['highestIndex'] = kd_HSCEI['highestIndex'] * mlt   
kd_HSCEI['lowestIndex'] = kd_HSCEI['lowestIndex'] * mlt 
kd_HSCEI['closeIndex'] = kd_HSCEI['closeIndexR'] 

mlt = kd_HSI['closeIndexR'] / kd_HSI['closeIndex']
kd_HSI['openIndex'] = kd_HSI['openIndex'] * mlt
kd_HSI['highestIndex'] = kd_HSI['highestIndex'] * mlt    
kd_HSI['lowestIndex'] = kd_HSI['lowestIndex'] * mlt 
kd_HSI['closeIndex'] = kd_HSI['closeIndexR'] 

rd = pd.concat([kd_HSCEI, kd_HSI] )
rd = rd.drop('closeIndexR',axis=1)
rd.replace({'ticker':'HSI'}, 'SH900998',inplace=True)
rd.replace({'ticker':'HSCEI'}, 'SH900999',inplace=True)
print(rd)

rd.to_csv("day/Day.txt", header=False, index=False, na_rep='0' , sep= ' ',float_format ="%.2f")




