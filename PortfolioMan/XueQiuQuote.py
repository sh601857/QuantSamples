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
    Cookie = r'bid=cdf359ce9660d4b54f3244148b734529_ir8ig83q; webp=0; s=7e11avbm3a; Hm_lvt_63c1867417313f92f41e54d6ef61187d=1496150989; aliyungf_tc=AQAAAE/c8V5XXQMAZKL8clIF7gVWRLSU; device_id=c800e49ed19d347c52933996e85a6873; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=1ceb0cefe0943930a6119d2282604487cd89bf3b; xq_a_token.sig=lr6saO0VDRbgRicrfD1dgM69GOA; xq_r_token=b6e83709ad9a16f4e5ca59053afe17a96799521d; xq_r_token.sig=paFernk6_XXbzKtjm5ALJ8Fkyo4; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1130417241; u.sig=lSLwGQM8984PiikcYfzxf83SDM0; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1498565578,1498650889,1498739370,1498888573; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1498901863'
    headers = {'Cookie': Cookie, 
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}    
    #try:
    if True:
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        
        nav_detail = response.read().decode('utf-8') 
        df1 = pd.read_json(nav_detail, orient='index',convert_axes=False)
        df1 = df1[['code','name','current','percentage','open','high','low','close','volume','amount', 'pe_ttm','pb','totalShares','float_shares','lot_size','kzz_stock_current']]        
        #df1 = pd.read_json(nav_detail, orient='index',convert_axes=False)
        #df1 = df1[['code','percentage','open','high','low','close','volume','amount', 'pe_ttm','pb','totalShares','float_shares','lot_size','kzz_stock_current']]
        return df1
        #print(df1)
        #nav_obj = json.load(StringIO(nav_detail))
        #latest_Q_Item = nav_obj[ticker]
        #return (ticker, latest_Q_Item['name'] , float( latest_Q_Item['current'] ),  datetime.strptime(latest_Q_Item['time'] , '%a %b %d %H:%M:%S %z %Y') )  
    #except:        
        #return None
    
    
#print( GetHKQuote('02601,00998') )


