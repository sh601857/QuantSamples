import datetime
import pandas as pd
import numpy as np
import talib as ta
import pybrain as brain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter

secID='000300'
HISTORY = 9

MAS     = 12
MAL     = 26
MAM     = 9

HOLD    = 5


rawData = pd.read_csv(secID+'.csv', index_col=0, parse_dates=[1])
cnpa = np.array(rawData['closeIndex'])
rawData['EMAS'] = ta.EMA( cnpa ,timeperiod=MAS)
rawData['EMAL'] = ta.EMA( cnpa ,timeperiod=MAL)
rawData['DIFF'] = np.log( rawData['EMAS'] / rawData['EMAL'] )*100
rawData['DEA']  = ta.EMA( np.array(rawData['DIFF']) ,timeperiod=MAM)
rawData['CDIS'] = np.log( rawData['closeIndex'] / rawData['EMAL'] )*100

print( rawData.head(5) )
print( rawData.tail(5) )
rawData=rawData.dropna(axis=0)

#training_set = (datetime.date(2011,1,1), datetime.date(2014,1,1))       
#testing_set  = (datetime.date(2016,1,1),datetime.date(2016,6,30))      

 

from pybrain.datasets import SupervisedDataSet
### Build train data set
def make_data_set(beg,end):
    ds = SupervisedDataSet(HISTORY*3, 1) 
    trainQ = rawData[(rawData.tradeDate <= end) & ( rawData.tradeDate >= beg)]
    

    for idx in range(1, len(plist) - HISTORY - 1-HOLD-1):
        sample = []
        for i in range(HISTORY):
            sample.append(plist[idx + i] / plist[idx + i - 1])
            
        cur = idx + HISTORY - 1  
        answer = max( clist[cur+1:cur+HOLD+1] ) / clist[cur]
        
        ds.addSample(sample, answer)
    return ds


#fnn = buildNetwork(HISTORY, 15, 7, 1)
#training_ds = make_data_set(training_set[0],training_set[1])
#testing_ds = make_data_set(testing_set[0],testing_set[1])

#trainer = BackpropTrainer(fnn, training_ds, momentum = 0.1, verbose = True, weightdecay = 0.01)
#trainer.trainEpochs(epochs = 25)
#NetworkWriter.writeToFile(fnn, secID+'_fnn.csv')

#ts = fnn.activateOnDataset(testing_ds)
#print(training_ds)
#print(ts)

