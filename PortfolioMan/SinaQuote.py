#coding=utf-8
import pandas as pd
import numpy as np
import urllib.request
from datetime import datetime
from io import StringIO
import json
import sqlite3

closedQEnd = ['1991-03-31', '1991-06-30', '1994-12-31', '1995-09-30',
               '1995-12-31', '1996-03-31', '1996-06-30', '1996-09-30',
               '1997-06-30', '1999-12-31', '2000-09-30', '2000-12-31',
               '2001-03-31', '2001-06-30', '2001-09-30', '2002-03-31',
               '2002-06-30', '2002-09-30', '2005-12-31', '2006-09-30',
               '2006-12-31', '2007-03-31', '2007-06-30', '2007-09-30',
               '2007-12-31', '2008-09-30', '2011-12-31', '2012-03-31',
               '2012-06-30', '2012-09-30', '2013-03-31', '2013-06-30',
               '2016-12-31', '2017-09-30', '2017-12-31']

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
    import socket
    socket.setdefaulttimeout(10.0) 
    # http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=150022&num=2000
    url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=" + fundCode
    try:
        response = urllib.request.urlopen(url)
        nav_detail = response.read().decode('gb2312')        
        nav_obj = json.load(StringIO(nav_detail))
        latest_Nav_Item = nav_obj['result']['data']['data'][0]
        return (fundCode, latest_Nav_Item['fbrq'][:10] , float( latest_Nav_Item['jjjz'] ), float( latest_Nav_Item['ljjz'] ) )  
    except:        
        return None 
    
def FundAdjNaV(NAV, ACCUM_NAV):
    AdjNAV = NAV.copy()
    SR=1.0
    for r in range(1,len(NAV)):
        div = (ACCUM_NAV[r] - ACCUM_NAV[r-1]) * SR - (NAV[r] - NAV[r-1])
        if div > 0.003:   # 分红
            AdjNAV[r] = ( div  + NAV[r] ) * AdjNAV[r-1] / NAV[r-1] 
            #print(r, div , SR)
        elif div< -0.003: # 拆分
            AdjNAV[r] = ACCUM_NAV[r] * AdjNAV[r-1] / ACCUM_NAV[r-1]
            SR = NAV[r] / ACCUM_NAV[r] 
            #print(r, div , SR)
        else:
            AdjNAV[r] = NAV[r] * AdjNAV[r-1] / NAV[r-1]
    return AdjNAV

def FundFAdjNaVSR( npNav ):
    npNav['adjNav'] = npNav['jjjz']
    for r in range(1,len(npNav)):        
        #div = (npNav['ljjz'][r] / npNav['sp'][r] - npNav['ljjz'][r-1] / npNav['sp'][r-1] )  - (npNav['jjjz'][r] - npNav['jjjz'][r-1])
        div = (npNav['ljjz'][r] - npNav['ljjz'][r-1]  )  - (npNav['jjjz'][r] * npNav['sp'][r] - npNav['jjjz'][r-1] * npNav['sp'][r-1] )
        div = div / npNav['sp'][r]
        if div / npNav['jjjz'][r] > 0.003:   # 分红
            npNav['adjNav'][r] = ( div  + npNav['jjjz'][r]  ) * npNav['sp'][r] / (npNav['jjjz'][r-1]  * npNav['sp'][r-1] )  * npNav['adjNav'][r-1]
            npNav['div'][r] = div
            
        elif div / npNav['jjjz'][r] < -0.003: # 拆分
            npNav['adjNav'][r] = npNav['jjjz'][r] * npNav['sp'][r]  / npNav['jjjz'][r-1] / npNav['sp'][r-1] * npNav['adjNav'][r-1] 
            npNav['div'][r] = div
        else:
            npNav['adjNav'][r] = npNav['jjjz'][r] * npNav['sp'][r]  / npNav['jjjz'][r-1] / npNav['sp'][r-1] * npNav['adjNav'][r-1] 
    return npNav


def GetHNav(fundCode):
    import socket
    socket.setdefaulttimeout(10.0) 
    # http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=150022&num=2000
    url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=" + fundCode + "&num=9000"
    try:
        response = urllib.request.urlopen(url)
        nav_detail = response.read().decode('gb2312')        
        nav_obj = json.load(StringIO(nav_detail))
        navs = nav_obj['result']['data']['data']
        # return numpy ndarray
        #navlist =[]
        #for nav in navs:
            #navlist.append( (  np.datetime64(nav['fbrq'][0:10]) , float(nav['jjjz']), float(nav['ljjz']) ) )
        #ret = np.rec.array(navlist, dtype= np.dtype([('fbrq','datetime64[D]'),('jjjz', float),('ljjz', float) ]))
        
        #return a dataframe
        #ret = pd.DataFrame(navs)
        #vadate = [r for r in ret.index if not ret.loc[r,'fbrq'][:10] in closedQEnd ]
        #ret = ret.loc[ vadate,:]

        navlist =[]
        for nav in reversed(navs) :
            if nav['fbrq'][0:10] in closedQEnd:
                continue
            navlist.append( ( nav['fbrq'][0:10] , float(nav['jjjz']), float(nav['ljjz']), 1.0, 0.0, 1.0 ) )
            
        npNav = np.rec.array(navlist, dtype= np.dtype([('fbrq','object'),('jjjz', float),('ljjz', float) ,('sp', float) ,('div', float),('adjNav', float)]))    
       
        # deal with fund split
        conn = sqlite3.connect('FundDB.db')
        cursor = conn.cursor()         
        for row in  cursor.execute('select TDate, Ratio from d_fund_split where SecID="{0}"'.format(fundCode)):
            npNav.sp[ npNav.fbrq==row[0] ] = row[1]
        conn.close()               
        npNav.sp = np.cumprod( npNav.sp )    
        npNav = FundFAdjNaVSR(npNav)
        return  npNav
    except:   
        #raise
        return None 
    
#hnav = GetHNav('511220')#159901
#np.set_printoptions(threshold=5000)
#pd.set_option('display.max_rows', 5000) 
#print( hnav )
#print( hnav[ abs( hnav.div ) >0.003 ] )


#sdf = GetQuote('sh601166,hk00998')
#print(sdf)