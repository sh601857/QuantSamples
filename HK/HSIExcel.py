import pandas as pd
import numpy as np
import sqlite3

df = pd.read_excel("HSCEI.xlsx",sheetname='D1',index_col=None)
print(df.head(5))
dtlist=[]
for i in range(len(df)) : 
    drow = df.iloc[i]
    drow['tradedate'] = drow['tradedate'].strftime('%Y%m%d')
    dtlist.append( tuple( drow.values ) )
print(dtlist[:5])

sql = "INSERT OR IGNORE INTO HKITRI VALUES (?, ?, ?)"
conn = sqlite3.connect('HKI.db')
cursor = conn.cursor()



cursor.executemany(sql, dtlist)

conn.commit()			
conn.close()