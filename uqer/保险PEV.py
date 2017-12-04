import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#设置研究股票
secID_a = '601318.XSHG'
secID_h= '02318.XHKG'

#设置计算周期
start = '20081231'
end = ''
r = DataAPI.MktFxRefRateGet(currencyPair=u"HKD/CNY",beginDate= start,endDate = end,field=u"",pandas="1")
a = DataAPI.MktEqudGet(secID= secID_a,beginDate= start,endDate = end,isOpen="",field=u"secID,tradeDate,closePrice",pandas="1")
h = DataAPI.MktHKEqudGet(secID=secID_h,beginDate= start,endDate = end,field=u"secID,tradeDate,closePrice",pandas="1")

a['tradeDate'] = pd.to_datetime(a['tradeDate'])
a = a.set_index('tradeDate')
a.loc[:'2015-07-26','closePrice'] = 0.5 * a.loc[:'2015-07-26','closePrice']

security = pd.merge(h,r,on = 'tradeDate')
security['rmb_hp']=security['closePrice']*security['midRate']
security['tradeDate'] = pd.to_datetime(security['tradeDate'])
security = security.set_index('tradeDate')
security.loc[:'2015-07-26','rmb_hp'] = 0.5 * security.loc[:'2015-07-26','rmb_hp']

ev = pd.Series([8.363 ,9.709, 10.569, 12.057, 13.146 ,14.778 ,14.883 ,16.359 ,18.056 ,19.697 ,20.822 ,23.015 ,25.799 ,28.961 ,30.243 ,33.618 ,34.885 ,40.434 ,
                43],  index = pd.date_range('2008-12-31', end='2017-12-31', freq='6M'))
plt.figure(figsize=(30,10))
plt.title(secID_h)
#print(a)
plt.plot(a.index, a['closePrice'], label='ap')
plt.plot(security.index, security['rmb_hp'])
plt.plot(ev.index, ev, label='ev')
plt.plot(ev.index, ev*1.8, label='1.8ev')
plt.plot(ev.index, ev*1.5, label='1.5ev')
plt.plot(ev.index, ev*0.8, label='0.8ev')

plt.text(pd.Timestamp('2011-12-31'), 60, '2011-G= {0:.3f}'.format( ev[-2] / ev['2011-12-31']) , fontsize=12)

plt.yscale(u'log')
#plt.yticks([10.0,20.0,30,40,40,40.0])
plt.ylim(10,80)
plt.tick_params('y', labelright = True ,labelleft = False)
plt.minorticks_off()
axes = plt.gca()
axes.yaxis.set_major_locator(mticker.FixedLocator([10.0,20.0,40,80]))
axes.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

plt.xlim( security.index[0] + pd.Timedelta('-10 days') , pd.Timestamp('2017-12-31') )

plt.legend(loc=2,frameon=False,ncol	= 5)
#plt.tight_layout()
#plt.show()


####################################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#设置研究股票
secID_a = '601601.XSHG'
secID_h= '02601.XHKG'

#设置计算周期
start = '20091231'
end = ''
r = DataAPI.MktFxRefRateGet(currencyPair=u"HKD/CNY",beginDate= start,endDate = end,field=u"",pandas="1")
a = DataAPI.MktEqudGet(secID= secID_a,beginDate= start,endDate = end,isOpen="",field=u"secID,tradeDate,closePrice",pandas="1")
h = DataAPI.MktHKEqudGet(secID=secID_h,beginDate= start,endDate = end,field=u"secID,tradeDate,closePrice",pandas="1")

a['tradeDate'] = pd.to_datetime(a['tradeDate'])
#a = a.set_index('tradeDate')

security = pd.merge(h,r,on = 'tradeDate')
security['rmb_hp']=security['closePrice']*security['midRate']
security['tradeDate'] = pd.to_datetime(security['tradeDate'])
security = security.set_index('tradeDate')

ev = pd.Series([11.596 ,12.177 ,12.801 ,12.792 ,13.205 ,14.167 ,14.928 ,15.419 ,15.932 ,16.982 ,18.902 ,21.393 ,22.691 ,23.765 ,27.140 ,29.955 ,
                32.5],  index = pd.date_range('2009-12-31', end='2017-12-31', freq='6M'))
plt.figure(figsize=(20,10))
plt.title(secID_h)
#print(a)
plt.plot(a['tradeDate'], a['closePrice'], label='ap')
plt.plot(security.index, security['rmb_hp'])
plt.plot(ev.index, ev, label='ev')
plt.plot(ev.index, ev*1.8, label='1.8ev')
plt.plot(ev.index, ev*1.5, label='1.5ev')
plt.plot(ev.index, ev*0.8, label='0.8ev')

plt.text(pd.Timestamp('2011-12-31'), 60, '2011-G= {0:.3f}'.format( ev[-2] / ev['2011-12-31']) , fontsize=12)

plt.yscale(u'log')
#plt.yticks([10.0,20.0,30,40,40,40.0])
plt.ylim(10,80)
plt.tick_params('y', labelright = True ,labelleft = False)
plt.minorticks_off()
axes = plt.gca()
axes.yaxis.set_major_locator(mticker.FixedLocator([10.0,20.0,40,80]))
axes.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

