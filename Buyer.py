#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2018-10-11 下午5:24
'''

import binance
import datetime
keys = binance.prices().keys()
'''
kline = 
{'close': u'0.00001842',
 'closeTime': 1539250199999,
 'high': u'0.00001960',
 'low': u'0.00001831',
 'numTrades': 1762,
 'open': u'0.00001869',
 'openTime': 1539248400000,
 'quoteVolume': u'66.55352920',
 'volume': u'3471331.00000000'}

'''

def isPositive(line):
    open = float(line['open'])
    close = float(line['close'])
    if close>open:
        return True
    elif close<open:
        return False
    else:
        return None

def is3Positive(lines):
    if isPositive(lines[-2]) and isPositive(lines[-3]) and isPositive(lines[-4]):
        return True
    elif not (isPositive(lines[-2]) or isPositive(lines[-3]) or isPositive(lines[-4])):
        return False
    else:
        return None

for key in keys:
    try:
        kline = binance.klines(key,'1w')
        ret = is3Positive(kline)
        if not ret is None and ret==True and not isPositive(kline[-5]):
            print key
    except Exception:
        print("Error",key,"1 week line")