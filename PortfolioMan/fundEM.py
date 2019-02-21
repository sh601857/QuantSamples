#coding=utf-8

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from io import StringIO
import xlwings as xw

#  http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=501041&page=1&per=50
#  https://www.jianshu.com/p/d79d3cd62560

def GetNavGS(fundCode):
    import socket
    socket.setdefaulttimeout(10.0) 
    # http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=150022&num=2000
    url = "http://fundgz.1234567.com.cn/js/{0}.js".format( fundCode )
    try:
        response = requests.get(url)
        nav_detail = response.content.decode('utf8')   
        nav_obj = json.loads(nav_detail[8:-2])
        return (nav_obj['fundcode'],nav_obj['jzrq'],nav_obj['dwjz'],nav_obj['gsz'] )
    except:   
        print( '{0} failed'.format( fundCode) )
        return None 
        
#print( GetNav('163407') )

def GetNav(fundCode):
    rs = GetHNav(fundCode)
    return ( fundCode, rs[0]['date'], rs[0]['jjjz'], rs[0]['ljjz'] , rs[0]['pct'])    
        
def GetHNav(fundCode, start='', end='', per=2):
    import socket
    socket.setdefaulttimeout(10.0)
    record = {'Code': fundCode}
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': fundCode, 'page': 1, 'per': per, 'sdate': start, 'edate': end}
    rsp = requests.get(url, params=params, proxies=None)
    rsp.raise_for_status()
    html = rsp.text
    soup = BeautifulSoup(html, 'html.parser')
    records = []
    tab = soup.findAll('tbody')[0]
    for tr in tab.findAll('tr'):
        if tr.findAll('td') and len((tr.findAll('td'))) == 7:
            record['date'] = str(tr.select('td:nth-of-type(1)')[0].getText().strip())
            record['jjjz'] = str(tr.select('td:nth-of-type(2)')[0].getText().strip())
            record['ljjz'] = str(tr.select('td:nth-of-type(3)')[0].getText().strip())
            record['pct'] = str(tr.select('td:nth-of-type(4)')[0].getText().strip())
            records.append(record.copy())
    return records

#print( GetHNav('163407') )