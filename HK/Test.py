# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

data = np.array([[1,2,3,4],[1,2,3,4],[1,2,np.NAN,4],[1,12,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]])

print('data.mean')
mean = data.mean(axis=0)
print(mean)

print('data.std')
std = data.std(axis=0)
print(std)

print('data.std1')
std1 = np.zeros((4,))
for j in range(0,4):
    std1[j] = data[:,j].std()
print(std1)

print('out')
outi = np.zeros((10,))
numj = np.zeros((4,))
for i in range(2,4):
    out = abs( data[i,:] - mean ) > 2 * std1
    print(out)
    numj =numj+out
    outi[i] = out.any()
  
print(numj)  
print(outi)


#import webbrowser, urllib.request
#tickers='hk00998'
#url = 'http://qt.gtimg.cn/q={0}'.format( tickers )
#response = urllib.request.urlopen(url)
#stocks_detail = response.read().decode('gb2312')    
#stock_details = stocks_detail.split('~')
#for i in range( len( stock_details ) ):
    #print( '{0:3} : {1}'.format(i, stock_details[i] )  )
    
    
#import webbrowser, urllib.request
#tickers='hk00998'
#url = 'http://hq.sinajs.cn/list={0}'.format( tickers )
#response = urllib.request.urlopen(url)
#stocks_detail = response.read().decode('gb2312')
#stock_details = stocks_detail.split(',')
#for i in range( len( stock_details ) ):
    #print( '{0:3} : {1}'.format(i, stock_details[i] )  )