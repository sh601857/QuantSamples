# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

ll = 2

if ll == 1:
    stocks = [('90004',u'白云机场'),('90276',u'恒瑞医药'),('90519',u'贵州茅台'),
              ('93288',u'海天味业'),('72415',u'海康威视'),('72304',u'洋河股份')]
elif ll == 2:          
    stocks = [('93833',u'欧派家居'),('70651',u'格力电器'),('72508',u'老板电器'),
              ('72572',u'索菲亚  '),('70333',u'美的集团'),('72032',u'苏泊尔  ')]		  
elif ll == 3:          
    stocks = [('93833',u'欧派家居'),('70651',u'格力电器'),('72508',u'老板电器'),
              ('72572',u'索菲亚  '),('70333',u'美的集团'),('72032',u'苏泊尔  ')]			  
          
conn = sqlite3.connect(u'D:\\yun\百度云\\PortfolioMan\\dat\\HKI.db')

def PlotOnAxe(ax, df):
    #ax.plot(df.index, df.shares, label='shares', color='black' )
    ax.plot(range(0,len(df)), df.pct, label='pct' , color='blue' )
    #df.shares.plot(ax=ax, label='shares', color='black')
    #df.pct.plot(ax=ax, label='pct', color='blue', secondary_y=True,)
    
    xsticks = np.arange(start=len(df)-1,stop=0,step=-50)
    xstickslables = [ df.iloc[i,0] for i in xsticks ]
    ax.set_xticks(xsticks)
    ax.set_xticklabels( xstickslables )
    ax.set_xlim(0, len(df)+5)
    
plt.switch_backend('TkAgg') 
fig = plt.figure(figsize=(20, 10), facecolor=(.94,.94,.94))
axes=[]
axes.append( fig.add_axes([0.02, 0.55, 0.29, 0.4]) )
axes.append( fig.add_axes([0.34, 0.55, 0.29, 0.4]) )
axes.append( fig.add_axes([0.66, 0.55, 0.29, 0.4]) )
axes.append( fig.add_axes([0.02, 0.05, 0.29, 0.4]) )
axes.append( fig.add_axes([0.34, 0.05, 0.29, 0.4]) )
axes.append( fig.add_axes([0.66, 0.05, 0.29, 0.4]) )

for ax in axes:
    ax.set_axis_bgcolor((.94,.94,.94))
    ax.tick_params('y', labelright = True ,labelleft = False )

for i in range(0,len(stocks)):
    secid = stocks[i][0]
    df = pd.read_sql_query('select tradedate,shares,pct from HKTHolds where secid=\'{0}\' order by tradedate'.format(secid), conn)
    df = df[-200:]

    PlotOnAxe(axes[i], df )
    axes[i].set_title(stocks[i][1])
    
conn.close()
#plt.tight_layout() 
mng = plt.get_current_fig_manager()
mng.window.state('zoomed') #works fine on Windows!

plt.show()

