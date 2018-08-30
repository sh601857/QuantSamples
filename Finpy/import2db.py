#coding=utf-8

import pandas as pd
import numpy as np

secID = '601318.XSHG'

ev = pd.Series([16.727, 19.418, 21.138, 24.415, 26.293, 29.956, 29.765, 32.969, 36.113, 39.394, 41.643, 46.030, 51.597, 58.421, 30.243, 33.968, 34.885, 40.984, 45.140,50.73,
                54.17],  index = pd.date_range('2008-12-31', end='2018-12-31', freq='6M'), name='ev')

