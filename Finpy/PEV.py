#coding=utf-8

import pandas as pd
import numpy as np
import QRep
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def plot_pev(secID_a,secID_h,start):
    
    a = QRep.get_pev(secID_a, start)
    h = QRep.get_pev(secID_h, start)
    h_a = h['pev'] / a['pev']
    h_a.dropna(inplace=True)
    #print(h_a[-5:])
    
    cmin = min(a['pev'].min(), h['pev'].min() , h_a.min())
    cmax = max(a['pev'].max(), h['pev'].max() , h_a.max())
    ymin = 1.0
    while ymin > cmin and ymin > 0.0:
        ymin = ymin - 0.2
    ymax =1.0
    while ymax < cmax:
        ymax = ymax + 0.2
    
    plt.figure(figsize=(20, 10), facecolor=(.94,.94,.94))
    plt.plot(a.index, a['pev'], label=secID_a[:-5], color='red')
    plt.plot(h.index, h['pev'], label=secID_h[:-5], color='green')
    plt.plot(h_a.index, h_a, label='{0}/{1}'.format(secID_h[:-5], secID_a[:-5] ) , color='black')
    
    plt.text(a.index[0] + pd.Timedelta('20 days'), ymax - 0.3* (ymax-ymin) , '{0}'.format( h_a[-5:] ), fontsize=10)
    
    plt.legend(loc=2,frameon=False, ncol= 5)
    plt.xlim( a.index[0] + pd.Timedelta('-10 days') , a.index[-1] + pd.Timedelta('10 days') )
    #plt.yscale(u'log')
    plt.yticks(np.arange(ymin,ymax,0.2))
    
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)    
    ax.set_facecolor((.94,.94,.94))
    ax.grid(b=True, axis='y', which='major', color='gray', linestyle='--', linewidth = 0.5)
    
    plt.tight_layout()
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed') #works fine on Windows!
    
    plt.show()


#plot_pev('601088.XSHG','01088.XHKG','2010-01-01')

#plot_pev('601318.XSHG','02318.XHKG','2012-01-01')
#plot_pev('601601.XSHG','02601.XHKG','2015-01-01')
#plot_pev('601336.XSHG', '01336.XHKG','2012-01-01')


#plot_pev('601288.XSHG','01288.XHKG','2014-01-01')
#plot_pev('600036.XSHG','03968.XHKG','2014-01-01')
#plot_pev('601939.XSHG','00939.XHKG','2014-01-01')
#plot_pev('600016.XSHG','01988.XHKG','2014-01-01')

#plot_pev('601166.XSHG','601288.XSHG','2014-01-01')
#plot_pev('601288.XSHG','601939.XSHG','2012-01-01')
#plot_pev('601601.XSHG', '601318.XSHG','2014-01-01')
