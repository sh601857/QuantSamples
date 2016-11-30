# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import talib as ta
import math



hkd = pd.read_csv('HKRawQ/HKD2CNY.csv', index_col=[0] ,delimiter=',')

tickers = ['00811','00939','00998','01288','01339','01398','01918','01988',
           '02318','02328','02883','03328','03618','03899','03968','03988','06818']

for ticker in tickers:
    quote = pd.read_csv('HKRawQ/{0}.csv'.format(ticker), index_col=[0] ,delimiter=',',encoding='gbk')
    
    # 复权并转换为人民币价格
    dat = pd.merge( quote , hkd, on='tradeDate', how='left' )
    dat.sort_values(by='tradeDate' , ascending=True, inplace=True)
    
    # 开盘价修复
    for i in range(len(dat)):
        if dat.iloc[i,4] < 0.001 or math.isnan(dat.iloc[i,4]):
            dat.iloc[i,4] = dat.iloc[i,2]
    dat['midRate'].fillna(method='pad', inplace=True)
    dat.dropna(axis=0,inplace = True)
    dat['FFQM'] = 1.0
    
    nadat = dat.as_matrix( columns=['FFQM','preClosePrice','actPreClosePrice','openPrice','highestPrice','lowestPrice','closePrice','turnoverVol','turnoverValue','midRate'])
    
    #复权
    #for i in range(len(nadat)-2, -1, -1):
    #    nadat[i,0] = nadat[i+1,0] * nadat[i+1,1] / nadat[i+1,2]
    
    nadat[:,0] = nadat[:,0] * nadat[:,-1]
    
    
    for col in range(3, 7):
        nadat[:,col] = nadat[:,col] * nadat[:,0]
    
    ddd = pd.concat([dat['tradeDate'], pd.DataFrame(data=nadat[:,3:9], index=dat.index, 
                                                   columns=['openPrice','highestPrice','lowestPrice','closePrice','turnoverVol','turnoverValue']) ], axis=1)
    ddd.to_csv('HKQuotes/HK{0}.txt'.format(ticker),
              header=False, index=False,float_format="%.3f", date_format='%Y-%m-%d',encoding='gbk')
    

	
tickers = ['00966','01177']
for ticker in tickers:
    quote = pd.read_csv('HKRawQ/{0}.csv'.format(ticker), index_col=[0] ,delimiter=',',encoding='gbk')
    
    # 复权并转换为人民币价格
    dat = pd.merge( quote , hkd, on='tradeDate', how='left' )
    dat.sort_values(by='tradeDate' , ascending=True, inplace=True)
    
    # 开盘价修复
    for i in range(len(dat)):
        if dat.iloc[i,4] < 0.001 or math.isnan(dat.iloc[i,4]):
            dat.iloc[i,4] = dat.iloc[i,2]
    dat['midRate'].fillna(method='pad', inplace=True)
    dat.dropna(axis=0,inplace = True)
    dat['FFQM'] = 1.0
    
    nadat = dat.as_matrix( columns=['FFQM','preClosePrice','actPreClosePrice','openPrice','highestPrice','lowestPrice','closePrice','turnoverVol','turnoverValue','midRate'])
    
    #复权
    for i in range(len(nadat)-2, -1, -1):
        nadat[i,0] = nadat[i+1,0] * nadat[i+1,1] / nadat[i+1,2]
    
    nadat[:,0] = nadat[:,0] * nadat[:,-1]
      
    for col in range(3, 7):
        nadat[:,col] = nadat[:,col] * nadat[:,0]
    
    ddd = pd.concat([dat['tradeDate'], pd.DataFrame(data=nadat[:,3:9], index=dat.index, 
                                                   columns=['openPrice','highestPrice','lowestPrice','closePrice','turnoverVol','turnoverValue']) ], axis=1)
    ddd.to_csv('HKQuotes/HK{0}.txt'.format(ticker),
              header=False, index=False,float_format="%.3f", date_format='%Y-%m-%d',encoding='gbk')