import pandas_datareader.data as web
import datetime
import talib
import numpy

#Download data from yahoo finance
start = datetime.datetime(2005,1,1)
end = datetime.datetime(2016,6,21)
ticker = "000300" #^HSI  ^HSCE  
f=web.DataReader(ticker,'google',start,end)
print(f[:5])
print(f.tail(5))