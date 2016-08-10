# -*- coding: utf-8 -*-

#http://data.gtimg.cn/flashdata/hushen/daily/13/sz000750.js

from datetime import datetime
import webbrowser, urllib.request
import shutil
import numpy as np
import pandas as pd
import io

#http://data.gtimg.cn/flashdata/hk/daily/12/hkHSI.js
def GetDayKofYear( year , ticker ):

    url = 'http://data.gtimg.cn/flashdata/hk/daily/{0}/{1}.js'.format( year, ticker )
    cash ='temp.txt'

    try:    
        with urllib.request.urlopen(url) as response, open(cash, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

    dat = np.genfromtxt( cash, comments='\\',dtype="S6,f8,f8,f8,f8,f8",
                     skip_header=1, skip_footer=1,
                     names="D, O, C, H, L, V")
    return dat

#http://qt.gtimg.cn/q=sz000858
def GetLatestQuoteStock( tickers ):
    url = 'http://qt.gtimg.cn/q={0}'.format( tickers )
    #cash ='temp.txt'    
    #try:    
        #with urllib.request.urlopen(url) as response, open(cash, 'wb') as out_file:
            #shutil.copyfileobj(response, out_file)
    #except:
        #print("Unexpected error:", sys.exc_info()[0])
        #return None
    response = urllib.request.urlopen(url)
    stocks_detail = response.read().decode('gb2312')    
   
    stock_details = stocks_detail.split(';\n')
    stock_dict = dict()
    for stock_detail in stock_details:
        stock = stock_detail.split('~')
        if len(stock) <= 49:
            continue
        if stock[0][:4] =='v_hk' :
            fcode = stock[0][2:4] + stock[2]
            stock_dict[fcode] = {
                'name': stock[1],
                'code': fcode,
                'C': float(stock[3]),
                'PC': float(stock[4]),
                'O': float(stock[5]),
                'V': float(stock[6]) ,
                #'bid_volume': int(stock[7]) * 100,
                #'ask_volume': float(stock[8]) * 100,
                'bid1': float(stock[9]),
                #'bid1_volume': int(stock[10]) * 100,
                #'bid2': float(stock[11]),
                #'bid2_volume': int(stock[12]) * 100,
                #'bid3': float(stock[13]),
                #'bid3_volume': int(stock[14]) * 100,
                #'bid4': float(stock[15]),
                #'bid4_volume': int(stock[16]) * 100,
                #'bid5': float(stock[17]),
                #'bid5_volume': int(stock[18]) * 100,
                'ask1': float(stock[19]),
                #'ask1_volume': int(stock[20]) * 100,
                #'ask2': float(stock[21]),
                #'ask2_volume': int(stock[22]) * 100,
                #'ask3': float(stock[23]),
                #'ask3_volume': int(stock[24]) * 100,
                #'ask4': float(stock[25]),
                #'ask4_volume': int(stock[26]) * 100,
                #'ask5': float(stock[27]),
                #'ask5_volume': int(stock[28]) * 100,
                #'最近逐笔成交': stock[29],  # 换成英文
                'datetime': datetime.strptime(stock[30], '%Y/%m/%d %H:%M:%S') if stock[0][:4] =='v_hk' else datetime.strptime(stock[30], '%Y%m%d%H%M%S'),
                #'涨跌': float(stock[31]),  # 换成英文
                #'涨跌(%)': float(stock[32]),  # 换成英文
                'H': float(stock[33]),
                'L': float(stock[34]),
                #'价格/成交量(手)/成交额': stock[35],  # 换成英文
                #'成交量(手)': float(stock[36]),  # 换成英文
                'A': float(stock[37]) ,  # 换成英文
                #'turnover': float(stock[38]) if stock[38] != '' else None,
                'PE': float(stock[39]) if stock[39] != '' else None,
                #'unknown': stock[40],
                #'high_52W': float(stock[41]),  # 意义不明
                #'low_52W': float(stock[42]),  # 意义不明
                #'振幅': float(stock[43]),  # 换成英文
                'LMV': float(stock[44]) if stock[44] != '' else None,  # 换成英文
                'MV': float(stock[45]) if stock[44] != '' else None,  # 换成英文
                'PB': 0.0 if stock[0][:4] =='v_hk' else float(stock[46]),
                'DR': float(stock[47]),
                'high_52W': float(stock[48]),  # 换成英文
                'low_52W': float(stock[49])  # 换成英文                        
            }
        else :
            fcode = stock[0][2:4] + stock[2]
            stock_dict[fcode] = {
                'name': stock[1],
                'code': fcode,
                'C': float(stock[3]),
                'PC': float(stock[4]),
                'O': float(stock[5]),
                'V': float(stock[6]) * 100,
                #'bid_v': int(stock[7]) * 100,   #外盘
                #'ask_v': float(stock[8]) * 100, #内盘
                'bid1': float(stock[9]),
                'bid1_v': int(stock[10]) * 100,
                'bid2': float(stock[11]),
                'bid2_v': int(stock[12]) * 100,
                #'bid3': float(stock[13]),
                #'bid3_volume': int(stock[14]) * 100,
                #'bid4': float(stock[15]),
                #'bid4_volume': int(stock[16]) * 100,
                #'bid5': float(stock[17]),
                #'bid5_volume': int(stock[18]) * 100,
                'ask1': float(stock[19]),
                'ask1_v': int(stock[20]) * 100,
                'ask2': float(stock[21]),
                'ask2_v': int(stock[22]) * 100,
                #'ask3': float(stock[23]),
                #'ask3_volume': int(stock[24]) * 100,
                #'ask4': float(stock[25]),
                #'ask4_volume': int(stock[26]) * 100,
                #'ask5': float(stock[27]),
                #'ask5_volume': int(stock[28]) * 100,
                #'最近逐笔成交': stock[29],  # 换成英文
                'datetime': datetime.strptime(stock[30], '%Y%m%d%H%M%S'),
                #'涨跌': float(stock[31]),  # 换成英文
                #'涨跌(%)': float(stock[32]),  # 换成英文
                'H': float(stock[33]),
                'L': float(stock[34]),
                #'价格/成交量(手)/成交额': stock[35],  # 换成英文
                #'成交量(手)': int(stock[36]) * 100,  # 换成英文
                'A': float(stock[37]) * 10000,  # 换成英文
                #.'turnover': float(stock[38]) if stock[38] != '' else None,
                'PE': float(stock[39]) if stock[39] != '' else None,
                #'unknown': stock[40],
                #'high_2': float(stock[41]),  # 意义不明
                #'low_2': float(stock[42]),  # 意义不明
                #'振幅': float(stock[43]),  # 换成英文
                'LMV': float(stock[44]) if stock[44] != '' else None,  # 流通市值
                'MV': float(stock[45]) if stock[44] != '' else None,  # 总市值
                'PB': float(stock[46]),
                #.'涨停价': float(stock[47]),  # 换成英文
                #.'跌停价': float(stock[48])  # 换成英文
                }
            stock_df = pd.DataFrame(list(stock_dict.values()),index=list(stock_dict.keys()) )
    return stock_df  



#dat = GetDayKofYear(16, 'hkHSI')
#print(dat)
dat =  GetLatestQuoteStock( 'hkHSI,sh600000' )
print(dat)