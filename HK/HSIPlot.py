#from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sqlite3
import talib as ta
import math
#engine = create_engine('sqlite:///:HKI.db')

conn = sqlite3.connect('u'D:\\yun\°Ù¶ÈÔÆ\\PortfolioMan\\dat\\HKI.db)
r = pd.read_sql_query('SELECT * FROM HKITRI where secid=\'HSI\' ORDER BY tradedate', conn)

NDays = 3;


N=len(r)
if NDays>1 and N > 150:
    #Create NDays k   
    r=r.iloc[range((N-1) % NDays, N, NDays)]

N=len(r)
prices = r.closeprice.values

td = np.arange(N)
def format_date(x, pos=None):
    thisind = np.clip(int(x + 0.5), 0, N-1 )
    return r.iloc[thisind].tradedate

left, width = 0.01, 0.95
rect1 = [left, 0.3, width, 0.68]
rect2 = [left, 0.1, width, 0.2]

fig = plt.figure(facecolor='white',figsize=(20,8))
axescolor  = '#f6f6f6'  # the axes background color

ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax1.tick_params('y', labelright = True ,labelleft = False )
ax2.tick_params('y', labelright = True ,labelleft = False )

#set x sticks
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
xsticks = np.arange(start=N-1,stop=0,step=-20)
ax1.xaxis.set_ticks(xsticks)
ax1.set_xlim(-2,N+1)
plt.setp(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')
for label in ax1.get_xticklabels():
    label.set_visible(False)
fig.autofmt_xdate()

# set ax1 y sticks
ax1.set_yscale(u'log')
ymax = prices.max()*1.02
ymin = prices.min()*0.98
ylst = prices[N-1]
ax1.set_ylim( ymin, ymax )
ysticks = [ylst]
ys = ylst*1.1
while ys < ymax: 
    ysticks.append(ys)
    ys=ys*1.1
ys = ylst*0.9	
while ys > ymin: 
    ysticks.append(ys)
    ys=ys*0.9
ysticks.sort()
ax1.yaxis.set_ticks(ysticks)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f'))
ax1.yaxis.grid(True,color='0.6', linestyle='-', linewidth=0.5)



ema12 = ta.EMA(prices,12)
ema50 = ta.EMA(prices,50)
ax1.plot(td,ema12,color='k',label='EMA12')
ax1.plot(td,ema50,color='r',label='EMA50')
ax1.plot( td, prices ,label="C")
s = 'C:%1.3f, EMA12:%1.3f, EMA50::%1.3f' % (prices[-1], ema12[-1], ema50[-1])
t4 = ax1.text(0.01, 0.95, s, transform=ax1.transAxes, fontsize=9)

dif = ( ta.EMA(prices,12) / ta.EMA(prices,26) )
for i in range(len(dif)) :
    dif[i] = math.log(dif[i])*100.0
dea = ta.EMA(dif,9)
macd = (dif-dea)*2

ax2.plot(td,dif,color='k')
ax2.plot(td,dea,color='r')
up = macd > 0
ax2.bar(td[up],macd[up],color='r',align='center',edgecolor='r')
ax2.bar(td[~up],macd[~up],color='b',align='center',edgecolor='b')


s = 'dif:%1.3f, dea:%1.3f, macd::%1.3f' % (dif[-1], dea[-1], macd[-1])
t4 = ax2.text(0.01, 0.85, s, transform=ax2.transAxes, fontsize=9)

fig.show()
pass