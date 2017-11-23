import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


q = ts.get_k_data('601318',start='2008-12-31',autype=None)
q['sharechange'] = 1.0
q['date'] = pd.to_datetime(q['date'],format='%Y-%m-%d')
q.set_index('date',inplace=-True)

q.loc[:'2015-07-26','sharechange'] = 0.5


q['c']=q['close']*q['sharechange']

ev = pd.Series([8.363 ,9.709, 10.569, 12.057, 13.146 ,14.778 ,14.883 ,16.359 ,18.056 ,19.697 ,20.822 ,23.015 ,25.799 ,28.961 ,30.243 ,33.618 ,34.885 ,40.434 ,
                43],  index = pd.date_range('2008-12-31', end='2017-12-31', freq='6M'))

plt.plot(q.index, q['c'])
plt.plot(ev.index, ev, label='ev')
plt.plot(ev.index, ev*1.8, label='1.8ev')
plt.plot(ev.index, ev*1.5, label='1.5ev')
plt.plot(ev.index, ev*0.8, label='0.8ev')


plt.yscale(u'log')
plt.yticks([10.0,20.0,40.0,80.0])
plt.ylim(10,80)
plt.xlim( q.index[0] + pd.Timedelta('-10 days') , q.index[-1] + pd.Timedelta('20 days'))

plt.legend(loc=0)
plt.tight_layout()
plt.show()
