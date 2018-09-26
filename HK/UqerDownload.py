# -*- coding: utf-8 -*-

from uqer import Client
import pandas as pd

uqer = Client(username='huyijiong@139.com', password='qwe123!@#')

#files = uqer.list_data()
#print(files)
uqer.download_data( 'HKI.csv' )
uqer.download_data( filename='HKRawQ/HKD2CNY.csv' ) 
uqer.download_data( filename='HKRawQ/USD2CNY.csv' ) 
uqer.download_data( filename='HKRawQ/SHHK.csv' ) 

HKD2CNY = pd.read_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\HKD2CNY.csv', delimiter=',',usecols=[1,2], parse_dates=[0],index_col=[0])
SHHK = pd.read_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\SHHK.csv', delimiter=',',usecols=[1,2,3], parse_dates=[0],index_col=[0])
SHHK['midRate'] = ( SHHK['stlBid'] + SHHK['stlAsk'] ) * 0.5

HKD2CNY = HKD2CNY[HKD2CNY.index < SHHK.index[0]]
SHHK = SHHK[['midRate']]

SHHK = pd.concat( [HKD2CNY,SHHK] , axis=0 )

SHHK.to_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\SHHKEX.csv',encoding='gbk', float_format='%.5f' , date_format='%Y-%m-%d')


tickers = ['00811','00902','00939','00966','00998', '01071', '01177','01288','01336','01339','01398','01816','01918','01963','01988',
           '02318','02328','02333','02601','02799','02883','03328','03618','03899','03900','03968','03988','06818']
#for ticker in tickers:
#    uqer.download_data( filename='HKQuotes/HK{0}.txt'.format(ticker) )

for ticker in tickers:
    uqer.download_data( filename='HKRawQ/{0}.csv'.format(ticker) )



#uqer.download_data( 'StocksFin2B.xlsx' )


#import mercury

#uqer = mercury.Client(uqername, uqerpwd)
## all_files = uqer.list_data()
#uqer.download_data(filename)