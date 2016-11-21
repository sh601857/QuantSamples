#coding=utf-8

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates
import sqlite3
import os, re

def str2float(str):
    newstr = str.replace(',', '' )
    try:
        x = float(newstr)
    except ValueError:
        x = float('NaN') 
    return x

def GetStk_Holder_Count(stockCode):

    URL = "http://stock.finance.qq.com/corp1/stk_holder_count.php?zqdm=" + stockCode
    response = urllib.request.urlopen(URL)
    page = response.read().decode('gb2312') 

    soup = BeautifulSoup(page,'lxml')

    tables = soup.findAll('table')
    tab = tables[1]
    rows = tab.findAll('tr')
    th = ['Date','Holders','SharesPerHolder','TotalShares','CircuShares']   
#   for td in rows[0].findAll('td'):
#       th.append(td.getText())
    date=[]
    holders=[]
    sharesPer=[]
    totalS=[]
    circuS=[]
    for tr in rows[1:]:
        tds = tr.findAll('td')
        date.append( pd.Timestamp( tds[0].getText() ) )
        holders.append( str2float(tds[1].getText() ) )
        sharesPer.append( str2float( tds[2].getText() ) )
        totalS.append( str2float( tds[3].getText() ) )
        circuS.append( str2float( tds[4].getText() ) )
    ret = pd.DataFrame({ 'Holders' : holders,
                         'SharesPerHolder' : sharesPer,
                         'TotalShares'  : totalS,
                         'CircuShares' :circuS
                         },index=date )  

    return ret

stock = '601318'
ret = GetStk_Holder_Count(stock)
if len(ret) >0 :
    conn = sqlite3.connect('StockDB.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Stock_Holders (
        SecID text NOT NULL,
        RepDate text,
        Holders real,
        SharesPerHolder real,
        TotalShares real,
        CircuShares real,
        PRIMARY KEY (SecID, RepDate)
        )
    """)
    
    sql = "INSERT OR IGNORE INTO Stock_Holders VALUES (?, ?, ?, ?, ?, ?)"
    sqltuplelist = []
    for r in range(len(ret)):
        sqltuplelist.append( (stock, ret.index[r].strftime('%Y-%m-%d'), ret.ix[r,'Holders'], ret.ix[r,'SharesPerHolder'], 
                                   ret.ix[r,'TotalShares'], ret.ix[r,'CircuShares'] ) )
    cursor.executemany(sql, sqltuplelist)
    conn.commit()			
    conn.close()

ret['Holders'] =ret['Holders']/10000
ax1=ret['Holders'].plot( marker='o',figsize=(18,10) )
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
ax1.xaxis.set_tick_params(width=2,size=8,which='major')
ax1.xaxis.set_tick_params(width=1,size=4,which='minor')   
plt.setp(ax1.get_xticklabels(), rotation=0, horizontalalignment='left')

ax1.xaxis.set_minor_locator(matplotlib.dates.MonthLocator(bymonthday=-1, interval=3))
#ax1.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter(''))

plt.title(stock+'Holders')
plt.tight_layout()
plt.show()

