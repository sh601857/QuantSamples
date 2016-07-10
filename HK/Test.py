# -*- coding: utf-8 -*-


#import webbrowser, urllib.request
#tickers='hk00998'
#url = 'http://qt.gtimg.cn/q={0}'.format( tickers )
#response = urllib.request.urlopen(url)
#stocks_detail = response.read().decode('gb2312')    
#stock_details = stocks_detail.split('~')
#for i in range( len( stock_details ) ):
    #print( '{0:3} : {1}'.format(i, stock_details[i] )  )
    
    
import webbrowser, urllib.request
tickers='hk00998'
url = 'http://hq.sinajs.cn/list={0}'.format( tickers )
response = urllib.request.urlopen(url)
stocks_detail = response.read().decode('gb2312')
stock_details = stocks_detail.split(',')
for i in range( len( stock_details ) ):
    print( '{0:3} : {1}'.format(i, stock_details[i] )  )