plt.xlim( security.index[0] + pd.Timedelta('-10 days') , pd.Timestamp('2017-12-31'))

plt.legend(loc=2,frameon=False,ncol	= 5)
#plt.tight_layout()
#plt.show()

############################################################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#设置研究股票
secID_a = '601336.XSHG'
secID_h= '01336.XHKG'

#设置计算周期
start = '20111231'
end = ''
r = DataAPI.MktFxRefRateGet(currencyPair=u"HKD/CNY",beginDate= start,endDate = end,field=u"",pandas="1")
a = DataAPI.MktEqudGet(secID= secID_a,beginDate= start,endDate = end,isOpen="",field=u"secID,tradeDate,closePrice",pandas="1")
h = DataAPI.MktHKEqudGet(secID=secID_h,beginDate= start,endDate = end,field=u"secID,tradeDate,closePrice",pandas="1")

a['tradeDate'] = pd.to_datetime(a['tradeDate'])
#a = a.set_index('tradeDate')

security = pd.merge(h,r,on = 'tradeDate')
security['rmb_hp']=security['closePrice']*security['midRate']
security['tradeDate'] = pd.to_datetime(security['tradeDate'])
security = security.set_index('tradeDate')

ev = pd.Series([15.718 ,17.999 ,18.230 ,19.485 ,20.646 ,23.446 ,27.331 ,31.815 ,33.107 ,35.160 ,41.496 ,45.548 ,
                49.0],  index = pd.date_range('2011-12-31', end='2017-12-31', freq='6M'))
plt.figure(figsize=(20,10))
plt.title(secID_h)
#print(a)
plt.plot(a['tradeDate'], a['closePrice'], label='ap')
plt.plot(security.index, security['rmb_hp'])
plt.plot(ev.index, ev, label='ev')
plt.plot(ev.index, ev*1.8, label='1.8ev')
plt.plot(ev.index, ev*1.5, label='1.5ev')
plt.plot(ev.index, ev*0.8, label='0.8ev')

plt.text(pd.Timestamp('2011-12-31'), 60, '2011-G= {0:.3f}'.format( ev[-2] / ev['2011-12-31']) , fontsize=12)

plt.yscale(u'log')
#plt.yticks([10.0,20.0,30,40,40,40.0])
plt.ylim(10,80)
plt.tick_params('y', labelright = True ,labelleft = False)
plt.minorticks_off()
axes = plt.gca()
axes.yaxis.set_major_locator(mticker.FixedLocator([10.0,20.0,40,80]))
axes.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

plt.xlim( security.index[0] + pd.Timedelta('-10 days') , pd.Timestamp('2017-12-31'))

plt.legend(loc=2,frameon=False,ncol	= 5)
#plt.tight_layout()
#plt.show()

####################################################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#设置研究股票
secID_a = '601628.XSHG'
secID_h= '02628.XHKG'

#设置计算周期
start = '20081231'
end = ''
r = DataAPI.MktFxRefRateGet(currencyPair=u"HKD/CNY",beginDate= start,endDate = end,field=u"",pandas="1")
a = DataAPI.MktEqudGet(secID= secID_a,beginDate= start,endDate = end,isOpen="",field=u"secID,tradeDate,closePrice",pandas="1")
h = DataAPI.MktHKEqudGet(secID=secID_h,beginDate= start,endDate = end,field=u"secID,tradeDate,closePrice",pandas="1")

a['tradeDate'] = pd.to_datetime(a['tradeDate'])
#a = a.set_index('tradeDate')

security = pd.merge(h,r,on = 'tradeDate')
security['rmb_hp']=security['closePrice']*security['midRate']
security['tradeDate'] = pd.to_datetime(security['tradeDate'])
security = security.set_index('tradeDate')

ev = pd.Series([8.494,9.458,10.091,9.851,10.547,10.490,10.361,11.828 ,11.944 ,12.855 ,12.108 ,13.811 ,16.094 ,18.285 ,19.822 ,20.653 ,23.069 ,24.678,
                26.5],  index = pd.date_range('2008-12-31', end='2017-12-31', freq='6M'))
plt.figure(figsize=(20,10))
plt.title(secID_h)
#print(a)
plt.plot(a['tradeDate'], a['closePrice'], label='ap')
plt.plot(security.index, security['rmb_hp'])
plt.plot(ev.index, ev, label='ev')
plt.plot(ev.index, ev*1.8, label='1.8ev')
plt.plot(ev.index, ev*1.5, label='1.5ev')
plt.plot(ev.index, ev*0.8, label='0.8ev')

plt.text(pd.Timestamp('2011-12-31'), 60, '2011-G= {0:.3f}'.format( ev[-2] / ev['2011-12-31']) , fontsize=12)

plt.yscale(u'log')
#plt.yticks([10.0,20.0,30,40,40,40.0])
plt.ylim(5,80)
plt.tick_params('y', labelright = True ,labelleft = False)
plt.minorticks_off()
axes = plt.gca()
axes.yaxis.set_major_locator(mticker.FixedLocator([5,10.0,20.0,40,80]))
axes.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

plt.xlim( security.index[0] + pd.Timedelta('-10 days') , pd.Timestamp('2017-12-31'))

plt.legend(loc=2,frameon=False,ncol	= 5)



#plt.tight_layout()
#plt.show()

