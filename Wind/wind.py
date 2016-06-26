from WindPy import w
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
w.start()
dd = w.wsd("601318.SH", "close,adjfactor", "2010-01-01", "2016-06-25", "Fill=Previous;PriceAdj=F")

df = pd.DataFrame( np.array(dd.Data).T , index=dd.Times, columns=dd.Fields )

#print(df.head(5))
df[['CLOSE']].plot()

plt.show()