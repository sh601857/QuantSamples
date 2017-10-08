# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import talib as ta
import math
import gtimg


hkd = pd.read_csv('HKRawQ/HKD2CNY.csv', index_col=[0] ,delimiter=',')


usd = pd.read_csv('HKRawQ/USD2CNY.csv', index_col=[0] ,delimiter=',')



tickers = ['00811','00902','00939','00998','01071','01288','01336','01339','01398','01816','01918','01988',
           '02318','02328','02333','02601','02799','02883','03328','03618','03899','03968','03988','06818',
           '00966','01177']


for ticker in tickers:
    quote = gtimg.GetDayKofYear('17', 'hk'+ticker,df=1)
    quote['A'] = quote['C'] * quote['V']
    quote['D'] = quote.apply(lambda row: ( row['D'].decode('gb2312') ), axis = 1)
    quote['D'] = quote.apply(lambda row: ('20{0}-{1}-{2}'.format( row['D'][:2],row['D'][2:4] ,row['D'][4:]) ), axis = 1)    
    #quote = pd.read_csv('HKRawQ/{0}.csv'.format(ticker), index_col=[0] ,delimiter=',',encoding='gbk')

    # 复权并转换为人民币价格
    dat = pd.merge( quote , hkd, left_on='D', right_on='tradeDate', how='left' )
    dat.sort_values(by='D' , ascending=True, inplace=True)

    dat['midRate'].fillna(method='pad', inplace=True)
    dat.drop('tradeDate',axis=1,inplace = True)
    dat.dropna(axis=0,inplace = True)
    
    nadat = dat.as_matrix( columns=['O','H','L','C','V','A','midRate'])
    for col in [0,1,2,3,5]:
        nadat[:,col] = nadat[:,col] * nadat[:,-1]

    ddd = pd.concat([dat['D'], pd.DataFrame(data=nadat[:,:-1], index=dat.index, 
                                                    columns=['O','H','L','C','V','A']) ], axis=1)
    ddd.to_csv('HKQuotes/HK{0}.txt'.format(ticker),
               header=False, index=False,float_format="%.3f", date_format='%Y-%m-%d',encoding='gbk')
    
hkd100 = hkd
hkd100['midRate'] = hkd100['midRate'] * 100
hkd100.to_csv('HKD2CNY.txt',header=False, index=False,float_format="%.3f", date_format='%Y-%m-%d',encoding='gbk')
usd100 = usd
usd100['midRate'] = usd100['midRate'] * 100
usd100.to_csv('USD2CNY.txt',header=False, index=False,float_format="%.3f", date_format='%Y-%m-%d',encoding='gbk')