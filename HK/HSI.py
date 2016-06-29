import urllib.request 
import shutil
import csv
import codecs
from datetime import date
import sqlite3
import numpy as np
import matplotlib.finance as finance
import matplotlib.mlab as mlab
import sys


server = 'HKI.db'

startdate = date(2016,6,1)
enddate = date(2016,6,30)

fh = finance.fetch_historical_yahoo('^HSCE', startdate, enddate)#, cachename=ticker + '.csv'
# a numpy record array with fields: date, open, high, low, close, volume, adj_close)

r = mlab.csv2rec(fh); fh.close()
r.sort()
r=r[r.volume>0]



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


for tday in r.date :
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
                inserted=inserted+1
            if( len(row) > 4 and u'Hang Seng China Enterprises Index Total Return Index' in row[1] ):
                sqllist=[]
                sqllist.append(u'HSCEI')
                sqllist.append(tday.strftime('%Y%m%d'))
                sqllist.append(float(row[3]))
                sqltuple=tuple(sqllist)
                cursor.execute(sql,sqltuple)	
                inserted=inserted+1
            if( inserted>=2 ):
                break

conn.commit()			
conn.close()