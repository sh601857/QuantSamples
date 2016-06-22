import datetime
import pandas as pd
import numpy as np
import talib as ta
import pybrain as brain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
from pybrain.utilities           import percentError
#https://github.com/poweltalwar/DeepLearning/blob/master/neuralNets.py
secID='000300'
HISTORY = 9

MAS     = 12
MAL     = 26
MAM     = 9

HOLD    = 20


rawData = pd.read_csv(secID+'.csv', index_col=0, parse_dates=[1])
cnpa = np.array(rawData['closeIndex'])
rawData['EMAS'] = ta.EMA( cnpa ,timeperiod=MAS)
rawData['EMAL'] = ta.EMA( cnpa ,timeperiod=MAL)
rawData['DIFF'] = np.log( rawData['EMAS'] / rawData['EMAL'] )*100
rawData['DEA']  = ta.EMA( np.array(rawData['DIFF']) ,timeperiod=MAM)
rawData['CDIS'] = np.log( rawData['closeIndex'] / rawData['EMAL'] )*100

#print( rawData.head(5) )
#print( rawData.tail(5) )
rawData=rawData.dropna(axis=0)

training_set = (datetime.date(2010,1,1), datetime.date(2016,1,1))       
testing_set  = (datetime.date(2016,1,1),datetime.date(2016,6,30))      

 

from pybrain.datasets import SupervisedDataSet
### Build train data set
def make_data_set(beg,end):
    ds = ClassificationDataSet(HISTORY*3, class_labels=['None', 'Buy' , 'Sell']) #SupervisedDataSet(HISTORY*3, 1) 
    trainQ = rawData[(rawData.tradeDate <= end) & ( rawData.tradeDate >= beg)]
    

    for idx in range(1, len(trainQ) - HISTORY - 1 - HOLD-1):
        sample = []
        for i in range(HISTORY):
            #sample.append( trainQ.iloc[idx+i]['EMAL'] )#  [['EMAL','DIFF','DEA','CDIS']] ) )
            sample.append( trainQ.iloc[idx+i]['DIFF'] )
            sample.append( trainQ.iloc[idx+i]['DEA'] )
            sample.append( trainQ.iloc[idx+i]['CDIS'] )
        cur = idx + HISTORY - 1 
        if max( trainQ.iloc[cur+1:cur+HOLD+1]['EMAS'] ) / trainQ.iloc[cur]['closeIndex'] > 1.05 : 
            answer = 1
        elif min( trainQ.iloc[cur+1:cur+HOLD+1]['EMAS'] ) / trainQ.iloc[cur]['closeIndex'] < 0.95:
            answer = 2
        else:
            answer = 0
#        print(sample)    
        ds.addSample(sample, answer)
    return ds
training_ds = make_data_set(training_set[0],training_set[1])
testing_ds = make_data_set(testing_set[0],testing_set[1])
training_ds._convertToOneOfMany()
testing_ds._convertToOneOfMany()
print(testing_ds)

fnn = buildNetwork(training_ds.indim, HISTORY*3, training_ds.outdim)

trainer = BackpropTrainer(fnn, training_ds, momentum = 0.1, verbose = True, weightdecay = 0.01)
trainer.trainEpochs(epochs = 25)
#NetworkWriter.writeToFile(fnn, secID+'_fnn.csv')

#ts = fnn.activateOnDataset(testing_ds)
#print(training_ds)
#print(ts)
print( 'Percent Error on Test dataset: ' , percentError( trainer.testOnClassData (
    dataset=testing_ds )
                                                        , testing_ds['class'] ) )
