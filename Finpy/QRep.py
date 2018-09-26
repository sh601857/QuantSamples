#coding=utf-8

import pandas as pd
import numpy as np
from scipy import interpolate
from sqlalchemy import create_engine
import datetime

DB_CONNECT_STRING = u'sqlite:///D:\\yun\\百度云\\db\\Finpy.db'


def get_RMBC(secID,start,end='2099-12-31',field=u"tradeDate,closePrice",hkd='SHHKEX'):
    sql = "SELECT {3} FROM d_quote WHERE secID='{0}' AND tradeDate>='{1}' AND tradeDate<='{2}' ORDER BY tradeDate".format(secID,start,end,field)
    engine = create_engine(DB_CONNECT_STRING, echo=False)  
    c = pd.read_sql_query(sql, engine , index_col='tradeDate', parse_dates=['tradeDate'])
    if secID[-4:] == 'XHKG':
        if hkd == 'SHHKEX':
            r = pd.read_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\SHHKEX.csv', delimiter=',',usecols=[0,1], parse_dates=[0],index_col=[0])
        else:
            r = pd.read_csv('D:\\GitHub\\QuantSamples\\HK\\HKRawQ\\HKD2CNY.csv', delimiter=',',usecols=[1,2], parse_dates=[0],index_col=[0])
        c = pd.merge(c,r, how='left',left_index=True,right_index=True)
        c.fillna( method='pad' , inplace=True)
        c['closePrice']=c['closePrice']*c['midRate']
        return c[['closePrice']]
    else:
        return c
    
def get_ev(secID,start,end='2099-12-31'):
    
    sql = "SELECT endDateRep,ev,exDiv FROM d_ev WHERE secID='{0}' AND endDateRep>='{1}' AND endDateRep<='{2}' ORDER BY endDateRep".format(secID,start,end)
    engine = create_engine(DB_CONNECT_STRING, echo=False)  
    ev = pd.read_sql_query(sql, engine , index_col='endDateRep',parse_dates=['endDateRep'])
    return ev
#ev = get_ev('601088.XSHG', start='2008-01-01')
#print(ev)

def get_div(secID,start,end='2099-12-31'):
    sql = "SELECT exDivDate,sch,perCashDiv FROM d_equdiv WHERE secID='{0}' AND exDivDate>='{1}' AND exDivDate<='{2}' ORDER BY exDivDate".format(secID,start,end)
    engine = create_engine(DB_CONNECT_STRING, echo=False)  
    div = pd.read_sql_query(sql, engine , index_col='exDivDate',parse_dates=['exDivDate'])
    return div    
    
#div = get_div('601088.XSHG', start='2008-01-01')
#print(div)

def get_exev(secID,start,end='2099-12-31'):
    
    sql = "SELECT endDateRep,ev,exDiv FROM d_ev WHERE secID='{0}' AND endDateRep>='{1}' AND endDateRep<='{2}' ORDER BY endDateRep".format(secID,start,end)
    engine = create_engine(DB_CONNECT_STRING, echo=False)  
    ev = pd.read_sql_query(sql, engine , index_col='endDateRep',parse_dates=['endDateRep'])
    
    sql = "SELECT exDivDate,sch,perCashDiv FROM d_equdiv WHERE secID='{0}' AND exDivDate>='{1}' AND exDivDate<='{2}' ORDER BY exDivDate".format(secID,start,end)
    div = pd.read_sql_query(sql, engine , index_col='exDivDate',parse_dates=['exDivDate'])
    ev['ev'] = ev['ev']+ev['exDiv']
    div = pd.concat([div[['sch','perCashDiv']], ev['ev'] ],axis=1)   
    div.fillna(0.0,inplace=True)

    div['sch'] = div['sch'] + 1
    div['sch'] = div['sch'].cumprod()
    dlist = []
    for i in range(1,len(div)):
        if div.iloc[i,2] == 0:  # div row
            for j in range(i+1,len(div)): 
                if div.iloc[j,2] != 0:
                    break
            a = ( div.iloc[j,0] * div.iloc[j,2] + ( div.iloc[i-1:j-1,0].values * div.iloc[i:j,1].values ).sum()
                 -  div.iloc[i-1,0] * div.iloc[i-1,2]  ) / ( ( div.index[j] -  div.index[i-1] ) / np.timedelta64(1, 'D') )

            for l in range(i,j):
                drow = div.iloc[l,:].copy()
                drow.iloc[1] = 0.0
                drow.iloc[2] = ( div.iloc[i-1,0] * div.iloc[i-1,2] 
                + a * ( ( div.index[l] -  div.index[i-1] ) / np.timedelta64(1, 'D') )  ) / div.iloc[l,0]
                drow.name = drow.name - pd.Timedelta("0 days 01:00:00")
                dlist.append(drow)     
                div.iloc[l,2] = ( div.iloc[i-1,0] * div.iloc[i-1,2] 
                + a * ( ( div.index[l] -  div.index[i-1] ) / np.timedelta64(1, 'D') ) 
                - ( div.iloc[i-1:l,0].values * div.iloc[i:l+1,1].values ).sum() ) / div.iloc[l,0]
    div = div.append(dlist)
    div.sort_index(inplace=True)
    #print(dlist)
    return div

#eev = get_exev('601088.XSHG', start='2008-01-01')
#print(eev)


def get_pev(secID,start,end='2099-12-31'):
    ev = get_exev( secID, '{0}{1}'.format( int(start[0:4])-1, start[4:] ),end)
    a = get_RMBC(secID,start,end)
    evfun = interpolate.interp1d(ev.index.values.astype('float'), ev['ev']*ev['sch'], kind='linear')
    schfun = interpolate.interp1d(ev.index.values.astype('float'), ev['sch'], kind='zero')
    a['ev'] = evfun( a.index.values.astype('float') ) 
    a['pev'] = a['closePrice'] * schfun( a.index.values.astype('float') )  / a['ev']    
    return a