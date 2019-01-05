# -*- coding: utf-8 -*-

import urllib
import urllib.request
import re
import sqlite3
from bs4 import BeautifulSoup
from locale import *

setlocale(LC_NUMERIC, 'English_US')
#atof('123,456')    # 123456.0
class HKTHolds:
    def __init__(self):
        self.VIEWSTATE = []  
        self.EVENTVALIDATION = []
        #self.url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh"
        
    def init_post(self):
        url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh"
        response = urllib.request.urlopen(url)
        resu = response.read().decode('utf-8')
        self.VIEWSTATE = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', resu,re.I)
        self.EVENTVALIDATION = re.findall(r'input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', resu,re.I)
        
    def get_data(self,day,month,year,market='sh'):
        
        sql = "INSERT OR IGNORE INTO HKITRI VALUES (?, ?, ?)"
        
        url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t={0}".format(market)
        
        form ={
        '__VIEWSTATE':self.VIEWSTATE[0],
        '__EVENTVALIDATION':self.EVENTVALIDATION[0],
        #'today':20180102,
        #'sortBy':,
        #'alertMsg':,
        #'ddlShareholdingDay':day,
        #'ddlShareholdingMonth':month,
        #'ddlShareholdingYear':year,
        #'btnSearch.x':27,
        #'btnSearch.y':8,
        
        'txtShareholdingDate': '{0}/{1}/{2}'.format(year,month,day),
        'btnSearch': u'搜尋'
        }

        form_data = urllib.parse.urlencode(form).encode(encoding='UTF8')
        request = urllib.request.Request(url, data = form_data)
        response = urllib.request.urlopen(request)
        resu=response.read().decode('utf-8')
        #print(resu)
        relist = []

        soup = BeautifulSoup(resu, 'html.parser')
        
        tbodys = soup.find_all('tbody' )
        if len(tbodys)>0:
            for tr in tbodys[0].find_all('tr'):
                tds = tr.find_all('td')
                tradedate = '{0}{1}{2}'.format(year,month,day)
                divs = tds[0].find_all('div')
                code = divs[1].string.strip()            
                divs = tds[2].find_all('div')
                shares = atoi( divs[1].string.strip())
                divs = tds[3].find_all('div')
                pct = atof( divs[1].string.strip()[:-1] )
                
                relist.append ( ( code, tradedate, shares , pct ) )
            
        return relist
    
        
        
hknews = HKTHolds()
hknews.init_post()
#relist = hknews.get_data(29,12,2017)

    
sql = "INSERT OR REPLACE INTO HKTHolds VALUES (?, ?, ?, ?)"
conn = sqlite3.connect(u'D:\\yun\百度云\\PortfolioMan\\dat\\HKI.db')
cursor = conn.cursor()  

cursor.execute("select DISTINCT tradedate from hkitri where tradedate > '20181227' order by tradedate")
tdates = cursor.fetchall()
for tdate in tdates:   
    print( tdate[0] ,end=' ')
    
    relist = hknews.get_data( tdate[0][6:8] ,  tdate[0][4:6] ,  tdate[0][0:4] , 'sh') 
    if len( relist ) > 10:
        cursor.executemany(sql, relist)
        print (' sh ok' ,end=' ')
    relist = hknews.get_data( tdate[0][6:8] ,  tdate[0][4:6] ,  tdate[0][0:4] , 'sz') 
    if len( relist ) > 10:
        cursor.executemany(sql, relist)  
        print (' sz ok')
    
    conn.commit()

#for tdate in tdates:   
    #print( tdate[0] )
    #relist = hknews.get_data( tdate[0][6:8] ,  tdate[0][4:6] ,  tdate[0][0:4] , 'sz') 
    #if len( relist ) > 10:
        #cursor.executemany(sql, relist)
        ##conn.commit()		

#conn.commit()			
conn.close()

name = input("Press any key to exit\n")

#select * from hktholds where secid='90004'