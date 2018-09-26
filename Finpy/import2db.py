#coding=utf-8

import numpy as np
import pandas as pd
import xlwings as xw
from sqlalchemy import create_engine

import gtimg
import time

def write_one_table(DB_CONNECT_STRING, wbfile, tbname, topleftc ):
    
    #DB_CONNECT_STRING = 'sqlite:///D:\\yun\\百度云\\db\\Finpy.db'
    #DB_CONNECT_STRING = 'mysql+pymysql://root:enintech@10.0.0.152:3306/ecdu'
    
    engine = create_engine(DB_CONNECT_STRING, echo=True)
    wb = xw.Book( wbfile )
    
    sht = wb.sheets[tbname] 
    data = sht.range( topleftc ).options(pd.DataFrame, expand='table', index=False).value
    
    # delete existing records
    conn = engine.connect()
    trans = conn.begin()
    try:
        conn.execute( 'DELETE FROM {0}'.format(tbname) )
        trans.commit()
    except:
        trans.rollback()
        raise    
    finally:
        conn.close()
        
    # write data to db    
    data.to_sql(tbname, con=engine, if_exists='append', index=False)    

def write_all_excel_tables():
    
    DB_CONNECT_STRING = u'sqlite:///D:\\yun\\百度云\\db\\Finpy.db'
    wbfile = 'D:\\yun\\百度云\\db\\pev.xlsx'
    
    write_one_table( DB_CONNECT_STRING, wbfile, u'b_sec', 'B1')
    write_one_table( DB_CONNECT_STRING, wbfile, u'd_equdiv', 'B1')
    write_one_table( DB_CONNECT_STRING, wbfile, u'd_ev', 'B1')
    
    
def update_d_quote():
    
    import requests
    session=requests.Session()
    DB_CONNECT_STRING = u'sqlite:///D:\\yun\\百度云\\db\\Finpy.db'
    engine = create_engine(DB_CONNECT_STRING, echo=True)
    conn = engine.connect()
    secs = conn.execute("select secID,ticker,exchangeCD,sectype,qsyear from b_sec where valid=1")

    for sec in secs: 
        reyear = conn.execute("select MAX( tradeDate ) from d_quote where secID='{0}'".format(sec['secID']))
        ttt = reyear.scalar()
        if ttt is None:
            isyear = sec['qsyear']
        else:
            isyear = int( ttt[0:4] )
        
        code = '{0}{1}'.format( sec['exchangeCD'] , sec['ticker'] )
        qdf = gtimg.GetDayK(isyear, code, df=1,dateindex=1,session=session)
        qdf.columns = ['openPrice','closePrice','highestPrice','lowestPrice','turnoverVol']
        qdf.index.name = 'tradeDate'
        qdf['secID'] = sec['secID']
        qdf['tDate'] = qdf.index.strftime( '%Y-%m-%d' )
        # write data to db    
        insersql = sql = "INSERT OR REPLACE INTO d_quote (openPrice, closePrice, highestPrice, lowestPrice, turnoverVol, secID, 'tradeDate') VALUES (?, ?, ?, ?, ?, ?, ?)"
        trans = conn.begin()
        conn.execute( insersql, list(qdf.itertuples(index=False, name =None)) )
        trans.commit()        
   
        time.sleep(0.5)
    conn.close()

#write_all_excel_tables()
update_d_quote()
