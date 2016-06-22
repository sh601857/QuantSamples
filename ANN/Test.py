import pandas_datareader.data as web
import datetime
import talib
import numpy

#Download data from yahoo finance
start = datetime.datetime(2005,1,1)
end = datetime.datetime(2016,6,21)
ticker = "2318.HK" #^HSI  ^HSCE  
#f=web.DataReader(ticker,'yahoo-actions',start,end)
#f=web.DataReader(ticker,'yahoo',start,end)
print(f)
#print(f.tail(5))