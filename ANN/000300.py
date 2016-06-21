import datetime
import pandas as pd
import numpy as np
import pybrain as brain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter

secID='000300'
HISTORY = 9
MA1     = 3
HOLD    = 5


rawData = pd.read_csv(secID+'.csv', index_col=0, parse_dates=[1])
rawData['MA1'] = rawData['closeIndex'].rolling(window=MA1,center=False).mean()

print( rawData[0:5] )

#rawData['tradeDate'] = pd.to_datetime( rawData['tradeDate'] )
training_set = (datetime.date(2011,1,1), datetime.date(2014,1,1))       
testing_set  = (datetime.date(2016,1,1),datetime.date(2016,6,30))      

 

from pybrain.datasets import SupervisedDataSet
### Build train data set
def make_data_set(beg,end):
    ds = SupervisedDataSet(HISTORY, 1)
    
    
    trainQ = rawData[(rawData.tradeDate <= end) & ( rawData.tradeDate >= beg)]
    trainQ = trainQ.dropna(axis=0)
    print(trainQ[0:5])
    
    plist = list(trainQ.MA1)
    clist = list(trainQ.closeIndex)
 
    for idx in range(1, len(plist) - HISTORY - 1-HOLD-1):
        sample = []
        for i in range(HISTORY):
            sample.append(plist[idx + i] / plist[idx + i - 1])
        cur = idx + HISTORY - 1  
        answer = max( clist[cur+1:cur+HOLD+1] ) / clist[cur]
        
        ds.addSample(sample, answer)
    return ds


fnn = buildNetwork(HISTORY, 15, 7, 1)
training_ds = make_data_set(training_set[0],training_set[1])
testing_ds = make_data_set(testing_set[0],testing_set[1])

trainer = BackpropTrainer(fnn, training_ds, momentum = 0.1, verbose = True, weightdecay = 0.01)
trainer.trainEpochs(epochs = 25)
#NetworkWriter.writeToFile(fnn, secID+'_fnn.csv')

ts = fnn.activateOnDataset(testing_ds)
print(training_ds)
print(ts)

