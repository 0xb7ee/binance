#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2018-10-11 下午5:24
'''

import binance
import datetime
keys = binance.prices().keys()


eos30m = binance.klines(u'EOSBTC','30m')
eos60m = binance.klines(u'EOSBTC','1h')
eos24h = binance.klines(u'EOSBTC','1d')

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

def isPositive(kline):
    open = float(kline['open'])
    close = float(kline['close'])
    if kline['open']