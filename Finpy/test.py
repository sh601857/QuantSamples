# import requests
# session = requests.session()
# r = session.get('http://data.gtimg.cn/flashdata/hk/daily/12/hkHSI.js')
# print(r.text)
# r = session.get('http://data.gtimg.cn/flashdata/hk/daily/13/hkHSI.js')
# print(r.text)


import pandas as pd
HKD2CNY = pd.read_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\HKD2CNY.csv', delimiter=',',usecols=[1,2], parse_dates=[0],index_col=[0])
SHHK = pd.read_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\SHHK.csv', delimiter=',',usecols=[1,2,3], parse_dates=[0],index_col=[0])
SHHK['midRate'] = ( SHHK['stlBid'] + SHHK['stlAsk'] ) * 0.5

HKD2CNY = HKD2CNY[HKD2CNY.index < SHHK.index[0]]
SHHK = SHHK[['midRate']]

SHHK = pd.concat( [HKD2CNY,SHHK] , axis=0 )

SHHK.to_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\SHHKEX.csv',encoding='gbk', float_format='%.5f' , date_format='%Y-%m-%d')

print(SHHK)
