# -*- coding: utf-8 -*-

from uqer import Client

uqer = Client(username='huyijiong@139.com', password='qwe123!@#')

#files = uqer.list_data()
#print(files)
uqer.download_data( 'HKI.csv' )
uqer.download_data( filename='HKRawQ/HKD2CNY.csv' ) 
uqer.download_data( filename='HKRawQ/USD2CNY.csv' ) 



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