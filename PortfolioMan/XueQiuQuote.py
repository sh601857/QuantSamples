import pandas as pd
import numpy as np
import urllib.request
from urllib.parse import urlencode
from datetime import datetime
from io import StringIO
import json

def GetHKQuote(ticker):
    import socket
    socket.setdefaulttimeout(10.0) 
    url = "https://xueqiu.com/v4/stock/quote.json?code=" + ticker
    Cookie = r'bid=cdf359ce9660d4b54f3244148b734529_iqj6ec8n; webp=0; s=p8s128eojc; Hm_lvt_63c1867417313f92f41e54d6ef61187d=1495524722; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=526fb5682d02d7db77ea3ca68742d0080c8e77d6; xq_a_token.sig=KoqZXKVRHQuDo1vg5qGAQ0NNQTU; xq_r_token=c337850ccf43272c38482b3deeddd22d7755d66c; xq_r_token.sig=MPUfnxK762ju8tEl3BBtIEa7gMk; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1130417241; u.sig=lSLwGQM8984PiikcYfzxf83SDM0; aliyungf_tc=AQAAAD9eOCbX6Q4ABmIyPfrGkMFbLgNB; Hm_lvt_1db88642e346389874251b5a1eded6e3=1497930318,1497952246,1498005979,1498037299; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1498037300; __utmt=1; __utma=1.1838967863.1468310908.1498031936.1498037300.511; __utmb=1.1.10.1498037300; __utmc=1; __utmz=1.1476945669.153.2.utmcsr=danjuanapp.com|utmccn=(referral)|utmcmd=referral|utmcct=/plan/CSI007ZS'
    headers = {'Cookie': Cookie, 
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}    
    #try:
    if True:
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        
        nav_detail = response.read().decode('utf-8') 
        df1 = pd.read_json(nav_detail, orient='index',convert_axes=False)
        df1 = df1[['code','percentage','open','high','low','close','volume','amount', 'pe_ttm','pb','totalShares','float_shares','lot_size','kzz_stock_current']]
        return df1
        #print(df1)
        #nav_obj = json.load(StringIO(nav_detail))
        #latest_Q_Item = nav_obj[ticker]
        #return (ticker, latest_Q_Item['name'] , float( latest_Q_Item['current'] ),  datetime.strptime(latest_Q_Item['time'] , '%a %b %d %H:%M:%S %z %Y') )  
    #except:        
        #return None
    
    
#print( GetHKQuote('02601,00998') )


