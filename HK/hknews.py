import urllib
import urllib.request
import re

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
        
    def get_data(self,day,month,year):
        form ={
        '__VIEWSTATE':self.VIEWSTATE[0],
        '__EVENTVALIDATION':self.EVENTVALIDATION[0],
        #'today':20180102,
        #'sortBy':,
        #'alertMsg':,
        'ddlShareholdingDay':day,
        'ddlShareholdingMonth':month,
        'ddlShareholdingYear':year,
        'btnSearch.x':27,
        'btnSearch.y':8,
        }

        form_data = urllib.parse.urlencode(form).encode(encoding='UTF8')
        request = urllib.request.Request(url, data = form_data)
        response = urllib.request.urlopen(request)
        resu=response.read().decode('utf-8')
        print( resu )
        
        
    
#url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz"
url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh"

#form = {'ddlShareholdingDay':30, 'ddlShareholdingMonth':12, 'ddlShareholdingYear':2017}
#form_data = urllib.parse.urlencode(form)
#request = urllib.request.Request(url)
response = urllib.request.urlopen(url)
#print( response.info()  )

resu=response.read().decode('utf-8')
VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', resu,re.I)
EVENTVALIDATION =re.findall(r'input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', resu,re.I)
print( VIEWSTATE[0] )
print ( EVENTVALIDATION[0] )

form ={
'__VIEWSTATE':VIEWSTATE[0],
'__EVENTVALIDATION':EVENTVALIDATION[0],
#'today':20180102,
#'sortBy':,
#'alertMsg':,
'ddlShareholdingDay':20,
'ddlShareholdingMonth':12,
'ddlShareholdingYear':2017,
'btnSearch.x':27,
'btnSearch.y':8,
}

form_data = urllib.parse.urlencode(form).encode(encoding='UTF8')
print (form_data)
request = urllib.request.Request(url, data = form_data)
response = urllib.request.urlopen(request)
resu=response.read().decode('utf-8')

file_temp = open(u'file_temp.html', 'w')
file_temp.write(resu)
file_temp.close()
print( resu )
