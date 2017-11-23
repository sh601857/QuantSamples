import tushare as ts


#ts.set_token('1db4f7018e8afb5338d962295a5149129680c466a820be7df05fc67f6c429e8e')

mkt = ts.Market() 
df = mkt.TickRTSnapshot(securityID='000001.XSHE')

print( df )