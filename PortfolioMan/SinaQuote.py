#coding=utf-8
import pandas as pd
import numpy as np
import urllib.request
from datetime import datetime
from io import StringIO
import json

def GetQuote(stockCode):
    url = "http://hq.sinajs.cn/list=" + stockCode
    response = urllib.request.urlopen(url)
    stocks_detail = response.read().decode('gb2312')  
    
    stock_details = stocks_detail.split(';\n')
    stock_dict = dict()
    for stock_detail in stock_details:
        stock = stock_detail.split(',')
        if len(stock) <= 18:
            continue 
        fcode = stock[0][11: stock[0].find('=') ]
        if 'hk' in fcode : # hk 
            stock_dict[fcode] = {
                'code': fcode,
                'name': stock[1],
                'O': float(stock[2]),                
                'PC': float(stock[3]),
                'H': float(stock[4]),
                'L': float(stock[5]),                
                'C': float(stock[6]),
                #'涨跌': float(stock[7]),  
                #'涨幅': float(stock[8]),  
                'bid1': float(stock[9]),
                'ask1': float(stock[10]),
                'A': float(stock[11]) ,  
                'V': float(stock[12]) ,
                'PE': float(stock[13]) if stock[13] != '' else None,
                'DR': float(stock[14]) if stock[14] != '' else None,
                'high_52W': float(stock[15]),  
                'low_52W': float(stock[16]) ,
                'datetime': datetime.strptime(stock[17]+' ' + stock[18][0:-1], '%Y/%m/%d %H:%M')
                }
        else :
            stock_dict[fcode] = {
                'code': fcode,
                'name': stock[0][stock[0].find('"')+1: ],
                'O': float(stock[1]),                
                'PC': float(stock[2]),
                'C': float(stock[3]),
                'H': float(stock[4]),
                'L': float(stock[5]),                

                #'涨跌': float(stock[7]),  
                #'涨幅': float(stock[8]),  
                'bid1': float(stock[6]),
                'ask1': float(stock[7]),
                'V': float(stock[8]) ,
                'A': float(stock[9]) ,  

                'datetime': datetime.strptime(stock[30]+ stock[31], '%Y-%m-%d%H:%M:%S')
                }

    stock_df = pd.DataFrame(list(stock_dict.values()),index=list(stock_dict.keys()) )
    return stock_df   

def GetNav(fundCode):

    # http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=150022
    url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=" + fundCode
    try:
        response = urllib.request.urlopen(url)
        nav_detail = response.read().decode('gb2312')        
        nav_obj = json.load(StringIO(nav_detail))
        latest_Nav_Item = nav_obj['result']['data']['data'][0]
        return (fundCode, latest_Nav_Item['fbrq'][:10] , float( latest_Nav_Item['jjjz'] ), float( latest_Nav_Item['ljjz'] ) )  
    except:
        return None     
               
#sdf = GetQuote('sh601166,hk00998')
#print(sdf)