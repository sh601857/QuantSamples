# -*- coding:utf-8 -*-

from WindPy import w
import sqlite3
from datetime import datetime

server = 'windstock.db'
dt=datetime.now()
w.start();

# 命令如何写可以用命令生成器来辅助完成
# 定义打印输出函数，用来展示数据使用
#连接数据库
conn = sqlite3.connect('windstock.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS stockprice (
    secid text NOT NULL,
    tradedate text,
    openprice real,
    highprice real,
    lowprice real,
    closeprice real,
    volume real,
    amt real,
    PRIMARY KEY (secid,tradedate)
    )
""")

sql = "INSERT OR REPLACE INTO stockprice VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

# 通过wset来取数据集数据
print('\n\n'+'-----通过wset来取数据集数据,获取全部A股代码列表-----'+'\n')
wsetdata=w.wset('SectorConstituent','date=20160625;sectorId=a001010100000000;field=wind_code')
print(wsetdata)

for j in range(0,len(wsetdata.Data[0])):
    # 通过wsd来提取时间序列数据，比如取开高低收成交量，成交额数据
    print( u"\n\n-----第 %i 次通过wsd来提取 %s 开高低收成交量数据-----\n" %(j,str(wsetdata.Data[0][j])) )
    wssdata=w.wss(str(wsetdata.Data[0][j]),'ipo_date')
    wsddata1=w.wsd(str(wsetdata.Data[0][j]), "open,high,low,close,volume,amt", wssdata.Data[0][0], dt, "Fill=Previous")
    if wsddata1.ErrorCode!=0:
        continue
    print (wsddata1)
    for i in range(0,len(wsddata1.Data[0])):
        sqllist=[]
        sqltuple=()
        sqllist.append(str(wsetdata.Data[0][j]))
        if len(wsddata1.Times)>1:
            sqllist.append(wsddata1.Times[i].strftime('%Y%m%d'))
        for k in range(0, len(wsddata1.Fields)):
            sqllist.append(wsddata1.Data[k][i])
        sqltuple=tuple(sqllist)
        cursor.execute(sql,sqltuple)
    conn.commit()
conn.close()
